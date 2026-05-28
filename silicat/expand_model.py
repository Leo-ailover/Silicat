"""Expand a 12-layer 91M model to 24-layer 176M by duplicating all layers.

This is a depth-growth / layer-stacking technique: each of the 24 output
layers is initialised from one of the 12 source layers (layer i → i%12).
The model inherits pretrained representations and skips a full re-pretrain.

Usage:
    python -m silicat.expand_model \
        --src checkpoints/latest.pt \
        --dst checkpoints/expanded.pt \
        --n-layer 24
"""
from __future__ import annotations

import argparse
from pathlib import Path

import torch

from .model import GPT, GPTConfig


def expand(src_path: Path, dst_path: Path, n_layer: int) -> None:
    ck = torch.load(src_path, map_location="cpu")
    old_cfg = GPTConfig(**ck["config"])
    src_n = old_cfg.n_layer

    print(f"Source: {src_n} layers  {sum(v.numel() for v in ck['model'].values())/1e6:.1f}M params")

    # Build new config — same width, more layers
    new_cfg = GPTConfig(
        vocab_size=old_cfg.vocab_size,
        block_size=old_cfg.block_size,
        n_layer=n_layer,
        n_head=old_cfg.n_head,
        n_embd=old_cfg.n_embd,
        dropout=old_cfg.dropout,
        bias=old_cfg.bias,
    )
    new_model = GPT(new_cfg)
    new_sd = new_model.state_dict()
    src_sd = ck["model"]

    copied = 0
    for key in new_sd:
        if key.startswith("transformer.h."):
            # transformer.h.{i}.xxx  →  map i → i % src_n
            parts = key.split(".")
            layer_idx = int(parts[2])
            src_key = ".".join(parts[:2] + [str(layer_idx % src_n)] + parts[3:])
            if src_key in src_sd:
                new_sd[key] = src_sd[src_key].clone()
                copied += 1
        elif key in src_sd:
            new_sd[key] = src_sd[key].clone()
            copied += 1

    new_model.load_state_dict(new_sd)
    total = sum(p.numel() for p in new_model.parameters())
    print(f"Target: {n_layer} layers  {total/1e6:.1f}M params  ({copied} tensors copied)")

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model": new_sd, "config": new_cfg.__dict__, "step": 0}, dst_path)
    print(f"Saved → {dst_path}")


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--src", default="checkpoints/latest.pt")
    p.add_argument("--dst", default="checkpoints/expanded.pt")
    p.add_argument("--n-layer", type=int, default=24)
    args = p.parse_args()
    expand(Path(args.src), Path(args.dst), args.n_layer)


if __name__ == "__main__":
    _cli()
