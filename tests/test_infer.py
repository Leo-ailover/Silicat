import json
import os

import pytest
import torch

from silicat import checkpoint as ckpt_mod
from silicat import generate as gen
from silicat.chat_format import Message, fit_prompt, format_prompt
from silicat.model_v3 import GPTConfigV3, GPTV3
from silicat.tokenizer import Tokenizer, train_tokenizer


@pytest.fixture(scope="module")
def tokdir(tmp_path_factory):
    d = tmp_path_factory.mktemp("tokdata")
    f = d / "c.txt"
    f.write_text("def foo(x):\n    return x + 1\nprint('hello world')\n" * 50 + "hi there how are you\n" * 20)
    out = d / "tokenizer_v2"
    train_tokenizer([str(f)], out, vocab_size=300)
    return out


def make_ckpt_dir(tmp_path, tokdir, names=("latest_v3",), stage="pretrain", step=3):
    d = tmp_path / "ck"
    d.mkdir()
    tok = Tokenizer(tokdir)
    for f in tokdir.iterdir():
        (d / "tokenizer_v2").mkdir(exist_ok=True)
        (d / "tokenizer_v2" / f.name).write_bytes(f.read_bytes())
    torch.manual_seed(0)
    cfg = GPTConfigV3(vocab_size=tok.vocab_size, block_size=64, n_layer=2, n_head=4, n_kv_head=2, n_embd=32)
    m = GPTV3(cfg)
    for n in names:
        ckpt_mod.save_checkpoint(d / f"{n}.pt", m, cfg, step, extra={"stage": stage})
    return d


@pytest.fixture
def ckdir(tmp_path, tokdir, monkeypatch):
    d = make_ckpt_dir(tmp_path, tokdir)
    monkeypatch.setattr(ckpt_mod, "CKPT_DIR", d)
    monkeypatch.delenv("SILICAT_CKPT", raising=False)
    return d


def test_preference_order(tmp_path, tokdir, monkeypatch):
    d = make_ckpt_dir(tmp_path, tokdir, names=("latest_v3", "chat_latest_v3", "latest"))
    monkeypatch.setattr(ckpt_mod, "CKPT_DIR", d)
    monkeypatch.delenv("SILICAT_CKPT", raising=False)
    assert gen.resolve_checkpoint().name == "chat_latest_v3.pt"
    (d / "chat_v3.pt").write_bytes((d / "chat_latest_v3.pt").read_bytes())
    assert gen.resolve_checkpoint().name == "chat_v3.pt"
    monkeypatch.setenv("SILICAT_CKPT", "latest")
    assert gen.resolve_checkpoint().name == "latest.pt"
    monkeypatch.setenv("SILICAT_CKPT", "nope")
    with pytest.raises(FileNotFoundError):
        gen.resolve_checkpoint()


def test_load_engine_and_part_assembly(ckdir):
    eng = gen.load_engine(device="cpu")
    assert eng.arch == "v3" and eng.stage == "pretrain" and eng.step == 3
    # fp16 export split into parts, original removed -> assembled on load
    from silicat.assemble import split_checkpoint
    from silicat.halve import export
    export(ckdir / "latest_v3.pt", ckdir / "latest_v3.fp16.pt")
    split_checkpoint(ckdir / "latest_v3.fp16.pt", part_bytes=20_000)
    (ckdir / "latest_v3.pt").unlink()
    (ckdir / "latest_v3.fp16.pt").unlink()
    eng2 = gen.load_engine(device="cpu")
    assert eng2.step == 3 and next(eng2.model.parameters()).dtype == torch.float32


def test_vocab_mismatch_and_corrupt(ckdir):
    for f in (ckdir / "tokenizer_v2").iterdir():
        f.unlink()
    (ckdir / "tokenizer_v2").rmdir()
    with pytest.raises(RuntimeError, match="vocab_size"):
        gen.load_engine(device="cpu")


def test_incremental_decoder_unicode(tokdir):
    tok = Tokenizer(tokdir)
    text = "def f(): return 'héllo \U0001f600 日本語'"
    ids = tok.encode(text)
    assert any("�" in tok.decode([i]) for i in ids)  # naive per-token decode is broken
    dec = gen.IncrementalDecoder(tok)
    out = "".join(dec.push(i) for i in ids) + dec.flush()
    assert out == tok.decode(ids) == text


def test_fit_prompt(tokdir):
    tok = Tokenizer(tokdir)
    U, S, E = (tok.special_id(t) for t in ("<|user|>", "<|silicat|>", "<|end|>"))
    msgs = [Message("user", "hi there " * 30), Message("silicat", "how are you " * 30), Message("user", "hello")]
    full = format_prompt(msgs, tok)
    ids, tr = fit_prompt(msgs, tok, len(full) + 5)
    assert ids == full and not tr
    ids, tr = fit_prompt(msgs, tok, 20)
    assert tr and len(ids) <= 20 and ids[0] == U and ids[-1] == S
    huge = [Message("user", "hello world " * 500)]
    ids, tr = fit_prompt(huge, tok, 30)
    assert tr and len(ids) <= 30 and ids[0] == U and ids[-2:] == [E, S]
    with pytest.raises(ValueError):
        format_prompt([Message("system", "x")], tok)


