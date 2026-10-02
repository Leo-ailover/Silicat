"""Download a Python code corpus and tokenize it into a flat binary file.

Strategy is nanoGPT-style: tokenize once, save as a `uint16` (v1) / `uint32` (v2) memmap, then
training samples random windows out of it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np
from tqdm import tqdm

from .tokenizer import Tokenizer, train_tokenizer


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("SILICAT_DATA_DIR", ROOT / "data"))
_CKPT = Path(os.environ.get("SILICAT_CKPT_DIR", ROOT / "checkpoints"))
TOK_DIR = _CKPT / "tokenizer"

# v2 paths (new 32k-vocab tokenizer + mixed corpus)
TOK_DIR_V2 = _CKPT / "tokenizer_v2"
CORPUS_V2 = DATA_DIR / "corpus_v2.txt"

SPLIT_BLOCK = 4096      # tokens per train/val assignment block (multiple of 512)
SPLIT_SEED = 1234
NGRAM = 32              # rolling-hash window for train/val overlap filter
OVERLAP_THRESHOLD = 0.05


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
        "/usr/local/lib/python3.11",
        "/usr/lib/python3.11",
        "/usr/lib/python3",
        "/root",
        "/tmp/pkgs_src",
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
    train, val = _tail_split(arr, val_frac)
    train.tofile(DATA_DIR / "train.bin")
    val.tofile(DATA_DIR / "val.bin")
    meta = {
        "vocab_size": tok.vocab_size,
        "n_train_tokens": int(len(train)),
        "n_val_tokens": int(len(val)),
    }
    (DATA_DIR / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"wrote train.bin ({len(train):,} toks) and val.bin ({len(val):,} toks)")


def _tail_split(arr: np.ndarray, val_frac: float) -> tuple[np.ndarray, np.ndarray]:
    if not 0 < val_frac < 1:
        raise ValueError(f"val_frac must be in (0, 1), got {val_frac}")
    n_val = max(1, int(len(arr) * val_frac))
    return arr[: len(arr) - n_val], arr[len(arr) - n_val :]


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def _ngram_hashes(arr: np.ndarray, n: int = NGRAM) -> np.ndarray:
    """Polynomial rolling hash of every n-gram (uint64, wraps); len = len(arr)-n+1."""
    m = len(arr) - n + 1
    h = np.zeros(m, dtype=np.uint64)
    mul = np.uint64(0x9E3779B97F4A7C15)
    for j in range(n):
        h = h * mul + (arr[j : j + m].astype(np.uint64) + np.uint64(1))
    return h


def block_split(
    arr: np.ndarray,
    val_frac: float = 0.05,
    block: int = SPLIT_BLOCK,
    seed: int = SPLIT_SEED,
    threshold: float = OVERLAP_THRESHOLD,
    ngram: int = NGRAM,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """Deterministic block-level random train/val split.

    The token stream is cut into `block`-token blocks; a seeded permutation picks
    candidate val blocks. A candidate is accepted only if at most `threshold` of its
    `ngram`-grams also occur in blocks that stay in train (so duplicated code /
    the 3x repeated synthetic text cannot leak). Rejected candidates stay in train.
    Train and val are concatenations of their blocks in original order; the trailing
    partial block always goes to train."""
    if not 0 < val_frac < 1:
        raise ValueError(f"val_frac must be in (0, 1), got {val_frac}")
    nb = len(arr) // block
    if nb < 2:
        raise ValueError(f"need at least 2 blocks of {block} tokens, have {len(arr)} tokens")
    target = min(nb - 1, max(1, int(np.ceil(val_frac * nb))))
    bl = block - ngram + 1  # windows fully inside a block
    H = _ngram_hashes(arr[: nb * block], ngram)
    hb = [H[b * block : b * block + bl] for b in range(nb)]
    uniq, counts = np.unique(np.concatenate(hb), return_counts=True)
    counts = counts.astype(np.int64)
    order = np.random.default_rng(seed).permutation(nb)
    val_blocks: list[int] = []
    rejected = 0
    for b in order:
        if len(val_blocks) >= target:
            break
        u, inv, own = np.unique(hb[b], return_inverse=True, return_counts=True)
        idx = np.searchsorted(uniq, u)
        other = counts[idx] - own  # occurrences elsewhere (blocks still in train)
        frac = float((other[inv] > 0).mean())
        if frac > threshold:
            rejected += 1
            continue
        counts[idx] -= own
        val_blocks.append(int(b))
    if not val_blocks:
        raise ValueError("no block passed the overlap filter; raise threshold or val_frac")
    val_blocks.sort()
    vset = set(val_blocks)
    tr_idx = [b for b in range(nb) if b not in vset]
    train = np.concatenate([arr[b * block : (b + 1) * block] for b in tr_idx] + [arr[nb * block :]])
    val = np.concatenate([arr[b * block : (b + 1) * block] for b in val_blocks])
    info = {
        "split": "interleaved_blocks",
        "block": block,
        "seed": seed,
        "ngram": ngram,
        "overlap_threshold": threshold,
        "n_blocks": nb,
        "n_val_blocks": len(val_blocks),
        "n_val_target": target,
        "n_rejected_overlap": rejected,
        "val_block_index_sha256": hashlib.sha256(json.dumps(val_blocks).encode()).hexdigest(),
        "val_blocks": val_blocks,
    }
    return train, val, info


def _encode_corpus(tok: Tokenizer, text: str, chunk_chars: int = 200_000) -> np.ndarray:
    """Encode in paragraph-aligned chunks (batched, multi-threaded)."""
    chunks, i, n = [], 0, len(text)
    while i < n:
        end = min(n, i + chunk_chars)
        if end < n:
            nl = text.find("\n\n", end)
            end = n if nl == -1 else nl + 2
        chunks.append(text[i:end])
        i = end
    parts = []
    for k in tqdm(range(0, len(chunks), 16), desc="encoding"):
        for ids in tok.encode_batch(chunks[k : k + 16]):
            parts.append(np.asarray(ids, dtype=np.uint32))
    return np.concatenate(parts)


def prepare_v2(val_frac: float = 0.05, vocab_size: int = 32768) -> None:
    """Build v2 token bins from data/corpus_v2.txt with a 32k-vocab tokenizer.

    Validation is a deterministic block-level random sample (see `block_split`)."""
    DATA_DIR.mkdir(exist_ok=True)
    TOK_DIR_V2.mkdir(parents=True, exist_ok=True)

    if not CORPUS_V2.exists():
        raise FileNotFoundError(
            f"{CORPUS_V2} not found - run `git checkout -- data/corpus_v2.txt` (it is committed), or rebuild with `python data/collect_corpus_v2.py --force` then `python data/build_corpus.py`"
        )

    if not (TOK_DIR_V2 / "vocab.json").exists():
        print(f"training v2 tokenizer ({vocab_size} vocab)...")
        train_tokenizer([str(CORPUS_V2)], TOK_DIR_V2, vocab_size=vocab_size)
    else:
        print(f"reusing tokenizer at {TOK_DIR_V2}")

    tok = Tokenizer(TOK_DIR_V2)
    print(f"tokenizer vocab size: {tok.vocab_size}")

    print("encoding corpus v2...")
    arr = _encode_corpus(tok, CORPUS_V2.read_text(encoding="utf-8"))
    assert (arr >= 4).all(), "special-token id found in corpus encoding"
    train, val, info = block_split(arr, val_frac)
    for name, a in (("train_v2.bin", train), ("val_v2.bin", val)):
        tmp = DATA_DIR / (name + ".tmp")
        a.tofile(tmp)
        os.replace(tmp, DATA_DIR / name)
    meta = {
        "vocab_size": tok.vocab_size,
        "n_train_tokens": int(len(train)),
        "n_val_tokens": int(len(val)),
        "dtype": "uint32",
        "val_frac": val_frac,
        "corpus_sha256": _sha256_file(CORPUS_V2),
        "tokenizer_sha256": hashlib.sha256(
            (TOK_DIR_V2 / "vocab.json").read_bytes() + (TOK_DIR_V2 / "merges.txt").read_bytes()
        ).hexdigest(),
        **info,
    }
    (DATA_DIR / "meta_v2.json").write_text(json.dumps(meta, indent=2))
    print(
        f"wrote train_v2.bin ({len(train):,} toks) and val_v2.bin ({len(val):,} toks); "
        f"{info['n_val_blocks']}/{info['n_val_target']} val blocks, "
        f"{info['n_rejected_overlap']} candidates rejected for train overlap"
    )


def load_split(split: str, v2: bool = False) -> np.ndarray:
    if v2:
        p = DATA_DIR / f"{split}_v2.bin"
        dtype = np.uint32
    else:
        p = DATA_DIR / f"{split}.bin"
        dtype = np.uint16
    if not p.exists():
        raise FileNotFoundError(f"{p} not found; run `python -m silicat.dataset`")
    return np.memmap(p, dtype=dtype, mode="r")


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--v2", action="store_true", help="build v2 corpus (32k tokenizer)")
    p.add_argument("--max-samples", type=int, default=5000)
    p.add_argument("--sample-chars", type=int, default=4000)
    p.add_argument("--val-frac", type=float, default=0.05)
    p.add_argument("--vocab-size", type=int, default=None, help="default: 32768 with --v2, else 8192")
    p.add_argument(
        "--source",
        choices=["auto", "hf", "local"],
        default="auto",
        help="'hf' = HuggingFace (codeparrot), 'local' = local .py files, 'auto' = try hf then local",
    )
    args = p.parse_args()
    if args.v2:
        prepare_v2(val_frac=args.val_frac, vocab_size=args.vocab_size or 32768)
    else:
        prepare(
            max_samples=args.max_samples,
            sample_chars=args.sample_chars,
            val_frac=args.val_frac,
            vocab_size=args.vocab_size or 8192,
            source=args.source,
        )


if __name__ == "__main__":
    _cli()
