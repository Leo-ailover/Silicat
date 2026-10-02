"""Split checkpoints into <=45MB parts for git and reassemble them.

GitHub blocks blobs >100MB, so checkpoints are committed as
`checkpoints/<name>.partNN` and concatenated on demand. Generic over names
(latest.pt, latest_v2.pt, latest_v3.pt, latest_v3.fp16.pt, chat_v3.pt, ...).

CLI:
    python -m silicat.assemble checkpoints/latest_v3.fp16.pt          # assemble
    python -m silicat.assemble --split checkpoints/latest_v3.fp16.pt  # split into parts
"""
from __future__ import annotations

import argparse
import os
import re
import zipfile
from pathlib import Path

PART_BYTES = 45 * 1024 * 1024


def list_parts(ckpt_path: Path) -> list[Path]:
    """Parts of `ckpt_path` sorted numerically; raises if indices are not 0..N-1."""
    ckpt_path = Path(ckpt_path)
    pat = re.compile(re.escape(ckpt_path.name) + r"\.part(\d+)$")
    found = []
    for p in ckpt_path.parent.glob(ckpt_path.name + ".part*"):
        m = pat.match(p.name)
        if m:
            found.append((int(m.group(1)), p))
    found.sort()
    if found and [i for i, _ in found] != list(range(len(found))):
        have = [i for i, _ in found]
        missing = sorted(set(range(max(have) + 1)) - set(have))
        raise RuntimeError(f"{ckpt_path.name}: part indices not contiguous (missing {missing})")
    return [p for _, p in found]


def _valid(path: Path) -> bool:
    try:
        return zipfile.is_zipfile(path)
    except OSError:
        return False


def ensure_assembled(ckpt_path: Path, refresh: bool = False) -> Path:
    """Return a valid `ckpt_path`, concatenating `ckpt_path.partNN` if needed.

    An existing, structurally valid file is kept untouched (it may be a live
    training checkpoint) unless `refresh=True` and some part is newer than it
    (use refresh only for derived export files). A truncated file is moved
    aside to `.corrupt`. Assembly is atomic (tmp + os.replace)."""
    ckpt_path = Path(ckpt_path)
    parts = list_parts(ckpt_path)
    if ckpt_path.exists():
        if _valid(ckpt_path):
            stale = refresh and parts and max(p.stat().st_mtime for p in parts) > ckpt_path.stat().st_mtime
            if not stale:
                return ckpt_path
        else:
            bad = ckpt_path.with_name(ckpt_path.name + ".corrupt")
            print(f"WARNING: {ckpt_path} is not a valid checkpoint; moving to {bad}")
            os.replace(ckpt_path, bad)
    if not parts:
        raise FileNotFoundError(
            f"no checkpoint at {ckpt_path} and no `{ckpt_path.name}.part*` files to reassemble from"
        )
    print(f"reassembling {ckpt_path} from {len(parts)} parts...")
    tmp = ckpt_path.with_name(ckpt_path.name + ".assembling")
    try:
        with tmp.open("wb") as out:
            for p in parts:
                with p.open("rb") as f:
                    while chunk := f.read(1 << 22):
                        out.write(chunk)
            out.flush()
            os.fsync(out.fileno())
        if not _valid(tmp):
            raise RuntimeError(f"assembled {ckpt_path.name} is not a valid archive (missing/truncated part?)")
        os.replace(tmp, ckpt_path)
    finally:
        tmp.unlink(missing_ok=True)
    print(f"wrote {ckpt_path} ({ckpt_path.stat().st_size / 1e6:.1f} MB)")
    return ckpt_path


def split_checkpoint(src: Path, part_bytes: int = PART_BYTES) -> list[Path]:
    """Split `src` into `src.part00..`; stale parts are removed only after the new
    ones are fully written (new parts are staged as .new files then renamed)."""
    src = Path(src)
    staged: list[Path] = []
    with src.open("rb") as f:
        i = 0
        while chunk := f.read(part_bytes):
            p = src.with_name(f"{src.name}.part{i:02d}.new")
            p.write_bytes(chunk)
            staged.append(p)
            i += 1
    for old in list_parts(src):
        old.unlink()
    final = []
    for i, p in enumerate(staged):
        dst = src.with_name(f"{src.name}.part{i:02d}")
        os.replace(p, dst)
        final.append(dst)
    print(f"split {src} into {len(final)} parts")
    return final


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("--split", action="store_true")
    p.add_argument("--refresh", action="store_true")
    args = p.parse_args()
    if args.split:
        split_checkpoint(Path(args.path))
    else:
        ensure_assembled(Path(args.path), refresh=args.refresh)


if __name__ == "__main__":
    _cli()
