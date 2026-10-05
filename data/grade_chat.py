"""Deterministic quality grader for chat examples.

    python data/grade_chat.py FILE.jsonl            # report pass/fail per row + summary
    python data/grade_chat.py FILE.jsonl --failures # print only failing rows with reasons
    python data/grade_chat.py FILE.jsonl --json     # machine-readable results

A row passes only if ALL checks pass:
  schema      user/silicat alternation, non-empty
  prompt      a real request (>= 3 words), not a bare keyword like "Unittest"
  depth       the answer explains: >= 150 chars, or contains a code block plus >= 1 sentence of prose
  fences      every ``` fence is closed
  syntax      every ```python block parses (ast)
  executes    self-contained python blocks run cleanly in a subprocess (5 s timeout); blocks that
              need the network, files, extra packages, input() or long sleeps are skipped, not failed
  style       no LLM filler ("As an AI", "I hope this helps", leading "Certainly!"/"Sure,")
  length      fits the 512-token block with the chat template (needs checkpoints/tokenizer_v2)

Correctness of the *explanation* is not machine-checkable; that is the job of the separate LLM
judge pass. This script is the gate every generated row must clear first.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOK_DIR = ROOT / "checkpoints" / "tokenizer_v2"
BLOCK = 512

FENCE_RE = re.compile(r"```([\w+-]*)\n(.*?)```", re.S)
FILLER_RE = re.compile(r"\bas an ai\b|\bi hope this helps\b|\blet me know if\b|\A\s*(certainly|sure|of course|great question)\b[!,.]", re.I)
SKIP_EXEC_RE = re.compile(
    r"input\(|requests|urllib|http\.|socket|flask|fastapi|django|starlette|uvicorn|redis|pymongo|sqlalchemy|"
    r"psycopg|boto|pandas|numpy|matplotlib|scipy|sklearn|torch|aiohttp|httpx|bs4|yaml|toml\b|click|tqdm|"
    r"open\(|pathlib|shutil|os\.(remove|rmdir|system|makedirs|mkdir|chdir|listdir|walk|unlink)|subprocess|"
    r"while True|time\.sleep\([^0)]|threading|multiprocessing|concurrent|tkinter|argparse|sys\.argv|"
    r"unittest\.main|pytest|sqlite3\.connect\(['\"](?!:memory:)|getpass|signal\.|logging\.FileHandler|\.\.\.\s*$",
    re.M,
)
UNDEFINED_ERRORS = ("NameError", "ModuleNotFoundError", "ImportError")


def _tokenizer():
    try:
        from tokenizers import Tokenizer
        from tokenizers.models import BPE
        from tokenizers.pre_tokenizers import ByteLevel
        from tokenizers.decoders import ByteLevel as BLDec

        tok = Tokenizer(BPE.from_file(str(TOK_DIR / "vocab.json"), str(TOK_DIR / "merges.txt")))
        tok.pre_tokenizer = ByteLevel(add_prefix_space=False)
        tok.decoder = BLDec()
        return tok
    except Exception:
        return None


def run_block(code: str) -> str | None:
    """Return None if the block ran cleanly (or was skipped/undefined-name snippet), else an error line."""
    if SKIP_EXEC_RE.search(code) or len(code.strip().splitlines()) < 2:
        return None
    try:
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=5, cwd=d)
    except subprocess.TimeoutExpired:
        return "timeout"
    if p.returncode == 0:
        return None
    last = (p.stderr.strip().splitlines() or ["error"])[-1]
    if last.startswith(UNDEFINED_ERRORS):  # snippet referring to context defined elsewhere
        return None
    return last[:160]


def grade(row: dict, tok=None, execute: bool = True) -> list[str]:
    reasons: list[str] = []
    msgs = row.get("messages")
    if not isinstance(msgs, list) or len(msgs) < 2:
        return ["schema: no messages"]
    for i, m in enumerate(msgs):
        want = "user" if i % 2 == 0 else "silicat"
        if m.get("role") != want or not str(m.get("content", "")).strip():
            return [f"schema: message {i} role/content"]
    prompt, answer = msgs[0]["content"].strip(), msgs[-1]["content"].strip()

    if len(prompt.split()) < 3:
        reasons.append("prompt: bare keyword")
    blocks = FENCE_RE.findall(answer)
    prose = FENCE_RE.sub("", answer).strip()
    if len(answer) < 150 and not (blocks and len(prose) >= 20):
        reasons.append("depth: too shallow")
    # fences/style/syntax/execution apply to EVERY silicat turn, not just the last one
    for turn, m in enumerate(msgs[1::2], 1):
        a = m["content"]
        at = f" (turn {turn})" if len(msgs) > 2 else ""
        if a.count("```") % 2:
            reasons.append(f"fences: unterminated{at}")
        if FILLER_RE.search(a):
            reasons.append(f"style: filler phrase{at}")
        for lang, code in FENCE_RE.findall(a):
            if lang.lower() in ("python", "py", ""):
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    if lang:  # untagged blocks may be shell/output
                        reasons.append(f"syntax: {e.msg} (line {e.lineno}){at}")
                    continue
                if execute and lang:
                    err = run_block(code)
                    if err:
                        reasons.append(f"executes: {err}{at}")
    if tok is not None:
        n = sum(len(tok.encode(m["content"]).ids) + 2 for m in msgs)
        if n > BLOCK:
            reasons.append(f"length: {n} tokens > {BLOCK}")
    return reasons


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--failures", action="store_true", help="print failing rows only")
    ap.add_argument("--json", action="store_true", help="emit one JSON result per row")
    ap.add_argument("--no-exec", action="store_true", help="skip running code blocks")
    args = ap.parse_args()
    tok = _tokenizer()
    total = passed = 0
    from collections import Counter
    why = Counter()
    for f in args.files:
        for ln, line in enumerate(f.open(encoding="utf-8"), 1):
            if not line.strip():
                continue
            total += 1
            try:
                row = json.loads(line)
                reasons = grade(row, tok, execute=not args.no_exec)
            except json.JSONDecodeError as e:
                row, reasons = {}, [f"schema: bad json ({e.msg})"]
            ok = not reasons
            passed += ok
            why.update(r.split(":")[0] for r in reasons)
            if args.json:
                print(json.dumps({"file": str(f), "line": ln, "pass": ok, "reasons": reasons}))
            elif not ok or not args.failures:
                q = (row.get("messages") or [{}])[0].get("content", "")[:70].replace("\n", " ")
                print(f"{'PASS' if ok else 'FAIL'} {f.name}:{ln} {q!r} {'; '.join(reasons)}")
    if not args.json:
        print(f"\n{passed}/{total} passed" + (f"  failures by check: {dict(why)}" if why else ""))
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
