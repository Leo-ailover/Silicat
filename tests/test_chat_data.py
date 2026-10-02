"""Validators for the committed chat datasets (skipped if the files are absent)."""
import json
import re

import pytest

from silicat.chat_format import Message, format_for_training

REPO_DATA = __import__("pathlib").Path(__file__).resolve().parents[1] / "data"
TRAIN, EVAL = REPO_DATA / "silicat_chat_v3.jsonl", REPO_DATA / "silicat_chat_eval.jsonl"
BLOCK = 512  # chat training block size (train.py V3_DEFAULTS)


def load(path):
    if not path.exists():
        pytest.skip(f"{path.name} not present")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


@pytest.fixture(scope="module")
def train_rows():
    return load(TRAIN)


@pytest.fixture(scope="module")
def eval_rows():
    return load(EVAL)


def norm(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def first_user(row):
    return norm(row["messages"][0]["content"])


def test_schema_and_alternation(train_rows, eval_rows):
    for name, rows in (("train", train_rows), ("eval", eval_rows)):
        assert rows, name
        for i, r in enumerate(rows):
            assert set(r) >= {"messages"}, (name, i)
            msgs = r["messages"]
            assert len(msgs) >= 2 and len(msgs) % 2 == 0, (name, i)
            for k, m in enumerate(msgs):
                assert m["role"] == ("user" if k % 2 == 0 else "silicat"), (name, i, k)
                assert isinstance(m["content"], str) and m["content"].strip(), (name, i, k)


def test_no_exact_duplicate_rows_and_balanced_fences(train_rows):
    seen = set()
    for i, r in enumerate(train_rows):
        key = json.dumps(r["messages"], sort_keys=True)
        assert key not in seen, f"duplicate row {i}"
        seen.add(key)
        for m in r["messages"]:
            if m["role"] == "silicat":
                assert m["content"].count("```") % 2 == 0, f"unbalanced code fence in row {i}"


def test_train_and_eval_prompts_are_disjoint(train_rows, eval_rows):
    tr = {first_user(r) for r in train_rows}
    overlap = [first_user(r) for r in eval_rows if first_user(r) in tr]
    assert not overlap, overlap[:3]


def test_every_row_fits_in_block_with_final_end(train_rows, eval_rows, real_tok):
    for name, rows in (("train", train_rows), ("eval", eval_rows)):
        for i, r in enumerate(rows):
            ids, mask = format_for_training([Message(m["role"], m["content"]) for m in r["messages"]], real_tok)
            assert len(ids) <= BLOCK, f"{name} row {i}: {len(ids)} tokens > {BLOCK}"
            assert ids[-1] == 3 and mask[-1] == 1 and sum(mask) > 1
            assert not any(t < 4 for k, t in enumerate(ids) if mask[k] and t != 3), f"{name} row {i}: special id in body"
