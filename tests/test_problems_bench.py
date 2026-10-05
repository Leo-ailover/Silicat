"""Unit-tested problem pipeline (data/build_problems.py) and the pass@1 harness (silicat/bench.py)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "data"))

import build_problems as bp  # noqa: E402
from silicat.bench import extract_code, run_tests, summarize  # noqa: E402

GOOD = {
    "id": "X001", "topic": "strings", "difficulty": "easy",
    "prompt": "Write a function `shout(s)` that returns s upper-cased with an exclamation mark appended.",
    "entry_point": "shout",
    "solution": "def shout(s):\n    return s.upper() + '!'\n",
    "tests": "assert shout('hi') == 'HI!'\nassert shout('') == '!'\nassert shout('a b') == 'A B!'\n",
    "example": "print(shout('hey'))  # HEY!",
    "explanation": "Upper-case the string, then append the mark.",
}


def test_extract_code_prefers_block_defining_entry_point():
    reply = "Helper:\n```python\nx = 1\n```\nMain:\n```python\ndef shout(s):\n    return s\n```"
    assert extract_code(reply, "shout").startswith("def shout")


def test_extract_code_unclosed_fence_and_no_fence():
    assert extract_code("```python\ndef f():\n    return 1", "f").startswith("def f")
    assert extract_code("def f():\n    return 1", "f") == "def f():\n    return 1"


def test_run_tests_pass_fail_timeout():
    assert run_tests(GOOD["solution"], GOOD["tests"]) == (True, "")
    ok, err = run_tests("def shout(s):\n    return s\n", GOOD["tests"])
    assert not ok and "AssertionError" in err
    ok, err = run_tests("while True:\n    pass\n", "", timeout=1)
    assert not ok and err == "timeout"


def test_verify_accepts_good_problem():
    assert bp.verify(dict(GOOD)) is None


def test_verify_rejects_tests_that_pass_a_stub():
    weak = dict(GOOD, tests="assert shout is not None\n")
    assert bp.verify(weak) == "tests pass a stub"


def test_verify_rejects_wrong_example_output():
    bad = dict(GOOD, example="print(shout('hey'))  # hey!")
    assert bp.verify(bad).startswith("example output mismatch")


def test_class_stub_and_chat_row():
    cls = dict(GOOD, entry_point="Box", solution="class Box:\n    def get(self):\n        return 3\n",
               tests="assert Box().get() == 3\n", example="print(Box().get())  # 3")
    assert "class Box" in bp.stub_for(cls)
    assert bp.verify(cls) is None
    row = bp.to_chat(GOOD)
    assert row["messages"][0]["content"] == GOOD["prompt"]
    assert "```python\ndef shout" in row["messages"][1]["content"]


def test_summarize():
    s = summarize([{"difficulty": "easy", "passed": True}, {"difficulty": "medium", "passed": False}])
    assert s["all"] == {"passed": 1, "total": 2, "pass@1": 0.5}
    assert s["easy"]["pass@1"] == 1.0


def test_extra_pretrain_docs(tmp_path):
    import json

    from silicat.dataset import extra_pretrain_docs

    assert extra_pretrain_docs(tmp_path / "missing") == ("", {})
    (tmp_path / "b.jsonl").write_text(json.dumps({"text": "second"}) + "\n", encoding="utf-8")
    (tmp_path / "a.jsonl").write_text(json.dumps({"text": " first "}) + "\n\n" + json.dumps({"text": ""}) + "\n", encoding="utf-8")
    text, shas = extra_pretrain_docs(tmp_path)
    assert text == "first\n\nsecond\n\n"
    assert list(shas) == ["a.jsonl", "b.jsonl"] and all(len(h) == 64 for h in shas.values())
