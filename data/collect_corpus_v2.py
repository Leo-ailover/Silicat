"""Collect a mixed Python + English corpus for v2 tokenizer training and pretraining.

Sources (all local or raw.githubusercontent.com — no HuggingFace):
  1. Python stdlib + installed packages (.py files)
  2. Cloned repos in /tmp (TheAlgorithms, flask, nanoGPT, requests)
  3. Jupyter notebooks (.ipynb) — extracts code + markdown cells
  4. README / markdown from cloned repos
  5. TinyShakespeare from raw.githubusercontent.com
  6. Existing chat JSONL (question + answer as plain text)

Output: data/corpus_v2.txt
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path


OUT = Path("data/corpus_v2.txt")

PY_ROOTS = [
    "/usr/lib/python3.11",
    "/usr/local/lib/python3.11",
    "/tmp/Python",           # TheAlgorithms
    "/tmp/nanoGPT",
    "/tmp/flask",
    "/tmp/requests",
    "/tmp/PythonDataScienceHandbook",
]

SKIP_DIRS = {"test", "tests", "__pycache__", ".git", "node_modules", "vendor"}

SHAKESPEARE_URL = (
    "https://raw.githubusercontent.com/karpathy/char-rnn/master/"
    "data/tinyshakespeare/input.txt"
)


def _read_py_files(roots: list[str], max_chars_per_file: int = 8000) -> list[str]:
    docs = []
    for root in roots:
        p = Path(root)
        if not p.exists():
            continue
        for f in p.rglob("*.py"):
            if any(part in SKIP_DIRS for part in f.parts):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if len(text) < 50:
                continue
            docs.append(text[:max_chars_per_file])
    print(f"  Python .py files: {len(docs)} docs")
    return docs


def _read_notebooks(roots: list[str], max_chars_per_cell: int = 4000) -> list[str]:
    docs = []
    for root in roots:
        p = Path(root)
        if not p.exists():
            continue
        for f in p.rglob("*.ipynb"):
            try:
                nb = json.loads(f.read_text(encoding="utf-8", errors="ignore"))
            except (json.JSONDecodeError, OSError):
                continue
            cells = nb.get("cells", [])
            parts = []
            for cell in cells:
                src = "".join(cell.get("source", []))
                if src.strip():
                    parts.append(src[:max_chars_per_cell])
            if parts:
                docs.append("\n\n".join(parts))
    print(f"  Jupyter notebooks: {len(docs)} notebooks")
    return docs


def _read_markdown(roots: list[str], max_chars_per_file: int = 6000) -> list[str]:
    docs = []
    for root in roots:
        p = Path(root)
        if not p.exists():
            continue
        for f in p.rglob("*.md"):
            if any(part in SKIP_DIRS for part in f.parts):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if len(text) < 100:
                continue
            docs.append(text[:max_chars_per_file])
        for f in p.rglob("*.rst"):
            if any(part in SKIP_DIRS for part in f.parts):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if len(text) < 100:
                continue
            docs.append(text[:max_chars_per_file])
    print(f"  Markdown/RST files: {len(docs)} docs")
    return docs


def _download_shakespeare() -> str:
    try:
        with urllib.request.urlopen(SHAKESPEARE_URL, timeout=15) as r:
            text = r.read().decode("utf-8")
        print(f"  TinyShakespeare: {len(text):,} chars")
        return text
    except Exception as e:
        print(f"  TinyShakespeare: FAILED ({e})")
        return ""


def _load_chat_jsonl(path: Path) -> list[str]:
    docs = []
    if not path.exists():
        return docs
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            msgs = row.get("messages", [])
            parts = []
            for m in msgs:
                role = m.get("role", "")
                content = m.get("content", "").strip()
                if content:
                    parts.append(f"{role}: {content}")
            if parts:
                docs.append("\n".join(parts))
    print(f"  Chat JSONL: {len(docs)} examples")
    return docs


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)
    docs: list[str] = []

    print("Collecting Python code...")
    docs.extend(_read_py_files(PY_ROOTS))

    print("Collecting Jupyter notebooks...")
    docs.extend(_read_notebooks(PY_ROOTS))

    print("Collecting Markdown / RST...")
    docs.extend(_read_markdown(PY_ROOTS))

    print("Downloading TinyShakespeare...")
    shakespeare = _download_shakespeare()
    if shakespeare:
        docs.append(shakespeare)

    print("Loading chat examples...")
    docs.extend(_load_chat_jsonl(Path("data/silicat_chat.jsonl")))

    print(f"\nTotal documents: {len(docs):,}")

    with OUT.open("w", encoding="utf-8") as f:
        for doc in docs:
            f.write(doc.strip())
            f.write("\n\n")

    size_mb = OUT.stat().st_size / 1e6
    print(f"Wrote {OUT} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
