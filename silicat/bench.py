"""Functional-correctness benchmark: does Silicat write code that passes unit tests?

    python -m silicat.bench [--ckpt PATH] [--bench data/problems/benchmark.jsonl] [--limit N]
                            [--max-new-tokens 384] [--json OUT.json] [--oracle]

Each held-out problem (data/problems/benchmark.jsonl, built by data/build_problems.py and never
trained on) is sent as a user turn; the reply is greedy-decoded, the code is extracted (the fenced
block that defines the entry point, else the first block, else the whole reply) and run together
with the problem's assert tests in a fresh subprocess (5 s timeout). Reports pass@1 overall and
per difficulty. --oracle scores the reference solutions instead of the model (harness self-test,
should be 100%).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENCH = ROOT / "data" / "problems" / "benchmark.jsonl"

_FENCE = re.compile(r"```[ \t]*([\w+-]*)[ \t]*\n(.*?)(?:```|\Z)", re.S)


def extract_code(reply: str, entry_point: str) -> str:
    """Pick the code to test from a model reply (an unclosed final fence is accepted)."""
    blocks = [(lang.lower(), body) for lang, body in _FENCE.findall(reply)]
    blocks = [b for lang, b in blocks if lang in ("", "python", "py", "python3")]
    if not blocks:
        return reply
    defines = re.compile(rf"^\s*(?:async\s+)?(?:def|class)\s+{re.escape(entry_point)}\b", re.M)
    for b in blocks:
        if defines.search(b):
            return b
    return blocks[0]


def run_tests(code: str, tests: str, timeout: float = 5.0) -> tuple[bool, str]:
    """Run code + tests in an isolated interpreter inside a temp dir. Returns (passed, error)."""
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "candidate.py"
        f.write_text(code + "\n\n" + tests + "\n", encoding="utf-8")
        try:
            p = subprocess.run([sys.executable, "-I", str(f)], cwd=d, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return False, "timeout"
    if p.returncode == 0:
        return True, ""
    lines = p.stderr.strip().splitlines()
    return False, (lines[-1] if lines else f"exit {p.returncode}")[:200]


def load_problems(path: Path, limit: int | None = None) -> list[dict]:
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows[:limit] if limit else rows


def summarize(results: list[dict]) -> dict:
    by: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for r in results:
        for k in ("all", r.get("difficulty", "?")):
            by[k][0] += r["passed"]
            by[k][1] += 1
    return {k: {"passed": p, "total": n, "pass@1": round(p / n, 4) if n else 0.0} for k, (p, n) in by.items()}


def main() -> None:
    ap = argparse.ArgumentParser(description="pass@1 of Silicat on held-out unit-tested problems")
    ap.add_argument("--ckpt", default=None, help="checkpoint path/name (default: best available)")
    ap.add_argument("--bench", type=Path, default=DEFAULT_BENCH)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--max-new-tokens", type=int, default=384)
    ap.add_argument("--temperature", type=float, default=0.0, help="0 = greedy (deterministic)")
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--oracle", action="store_true", help="score the reference solutions (harness self-test)")
    ap.add_argument("--json", default=None, help="write per-problem results to this file")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    problems = load_problems(args.bench, args.limit)
    gen = None
    if not args.oracle:
        from .chat_format import Message, fit_prompt
        from .generate import load_engine, stream

        eng = load_engine(args.ckpt)
        tok = eng.tok
        stop_ids = {tok.special_id(t) for t in ("<|end|>", "<|user|>", "<|silicat|>")}
        block = eng.cfg.block_size
        print(f"loaded: {eng.arch}/{eng.stage} step {eng.step}, {eng.model.num_params():,} params, file {eng.path.name}")

        def gen(text: str) -> str:
            budget = min(args.max_new_tokens, block - 32)
            ids, _ = fit_prompt([Message("user", text)], tok, block - budget)
            out = list(stream(eng.model, ids, max_new_tokens=budget, temperature=args.temperature,
                              repetition_penalty=1.0, stop_ids=stop_ids, seed=0, device=eng.device))
            return tok.decode(out)

    results, t0 = [], time.time()
    for p in problems:
        reply = p["solution"] if args.oracle else gen(p["prompt"])
        code = extract_code(reply, p["entry_point"])
        ok, err = run_tests(code, p["tests"], args.timeout)
        results.append({"id": p["id"], "difficulty": p.get("difficulty", "?"), "passed": ok, "error": err,
                        "reply": reply if not args.oracle else ""})
        if not args.quiet:
            print(f"{p['id']:>6} {'PASS' if ok else 'FAIL'} {err}")
    summary = summarize(results)
    for k, v in sorted(summary.items(), key=lambda kv: kv[0] != "all"):
        print(f"pass@1 {k:>7}: {v['passed']}/{v['total']} = {v['pass@1']:.1%}")
    print(f"{time.time() - t0:.0f}s")
    if args.json:
        Path(args.json).write_text(json.dumps({"summary": summary, "results": results}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
