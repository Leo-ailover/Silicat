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


def _load_corpus(max_samples: int, sample_chars: int) -> list[str]:
    """Pull a small Python-code corpus. Uses `datasets` in streaming mode so
    we never download the full ~50GB."""
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
) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    TOK_DIR.mkdir(parents=True, exist_ok=True)

    raw = DATA_DIR / "corpus.txt"
    if not raw.exists():
        print("downloading corpus...")
        corpus = _load_corpus(max_samples, sample_chars)
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
    args = p.parse_args()
    prepare(
        max_samples=args.max_samples,
        sample_chars=args.sample_chars,
        val_frac=args.val_frac,
        vocab_size=args.vocab_size,
    )


if __name__ == "__main__":
    _cli()
