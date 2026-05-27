"""Byte-level BPE tokenizer for Silicat, with chat special tokens."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from tokenizers import ByteLevelBPETokenizer
from tokenizers.processors import TemplateProcessing


SPECIAL_TOKENS = ["<|pad|>", "<|user|>", "<|silicat|>", "<|end|>"]


class Tokenizer:
    """Thin wrapper around `tokenizers.ByteLevelBPETokenizer`."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(
                f"tokenizer file not found at {self.path}. "
                f"Run `python -m silicat.tokenizer train` to build it."
            )
        self.tk = ByteLevelBPETokenizer.from_file(
            vocab_filename=str(self.path / "vocab.json"),
            merges_filename=str(self.path / "merges.txt"),
        )
        # special tokens are not added by ByteLevelBPETokenizer.from_file —
        # add them explicitly so encode/decode round-trip correctly.
        self.tk.add_special_tokens(SPECIAL_TOKENS)

    def encode(self, text: str) -> list[int]:
        return self.tk.encode(text).ids

    def decode(self, ids: Iterable[int]) -> str:
        return self.tk.decode(list(ids), skip_special_tokens=False)

    @property
    def vocab_size(self) -> int:
        return self.tk.get_vocab_size()

    def special_id(self, tok: str) -> int:
        return self.tk.token_to_id(tok)


def train_tokenizer(
    files: list[str],
    out_dir: str | Path,
    vocab_size: int = 8192,
) -> None:
    """Train a byte-level BPE on the given files and save to `out_dir`."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tk = ByteLevelBPETokenizer()
    tk.train(
        files=files,
        vocab_size=vocab_size,
        min_frequency=2,
        special_tokens=SPECIAL_TOKENS,
    )
    tk.save_model(str(out))
    print(f"saved tokenizer to {out} (vocab_size={tk.get_vocab_size()})")


def _cli() -> None:
    import argparse

    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train")
    t.add_argument("--files", nargs="+", required=True)
    t.add_argument("--out", default="checkpoints/tokenizer")
    t.add_argument("--vocab-size", type=int, default=8192)
    args = p.parse_args()
    if args.cmd == "train":
        train_tokenizer(args.files, args.out, vocab_size=args.vocab_size)


if __name__ == "__main__":
    _cli()
