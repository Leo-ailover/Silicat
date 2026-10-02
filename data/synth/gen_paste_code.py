"""Generate data/synth/paste_code.jsonl: "fix this code" tasks with pasted code.

The existing chat data has almost no pasted-code prompts. This mines clean python
blocks from the TRAIN split of the built dataset (so nothing is derived from the
held-out eval rows; rows record `derived_from` and the builder re-checks) and
injects ONE verified syntax-level bug per row:
  colon   remove the ':' ending a def/if/for/... line
  paren   remove the last ')' of a line with balanced brackets
  indent  dedent the first body line of a block
  typo    `return` -> `retrun`
Every buggy snippet is checked to FAIL ast.parse and every fixed snippet to
parse; the shown error is the real SyntaxError of the buggy code; the diagnosis
text is produced from the injector's own record (line number, what was changed).
Multi-turn rows add a follow-up ("which line?" / "why?") answered from the same
record. Nothing is executed. Deterministic (seed 0); each source block is used at
most twice (different bug kinds).

Usage: python data/synth/gen_paste_code.py   (writes data/synth/paste_code.jsonl;
then re-run python data/build_chat_dataset.py)
"""
from __future__ import annotations

import argparse
import ast
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_chat_dataset as B  # noqa: E402

HEADER_RE = re.compile(r"^(\s*)(def|class|if|elif|else|for|while|with|try|except|finally)\b.*:\s*$")

PROMPTS = [
    "Fix this code:\n\n```python\n{code}\n```",
    "This doesn't run, can you fix it?\n\n```python\n{code}\n```",
    "```python\n{code}\n```\nWhy does this fail?",
    "I get an error when I run this:\n\n```python\n{code}\n```\n\n```\n{err}\n```",
    "Here is my code:\n\n```python\n{code}\n```\n\nPython says:\n\n```\n{err}\n```\nWhat's wrong?",
    "Can you debug this for me?\n\n```python\n{code}\n```",
    "Find the bug:\n\n```python\n{code}\n```",
    "Why do I get a SyntaxError here?\n\n```python\n{code}\n```",
]
FOLLOWUPS = {
    "line": ("Which line was wrong?", "Line {n}: `{bad}`\n\nIt should be `{good}`."),
    "why": ("Why does Python reject that?", "{why}"),
}
WHY = {
    "colon": "Every compound statement (`def`, `class`, `if`, `for`, `while`, `with`, `try`, ...) must end its header line with a `:`. Without it the parser cannot tell where the block starts, so it reports a SyntaxError.",
    "paren": "Parentheses must be balanced. With a `(` that is never closed the parser keeps reading into the next lines and fails with a SyntaxError.",
    "indent": "Python uses indentation to mark a block. A statement after a header line ending in `:` must be indented, otherwise the parser raises an IndentationError (a kind of SyntaxError).",
    "typo": "`retrun` is not a Python keyword, so the parser sees two names next to each other and reports a SyntaxError. Keywords must be spelled exactly.",
}


def real_error(code: str) -> tuple[str, int] | None:
    try:
        ast.parse(code)
    except SyntaxError as e:
        text = (e.text or "").rstrip("\n")
        err = f'  File "main.py", line {e.lineno}\n    {text.strip()}\n{type(e).__name__}: {e.msg}'
        return err, e.lineno or 0
    except (ValueError, RecursionError):
        return None
    return None


def inject(lines: list[str], kind: str, rng: random.Random):
    """-> (buggy_lines, line_no_1based, diagnosis) or None."""
    idx = list(range(len(lines)))
    rng.shuffle(idx)
    for i in idx:
        l = lines[i]
        if kind == "colon" and HEADER_RE.match(l) and "#" not in l:
            new = l.rstrip()[:-1]
            return lines[:i] + [new] + lines[i + 1 :], i + 1, f"line {i + 1} (`{l.strip()}`) is missing the `:` at the end of the statement"
        if kind == "paren" and l.rstrip().endswith(")") and l.count("(") == l.count(")") and "#" not in l and '"' not in l and "'" not in l:
            new = l.rstrip()[:-1]
            return lines[:i] + [new] + lines[i + 1 :], i + 1, f"line {i + 1} (`{l.strip()}`) is missing its closing `)`"
        if kind == "indent" and i > 0 and HEADER_RE.match(lines[i - 1]) and l.startswith(" ") and l.strip():
            new = l[4:] if l.startswith("    ") else l.lstrip()
            return lines[:i] + [new] + lines[i + 1 :], i + 1, f"line {i + 1} (`{l.strip()}`) must be indented under the statement on line {i}"
        if kind == "typo" and re.match(r"^\s*return\b", l):
            new = l.replace("return", "retrun", 1)
            return lines[:i] + [new] + lines[i + 1 :], i + 1, f"line {i + 1} has the typo `retrun`; the keyword is `return`"
    return None


def mine_blocks(max_lines: int = 22, max_chars: int = 900) -> list[tuple[str, str]]:
    args = B.parse_args([])
    train, _ = B.build(args, exclude=frozenset({"paste_code"}), write=False)
    seen, blocks = set(), []
    for r in train:
        if r.source in B.SYNTHETIC_SOURCES or len(r.msgs) != 2:
            continue
        key = B.norm_key(r.prompt)
        for kind, lang, body in B.split_fences(r.answer):
            n = body.count("\n") + 1
            if kind == "code" and lang == "python" and 4 <= n <= max_lines and len(body) <= max_chars and B.parses(body) and "..." not in body:
                h = B.sha(body)
                if h not in seen:
                    seen.add(h)
                    blocks.append((key, body))
    blocks.sort(key=lambda x: B.sha(x[1]))
    return blocks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-rows", type=int, default=700)
    ap.add_argument("--multi-turn-frac", type=float, default=0.25)
    ap.add_argument("--out", type=Path, default=HERE / "paste_code.jsonl")
    a = ap.parse_args()
    rng = random.Random(0)
    blocks = mine_blocks()
    rng.shuffle(blocks)
    rows, kinds = [], ["colon", "paren", "indent", "typo"]
    used = {k: 0 for k in kinds}
    for key, good in blocks:
        if len(rows) >= a.max_rows:
            break
        lines = good.split("\n")
        order = sorted(kinds, key=lambda k: (used[k], rng.random()))
        made = 0
        for kind in order:
            if made >= 2:
                break
            res = inject(lines, kind, rng)
            if not res:
                continue
            buggy_lines, n, diag = res
            buggy = "\n".join(buggy_lines)
            err = real_error(buggy)
            if err is None or buggy == good:
                continue
            used[kind] += 1
            made += 1
            tmpl = rng.choice(PROMPTS)
            user = tmpl.format(code=buggy, err=err[0])
            fixed_txt = f"The problem is that {diag}. Here is the fixed code:\n\n```python\n{good}\n```"
            msgs = [{"role": "user", "content": user}, {"role": "silicat", "content": fixed_txt}]
            if rng.random() < a.multi_turn_frac:
                q, ans = FOLLOWUPS[rng.choice(["line", "why"])]
                msgs += [{"role": "user", "content": q}, {"role": "silicat", "content": ans.format(n=n, bad=buggy_lines[n - 1].strip(), good=lines[n - 1].strip(), why=WHY[kind])}]
            rows.append({"messages": msgs, "derived_from": key})
    with a.out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    multi = sum(len(r["messages"]) > 2 for r in rows)
    print(f"wrote {len(rows)} rows ({multi} multi-turn), by kind {used}, from {len(blocks)} candidate blocks -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
