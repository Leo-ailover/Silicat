"""Reassemble a checkpoint from split parts if needed.

The trained checkpoint is ~195MB (fp16) and GitHub blocks single blobs >100MB.
We commit `checkpoints/latest.pt.part00`, `part01`, ... (each <100MB) and
concatenate them on first load if `latest.pt` is missing."""
from __future__ import annotations

from pathlib import Path


def ensure_assembled(ckpt_path: Path) -> Path:
    """If `ckpt_path` exists, return it. Otherwise concatenate
    `ckpt_path.part00`, `part01`, ... into `ckpt_path` and return it."""
    if ckpt_path.exists():
        return ckpt_path
    parts = sorted(ckpt_path.parent.glob(ckpt_path.name + ".part*"))
    if not parts:
        raise FileNotFoundError(
            f"no checkpoint at {ckpt_path} and no `{ckpt_path.name}.part*` files to "
            f"reassemble from"
        )
    print(f"reassembling {ckpt_path} from {len(parts)} parts...")
    with ckpt_path.open("wb") as out:
        for p in parts:
            out.write(p.read_bytes())
    print(f"wrote {ckpt_path} ({ckpt_path.stat().st_size / 1e6:.1f} MB)")
    return ckpt_path
