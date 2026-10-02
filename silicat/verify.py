"""Sanity check of a trained Silicat: run a broad prompt set, check each reply,
print a pass summary and exit non-zero if too many fail.

    python -m silicat.verify [--ckpt PATH] [--n-prompts N] [--max-new-tokens 200]
                             [--min-pass 0.8] [--n-eval 10] [--json OUT.json]

Per reply (greedy by default, so the run is deterministic):
  nonempty    the reply has text
  terminated  the model emitted <|end|> within the token budget
  no_leak     no <|pad|>/<|user|>/<|silicat|> control token was generated
  fences      markdown ``` fences are balanced
  python_ok   every closed ```python fence passes ast.parse
  has_code    (code prompts only) at least one closed ```python fence exists
Prompts: a canned set plus user turns from data/silicat_chat_eval.jsonl (held out).
"""
from __future__ import annotations

import argparse
import ast
import json
import random
import re
import sys
import time
from pathlib import Path

import torch

from .chat_format import Message, fit_prompt
from .generate import load_engine, stream

# (prompt, expects_python_code)
CANNED: list[tuple[str, bool]] = [
    ("hi", False),
    ("who are you?", False),
    ("what can you help me with?", False),
    ("what is a python decorator?", False),
    ("explain the difference between a list and a tuple", False),
    ("what does the 'with' statement do in python?", False),
    ("write a function that checks if a number is prime", True),
    ("write fizzbuzz", True),
    ("reverse a string in python", True),
    ("write a function to compute the nth fibonacci number", True),
    ("how do I read a file line by line in python?", True),
    ("write a function that returns the largest element of a list without using max", True),
    ("write a python class for a stack with push, pop and peek", True),
    ("write a function to count word frequencies in a string", True),
    ("show me how to sort a list of dictionaries by a key", True),
    ("write a function that merges two sorted lists", True),
    ("write a function that checks whether a string is a palindrome", True),
    ("how do I handle an exception when dividing by zero?", True),
    ("write a recursive function to compute factorial", True),
    ("write a function to flatten a nested list", True),
    ("write a binary search function", True),
    ("how do I make an HTTP GET request in python?", True),
    ("write a function that removes duplicates from a list while keeping order", True),
    ("write a context manager that times a block of code", True),
]

FENCE = re.compile(r"```[ \t]*([\w+-]*)[ \t]*\n(.*?)```", re.S)
CONTROL = ("<|pad|>", "<|user|>", "<|silicat|>")


def check_reply(reply: str, terminated: bool, expects_code: bool) -> dict[str, bool]:
    """Pure function: evaluate one decoded reply."""
    closed = FENCE.findall(reply)
    py = [code for lang, code in closed if lang.lower() in ("python", "py")]
    ok = True
    for code in py:
        try:
            ast.parse(code)
        except SyntaxError:
            ok = False
    res = {
        "nonempty": bool(reply.strip()),
        "terminated": terminated,
        "no_leak": not any(c in reply for c in CONTROL),
        "fences": reply.count("```") % 2 == 0,
        "python_ok": ok,
    }
    if expects_code:
        res["has_code"] = bool(py)
    return res


def load_eval_prompts(path: Path, n: int, seed: int) -> list[tuple[str, bool]]:
    if n <= 0 or not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            msgs = json.loads(line)["messages"]
        except (ValueError, KeyError):
            continue
        if msgs and msgs[0]["role"] == "user" and len(msgs) >= 2:
            rows.append((msgs[0]["content"], "```python" in msgs[1]["content"]))
    random.Random(seed).shuffle(rows)
    return rows[:n]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ckpt", default=None, help="checkpoint path/name (default: best available)")
    ap.add_argument("--n-prompts", type=int, default=len(CANNED), help="canned prompts to use")
    ap.add_argument("--n-eval", type=int, default=10, help="extra prompts from the held-out chat eval file")
    ap.add_argument("--eval-file", default=None)
    ap.add_argument("--max-new-tokens", type=int, default=200)
    ap.add_argument("--temperature", type=float, default=0.0, help="0 = greedy (deterministic)")
    ap.add_argument("--top-k", type=int, default=40)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--repetition-penalty", type=float, default=1.1)
    ap.add_argument("--no-repeat-ngram", type=int, default=0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--min-pass", type=float, default=0.8, help="required fraction of prompts passing every check")
    ap.add_argument("--report-only", action="store_true", help="always exit 0")
    ap.add_argument("--json", default=None, help="write results to this file")
    ap.add_argument("--quiet", action="store_true", help="do not print replies")
    args = ap.parse_args(argv)

    try:
        eng = load_engine(args.ckpt)
    except Exception as e:
        print(f"FAIL: could not load model: {type(e).__name__}: {e}")
        return 1
    tok = eng.tok
    print(
        f"loaded: {eng.arch}/{eng.stage} {eng.model.num_params():,} params, step {eng.step}, "
        f"device {eng.device}, file {eng.path.name}"
    )
    print("-" * 60)

    from . import checkpoint as ckpt_mod
    eval_file = Path(args.eval_file) if args.eval_file else ckpt_mod.ROOT / "data" / "silicat_chat_eval.jsonl"
    prompts = CANNED[: max(args.n_prompts, 0)] + load_eval_prompts(eval_file, args.n_eval, args.seed)
    stop_ids = {tok.special_id(t) for t in ("<|end|>", "<|user|>", "<|silicat|>")}
    block = eng.cfg.block_size
    results = []
    t0 = time.time()
    for text, expects_code in prompts:
        budget = min(args.max_new_tokens, block - 16)
        ids, _ = fit_prompt([Message("user", text)], tok, block - budget)
        out: list[int] = []
        info: dict = {}
        for t in stream(
            eng.model, ids, max_new_tokens=budget, temperature=args.temperature,
            top_k=args.top_k, top_p=args.top_p, repetition_penalty=args.repetition_penalty,
            no_repeat_ngram=args.no_repeat_ngram, stop_ids=stop_ids, seed=args.seed,
            info=info, device=eng.device,
        ):
            out.append(t)
        reply = tok.decode(out)
        checks = check_reply(reply, info.get("finish_reason") == "stop", expects_code)
        ok = all(checks.values())
        failed = [k for k, v in checks.items() if not v]
        results.append({"prompt": text, "reply": reply, "tokens": len(out), "ok": ok, "failed": failed})
        if not args.quiet:
            print(f"USER:    {text}")
            print(f"SILICAT: {reply}")
        print(f"  -> {'PASS' if ok else 'FAIL ' + ','.join(failed)} ({len(out)} tokens)")
        print("-" * 60)

    n = len(results)
    n_ok = sum(r["ok"] for r in results)
    rate = n_ok / n if n else 0.0
    by_check: dict[str, int] = {}
    for r in results:
        for k in r["failed"]:
            by_check[k] = by_check.get(k, 0) + 1
    print(f"passed {n_ok}/{n} ({rate:.0%}); required {args.min_pass:.0%}; {time.time() - t0:.0f}s")
    if by_check:
        print("failures by check: " + ", ".join(f"{k}={v}" for k, v in sorted(by_check.items())))
    if args.json:
        Path(args.json).write_text(
            json.dumps({"ckpt": eng.path.name, "step": eng.step, "pass_rate": rate, "results": results}, indent=1),
            encoding="utf-8",
        )
    passed = n > 0 and rate >= args.min_pass
    print("RESULT: PASS" if passed else "RESULT: FAIL")
    return 0 if (passed or args.report_only) else 1


if __name__ == "__main__":
    sys.exit(main())
