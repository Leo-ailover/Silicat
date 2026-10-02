"""Training loop for Silicat.

Two stages, selected with `--stage`:
  - `pretrain`: next-token prediction on the raw Python corpus (resumable)
  - `chat`:     supervised fine-tune on JSONL chat data, loss masked so we only
                learn on Silicat's reply tokens. Output goes to chat{sfx}.pt
                (v3: checkpoints/chat_v3.pt), never over the pretrain checkpoint.

Checkpoints are written atomically via `silicat.checkpoint`. Pretrain resumes
model + AdamW + LR position from `latest_v3.pt`, or (after a container wipe)
from the committed fp16 parts with a fresh optimizer and a short LR re-warmup.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import signal
import time
from contextlib import nullcontext
from pathlib import Path

import numpy as np
import torch

from .checkpoint import (
    CKPT_DIR,
    archive_existing,
    checkpoint_exists,
    resolve_resumable,
    save_checkpoint,
    state_to_fp32,
)
from .chat_format import Message, format_for_training
from .dataset import DATA_DIR, TOK_DIR, TOK_DIR_V2, load_split
from .model import GPT, GPTConfig
from .model_v3 import GPTV3, GPTConfigV3
from .tokenizer import Tokenizer

ARCH_KEYS = ("n_layer", "n_head", "n_kv_head", "n_embd", "vocab_size")
V3_DEFAULTS = dict(n_layer=12, n_head=12, n_kv_head=4, n_embd=768, block_size=512, batch_size=8)
LEGACY_DEFAULTS = dict(n_layer=6, n_head=6, n_embd=384, block_size=256, batch_size=32)


# --------------------------------------------------------------- utilities
def _device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


class _Stop:
    """SIGTERM/SIGINT set a flag (checked at step boundaries); a second signal kills."""

    def __init__(self) -> None:
        self.flag = False
        self._old: dict = {}

    def _handler(self, sig, frm) -> None:
        if self.flag:
            signal.signal(sig, signal.SIG_DFL)
            os.kill(os.getpid(), sig)
            return
        self.flag = True
        print(f"\nsignal {sig}: finishing the current step, then saving and exiting", flush=True)

    def __enter__(self) -> "_Stop":
        for s in (signal.SIGTERM, signal.SIGINT):
            try:
                self._old[s] = signal.signal(s, self._handler)
            except ValueError:  # not in main thread
                pass
        return self

    def __exit__(self, *exc) -> None:
        for s, h in self._old.items():
            signal.signal(s, h)


def _cpu_has_bf16() -> bool:
    for n in ("_is_amx_tile_supported", "_is_avx512_bf16_supported"):
        try:
            if getattr(torch.cpu, n)():
                return True
        except Exception:
            pass
    try:
        flags = Path("/proc/cpuinfo").read_text()
        return "amx_bf16" in flags or "avx512_bf16" in flags
    except OSError:
        return False


def _resolve_precision(args: argparse.Namespace, device: str):
    """-> (autocast ctx factory, description). bf16 autocast only; weights/optimizer stay fp32."""
    mode = args.precision
    if args.amp and mode == "auto":
        mode = "bf16"
    if mode == "auto":
        if device == "cuda":
            mode = "bf16" if torch.cuda.is_bf16_supported() else "fp32"
        elif device == "cpu":
            mode = "bf16" if _cpu_has_bf16() else "fp32"
        else:
            mode = "fp32"
    if mode == "bf16" and device not in ("cuda", "cpu"):
        mode = "fp32"
    if mode == "bf16":
        return (lambda: torch.autocast(device_type=device, dtype=torch.bfloat16)), "bf16 autocast"
    return (lambda: nullcontext()), "fp32"


def _get_batch(
    data: np.ndarray,
    batch_size: int,
    block_size: int,
    device: str,
    generator: torch.Generator | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    ix = torch.randint(0, len(data) - block_size - 1, (batch_size,), generator=generator)
    return _batch_at(data, ix.tolist(), block_size, device)


def _batch_at(data: np.ndarray, starts, block_size: int, device: str):
    x = torch.stack([torch.from_numpy(np.asarray(data[i : i + block_size], dtype=np.int64)) for i in starts])
    y = torch.stack([torch.from_numpy(np.asarray(data[i + 1 : i + 1 + block_size], dtype=np.int64)) for i in starts])
    return x.to(device), y.to(device)


def _eval_starts(n_tokens: int, block_size: int, split_block: int | None, max_windows: int) -> list[int]:
    """Fixed, deterministic, non-overlapping eval windows. With a block-level split the
    windows stay inside split blocks (no seams); otherwise evenly strided."""
    if split_block and split_block > block_size:
        per = (split_block - 1) // block_size
        starts = [b * split_block + j * block_size for b in range(n_tokens // split_block) for j in range(per)]
    else:
        starts = list(range(0, max(0, n_tokens - block_size - 1), block_size))
    starts = [s for s in starts if s + block_size + 1 <= n_tokens]
    if not starts:
        raise ValueError(f"eval data too small ({n_tokens} tokens) for block size {block_size}")
    if len(starts) > max_windows:
        idx = np.unique(np.linspace(0, len(starts) - 1, max_windows).round().astype(int))
        starts = [starts[i] for i in idx]
    return starts


def _evaluate(model, data, starts, batch_size, block_size, device, ctx) -> float:
    model.eval()
    tot, n = 0.0, 0
    with torch.no_grad():
        for i in range(0, len(starts), batch_size):
            chunk = starts[i : i + batch_size]
            x, y = _batch_at(data, chunk, block_size, device)
            with ctx():
                _, loss = model(x, targets=y)
            tot += loss.item() * len(chunk)
            n += len(chunk)
    model.train()
    return tot / n


def _lr_at(step: int, *, warmup: int, total: int, lr_max: float, lr_min: float) -> float:
    if step < warmup:
        return lr_max * (step + 1) / max(1, warmup)
    if step >= total:
        return lr_min
    t = (step - warmup) / max(1, total - warmup)
    return lr_min + 0.5 * (lr_max - lr_min) * (1.0 + math.cos(math.pi * t))


def _lr_wsd(step: int, *, warmup: int, stable_end: int, total: int, lr_max: float, lr_min: float) -> float:
    """Warmup-Stable-Decay: linear warmup → flat plateau → cosine decay."""
    if step < warmup:
        return lr_max * (step + 1) / max(1, warmup)
    if step < stable_end:
        return lr_max
    if step >= total:
        return lr_min
    t = (step - stable_end) / max(1, total - stable_end)
    return lr_min + 0.5 * (lr_max - lr_min) * (1.0 + math.cos(math.pi * t))


def _sched(args: argparse.Namespace, step: int) -> float:
    if args.wsd:
        return _lr_wsd(step, warmup=args.warmup, stable_end=int(args.max_steps * 0.8),
                       total=args.max_steps, lr_max=args.lr, lr_min=args.lr * 0.1)
    return _lr_at(step, warmup=args.warmup, total=args.max_steps, lr_max=args.lr, lr_min=args.lr * 0.1)


def _build_cfg(vocab_size: int, args: argparse.Namespace) -> GPTConfig:
    return GPTConfig(
        vocab_size=vocab_size,
        block_size=args.block_size,
        n_layer=args.n_layer,
        n_head=args.n_head,
        n_embd=args.n_embd,
        dropout=args.dropout,
    )


def _build_cfg_v3(vocab_size: int, args: argparse.Namespace) -> GPTConfigV3:
    kv = args.n_kv_head or 4
    if args.n_embd % args.n_head:
        raise SystemExit(f"--n-embd {args.n_embd} must be divisible by --n-head {args.n_head}")
    if args.n_head % kv:
        raise SystemExit(f"--n-head {args.n_head} must be divisible by --n-kv-head {kv}")
    if (args.n_embd // args.n_head) % 2:
        raise SystemExit(f"head_dim {args.n_embd // args.n_head} must be even for RoPE")
    return GPTConfigV3(
        vocab_size=vocab_size,
        block_size=args.block_size,
        n_layer=args.n_layer,
        n_head=args.n_head,
        n_kv_head=kv,
        n_embd=args.n_embd,
        dropout=args.dropout,
    )


def _resolve_defaults(args: argparse.Namespace) -> None:
    """Fill unset (None) flags; explicit user values always win. Pretrain defaults are
    unchanged from before; chat gets SFT-appropriate lr/warmup/eval settings."""
    base = V3_DEFAULTS if args.v3 else LEGACY_DEFAULTS
    args._explicit = {k: getattr(args, k) for k in ("n_layer", "n_head", "n_kv_head", "n_embd", "block_size")
                      if getattr(args, k) is not None}
    for k, v in base.items():
        if getattr(args, k, None) is None:
            setattr(args, k, v)
    chat = args.stage == "chat"
    if args.lr is None:
        args.lr = 1e-4 if chat else 3e-4
    if args.warmup is None:
        args.warmup = 50 if chat else 100
    if args.eval_interval is None:
        args.eval_interval = 100 if chat else 200
    if args.max_steps is None and not chat:
        args.max_steps = 2000  # chat: derived from --chat-epochs after the data is loaded


# ----------------------------------------------------------------- pretrain
def _check_resume_config(ck: dict, cfg) -> None:
    old, new = ck["config"], cfg.__dict__
    bad = [(k, old.get(k), new.get(k)) for k in ARCH_KEYS if k in new and old.get(k) != new.get(k)]
    if bad:
        raise SystemExit("checkpoint config differs from CLI flags: " + ", ".join(f"{k}: ckpt={a} cli={b}" for k, a, b in bad))
    if old.get("block_size") != new.get("block_size"):
        print(f"WARNING: block_size differs (ckpt {old.get('block_size')}, cli {new.get('block_size')})", flush=True)


def pretrain(args: argparse.Namespace) -> None:
    device = args.device or _device()
    ctx, prec = _resolve_precision(args, device)
    print(f"device: {device} | precision: {prec} | seed: {args.seed}")

    tok = Tokenizer(TOK_DIR_V2 if (args.v2 or args.v3) else TOK_DIR)
    torch.manual_seed(args.seed)
    if args.v3:
        cfg = _build_cfg_v3(tok.vocab_size, args)
        model = GPTV3(cfg).to(device)
        ckpt_name = "latest_v3"
    else:
        cfg = _build_cfg(tok.vocab_size, args)
        model = GPT(cfg).to(device)
        ckpt_name = "latest_v2" if args.v2 else "latest"
    print(f"params: {model.num_params():,}")

    start_step, restored, res = 0, False, None
    if args.resume and args.fresh:
        raise SystemExit("--resume and --fresh are mutually exclusive")
    if args.resume:
        res = resolve_resumable(ckpt_name)
        if res is None:
            if args.require_resume:
                raise SystemExit("--require-resume: no checkpoint or parts found")
            print("WARNING: --resume given but no checkpoint or parts exist; starting at step 0", flush=True)
    elif checkpoint_exists(ckpt_name):
        if not args.fresh:
            raise SystemExit(
                f"checkpoint {ckpt_name} (or its parts) already exists; pass --resume to continue, "
                "or --fresh to archive it to checkpoints/old/ and start over"
            )
        archive_existing(ckpt_name)
    optim = model.configure_optimizer(args.lr, args.weight_decay)
    if res is not None:
        ck, src = res
        if ck.get("stage", "pretrain") == "chat":
            raise SystemExit(f"{src} holds chat weights; refusing to resume pretraining from it")
        _check_resume_config(ck, cfg)
        model.load_state_dict(state_to_fp32(ck["model"]))
        start_step = int(ck.get("step", 0))
        if ck.get("optim") and not ck.get("dtype"):
            try:
                optim.load_state_dict(ck["optim"])
                restored = True
            except Exception as e:
                print(f"WARNING: could not restore optimizer state ({e})", flush=True)
        if ck.get("seed") not in (None, args.seed):
            print(f"WARNING: checkpoint seed {ck['seed']} != --seed {args.seed}; data order changes", flush=True)
        print(f"resumed from step {start_step} ({src.name}); "
              + ("optimizer state restored" if restored
                 else f"NO optimizer state (fp16 export): fresh AdamW with {args.rewarmup}-step LR re-warmup"),
              flush=True)
        del ck
    rewarm = args.rewarmup if (start_step > 0 and not restored) else 0

    v2data = args.v2 or args.v3
    train_data = load_split("train", v2=v2data)
    val_data = load_split("val", v2=v2data)
    split_block = None
    meta = DATA_DIR / "meta_v2.json"
    if v2data and meta.exists():
        split_block = json.loads(meta.read_text()).get("block")
    val_starts = _eval_starts(len(val_data), args.block_size, split_block, args.eval_windows)
    g = torch.Generator().manual_seed(args.seed + 7)
    tr_starts = torch.randint(0, len(train_data) - args.block_size - 1, (len(val_starts),), generator=g).tolist()

    accum = args.grad_accum
    tok_per_step = args.batch_size * args.block_size * accum
    total_tok = args.max_steps * tok_per_step
    print(f"tokens/step {tok_per_step:,} | total {total_tok / 1e6:.1f}M tokens "
          f"= {total_tok / max(1, len(train_data)):.2f} epochs of {len(train_data) / 1e6:.2f}M train tokens | "
          f"eval windows {len(val_starts)}", flush=True)

    metrics_path = CKPT_DIR / f"metrics_{ckpt_name}.jsonl"
    CKPT_DIR.mkdir(parents=True, exist_ok=True)

    def metric(rec: dict) -> None:
        with metrics_path.open("a") as f:
            f.write(json.dumps(rec) + "\n")

    extra = {"stage": "pretrain", "seed": args.seed}
    last_saved = start_step if res is not None else -1
    ema = None
    t0 = time.time()
    done = start_step
    with _Stop() as stop:
        for step in range(start_step, args.max_steps):
            lr = _sched(args, step)
            if rewarm:
                lr *= min(1.0, (step - start_step + 1) / rewarm)
            for gr in optim.param_groups:
                gr["lr"] = lr

            optim.zero_grad(set_to_none=True)
            loss_val = 0.0
            for k in range(accum):
                gen = torch.Generator().manual_seed(args.seed * 1_000_003 + step * accum + k)
                x, y = _get_batch(train_data, args.batch_size, args.block_size, device, gen)
                with ctx():
                    _, loss = model(x, targets=y)
                (loss / accum).backward()
                loss_val += loss.item() / accum
            if not math.isfinite(loss_val):
                raise SystemExit(f"loss is {loss_val} at step {step}; not saving a diverged model")
            gnorm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0))
            optim.step()
            done = step + 1
            ema = loss_val if ema is None else 0.98 * ema + 0.02 * loss_val

            if step % args.log_interval == 0:
                dt = time.time() - t0
                tps = (done - start_step) * tok_per_step / max(dt, 1e-9)
                print(f"step {step:>6} | loss {loss_val:.4f} (ema {ema:.4f}) | gnorm {gnorm:.2f} | "
                      f"lr {lr:.2e} | {tps:,.0f} tok/s | {dt:.1f}s", flush=True)
                metric({"step": step, "loss": loss_val, "ema": ema, "gnorm": gnorm, "lr": lr,
                        "tok_s": tps, "tokens": done * tok_per_step, "t": time.time()})

            if done % args.eval_interval == 0 and done < args.max_steps:
                vl = _evaluate(model, val_data, val_starts, args.batch_size, args.block_size, device, ctx)
                tl = _evaluate(model, train_data, tr_starts, args.batch_size, args.block_size, device, ctx)
                print(f"  eval loss: {vl:.4f} | train-eval loss: {tl:.4f} | gap {vl - tl:+.4f}", flush=True)
                metric({"step": done, "eval_loss": vl, "train_eval_loss": tl})

            if stop.flag:
                save_checkpoint(CKPT_DIR / f"{ckpt_name}.pt", model, cfg, done, optim, extra)
                print(f"stopped at step {done}; resume with --resume")
                return
            if args.save_interval and done % args.save_interval == 0 and done < args.max_steps:
                save_checkpoint(CKPT_DIR / f"{ckpt_name}.pt", model, cfg, done, optim, extra)
                last_saved = done

    if start_step >= args.max_steps:
        print(f"already at step {start_step} >= --max-steps {args.max_steps}; nothing to do")
        return
    vl = _evaluate(model, val_data, val_starts, args.batch_size, args.block_size, device, ctx)
    tl = _evaluate(model, train_data, tr_starts, args.batch_size, args.block_size, device, ctx)
    print(f"  final eval loss: {vl:.4f} | train-eval loss: {tl:.4f} | gap {vl - tl:+.4f}", flush=True)
    metric({"step": args.max_steps, "eval_loss": vl, "train_eval_loss": tl})
    if last_saved != args.max_steps:
        save_checkpoint(CKPT_DIR / f"{ckpt_name}.pt", model, cfg, args.max_steps, optim, extra)


# --------------------------------------------------------------------- chat
def _load_chat(path: Path, tok: Tokenizer, block_size: int):
    """-> (rows, keys, stats). rows are (ids, loss_mask). Rows that are malformed, use an
    unknown role, are longer than block_size (truncation would drop <|end|>), have no loss
    tokens, or exactly duplicate an earlier row are skipped and counted."""
    end = tok.special_id("<|end|>")
    rows, keys = [], []
    stats = dict(bad=0, role=0, too_long=0, no_loss=0, dup=0)
    seen: set[bytes] = set()
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                msgs = [Message(role=m["role"], content=m["content"]) for m in row["messages"]]
            except (ValueError, KeyError, TypeError):
                stats["bad"] += 1
                continue
            if not msgs or any(m.role not in ("user", "silicat") for m in msgs):
                stats["role"] += 1
                continue
            ids, mask = format_for_training(msgs, tok)
            if len(ids) > block_size:
                stats["too_long"] += 1
                continue
            if sum(mask) == 0 or ids[-1] != end:
                stats["no_loss"] += 1
                continue
            h = hashlib.md5(np.asarray(ids, dtype=np.int64).tobytes()).digest()
            if h in seen:
                stats["dup"] += 1
                continue
            seen.add(h)
            first_user = next((m.content for m in msgs if m.role == "user"), msgs[0].content)
            rows.append((ids, mask))
            keys.append(first_user)
    return rows, keys, stats


def _hash_bucket(key: str) -> int:
    return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16) % 1000


def _split_chat(rows, keys, frac: float, vmax: int):
    """Deterministic, process-independent split keyed on the first user message."""
    if frac <= 0 or len(rows) < 30:
        return list(range(len(rows))), []
    val = [i for i, k in enumerate(keys) if _hash_bucket(k) < frac * 1000]
    if not val:
        val = [min(range(len(keys)), key=lambda i: _hash_bucket(keys[i]))]
    held = {keys[i] for i in val}  # whole bucket leaves train, independent of the --val-max cap
    train = [i for i in range(len(rows)) if keys[i] not in held]
    return train, val[:vmax]


def _collate(seqs, pad_id: int, block_size: int, device: str):
    L = min(max(len(s[0]) for s in seqs), block_size)
    n = len(seqs)
    x = np.full((n, L), pad_id, dtype=np.int64)
    y = np.full((n, L), -100, dtype=np.int64)
    m = np.zeros((n, L), dtype=np.int64)
    for i, (ids, mask) in enumerate(seqs):
        ids, mask = ids[:L], mask[:L]
        x[i, : len(ids) - 1] = ids[:-1]
        y[i, : len(ids) - 1] = ids[1:]
        m[i, : len(ids) - 1] = mask[1:]
    return tuple(torch.from_numpy(a).to(device) for a in (x, y, m))


def _epoch_batches(lengths: list[int], bs: int, seed: int, epoch: int) -> list[list[int]]:
    """Length-bucketed batches: shuffle, sort within chunks of 50 batches, shuffle batch order."""
    rng = np.random.default_rng(seed + epoch)
    perm = rng.permutation(len(lengths))
    chunk = bs * 50
    batches: list[list[int]] = []
    for s in range(0, len(perm), chunk):
        c = sorted(perm[s : s + chunk].tolist(), key=lambda i: lengths[i])
        batches += [c[j : j + bs] for j in range(0, len(c), bs)]
    return [batches[i] for i in rng.permutation(len(batches))]


def _eval_chat(model, rows, pad_id, block_size, device, bs, ctx) -> float:
    """Token-weighted masked loss over `rows` in fixed length-sorted order."""
    model.eval()
    order = sorted(range(len(rows)), key=lambda i: len(rows[i][0]))
    tot, ntok = 0.0, 0
    with torch.no_grad():
        for j in range(0, len(order), bs):
            x, y, m = _collate([rows[i] for i in order[j : j + bs]], pad_id, block_size, device)
            with ctx():
                _, loss = model(x, targets=y, loss_mask=m)
            c = int(m.sum().item())
            tot += loss.item() * c
            ntok += c
    model.train()
    return tot / max(1, ntok)


def chat(args: argparse.Namespace) -> None:
    device = args.device or _device()
    ctx, prec = _resolve_precision(args, device)
    print(f"device: {device} | precision: {prec} | seed: {args.seed}")
    tok = Tokenizer(TOK_DIR_V2 if (args.v2 or args.v3) else TOK_DIR)
    torch.manual_seed(args.seed)

    sfx = "_v3" if args.v3 else ("_v2" if args.v2 else "")
    base_name = f"latest{sfx}"
    res = resolve_resumable(base_name)
    if res is None:
        raise SystemExit(f"no checkpoints/{base_name}.pt (or parts) — run pretrain first")
    ck, src = res
    if ck.get("stage", "pretrain") == "chat":
        raise SystemExit(f"{src} holds chat weights; refusing to fine-tune a fine-tuned model")
    cfg_cls = GPTConfigV3 if args.v3 else GPTConfig
    cfg = cfg_cls(**ck["config"])
    cfg.dropout = args.dropout
    model = (GPTV3 if args.v3 else GPT)(cfg).to(device)
    model.load_state_dict(state_to_fp32(ck["model"]))
    pretrain_step = ck.get("step", 0)
    print(f"loaded pretrain checkpoint {src.name} from step {pretrain_step}")
    del ck
    for k, v in getattr(args, "_explicit", {}).items():
        if cfg.__dict__.get(k) != v:
            print(f"WARNING: --{k.replace('_', '-')} {v} ignored; checkpoint has {cfg.__dict__.get(k)}", flush=True)

    # ---- data
    default_data = args.chat_data is None
    if default_data:
        p3 = DATA_DIR / "silicat_chat_v3.jsonl"
        chat_path = p3 if (args.v3 and p3.exists()) else DATA_DIR / "silicat_chat.jsonl"
        if args.v3 and chat_path != p3:
            print(f"WARNING: {p3} missing; falling back to {chat_path}", flush=True)
    else:
        chat_path = Path(args.chat_data)
    if not chat_path.exists():
        raise SystemExit(f"no chat data at {chat_path}")
    rows, keys, st = _load_chat(chat_path, tok, cfg.block_size)
    print(f"chat data {chat_path}: {len(rows)} usable examples; skipped {st}")
    if st["too_long"]:
        print(f"  ({st['too_long']} examples exceed block size {cfg.block_size} and were skipped, not truncated)")

    eval_path = Path(args.chat_eval_data) if args.chat_eval_data else (
        DATA_DIR / "silicat_chat_eval.jsonl" if default_data else None)
    if eval_path is not None and eval_path.exists():
        val_rows, vkeys, _ = _load_chat(eval_path, tok, cfg.block_size)
        vk = set(vkeys)
        tr_idx = [i for i, k in enumerate(keys) if k not in vk]
        train_rows = [rows[i] for i in tr_idx]
        val_rows = val_rows[: args.val_max]
        print(f"held-out eval file {eval_path}: {len(val_rows)} examples "
              f"({len(rows) - len(train_rows)} overlapping train rows removed)")
    else:
        tr_idx, va_idx = _split_chat(rows, keys, args.chat_val_frac, args.val_max)
        train_rows = [rows[i] for i in tr_idx]
        val_rows = [rows[i] for i in va_idx]
        print(f"hash split: {len(train_rows)} train / {len(val_rows)} val")
    if not train_rows:
        raise SystemExit("no training examples")
    if not val_rows:
        print("WARNING: no held-out set; the final-step model is used")

    bs = min(args.batch_size, len(train_rows))
    accum = args.grad_accum
    lengths = [len(r[0]) for r in train_rows]
    plan_cache: dict[int, list[list[int]]] = {}

    def plan(epoch: int):
        if epoch not in plan_cache:
            plan_cache.clear()
            plan_cache[epoch] = _epoch_batches(lengths, bs, args.seed, epoch)
        return plan_cache[epoch]

    nb = len(_epoch_batches(lengths, bs, args.seed, 0))
    if args.max_steps is None:
        args.max_steps = max(1, math.ceil(args.chat_epochs * nb / accum))
    print(f"steps {args.max_steps} x {accum} micro-batches of {bs} = {args.max_steps * accum / nb:.2f} epochs "
          f"| lr {args.lr:g} warmup {args.warmup} {'wsd' if args.wsd else 'cosine'}", flush=True)

    optim = model.configure_optimizer(args.lr, args.weight_decay)
    pad_id = tok.special_id("<|pad|>")
    chat_ckpt = CKPT_DIR / f"chat_latest{sfx}.pt"
    best_ckpt = CKPT_DIR / f"chat_best{sfx}.pt"
    final_name = "chat_v3" if args.v3 else f"latest{sfx}"  # v1/v2 keep the legacy output name
    start_step, best_val, best_step, bad = 0, float("inf"), -1, 0
    if args.resume and chat_ckpt.exists():
        ck2 = torch.load(chat_ckpt, map_location=device, weights_only=True)
        model.load_state_dict(state_to_fp32(ck2["model"]))
        if ck2.get("optim"):
            optim.load_state_dict(ck2["optim"])
        start_step = ck2.get("step", 0)
        best_val = ck2.get("best_val", float("inf"))
        best_step = ck2.get("best_step", -1)
        bad = ck2.get("bad", 0)
        print(f"resumed chat fine-tune from step {start_step} (best val {best_val:.4f} @ {best_step})")
        del ck2

    extra_base = {"stage": "chat", "pretrain_step": pretrain_step, "seed": args.seed}

    def wip(step: int) -> None:
        save_checkpoint(chat_ckpt, model, cfg, step, optim,
                        {**extra_base, "best_val": best_val, "best_step": best_step, "bad": bad})

    ema, t0, step = None, time.time(), start_step
    stopped = False
    with _Stop() as stop:
        for step in range(start_step, args.max_steps):
            lr = _sched(args, step)
            for gr in optim.param_groups:
                gr["lr"] = lr
            optim.zero_grad(set_to_none=True)
            loss_val = 0.0
            for k in range(accum):
                mi = step * accum + k
                b = plan(mi // nb)[mi % nb]
                x, y, m = _collate([train_rows[i] for i in b], pad_id, cfg.block_size, device)
                with ctx():
                    _, loss = model(x, targets=y, loss_mask=m)
                (loss / accum).backward()
                loss_val += loss.item() / accum
            if not math.isfinite(loss_val):
                raise SystemExit(f"loss is {loss_val} at chat step {step}; aborting")
            gnorm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0))
            optim.step()
            done = step + 1
            ema = loss_val if ema is None else 0.95 * ema + 0.05 * loss_val
            if step % args.log_interval == 0:
                print(f"chat step {step:>5} (ep {mi // nb}) | loss {loss_val:.4f} (ema {ema:.4f}) | "
                      f"gnorm {gnorm:.2f} | lr {lr:.2e} | {time.time() - t0:.0f}s", flush=True)

            if val_rows and (done % args.eval_interval == 0 or done == args.max_steps):
                vl = _eval_chat(model, val_rows, pad_id, cfg.block_size, device, bs * 2, ctx)
                if vl < best_val:
                    best_val, best_step, bad = vl, done, 0
                    save_checkpoint(best_ckpt, model, cfg, done, None, {**extra_base, "val_loss": vl})
                else:
                    bad += 1
                print(f"  chat val loss {vl:.4f} (best {best_val:.4f} @ {best_step})", flush=True)
                wip(done)
                if args.patience and bad >= args.patience:
                    print(f"  early stop: no val improvement for {bad} evals")
                    break
            elif done % args.save_interval == 0:
                wip(done)
            if stop.flag:
                wip(done)
                print(f"stopped at chat step {done}; resume with --resume")
                stopped = True
                break
    if stopped:
        return

    if val_rows and best_ckpt.exists():
        bk = torch.load(best_ckpt, map_location=device, weights_only=True)
        model.load_state_dict(state_to_fp32(bk["model"]))
        print(f"  best checkpoint at step {bk['step']} (val loss {bk.get('val_loss', float('nan')):.4f})")
    elif val_rows:
        print("WARNING: best checkpoint missing; saving the final-step model")
    save_checkpoint(CKPT_DIR / f"{final_name}.pt", model, cfg, best_step if best_step >= 0 else step + 1,
                    None, {**extra_base, "val_loss": best_val if math.isfinite(best_val) else None})


def _cli() -> None:
    p = argparse.ArgumentParser(
        description="Silicat training. `--v3` presets: n-layer 12, n-head 12, n-kv-head 4, n-embd 768, "
                    "block-size 512, batch-size 8 (legacy: 6/6/384/256/32). Chat defaults: lr 1e-4, warmup 50, "
                    "eval-interval 100, data/silicat_chat_v3.jsonl (v3), steps = --chat-epochs worth.",
        epilog="v3 pretrain recipe: --stage pretrain --v3 --lr 3e-4 --warmup 400 --max-steps 10000 --wsd --resume",
    )
    p.add_argument("--stage", choices=["pretrain", "chat"], default="pretrain")
    p.add_argument("--device", default=None)
    p.add_argument("--batch-size", type=int, default=None)
    p.add_argument("--block-size", type=int, default=None)
    p.add_argument("--n-layer", type=int, default=None)
    p.add_argument("--n-head", type=int, default=None)
    p.add_argument("--n-embd", type=int, default=None)
    p.add_argument("--n-kv-head", type=int, default=None, help="GQA KV heads (v3 only; default 4)")
    p.add_argument("--dropout", type=float, default=0.0)
    p.add_argument("--lr", type=float, default=None, help="default 3e-4 pretrain, 1e-4 chat")
    p.add_argument("--weight-decay", type=float, default=0.1)
    p.add_argument("--max-steps", type=int, default=None, help="default 2000 pretrain; chat: from --chat-epochs")
    p.add_argument("--warmup", type=int, default=None, help="default 100 pretrain, 50 chat")
    p.add_argument("--log-interval", type=int, default=10)
    p.add_argument("--eval-interval", type=int, default=None, help="default 200 pretrain, 100 chat")
    p.add_argument("--save-interval", type=int, default=500, help="checkpoint every N optimizer steps (both stages)")
    p.add_argument("--precision", choices=["auto", "fp32", "bf16"], default="auto",
                   help="auto: bf16 autocast on CUDA / CPUs with AMX or avx512_bf16")
    p.add_argument("--amp", action="store_true", help="deprecated alias for --precision bf16")
    p.add_argument("--grad-accum", type=int, default=1, help="micro-batches per optimizer step")
    p.add_argument("--seed", type=int, default=1337)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--require-resume", action="store_true", help="with --resume: fail if nothing to resume")
    p.add_argument("--fresh", action="store_true", help="archive an existing checkpoint to checkpoints/old/ and restart")
    p.add_argument("--rewarmup", type=int, default=100,
                   help="LR re-warmup steps when resuming without optimizer state")
    p.add_argument("--eval-windows", type=int, default=64, help="fixed validation windows per eval (pretrain)")
    p.add_argument("--chat-data", default=None, help="default data/silicat_chat_v3.jsonl for --v3")
    p.add_argument("--chat-eval-data", default=None, help="held-out chat JSONL (default data/silicat_chat_eval.jsonl if present)")
    p.add_argument("--chat-val-frac", type=float, default=0.02, help="hash hold-out fraction when no eval file")
    p.add_argument("--val-max", type=int, default=400)
    p.add_argument("--chat-epochs", type=float, default=3.0)
    p.add_argument("--patience", type=int, default=0, help="chat: stop after N evals without val improvement (0=off)")
    p.add_argument("--v2", action="store_true", help="use v2 tokenizer and data paths")
    p.add_argument("--v3", action="store_true", help="use v3 model (RMSNorm/RoPE/GQA/SwiGLU)")
    p.add_argument("--wsd", action="store_true", help="use Warmup-Stable-Decay scheduler")
    args = p.parse_args()
    _resolve_defaults(args)
    if args.grad_accum < 1:
        raise SystemExit("--grad-accum must be >= 1")
    if args.stage == "pretrain":
        pretrain(args)
    else:
        chat(args)


if __name__ == "__main__":
    _cli()
