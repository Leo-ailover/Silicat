
import pytest

from conftest import tiny_v3
from silicat import checkpoint as C
from silicat import generate as gen


@pytest.fixture
def ckdir(tmp_path, tiny_env, monkeypatch):
    _, ck, _ = tiny_env
    m, cfg = tiny_v3(vocab=32768, block=64, n_layer=2, n_embd=32)
    C.save_checkpoint(ck / "latest_v3.pt", m, cfg, 3, None, {"stage": "pretrain"})
    monkeypatch.setattr(C, "CKPT_DIR", ck)
    monkeypatch.delenv("SILICAT_CKPT", raising=False)
    monkeypatch.delenv("SILICAT_API_KEY", raising=False)
    return ck


def test_greedy_generation_is_deterministic_and_cache_independent(ckdir):
    eng = gen.load_engine(device="cpu")
    prompt = eng.tok.encode("def add(a, b):")
    a = gen.generate(eng.model, prompt, max_new_tokens=12, temperature=0)
    b = gen.generate(eng.model, prompt, max_new_tokens=12, temperature=0)
    c = gen.generate(eng.model, prompt, max_new_tokens=12, temperature=0, use_cache=False)
    assert a == b == c and len(a) == 12 and all(isinstance(t, int) and t != 0 for t in a)


def test_seeded_sampling_is_reproducible(ckdir):
    eng = gen.load_engine(device="cpu")
    p = eng.tok.encode("hello")
    kw = dict(max_new_tokens=10, temperature=0.9, seed=5)
    assert gen.generate(eng.model, p, **kw) == gen.generate(eng.model, p, **kw)


def test_server_health_and_chat_smoke(ckdir):
    from fastapi.testclient import TestClient
    from silicat.server import create_app

    with TestClient(create_app()) as c:
        h = c.get("/api/health").json()
        assert h["model_loaded"] is True and h["arch"] == "v3" and h["step"] == 3 and h["vocab_size"] == 32768
        r = c.post("/api/chat", json={"messages": [{"role": "user", "content": "hi"}], "max_new_tokens": 4,
                                      "temperature": 0, "stream": False})
        assert r.status_code == 200 and r.json()["tokens"] <= 4
        assert c.post("/api/chat", json={"messages": []}).status_code == 422


def test_server_without_checkpoint_reports_not_loaded(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from silicat.server import create_app

    monkeypatch.setattr(C, "CKPT_DIR", tmp_path)
    monkeypatch.delenv("SILICAT_CKPT", raising=False)
    with TestClient(create_app()) as c:
        h = c.get("/api/health").json()
        assert h["model_loaded"] is False and h["error"]
        assert c.post("/api/chat", json={"messages": [{"role": "user", "content": "x"}]}).status_code == 503
