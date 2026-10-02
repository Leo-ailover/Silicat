"""Export a checkpoint as a compact fp16, weights-only file (for git push / serving).

The export keeps {model(fp16), config, step, arch, stage, dtype:"float16"} and
drops optimizer / RNG state. Tied tensors (tok_emb / head) stay a single
storage (201 MB instead of 252 MB for the 100.7M model). It NEVER overwrites
its source: the live fp32 checkpoint must stay untouched.

    python -m silicat.halve --src checkpoints/latest_v3.pt --dst checkpoints/latest_v3.fp16.pt
"""
from __future__ import annotations

import argparse
from pathlib import Path

import torch

from .checkpoint import CKPT_DIR, atomic_save, load_checkpoint

KEEP = ("config", "step", "arch", "stage", "best_loss", "best_step", "val_loss", "pretrain_step", "seed")


def export(src: Path, dst: Path) -> None:
    src, dst = Path(src), Path(dst)
    if src.resolve() == dst.resolve():
        raise SystemExit("refusing to halve in place: --dst must differ from --src")
    before = src.stat().st_size
    ck = load_checkpoint(src)
    memo: dict[tuple, torch.Tensor] = {}
    out = {}
    for k, v in ck["model"].items():
        if not v.is_floating_point():
            out[k] = v
            continue
        v32 = v.float()
        if not torch.isfinite(v32).all():
            raise SystemExit(f"non-finite values in {k}; refusing to export")
        if v32.abs().max() >= 65000:
            raise SystemExit(f"{k} exceeds fp16 range; refusing to export")
        key = (v.untyped_storage().data_ptr(), v.storage_offset(), tuple(v.shape), tuple(v.stride()))
        if key not in memo:  # preserve aliasing of tied weights
            memo[key] = v.detach().half().contiguous()
        out[k] = memo[key]
    new = {k: ck[k] for k in KEEP if k in ck}
    new.update({"model": out, "dtype": "float16"})
    atomic_save(new, dst)
    print(f"{before / 1e6:.1f} MB -> {dst.stat().st_size / 1e6:.1f} MB (step {ck.get('step')})")


convert = export


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--src", default=str(CKPT_DIR / "latest_v3.pt"))
    p.add_argument("--dst", default=str(CKPT_DIR / "latest_v3.fp16.pt"))
    args = p.parse_args()
    export(Path(args.src), Path(args.dst))


if __name__ == "__main__":
    _cli()
