"""Download a Python code corpus and tokenize it into a flat binary file.

Strategy is nanoGPT-style: tokenize once, save as a `uint16` memmap, then
training samples random windows out of it.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np
from tqdm import tqdm

from .tokenizer import Tokenizer, train_tokenizer


DATA_DIR = Path("data")
TOK_DIR = Path("checkpoints/tokenizer")


def _load_corpus_hf(max_samples: int, sample_chars: int) -> list[str]:
    """Pull a Python corpus from HuggingFace Hub (codeparrot-clean-valid)."""
    from datasets import load_dataset

    ds = load_dataset(
        "codeparrot/codeparrot-clean-valid",
        split="train",
        streaming=True,
    )
    out: list[str] = []
    for row in tqdm(ds, total=max_samples, desc="downloading corpus"):
        content = row.get("content", "")
        if not content:
            continue
        out.append(content[:sample_chars])
        if len(out) >= max_samples:
            break
    return out


def _load_corpus_local(max_samples: int, sample_chars: int, roots: list[str]) -> list[str]:
    """Build a corpus from .py files on the local filesystem.

    Useful when HuggingFace Hub is unreachable. Walks the given roots, skips
    test directories, and returns up to `max_samples` files truncated to
    `sample_chars` chars each."""
    skip_dirs = {"test", "tests", "__pycache__"}
    out: list[str] = []
    for root in roots:
        root_p = Path(root)
        if not root_p.exists():
            continue
        for p in root_p.rglob("*.py"):
            if any(part in skip_dirs for part in p.parts):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except (OSError, UnicodeDecodeError):
                continue
            if len(text) < 100:
                continue
            out.append(text[:sample_chars])
            if len(out) >= max_samples:
                return out
    return out


def _load_corpus(
    max_samples: int,
    sample_chars: int,
    source: str = "auto",
    local_roots: list[str] | None = None,
) -> list[str]:
    """Load a corpus. `source` is 'hf', 'local', or 'auto' (try hf, fall back to local)."""
    default_roots = [
        "/usr/local/lib/python3.11/dist-packages",
        "/usr/lib/python3.11",
    ]
    roots = local_roots or default_roots

    if source == "local":
        return _load_corpus_local(max_samples, sample_chars, roots)
    if source == "hf":
        return _load_corpus_hf(max_samples, sample_chars)
    # auto: try HF, fall back to local
    try:
        out = _load_corpus_hf(max_samples, sample_chars)
        if out:
            return out
    except Exception as e:
        print(f"[hf unreachable: {e}] falling back to local Python sources")
    return _load_corpus_local(max_samples, sample_chars, roots)


def _write_raw(corpus: list[str], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for doc in corpus:
            f.write(doc)
            f.write("\n\n")


def prepare(
    max_samples: int = 5000,
    sample_chars: int = 4000,
    val_frac: float = 0.05,
    vocab_size: int = 8192,
    source: str = "auto",
) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    TOK_DIR.mkdir(parents=True, exist_ok=True)

    raw = DATA_DIR / "corpus.txt"
    if not raw.exists():
        print(f"building corpus (source={source})...")
        corpus = _load_corpus(max_samples, sample_chars, source=source)
        print(f"loaded {len(corpus)} samples")
        _write_raw(corpus, raw)
    else:
        print(f"reusing existing {raw}")

    if not (TOK_DIR / "vocab.json").exists():
        print("training tokenizer...")
        train_tokenizer([str(raw)], TOK_DIR, vocab_size=vocab_size)
    else:
        print(f"reusing existing tokenizer at {TOK_DIR}")

    tok = Tokenizer(TOK_DIR)
    print(f"tokenizer vocab size: {tok.vocab_size}")

    print("encoding corpus...")
    text = raw.read_text(encoding="utf-8")
    # encode in chunks to avoid long single calls
    ids: list[int] = []
    chunk = 200_000
    for i in tqdm(range(0, len(text), chunk)):
        ids.extend(tok.encode(text[i : i + chunk]))
    arr = np.array(ids, dtype=np.uint16)
    n_val = int(len(arr) * val_frac)
    train, val = arr[:-n_val], arr[-n_val:]
    train.tofile(DATA_DIR / "train.bin")
    val.tofile(DATA_DIR / "val.bin")
    meta = {
        "vocab_size": tok.vocab_size,
        "n_train_tokens": int(len(train)),
        "n_val_tokens": int(len(val)),
    }
    (DATA_DIR / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"wrote train.bin ({len(train):,} toks) and val.bin ({len(val):,} toks)")


def load_split(split: str) -> np.ndarray:
    p = DATA_DIR / f"{split}.bin"
    if not p.exists():
        raise FileNotFoundError(f"{p} not found; run `python -m silicat.dataset`")
    return np.memmap(p, dtype=np.uint16, mode="r")


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--max-samples", type=int, default=5000)
    p.add_argument("--sample-chars", type=int, default=4000)
    p.add_argument("--val-frac", type=float, default=0.05)
    p.add_argument("--vocab-size", type=int, default=8192)
    p.add_argument(
        "--source",
        choices=["auto", "hf", "local"],
        default="auto",
        help="'hf' = HuggingFace (codeparrot), 'local' = local .py files, 'auto' = try hf then local",
    )
    args = p.parse_args()
    prepare(
        max_samples=args.max_samples,
        sample_chars=args.sample_chars,
        val_frac=args.val_frac,
        vocab_size=args.vocab_size,
        source=args.source,
    )


if __name__ == "__main__":
    _cli()
