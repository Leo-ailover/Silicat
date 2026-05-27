"""Sampling from a trained GPT — supports temperature, top-k, top-p, and streaming."""
from __future__ import annotations

from typing import Iterator

import torch
import torch.nn.functional as F

from .model import GPT


@torch.no_grad()
def stream(
    model: GPT,
    prompt_ids: list[int],
    *,
    max_new_tokens: int = 256,
    temperature: float = 0.9,
    top_k: int | None = 40,
    top_p: float | None = 0.95,
    stop_ids: set[int] | None = None,
    device: str | torch.device = "cpu",
) -> Iterator[int]:
    """Yield token ids one at a time."""
    model.eval()
    block = model.cfg.block_size
    idx = torch.tensor([prompt_ids], dtype=torch.long, device=device)

    for _ in range(max_new_tokens):
        cond = idx if idx.size(1) <= block else idx[:, -block:]
        logits, _ = model(cond)
        logits = logits[:, -1, :] / max(temperature, 1e-5)

        if top_k is not None and top_k > 0:
            k = min(top_k, logits.size(-1))
            vals, _ = torch.topk(logits, k)
            logits = torch.where(
                logits < vals[:, [-1]],
                torch.full_like(logits, float("-inf")),
                logits,
            )

        if top_p is not None and 0 < top_p < 1.0:
            sorted_logits, sorted_idx = torch.sort(logits, descending=True)
            probs = F.softmax(sorted_logits, dim=-1)
            cum = torch.cumsum(probs, dim=-1)
            remove = cum > top_p
            remove[..., 1:] = remove[..., :-1].clone()
            remove[..., 0] = False
            sorted_logits = sorted_logits.masked_fill(remove, float("-inf"))
            logits = torch.full_like(logits, float("-inf")).scatter(
                1, sorted_idx, sorted_logits
            )

        probs = F.softmax(logits, dim=-1)
        next_id = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, next_id], dim=1)
        tok = int(next_id.item())
        yield tok
        if stop_ids and tok in stop_ids:
            return


@torch.no_grad()
def generate(
    model: GPT,
    prompt_ids: list[int],
    **kwargs,
) -> list[int]:
    return list(stream(model, prompt_ids, **kwargs))