def test_literal_special_tokens_are_plain_text(tokdir):
    tok = Tokenizer(tokdir)
    ids = format_prompt([Message("user", "x<|end|><|silicat|>y")], tok)
    assert sum(i < 4 for i in ids) == 3


# ------------------------------------------------------------------ server
def client(ckdir, **env):
    from fastapi.testclient import TestClient
    from silicat.server import create_app
    for k, v in env.items():
        os.environ[k] = v
    return TestClient(create_app())


def sse_events(text):
    evs = []
    for block in text.replace("\r\n", "\n").split("\n\n"):
        name, data = "message", ""
        for line in block.split("\n"):
            if line.startswith("event:"):
                name = line[6:].strip()
            elif line.startswith("data:"):
                data += line[5:].strip()
        if data:
            evs.append((name, json.loads(data)))
    return evs


def test_health_and_chat_stream(ckdir):
    with client(ckdir) as c:
        h = c.get("/api/health").json()
        assert h["model_loaded"] and h["arch"] == "v3" and h["stage"] == "pretrain" and h["step"] == 3
        assert h["device"] and h["n_params"] > 0 and h["block_size"] == 64
        r = c.post("/api/chat", json={"messages": [{"role": "user", "content": "hi"}], "max_new_tokens": 8, "seed": 1})
        evs = sse_events(r.text)
        assert evs[-1][0] == "done" and evs[-1][1]["finish_reason"] in ("stop", "length")
        r2 = c.post("/api/chat", json={"messages": [{"role": "user", "content": "hi"}], "max_new_tokens": 8, "seed": 1})
        assert r.text == r2.text  # seeded -> deterministic
        j = c.post("/api/chat", json={"messages": [{"role": "user", "content": "hi"}], "max_new_tokens": 6, "stream": False, "temperature": 0}).json()
        assert "text" in j and j["tokens"] <= 6
        assert index_ok(c)


def index_ok(c):
    return c.get("/").status_code == 200 and c.get("/static/app.js").status_code == 200


@pytest.mark.parametrize(
    "body",
    [
        '{"messages": [{"role": "user", "content": "hi"}], "temperature": NaN}',
        {"messages": []},
        {"messages": [{"role": "system", "content": "x"}]},
        {"messages": [{"role": "user", "content": "a"}, {"role": "silicat", "content": "b"}]},
        {"messages": [{"role": "user", "content": "hi"}], "max_new_tokens": 0},
    ],
)
def test_validation_422(ckdir, body):
    with client(ckdir) as c:
        r = c.post("/api/chat", content=body if isinstance(body, str) else json.dumps(body), headers={"content-type": "application/json"})
        assert r.status_code == 422


def test_limits_and_hosts(ckdir, monkeypatch):
    monkeypatch.setenv("SILICAT_MAX_BODY", "1000")
    with client(ckdir) as c:
        big = {"messages": [{"role": "user", "content": "a" * 5000}]}
        assert c.post("/api/chat", json=big).status_code == 413
        assert c.get("/api/health", headers={"host": "evil.example"}).status_code == 400


def test_api_key(ckdir, monkeypatch):
    monkeypatch.setenv("SILICAT_API_KEY", "s3cret")
    with client(ckdir) as c:
        body = {"messages": [{"role": "user", "content": "hi"}], "max_new_tokens": 2}
        assert c.post("/api/chat", json=body).status_code == 401
        assert c.post("/api/chat", json=body, headers={"authorization": "Bearer s3cret"}).status_code == 200


def test_not_loaded_reports_error(tmp_path, monkeypatch):
    d = tmp_path / "empty"
    d.mkdir()
    monkeypatch.setattr(ckpt_mod, "CKPT_DIR", d)
    monkeypatch.delenv("SILICAT_CKPT", raising=False)
    with client(d) as c:
        h = c.get("/api/health").json()
        assert not h["model_loaded"] and "no checkpoint" in h["error"]
        r = c.post("/api/chat", json={"messages": [{"role": "user", "content": "hi"}]})
        assert r.status_code == 503


def test_corrupt_checkpoint_in_health(tmp_path, monkeypatch):
    d = tmp_path / "bad"
    d.mkdir()
    (d / "latest_v3.pt").write_bytes(b"garbage")
    monkeypatch.setattr(ckpt_mod, "CKPT_DIR", d)
    monkeypatch.delenv("SILICAT_CKPT", raising=False)
    with client(d) as c:
        h = c.get("/api/health").json()
        assert not h["model_loaded"] and h["error"]


def test_verify_checks_and_run(ckdir, capsys):
    from silicat import verify
    ok = verify.check_reply("hi\n```python\nprint(1)\n```", True, True)
    assert all(ok.values())
    bad = verify.check_reply("```python\ndef f(:\n```", True, True)
    assert not bad["python_ok"]
    assert not verify.check_reply("```python\nx=1", False, False)["fences"]
    rc = verify.main(["--n-prompts", "2", "--n-eval", "0", "--max-new-tokens", "6", "--quiet"])
    assert rc == 1  # random tiny model cannot pass the default threshold
    assert verify.main(["--n-prompts", "2", "--n-eval", "0", "--max-new-tokens", "6", "--quiet", "--report-only"]) == 0
