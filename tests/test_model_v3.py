import pytest
import torch

from conftest import tiny_v3
from silicat.model_v3 import GPTConfigV3, GPTV3


def test_shapes_and_finite_loss():
    m, cfg = tiny_v3()
    x = torch.randint(0, cfg.vocab_size, (3, 16))
    logits, loss = m(x, targets=x)
    assert logits.shape == (3, 16, cfg.vocab_size)
    assert loss is not None and torch.isfinite(loss)
    assert m(x)[1] is None


def test_causality():
    m, cfg = tiny_v3()
    a = torch.randint(0, cfg.vocab_size, (1, 20))
    b = a.clone()
    b[0, 12:] = (b[0, 12:] + 7) % cfg.vocab_size
    la, lb = m(a)[0], m(b)[0]
    assert torch.allclose(la[:, :12], lb[:, :12], atol=1e-5)
    assert not torch.allclose(la[:, 12:], lb[:, 12:], atol=1e-5)


def test_gqa_projection_sizes():
    m, cfg = tiny_v3(n_head=4, n_kv_head=2, n_embd=32)
    at = m.blocks[0].attn
    assert at.q_proj.out_features == 4 * cfg.head_dim
    assert at.k_proj.out_features == at.v_proj.out_features == 2 * cfg.head_dim


def test_gqa_requires_divisible_heads():
    with pytest.raises(AssertionError):
        GPTV3(GPTConfigV3(vocab_size=50, block_size=8, n_layer=1, n_head=4, n_kv_head=3, n_embd=32))


def test_nope_every_fourth_layer():
    m, _ = tiny_v3(n_layer=8)
    assert [b.attn.use_rope for b in m.blocks] == [True, True, True, False] * 2


def test_nope_layers_are_permutation_invariant_over_the_prefix_but_rope_is_not():
    torch.manual_seed(0)
    x = torch.randint(0, 100, (1, 10))
    xp = x.clone()
    xp[0, :9] = x[0, :9].flip(0)  # same prefix tokens, different order, same last token
    outs = {}
    for name, every in (("nope", 1), ("rope", 1000)):
        cfg = GPTConfigV3(vocab_size=100, block_size=32, n_layer=1, n_head=4, n_kv_head=2, n_embd=32, nope_every=every)
        torch.manual_seed(0)
        m = GPTV3(cfg).eval()
        outs[name] = (m(x)[0][0, -1], m(xp)[0][0, -1])
    assert torch.allclose(*outs["nope"], atol=1e-5)
    assert not torch.allclose(*outs["rope"], atol=1e-5)


def test_tied_embeddings_single_copy():
    m, _ = tiny_v3()
    sd = m.state_dict()
    assert "tok_emb.weight" in sd and "head.weight" not in sd
    assert m.num_params() == sum(p.numel() for p in m.parameters())


def test_default_config_is_about_100m_params():
    with torch.device("meta"):
        m = GPTV3(GPTConfigV3())
    n = m.num_params()
    assert 95e6 < n < 106e6, n


def test_masked_loss_equals_dense_loss_on_selected_positions():
    m, cfg = tiny_v3()
    x = torch.randint(0, cfg.vocab_size, (2, 12))
    y = torch.randint(0, cfg.vocab_size, (2, 12))
    mask = torch.zeros(2, 12, dtype=torch.long)
    mask[:, 6:] = 1
    _, masked = m(x, targets=y, loss_mask=mask)
    y2 = y.clone()
    y2[:, :6] = -100
    _, dense = m(x, targets=y2)
    assert torch.allclose(masked, dense, atol=1e-5)


def test_overlong_sequence_rejected():
    m, cfg = tiny_v3(block=16)
    with pytest.raises(ValueError):
        m(torch.zeros(1, 17, dtype=torch.long))


def test_kv_cache_matches_full_forward():
    m, cfg = tiny_v3()
    idx = torch.randint(0, cfg.vocab_size, (1, 20))
    full, _ = m(idx)
    cache = m.new_cache()
    pre, _ = m(idx[:, :8], cache=cache)
    rest = [m(idx[:, t:t + 1], cache=cache)[0] for t in range(8, 20)]
    got = torch.cat([pre, *rest], 1)
    assert torch.allclose(got, full, atol=1e-4)
    assert cache.length == 20
