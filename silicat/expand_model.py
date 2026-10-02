"""Grow a model in depth by layer stacking: new layer i is copied from source
layer i % src_n (works for v1 GPT and v3 GPTV3 checkpoints).

For v3 the NoPE/RoPE pattern is baked into layer index, so it is only preserved
when src_n % nope_every == 0 and n_layer % src_n == 0.

Usage:
    python -m silicat.expand_model --src checkpoints/latest_v3.pt \
        --dst checkpoints/expanded_v3.pt --n-layer 24
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import torch

from .checkpoint import CKPT_DIR, build_model, load_checkpoint, save_checkpoint, state_to_fp32
from .assemble import ensure_assembled

_BLOCK = re.compile(r"^blocks\.(\d+)\.(.*)$")


def expand(src_path: Path, dst_path: Path, n_layer: int) -> None:
    src_path = Path(src_path)
    if not src_path.exists():
        src_path = ensure_assembled(src_path)
    ck = load_checkpoint(src_path)
    cfg_d = dict(ck["config"])
    src_n = cfg_d["n_layer"]
    src_sd = state_to_fp32(ck["model"])
    print(f"Source: {src_n} layers  {sum(v.numel() for v in src_sd.values()) / 1e6:.1f}M tensor elements")

    if n_layer < src_n or n_layer % src_n:
        raise SystemExit(f"--n-layer must be a multiple of the source depth {src_n}")
    if "n_kv_head" in cfg_d and src_n % cfg_d.get("nope_every", 4):
        raise SystemExit(
            f"source depth {src_n} is not a multiple of nope_every={cfg_d['nope_every']}: "
            "stacking would move layers between RoPE and NoPE slots"
        )

    cfg_d["n_layer"] = n_layer
    new_model, new_cfg, arch = build_model(cfg_d)
    new_sd = new_model.state_dict()
    tied_head = arch == "v3"
    filled = set()
    for key in new_sd:
        if tied_head and key == "head.weight":
            continue  # tied to tok_emb.weight
        m = _BLOCK.match(key)
        sk = f"blocks.{int(m.group(1)) % src_n}.{m.group(2)}" if m else key
        if sk not in src_sd:
            raise KeyError(f"source checkpoint has no tensor {sk!r} (needed for {key!r})")
        if src_sd[sk].shape != new_sd[key].shape:
            raise ValueError(f"shape mismatch {key}: {tuple(src_sd[sk].shape)} vs {tuple(new_sd[key].shape)}")
        new_sd[key] = src_sd[sk].detach().clone()
        filled.add(key)
    if tied_head and "head.weight" in new_sd:
        new_sd["head.weight"] = new_sd["tok_emb.weight"]
    new_model.load_state_dict(new_sd)

    # verify
    got = new_model.state_dict()
    for key in filled:
        m = _BLOCK.match(key)
        sk = f"blocks.{int(m.group(1)) % src_n}.{m.group(2)}" if m else key
        assert torch.equal(got[key], src_sd[sk]), key
    total = sum(p.numel() for p in new_model.parameters())
    print(f"Target: {n_layer} layers  {total / 1e6:.1f}M params  ({len(filled)}/{len(new_sd)} tensors copied)")

    save_checkpoint(dst_path, new_model, new_cfg, 0, extra={"stage": "pretrain"})
    print("Note: copied o_proj/down weights are not rescaled for the deeper stack; use a LR warmup.")


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--src", default=str(CKPT_DIR / "latest.pt"))
    p.add_argument("--dst", default=str(CKPT_DIR / "expanded.pt"))
    p.add_argument("--n-layer", type=int, default=24)
    args = p.parse_args()
    expand(Path(args.src), Path(args.dst), args.n_layer)


if __name__ == "__main__":
    _cli()
