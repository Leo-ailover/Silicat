"""Clean and re-mix the committed pretraining corpus (data/corpus_v2.txt).

collect_corpus_v2.py cannot be re-run faithfully (its /tmp clones and the
installed site-packages are gone after a container wipe), so corpus_v2.txt is
treated as the frozen raw source and this script post-processes it. It is
deterministic and idempotent: the result is recorded in
data/corpus_v2.manifest.json and a second run on its own output is a no-op.

What it does (counts are printed and written to the manifest):
  1. Splits the file into regions: code/docs | TinyShakespeare | chat
     transcripts | the hand-appended synthetic block.
  2. Drops the chat region ("user: ...\\nsilicat: ..." plain text; it is SFT
     data in a different template than chat_format.py) and the synthetic block
     (it was written 3x, is only ~40 KB unique and was never trained on). The
     deduplicated snippets of data/corpus_synth.txt come back only with
     --include-synth.
  3. Cleans the code/docs region: drops runs of licence-header comments,
     ':copyright:' / ':license:' lines, charmap decoding tables, PDSH notebook
     book-information boilerplate; scrubs e-mail addresses and /home/<name>/.
  4. Drops exact-duplicate long paragraphs (whitespace-normalised, keep first).
  5. Re-chunks at paragraph boundaries into ~6 KB documents, dedupes chunks and
     shuffles them with a fixed seed. silicat.dataset.prepare_v2 takes the
     contiguous tail 5% as validation, so without the shuffle val was
     Shakespeare + chat + synth and not representative of train.
  6. Optional --add-stdlib: the part of the Python stdlib that
     collect_corpus_v2.py truncated away (first 8000 chars per file only),
     cut at top-level statement boundaries (PSF licence; installed Python's
     stdlib, so not byte-reproducible across Python versions).

The output is only written when it is a material change: a first run (no
manifest) or >= --min-gain of the characters removed/added. After a rewrite the
bins must be rebuilt:  python -m silicat.dataset --v2
(the existing checkpoints/tokenizer_v2 is reused).

Usage:  python data/build_corpus.py [--dry-run] [--include-synth]
                                    [--add-stdlib] [--drop-shakespeare]
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import random
import re
import sysconfig
from pathlib import Path

DATA = Path(__file__).resolve().parent
CORPUS = DATA / "corpus_v2.txt"
SYNTH = DATA / "corpus_synth.txt"
MANIFEST = DATA / "corpus_v2.manifest.json"
SNIPPET_SEP = "\n\x0c\n"  # written by gen_pretrain_corpus.py between snippets

CHUNK = 6000
MIN_DEDUP_PARA = 200
SEED = 0

LICENSE_RE = re.compile(
    r"Licensed under|Apache License|SPDX-License|All rights reserved|Permission is hereby granted"
    r"|WITHOUT WARRANTY|WITHOUT WARRANTIES|Copyright \(c\)|Copyright \d{4}|\(C\) ?\d{4}|GNU General Public",
    re.I,
)
TABLE_LINE_RE = re.compile(
    r"^\s*(u?'[^']{1,12}'\s+#.*0x[0-9A-Fa-f]{2,4}|0x[0-9A-Fa-f]+\s*:\s*(0x[0-9A-Fa-f]+|None|u?'[^']*'),?\s*#.*)$"
)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
HOME_RE = re.compile(r"/home/(?!user/)[A-Za-z0-9_.-]+/")
META_LINE_RE = re.compile(r"^\s*:(copyright|license):")
STDLIB_SKIP = {"test", "tests", "idle_test", "encodings", "pydoc_data", "__pycache__", "site-packages", "turtledemo"}


def sha(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


class Stats(dict):
    def add(self, k: str, n: int = 1) -> None:
        self[k] = self.get(k, 0) + n


# ---- region split ---------------------------------------------------------

def strip_trailing_repeats(text: str, min_len: int = 20_000) -> tuple[str, int, int]:
    """If `text` ends with a block repeated k>=2 times, return (text before the
    block, one copy's length P, k). Otherwise (text, 0, 1)."""
    end = len(text)
    if end < 3 * min_len:
        return text, 0, 1
    sig = text[-400:]
    j = text.rfind(sig, 0, end - 1)
    if j < 0:
        return text, 0, 1
    p = end - 400 - j
    if p < min_len:
        return text, 0, 1
    k = 1
    while end - (k + 1) * p >= 0 and text[end - (k + 1) * p : end - k * p] == text[end - p : end]:
        k += 1
    if k < 2:
        return text, 0, 1
    return text[: end - k * p], p, k


def split_regions(text: str) -> dict[str, str]:
    body, p, k = strip_trailing_repeats(text)
    synth = text[len(body):] if k >= 2 else ""
    shak_i = body.find("First Citizen:\nBefore we proceed any further")
    code, shak, chat = body, "", ""
    if shak_i >= 0:
        code = body[:shak_i]
        rest = body[shak_i:]
        # chat transcripts start after Shakespeare (~1.1 MB); first "user: hi"-style doc
        m = re.search(r"\n\nuser: .*\nsilicat: ", rest[1_000_000:])
        if m:
            cut = 1_000_000 + m.start()
            shak, chat = rest[:cut], rest[cut:]
        else:
            shak = rest
    return {"code": code, "shakespeare": shak, "chat": chat, "synth": synth, "synth_reps": str(k)}


# ---- cleaning -------------------------------------------------------------

def _drop_runs(lines: list[str], is_member, min_run: int, confirm=None) -> tuple[list[str], int]:
    out, removed, i = [], 0, 0
    while i < len(lines):
        if is_member(lines[i]):
            j = i
            while j < len(lines) and is_member(lines[j]):
                j += 1
            run = lines[i:j]
            if len(run) >= min_run and (confirm is None or confirm("\n".join(run))):
                removed += sum(len(x) + 1 for x in run)
                i = j
                continue
            out.extend(run)
            i = j
            continue
        out.append(lines[i])
        i += 1
    return out, removed


def _is_comment(l: str) -> bool:
    s = l.lstrip()
    return s.startswith("#") and not s.startswith("#!")


def clean_text(text: str, st: Stats) -> str:
    lines = text.split("\n")
    lines, n = _drop_runs(lines, _is_comment, 3, lambda r: bool(LICENSE_RE.search(r)))
    st.add("chars_license_comment_blocks", n)
    lines, n = _drop_runs(lines, lambda l: bool(TABLE_LINE_RE.match(l)), 16)
    st.add("chars_charmap_tables", n)
    kept = []
    for l in lines:
        if META_LINE_RE.match(l):
            st.add("chars_meta_copyright_lines", len(l) + 1)
            continue
        kept.append(l)
    text = "\n".join(kept)
    text, n1 = EMAIL_RE.subn("user@example.com", text)
    text, n2 = HOME_RE.subn("/home/user/", text)
    st.add("scrubbed_emails", n1)
    st.add("scrubbed_home_paths", n2)
    return text


def drop_boilerplate_paragraphs(paras: list[str], st: Stats) -> list[str]:
    out = []
    for p in paras:
        if p.lstrip().startswith(("<!--BOOK_INFORMATION-->", "<!--NAVIGATION-->")) or "CC-BY-NC-ND" in p:
            st.add("chars_pdsh_boilerplate", len(p) + 2)
            continue
        out.append(p)
    return out


def chunk_paragraphs(paras: list[str], target: int = CHUNK) -> list[str]:
    """Greedy ~target-char chunks; cut only before a paragraph that starts at
    column 0 (so indented method bodies stay with their def)."""
    chunks, cur, size = [], [], 0
    for p in paras:
        top = bool(p) and not p[0].isspace()
        if cur and ((size >= target and top) or size >= 3 * target):
            chunks.append("\n\n".join(cur))
            cur, size = [], 0
        cur.append(p)
        size += len(p) + 2
    if cur:
        chunks.append("\n\n".join(cur))
    return chunks


def process_region(text: str, st: Stats, label: str, seen: set[str]) -> list[str]:
    st.add(f"chars_in_{label}", len(text))
    text = clean_text(text, st)
    paras = [p for p in re.split(r"\n{2,}", text) if p.strip()]
    paras = drop_boilerplate_paragraphs(paras, st)
    kept = []
    for p in paras:
        if len(p) >= MIN_DEDUP_PARA:
            h = sha(norm(p))
            if h in seen:
                st.add("chars_duplicate_paragraphs", len(p) + 2)
                st.add("n_duplicate_paragraphs")
                continue
            seen.add(h)
        kept.append(p)
    return chunk_paragraphs(kept)


# ---- optional stdlib ------------------------------------------------------

def stdlib_chunks(max_chars: int, st: Stats, seen: set[str]) -> list[str]:
    """Remainder of each stdlib file beyond the 8000 chars collect_corpus_v2 kept,
    cut at top-level statement boundaries (never mid-call)."""
    root = Path(sysconfig.get_paths()["stdlib"])
    out, total = [], 0
    for f in sorted(root.rglob("*.py")):
        if any(part in STDLIB_SKIP for part in f.relative_to(root).parts):
            continue
        try:
            text = f.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (OSError, UnicodeDecodeError, SyntaxError, ValueError):
            continue
        if len(text) <= 8000:
            continue
        offs, o = [], 0
        for l in text.splitlines(keepends=True):
            offs.append(o)
            o += len(l)
        bounds = sorted({offs[(n.decorator_list[0].lineno if getattr(n, "decorator_list", None) else n.lineno) - 1] for n in tree.body})
        start = max([b for b in bounds if b <= 8000] or [0])
        cur_start = start
        for b in bounds + [len(text)]:
            if b - cur_start >= CHUNK or b == len(text):
                piece = text[cur_start:b]
                cur_start = b
                if len(piece.strip()) < 200:
                    continue
                st2 = Stats()
                piece = clean_text(piece, st2)
                h = sha(norm(piece))
                if h in seen:
                    continue
                seen.add(h)
                out.append(piece.strip())
                total += len(piece)
        if total >= max_chars:
            break
    st.add("chars_added_stdlib", total)
    st.add("n_chunks_stdlib", len(out))
    return out


# ---- main -----------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--src", type=Path, default=CORPUS)
    ap.add_argument("--out", type=Path, default=CORPUS)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="write even if not material / already built")
    ap.add_argument("--min-gain", type=float, default=0.01, help="min fraction of chars changed to justify a rewrite when a manifest exists")
    ap.add_argument("--include-synth", action="store_true", help="add deduplicated snippets of data/corpus_synth.txt")
    ap.add_argument("--add-stdlib", action="store_true", help="add stdlib text beyond the first 8000 chars of each file")
    ap.add_argument("--stdlib-max-chars", type=int, default=8_000_000)
    ap.add_argument("--drop-shakespeare", action="store_true")
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    raw = args.src.read_bytes()
    in_sha = hashlib.sha256(raw).hexdigest()
    prev = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else None
    if prev and prev.get("output_sha256") == in_sha and not args.force:
        print(f"{args.src} is already the output of build_corpus.py (manifest match); nothing to do")
        return
    text = raw.decode("utf-8")

    st = Stats()
    reg = split_regions(text)
    st["chars_input"] = len(text)
    st["chars_chat_region_dropped"] = len(reg["chat"])
    st["n_chat_user_lines_dropped"] = len(re.findall(r"(?m)^user: ", reg["chat"]))
    st["chars_synth_region_dropped"] = len(reg["synth"])
    st["synth_repetitions_found"] = int(reg["synth_reps"])
    st["chars_in_shakespeare"] = len(reg["shakespeare"])

    seen: set[str] = set()
    chunks = process_region(reg["code"], st, "code_docs", seen)
    if reg["shakespeare"] and not args.drop_shakespeare:
        chunks += chunk_paragraphs([p for p in re.split(r"\n{2,}", reg["shakespeare"]) if p.strip()])
    if args.include_synth and SYNTH.exists():
        s = SYNTH.read_text(encoding="utf-8")
        if "\x0c" not in s:  # legacy 3x-repeated, undelimited file: keep one copy
            body, pl, k = strip_trailing_repeats(s, min_len=1000)
            s = s[len(s) - pl:] if k >= 2 else s
        snips = s.split("\x0c")
        n0 = len(snips)
        uniq = [x.strip() for x in dict.fromkeys(snips) if x.strip()]
        st["n_synth_snippets"] = n0
        st["n_synth_unique_snippets"] = len(uniq)
        chunks += uniq
    if args.add_stdlib:
        chunks += stdlib_chunks(args.stdlib_max_chars, st, seen)

    before = len(chunks)
    uniq_chunks, seen_c = [], set()
    for c in chunks:
        h = sha(norm(c))
        if h not in seen_c:
            seen_c.add(h)
            uniq_chunks.append(c)
    st["n_duplicate_chunks"] = before - len(uniq_chunks)
    random.Random(args.seed).shuffle(uniq_chunks)
    out_text = "\n\n".join(c.strip() for c in uniq_chunks) + "\n\n"
    st["chars_output"] = len(out_text)
    st["n_documents_output"] = len(uniq_chunks)
    changed = abs(len(out_text) - len(text)) / max(1, len(text))
    st["fraction_chars_changed"] = round(changed, 4)

    for k, v in st.items():
        print(f"  {k:36s} {v:,}" if isinstance(v, int) else f"  {k:36s} {v}")

    material = prev is None or changed >= args.min_gain
    if args.dry_run or not (material or args.force):
        print("not writing:", "dry run" if args.dry_run else f"change {changed:.2%} < min-gain and manifest exists")
        return
    args.out.write_text(out_text, encoding="utf-8")
    out_sha = hashlib.sha256(out_text.encode("utf-8")).hexdigest()
    MANIFEST.write_text(json.dumps({
        "input_sha256": in_sha, "output_sha256": out_sha, "seed": args.seed,
        "options": {"include_synth": args.include_synth, "add_stdlib": args.add_stdlib, "drop_shakespeare": args.drop_shakespeare},
        "stats": st,
        "note": "val split in silicat.dataset.prepare_v2 is the tail 5%; documents are shuffled so it is a mix of sources. Rebuild bins: python -m silicat.dataset --v2",
    }, indent=2) + "\n")
    print(f"wrote {args.out} ({len(out_text)/1e6:.1f} MB) and {MANIFEST.name}; now run: python -m silicat.dataset --v2")


if __name__ == "__main__":
    main()
