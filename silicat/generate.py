"""Sampling and model/tokenizer discovery for inference.

- `stream` / `generate`: temperature, top-k, top-p, repetition penalty, no-repeat
  n-gram, seeds; works for v1 `GPT` (full recompute) and `GPTV3` (exact KV cache).
- `IncrementalDecoder`: unicode-safe streaming detokenization.
- `resolve_checkpoint` / `find_tokenizer` / `load_engine`: pick and load the best
  available checkpoint (chat v3 > pretrain v3 > v2 > v1) plus a matching tokenizer.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

import torch
import torch.nn.functional as F

from . import checkpoint as ckpt_mod
from .model import GPT
from .model_v3 import GPTV3
from .tokenizer import Tokenizer

PAD_ID = 0


def _sample(
    logits: torch.Tensor,
    ctx: list[int],
    *,
    temperature: float,
    top_k: int | None,
    top_p: float | None,
    repetition_penalty: float,
    no_repeat_ngram: int,
    ban_ids: Iterable[int],
    generator: torch.Generator | None,
) -> int:
    """Pick the next id from last-position logits (V,) given the running id list."""
    logits = logits.detach().float().cpu().clone()
    V = logits.numel()
    if repetition_penalty and repetition_penalty != 1.0 and ctx:
        ids = torch.tensor(sorted(set(ctx)), dtype=torch.long)
        ids = ids[ids < V]
        sc = logits[ids]
        logits[ids] = torch.where(sc > 0, sc / repetition_penalty, sc * repetition_penalty)
    n = no_repeat_ngram
    if n and n > 1 and len(ctx) >= n:
        prefix = tuple(ctx[len(ctx) - n + 1:])
        for i in range(len(ctx) - n + 1):
            if tuple(ctx[i:i + n - 1]) == prefix and ctx[i + n - 1] < V:
                logits[ctx[i + n - 1]] = float("-inf")
    for b in ban_ids:
        if 0 <= b < V:
            logits[b] = float("-inf")
    if not torch.isfinite(logits).any():  # everything banned: fall back to unconstrained
        logits = torch.zeros_like(logits)

    if temperature is None or temperature <= 0:
        return int(torch.argmax(logits).item())
    logits = logits / temperature

    if top_k is not None and top_k > 0:
        k = min(top_k, V)
        vals, _ = torch.topk(logits, k)
        logits = logits.masked_fill(logits < vals[-1], float("-inf"))

    if top_p is not None and 0 < top_p < 1.0:
        sorted_logits, sorted_idx = torch.sort(logits, descending=True)
        cum = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
        remove = cum > top_p
        remove[1:] = remove[:-1].clone()
        remove[0] = False
        sorted_logits = sorted_logits.masked_fill(remove, float("-inf"))
        logits = torch.full_like(logits, float("-inf")).scatter(0, sorted_idx, sorted_logits)

    probs = F.softmax(logits, dim=-1)
    return int(torch.multinomial(probs, 1, generator=generator).item())


@torch.inference_mode()
def stream(
    model: GPT | GPTV3,
    prompt_ids: list[int],
    *,
    max_new_tokens: int = 256,
    temperature: float = 0.9,
    top_k: int | None = 40,
    top_p: float | None = 0.95,
    repetition_penalty: float = 1.0,
    no_repeat_ngram: int = 0,
    stop_ids: set[int] | None = None,
    ban_ids: Iterable[int] | None = (PAD_ID,),
    seed: int | None = None,
    use_cache: bool = True,
    info: dict | None = None,
    device: str | torch.device | None = None,
) -> Iterator[int]:
    """Yield generated token ids one at a time. The stop token is NOT yielded.

    temperature <= 0 is greedy. Prompts longer than block_size-1 are left-truncated.
    If `info` is a dict it is filled with finish_reason ('stop' | 'length'),
    prompt_tokens (after truncation) and truncated (bool).
    v3 uses a KV cache; when the context reaches block_size the cache is reset and
    re-prefilled with the last block_size//2 tokens (positions restart at 0)."""
    model.eval()
    if device is None:
        device = next(model.parameters()).device
    block = model.cfg.block_size
    stop_ids = stop_ids or set()
    ban = tuple(ban_ids or ())
    prompt = list(prompt_ids)
    if not prompt:
        raise ValueError("empty prompt")
    truncated = len(prompt) > block - 1
    if truncated:
        prompt = prompt[-(block - 1):]
    gen = None
    if seed is not None:
        gen = torch.Generator()
        gen.manual_seed(seed)
    if info is not None:
        info.update(finish_reason="length", prompt_tokens=len(prompt), truncated=truncated)

    cached = use_cache and isinstance(model, GPTV3)
    ids = list(prompt)
    cache = model.new_cache() if cached else None

    def tensor(xs: list[int]) -> torch.Tensor:
        return torch.tensor([xs], dtype=torch.long, device=device)

    def last_logits(new: list[int], reset_to: list[int] | None = None) -> torch.Tensor:
        if not cached:
            cond = ids[-block:]
            return model(tensor(cond))[0][0, -1]
        if reset_to is not None:
            cache.reset()
            new = reset_to
        return model(tensor(new), cache=cache, last_only=True)[0][0, -1]

    sample_kw = dict(
        temperature=temperature, top_k=top_k, top_p=top_p,
        repetition_penalty=repetition_penalty, no_repeat_ngram=no_repeat_ngram,
        ban_ids=ban, generator=gen,
    )
    new = ids
    reset_to = None
    for step in range(max_new_tokens):
        if step > 0 and cached and cache.length + 1 > block:
            reset_to = ids[-(block // 2):]
        logits = last_logits(new, reset_to)
        reset_to = None
        tok = _sample(logits, ids, **sample_kw)
        if tok in stop_ids:
            if info is not None:
                info["finish_reason"] = "stop"
            return
        ids.append(tok)
        new = [tok]
        yield tok


@torch.inference_mode()
def generate(model: GPT | GPTV3, prompt_ids: list[int], **kwargs) -> list[int]:
    return list(stream(model, prompt_ids, **kwargs))


class IncrementalDecoder:
    """Turn a stream of token ids into text pieces without splitting multi-byte
    UTF-8 characters (byte-level BPE can end a token mid-character).

    `push(id)` returns the newly completed text ('' while holding back an
    incomplete character, for at most 4 tokens); `flush()` returns the rest."""

    MAX_HOLD = 4

    def __init__(self, tok: Tokenizer):
        self.tok = tok
        self.ids: list[int] = []
        self.prefix = 0   # start of the decode window
        self.read = 0     # ids before this index have been emitted

    def _delta(self, force: bool) -> str:
        prefix_text = self.tok.decode(self.ids[self.prefix:self.read])
        text = self.tok.decode(self.ids[self.prefix:])
        if len(text) <= len(prefix_text):
            return ""
        if text.endswith("�") and not force and len(self.ids) - self.read < self.MAX_HOLD:
            return ""
        self.prefix, self.read = self.read, len(self.ids)
        return text[len(prefix_text):]

    def push(self, tid: int) -> str:
        self.ids.append(tid)
        return self._delta(False)

    def flush(self) -> str:
        return self._delta(True)


# ---------------------------------------------------------------- discovery
# Preference: chat-finetuned v3 > pretrain v3 > v2 > v1.
CKPT_PREFERENCE = (
    "chat_v3", "chat_best_v3", "chat_latest_v3", "latest_v3", "latest_v2", "latest",
)


def resolve_checkpoint(explicit: str | os.PathLike | None = None) -> Path:
    """Path (maybe assembled lazily by load_model) of the checkpoint to serve.

    Order: `explicit`, then env SILICAT_CKPT (a path, or a bare name inside the
    checkpoint dir), then CKPT_PREFERENCE. An explicit choice that does not
    exist is an error, never a silent fallback."""
    d = ckpt_mod.CKPT_DIR
    choice = explicit or os.environ.get("SILICAT_CKPT")
    if choice:
        p = Path(choice)
        if not p.is_absolute() and not p.exists():
            q = d / (p.name if p.suffix == ".pt" else p.name + ".pt")
            p = q
        name = p.name.removesuffix(".pt").removesuffix(".fp16")
        if p.exists() or ckpt_mod.checkpoint_exists(name, p.parent):
            return p
        raise FileNotFoundError(f"checkpoint {choice!r} not found (looked for {p})")
    for name in CKPT_PREFERENCE:
        if ckpt_mod.checkpoint_exists(name, d):
            return d / f"{name}.pt"
    raise FileNotFoundError(
        f"no checkpoint found in {d} (tried {', '.join(CKPT_PREFERENCE)}). "
        "Train one with `python -m silicat.train` or set SILICAT_CKPT."
    )


def find_tokenizer(vocab_size: int, ckpt_dir: Path | None = None) -> Tokenizer:
    """Load the tokenizer in <ckpt_dir>/tokenizer* whose size equals vocab_size."""
    d = ckpt_dir or ckpt_mod.CKPT_DIR
    cands = sorted(
        (p for p in d.glob("tokenizer*") if (p / "vocab.json").exists()),
        key=lambda p: (p.name != "tokenizer_v2", p.name),
    )
    sizes: dict[str, int | str] = {}
    for p in cands:
        try:
            tok = Tokenizer(p)
        except Exception as e:
            sizes[p.name] = f"unusable ({e})"
            continue
        if tok.vocab_size == vocab_size:
            return tok
        sizes[p.name] = tok.vocab_size
    raise RuntimeError(
        f"no tokenizer with vocab_size={vocab_size} in {d} (found: {sizes or 'none'})"
    )


@dataclass
class Engine:
    model: GPT | GPTV3
    tok: Tokenizer
    cfg: object
    arch: str
    stage: str | None
    step: int
    path: Path
    device: str

    def info(self) -> dict:
        return {
            "arch": self.arch, "stage": self.stage, "step": self.step,
            "checkpoint": self.path.name, "block_size": self.cfg.block_size,
            "vocab_size": self.cfg.vocab_size, "n_params": self.model.num_params(),
            "device": self.device,
        }


def pick_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_engine(path: str | os.PathLike | None = None, device: str | None = None) -> Engine:
    """Resolve + load checkpoint and its tokenizer (vocab sizes must match)."""
    device = device or pick_device()
    p = resolve_checkpoint(path)
    model, cfg, ck = ckpt_mod.load_model(p, device)
    model.eval()
    tok = find_tokenizer(cfg.vocab_size, p.parent)
    stage = ck.get("stage")
    if stage is None:
        stage = "chat" if p.name.startswith("chat") else "pretrain"
    return Engine(model, tok, cfg, ck.get("arch", "v1"), stage, int(ck.get("step", 0)), p, device)
