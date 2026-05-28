"""Training loop for Silicat.

Two stages, both invoked by this script depending on `--stage`:
  - `pretrain`: next-token prediction on the raw Python corpus
  - `chat`:     supervised fine-tune on data/silicat_chat.jsonl, loss masked
                so we only learn on Silicat's reply tokens.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path

import numpy as np
import torch
from tqdm import tqdm

from .chat_format import Message, format_for_training
from .dataset import DATA_DIR, TOK_DIR, load_split
from .model import GPT, GPTConfig
from .tokenizer import Tokenizer


CKPT_DIR = Path("checkpoints")


def _device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _get_batch(
    data: np.ndarray, batch_size: int, block_size: int, device: str
) -> tuple[torch.Tensor, torch.Tensor]:
    ix = torch.randint(0, len(data) - block_size - 1, (batch_size,))
    x = torch.stack(
        [torch.from_numpy(np.asarray(data[i : i + block_size], dtype=np.int64)) for i in ix]
    )
    y = torch.stack(
        [
            torch.from_numpy(np.asarray(data[i + 1 : i + 1 + block_size], dtype=np.int64))
            for i in ix
        ]
    )
    return x.to(device), y.to(device)


def _lr_at(step: int, *, warmup: int, total: int, lr_max: float, lr_min: float) -> float:
    if step < warmup:
        return lr_max * (step + 1) / max(1, warmup)
    if step >= total:
        return lr_min
    t = (step - warmup) / max(1, total - warmup)
    return lr_min + 0.5 * (lr_max - lr_min) * (1.0 + math.cos(math.pi * t))


def _build_cfg(vocab_size: int, args: argparse.Namespace) -> GPTConfig:
    return GPTConfig(
        vocab_size=vocab_size,
        block_size=args.block_size,
        n_layer=args.n_layer,
        n_head=args.n_head,
        n_embd=args.n_embd,
        dropout=args.dropout,
    )


def _save(model: GPT, cfg: GPTConfig, step: int, name: str = "latest") -> None:
    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    path = CKPT_DIR / f"{name}.pt"
    torch.save(
        {
            "model": model.state_dict(),
            "config": cfg.__dict__,
            "step": step,
        },
        path,
    )
    print(f"saved {path}")


def pretrain(args: argparse.Namespace) -> None:
    device = args.device or _device()
    print(f"device: {device}")

    tok = Tokenizer(TOK_DIR)
    cfg = _build_cfg(tok.vocab_size, args)
    model = GPT(cfg).to(device)
    print(f"params: {model.num_params():,}")

    if args.resume and (CKPT_DIR / "latest.pt").exists():
        ck = torch.load(CKPT_DIR / "latest.pt", map_location=device)
        model.load_state_dict(ck["model"])
        start_step = ck.get("step", 0)
        print(f"resumed from step {start_step}")
    else:
        start_step = 0

    optim = model.configure_optimizer(args.lr, args.weight_decay)
    train_data = load_split("train")
    val_data = load_split("val")

    use_amp = device == "cuda" and args.amp
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    t0 = time.time()
    for step in range(start_step, args.max_steps):
        lr = _lr_at(
            step,
            warmup=args.warmup,
            total=args.max_steps,
            lr_max=args.lr,
            lr_min=args.lr * 0.1,
        )
        for g in optim.param_groups:
            g["lr"] = lr

        x, y = _get_batch(train_data, args.batch_size, args.block_size, device)
        with torch.amp.autocast("cuda", enabled=use_amp, dtype=torch.bfloat16):
            _, loss = model(x, targets=y)
        optim.zero_grad(set_to_none=True)
        scaler.scale(loss).backward()
        scaler.unscale_(optim)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optim)
        scaler.update()

        if step % args.log_interval == 0:
            dt = time.time() - t0
            print(f"step {step:>6} | loss {loss.item():.4f} | lr {lr:.2e} | {dt:.1f}s")

        if step > 0 and step % args.eval_interval == 0:
            model.eval()
            with torch.no_grad():
                losses = []
                for _ in range(20):
                    vx, vy = _get_batch(val_data, args.batch_size, args.block_size, device)
                    _, vl = model(vx, targets=vy)
                    losses.append(vl.item())
                print(f"  eval loss: {sum(losses) / len(losses):.4f}")
            model.train()
            _save(model, cfg, step)

    _save(model, cfg, args.max_steps)


def _load_chat(path: Path, tok: Tokenizer, block_size: int) -> list[tuple[list[int], list[int]]]:
    out: list[tuple[list[int], list[int]]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            msgs = [Message(role=m["role"], content=m["content"]) for m in row["messages"]]
            ids, mask = format_for_training(msgs, tok)
            if len(ids) > block_size:
                ids = ids[:block_size]
                mask = mask[:block_size]
            out.append((ids, mask))
    return out


def chat(args: argparse.Namespace) -> None:
    device = args.device or _device()
    print(f"device: {device}")
    tok = Tokenizer(TOK_DIR)

    ck_path = CKPT_DIR / "latest.pt"
    if not ck_path.exists():
        raise SystemExit("no checkpoints/latest.pt — run pretrain first")
    ck = torch.load(ck_path, map_location=device)
    cfg = GPTConfig(**ck["config"])
    model = GPT(cfg).to(device)
    model.load_state_dict(ck["model"])
    print(f"loaded pretrain checkpoint from step {ck.get('step', '?')}")

    chat_path = Path(args.chat_data)
    if not chat_path.exists():
        raise SystemExit(f"no chat data at {chat_path}")
    rows = _load_chat(chat_path, tok, cfg.block_size)
    print(f"loaded {len(rows)} chat examples")

    optim = model.configure_optimizer(args.lr, args.weight_decay)
    pad_id = tok.special_id("<|pad|>")

    def batch():
        idxs = np.random.randint(0, len(rows), size=args.batch_size)
        seqs = [rows[i] for i in idxs]
        L = max(len(s[0]) for s in seqs)
        L = min(L, cfg.block_size)
        x = np.full((args.batch_size, L), pad_id, dtype=np.int64)
        y = np.full((args.batch_size, L), -100, dtype=np.int64)
        m = np.zeros((args.batch_size, L), dtype=np.int64)
        for i, (ids, mask) in enumerate(seqs):
            ids = ids[:L]
            mask = mask[:L]
            # next-token targets: shift left
            x[i, : len(ids) - 1] = ids[:-1]
            y[i, : len(ids) - 1] = ids[1:]
            m[i, : len(ids) - 1] = mask[1:]
        return (
            torch.from_numpy(x).to(device),
            torch.from_numpy(y).to(device),
            torch.from_numpy(m).to(device),
        )

    start_step = 0
    chat_ckpt = CKPT_DIR / "chat_latest.pt"
    if args.resume and chat_ckpt.exists():
        ck2 = torch.load(chat_ckpt, map_location=device)
        model.load_state_dict(ck2["model"])
        optim_state = ck2.get("optim")
        if optim_state:
            optim.load_state_dict(optim_state)
        start_step = ck2.get("step", 0)
        print(f"resumed chat fine-tune from step {start_step}")

    for step in range(start_step, args.max_steps):
        lr = _lr_at(
            step,
            warmup=args.warmup,
            total=args.max_steps,
            lr_max=args.lr,
            lr_min=args.lr * 0.1,
        )
        for g in optim.param_groups:
            g["lr"] = lr
        x, y, m = batch()
        _, loss = model(x, targets=y, loss_mask=m)
        optim.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optim.step()
        if step % args.log_interval == 0:
            print(f"chat step {step:>5} | loss {loss.item():.4f} | lr {lr:.2e}", flush=True)
        if step > 0 and step % args.save_interval == 0:
            torch.save({"model": model.state_dict(), "config": cfg.__dict__, "step": step, "optim": optim.state_dict()}, chat_ckpt)
            print(f"  checkpoint saved at step {step}", flush=True)

    _save(model, cfg, args.max_steps, name="latest")


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stage", choices=["pretrain", "chat"], default="pretrain")
    p.add_argument("--device", default=None)
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--block-size", type=int, default=256)
    p.add_argument("--n-layer", type=int, default=6)
    p.add_argument("--n-head", type=int, default=6)
    p.add_argument("--n-embd", type=int, default=384)
    p.add_argument("--dropout", type=float, default=0.0)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--weight-decay", type=float, default=0.1)
    p.add_argument("--max-steps", type=int, default=2000)
    p.add_argument("--warmup", type=int, default=100)
    p.add_argument("--log-interval", type=int, default=10)
    p.add_argument("--eval-interval", type=int, default=200)
    p.add_argument("--save-interval", type=int, default=500)
    p.add_argument("--amp", action="store_true")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--chat-data", default="data/silicat_chat.jsonl")
    args = p.parse_args()
    if args.stage == "pretrain":
        pretrain(args)
    else:
        chat(args)


if __name__ == "__main__":
    _cli()
