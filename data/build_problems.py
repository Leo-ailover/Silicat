"""Build the unit-tested problem sets from data/problems/raw_*.jsonl.

    python data/build_problems.py [--bench-frac 0.2] [--seed 0]

Every raw problem ({id, topic, difficulty, prompt, entry_point, solution, tests, example, explanation})
is re-verified independently of whoever wrote it:
  passes     solution + tests exit cleanly (fresh interpreter, 5 s timeout)
  stub_fails a stub with the same name (returns None / empty class) FAILS the tests, so the tests test something
  example    solution + example runs, and each `print(...)  # out` comment matches the real output
Duplicates (same entry point or same normalised prompt) are dropped. A deterministic, per-difficulty
split then writes:
  data/problems/benchmark.jsonl   held-out pass@1 benchmark for `python -m silicat.bench` (NEVER trained on)
  data/problems/train.jsonl       the rest, full records (reference solutions + tests, e.g. for RL rewards)
  data/synth/problems_sft.jsonl   train split as chat rows (picked up by build_chat_dataset.py)
  data/problems/stats.json        counts and drop reasons
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from silicat.bench import run_tests  # noqa: E402

sys.path.insert(0, str(ROOT / "data"))
from grade_chat import _tokenizer, grade  # noqa: E402

PROB_DIR = ROOT / "data" / "problems"
FIELDS = ("id", "topic", "difficulty", "prompt", "entry_point", "solution", "tests", "example", "explanation")


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def stub_for(p: dict) -> str:
    name = p["entry_point"]
    if re.search(rf"^class\s+{re.escape(name)}\b", p["solution"], re.M):
        return f"class {name}:\n    pass\n"
    return f"def {name}(*args, **kwargs):\n    return None\n"


def example_ok(p: dict) -> str | None:
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "ex.py"
        f.write_text(p["solution"] + "\n\n" + p["example"] + "\n", encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, "-I", str(f)], cwd=d, capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            return "example timeout"
    if r.returncode != 0:
        return "example crashes: " + (r.stderr.strip().splitlines() or ["?"])[-1][:120]
    want = [m.group(1).strip() for line in p["example"].splitlines()
            if "print(" in line and (m := re.search(r"#\s?(.*)$", line))]
    got = [l.strip() for l in r.stdout.splitlines()]
    if want and want != got:
        return f"example output mismatch: expected {want} got {got}"
    return None


def verify(p: dict) -> str | None:
    missing = [k for k in FIELDS if not str(p.get(k, "")).strip()]
    if missing:
        return "missing fields: " + ",".join(missing)
    ok, err = run_tests(p["solution"], p["tests"])
    if not ok:
        return "solution fails tests: " + err
    stub_ok, _ = run_tests(stub_for(p), p["tests"])
    if stub_ok:
        return "tests pass a stub"
    return example_ok(p)


def to_chat(p: dict) -> dict:
    answer = f"{p['explanation'].strip()}\n\n```python\n{p['solution'].rstrip()}\n\n{p['example'].strip()}\n```"
    return {"messages": [{"role": "user", "content": p["prompt"].strip()}, {"role": "silicat", "content": answer}]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--bench-frac", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    raw = []
    for f in sorted(PROB_DIR.glob("raw_*.jsonl")):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    raw.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"  skip {f.name}:{i} bad json")
    drops: Counter = Counter()
    with ThreadPoolExecutor(4) as ex:
        verdicts = list(ex.map(verify, raw))
    seen_ep, seen_prompt, ok = set(), set(), []
    for p, why in zip(raw, verdicts):
        if why:
            drops[why.split(":")[0]] += 1
            print(f"  drop {p.get('id', '?')}: {why}")
            continue
        ep, pr = p["entry_point"].lower(), norm(p["prompt"])
        if ep in seen_ep or pr in seen_prompt:
            drops["duplicate"] += 1
            continue
        seen_ep.add(ep)
        seen_prompt.add(pr)
        ok.append(p)

    def h(p: dict) -> str:
        return hashlib.sha256(f"{args.seed}:{p['id']}:{p['entry_point']}".encode()).hexdigest()

    by_diff: dict[str, list[dict]] = defaultdict(list)
    for p in ok:
        by_diff[p["difficulty"]].append(p)
    bench, train = [], []
    for d, ps in sorted(by_diff.items()):
        ps.sort(key=h)
        k = round(len(ps) * args.bench_frac)
        bench += ps[:k]
        train += ps[k:]
    bench.sort(key=lambda p: p["id"])
    train.sort(key=lambda p: p["id"])

    tok = _tokenizer()
    sft, sft_drops = [], Counter()
    for p in train:
        row = to_chat(p)
        reasons = grade(row, tok)
        if reasons:
            sft_drops[reasons[0].split(":")[0]] += 1
            continue
        sft.append(row)

    def dump(path: Path, rows: list[dict]) -> None:
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

    dump(PROB_DIR / "benchmark.jsonl", [{k: p[k] for k in ("id", "difficulty", "topic", "prompt", "entry_point", "tests", "solution")} for p in bench])
    dump(PROB_DIR / "train.jsonl", train)
    dump(ROOT / "data" / "synth" / "problems_sft.jsonl", sft)
    stats = {"raw": len(raw), "verified_unique": len(ok), "dropped": dict(drops), "benchmark": len(bench),
             "train": len(train), "sft_rows": len(sft), "sft_dropped_by_grader": dict(sft_drops),
             "benchmark_by_difficulty": dict(Counter(p["difficulty"] for p in bench)), "bench_frac": args.bench_frac, "seed": args.seed}
    (PROB_DIR / "stats.json").write_text(json.dumps(stats, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
