import pytest
import torch

from conftest import tiny_v3
from silicat import checkpoint as C
from silicat.assemble import split_checkpoint
from silicat.halve import export


def make(tmp_path, step=7, with_optim=True):
    m, cfg = tiny_v3(n_layer=2)
    opt = m.configure_optimizer(1e-3, 0.1)
    x = torch.randint(0, cfg.vocab_size, (2, 8))
    m(x, targets=x)[1].backward()
    opt.step()
    p = tmp_path / "latest_v3.pt"
    C.save_checkpoint(p, m, cfg, step, opt if with_optim else None, {"stage": "pretrain", "seed": 1})
    return m, cfg, opt, p


def test_save_load_round_trip_restores_model_and_optimizer(tmp_path):
    m, cfg, opt, p = make(tmp_path)
    ck = C.load_checkpoint(p)
    assert ck["step"] == 7 and ck["arch"] == "v3" and ck["stage"] == "pretrain" and ck["seed"] == 1
    m2, cfg2, arch = C.build_model(ck["config"])
    m2.load_state_dict(ck["model"])
    for a, b in zip(m.parameters(), m2.parameters()):
        assert torch.equal(a, b)
    opt2 = m2.configure_optimizer(1e-3, 0.1)
    opt2.load_state_dict(ck["optim"])  # optimizer state restored, not restarted
    st = next(iter(opt2.state.values()))
    assert st["step"].item() == 1 and st["exp_avg"].abs().sum() > 0


def test_atomic_save_leaves_old_file_intact_on_failure(tmp_path, monkeypatch):
    _, _, _, p = make(tmp_path)
    before = p.read_bytes()

    def boom(obj, f):
        f.write(b"partial")
        raise RuntimeError("disk full")

    monkeypatch.setattr(torch, "save", boom)
    with pytest.raises(RuntimeError):
        C.atomic_save({"x": 1}, p)
    assert p.read_bytes() == before
    assert not list(tmp_path.glob("*.tmp"))


def test_resolve_prefers_local_then_export_parts(tmp_path):
    m, cfg, opt, p = make(tmp_path)
    ck, src = C.resolve_resumable("latest_v3", tmp_path)
    assert src == p and ck["optim"] is not None
    # container wipe: only the fp16 parts survive
    exp = C.export_path("latest_v3", tmp_path)
    export(p, exp)
    split_checkpoint(exp, part_bytes=20_000)
    p.unlink()
    exp.unlink()
    assert C.checkpoint_exists("latest_v3", tmp_path)
    ck, src = C.resolve_resumable("latest_v3", tmp_path)
    assert src == exp and ck["step"] == 7 and ck["dtype"] == "float16" and not ck.get("optim")
    model, _, _ = C.load_model(tmp_path / "latest_v3.pt")
    assert next(model.parameters()).dtype == torch.float32


def test_resolve_none_when_nothing_and_error_when_unreadable(tmp_path):
    assert C.resolve_resumable("latest_v3", tmp_path) is None
    (tmp_path / "latest_v3.pt").write_bytes(b"not a checkpoint")
    with pytest.raises(RuntimeError):
        C.resolve_resumable("latest_v3", tmp_path)
    assert (tmp_path / "latest_v3.pt.corrupt").exists()


def test_fp16_export_keeps_tied_weight_single_and_is_smaller(tmp_path):
    _, _, _, p = make(tmp_path, with_optim=False)
    exp = tmp_path / "e.fp16.pt"
    export(p, exp)
    ck = C.load_checkpoint(exp)
    assert ck["model"]["tok_emb.weight"].dtype == torch.float16 and "head.weight" not in ck["model"]
    assert exp.stat().st_size < 0.6 * p.stat().st_size
    with pytest.raises(SystemExit):
        export(p, p)


def test_archive_existing_moves_not_deletes(tmp_path):
    _, _, _, p = make(tmp_path)
    dest = C.archive_existing("latest_v3", tmp_path)
    assert dest is not None and (dest / p.name).exists() and not p.exists()
