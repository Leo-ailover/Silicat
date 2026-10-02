"""Tests for the chat/corpus data pipeline (run: pytest data/test_data_pipeline.py)."""
import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_chat_dataset as B  # noqa: E402

DATA = Path(__file__).resolve().parent


def load(p):
    return [json.loads(l) for l in (DATA / p).read_text(encoding="utf-8").splitlines()]


def test_fences_and_split():
    t = "intro\n```python\nx = 1\n```\noutro"
    assert B.fence_lines(t) == 2
    assert [k for k, _, _ in B.split_fences(t)] == ["text", "code", "text"]
    assert B.join_fences(B.split_fences(t)) == t


def test_add_missing_imports_only_when_unbound():
    code, n = B.add_missing_imports("print(os.getcwd())")
    assert n == 1 and code.startswith("import os")
    assert B.add_missing_imports("import os\nprint(os.getcwd())")[1] == 0


def test_schema_checks():
    ok = [{"role": "user", "content": "a"}, {"role": "silicat", "content": "b"}]
    assert B.check_schema(ok) is None
    assert B.check_schema(ok[:1]) is not None
    assert B.check_schema([ok[0], ok[0]]) == "role_order"
    assert B.check_schema([ok[0], {"role": "silicat", "content": " "}]) == "empty_message"


def test_junk_regexes():
    assert any(r.match("How do I implement Python coding pattern 108?") for r in B.JUNK_RES)
    assert not any(r.match("What is sqrt(16)?") for r in B.JUNK_RES)


def test_template_family_and_limits_in_built_files():
    train, ev = load("silicat_chat_v3.jsonl"), load("silicat_chat_eval.jsonl")
    assert len(ev) > 100 and len(train) > 5000
    keys = {B.norm_key(r["messages"][0]["content"]) for r in train}
    assert not any(B.norm_key(r["messages"][0]["content"]) in keys for r in ev), "eval/train prompt overlap"
    for r in train + ev:
        m = r["messages"]
        assert [x["role"] for x in m] == ["user", "silicat"] * (len(m) // 2)
        for x in m:
            assert x["content"] == x["content"].strip() and B.fence_lines(x["content"]) % 2 == 0
        assert not re.search(r"Pattern \d+", m[-1]["content"])


def test_token_length_within_block():
    tok_dir = DATA.parent / "checkpoints" / "tokenizer_v2"
    if not tok_dir.exists():
        pytest.skip("tokenizer missing")
    sys.path.insert(0, str(DATA.parent))
    from silicat.chat_format import Message, format_for_training
    from silicat.tokenizer import Tokenizer

    tok = Tokenizer(tok_dir)
    for r in load("silicat_chat_v3.jsonl")[:500] + load("silicat_chat_eval.jsonl"):
        ids, _ = format_for_training([Message(**x) for x in r["messages"]], tok)
        assert len(ids) <= 512 and ids[-1] == tok.special_id("<|end|>")


def test_corpus_has_no_chat_or_synth_repeats():
    p = DATA / "corpus_v2.txt"
    t = p.read_text(encoding="utf-8")
    assert "\nsilicat: " not in t
    import build_corpus as C

    _, per, k = C.strip_trailing_repeats(t)
    assert k == 1


def test_paste_code_reproducible_and_independent_of_other_synth(tmp_path):
    """gen_paste_code.py must regenerate the committed paste_code.jsonl byte for byte; it mines only
    silicat_chat.jsonl, so editing other synth files cannot change it."""
    import subprocess

    out = tmp_path / "pc.jsonl"
    subprocess.run([sys.executable, str(DATA / "synth" / "gen_paste_code.py"), "--out", str(out)],
                   check=True, capture_output=True)
    assert out.read_bytes() == (DATA / "synth" / "paste_code.jsonl").read_bytes()
