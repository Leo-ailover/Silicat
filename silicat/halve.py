"""Convert a checkpoint's float32 weights to float16 (halves file size).

Inference quality is essentially identical with fp16 for a model this small,
and it keeps the checkpoint under GitHub's 100MB blob limit so it can be
committed directly without git-lfs."""
from __future__ import annotations

import argparse
from pathlib import Path

import torch


def convert(src: Path, dst: Path) -> None:
    ck = torch.load(src, map_location="cpu", weights_only=False)
    state = ck["model"]
    converted = {
        k: (v.half() if v.is_floating_point() else v)
        for k, v in state.items()
    }
    ck["model"] = converted
    ck["dtype"] = "float16"
    torch.save(ck, dst)
    print(f"{src.stat().st_size / 1e6:.1f} MB  →  {dst.stat().st_size / 1e6:.1f} MB")


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--src", default="checkpoints/latest.pt")
    p.add_argument("--dst", default="checkpoints/latest.pt")
    args = p.parse_args()
    convert(Path(args.src), Path(args.dst))


if __name__ == "__main__":
    _cli()
