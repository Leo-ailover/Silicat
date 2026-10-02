import torch

from silicat.generate import stream
from silicat.model_v3 import GPTConfigV3, GPTV3


def tiny(block=32, vocab=100):
    torch.manual_seed(0)
    cfg = GPTConfigV3(vocab_size=vocab, block_size=block, n_layer=4, n_head=4, n_kv_head=2, n_embd=32)
    return GPTV3(cfg).eval(), cfg


def test_nope_layer_present_and_no_head_key():
    m, _ = tiny()
    assert [b.attn.use_rope for b in m.blocks] == [True, True, True, False]
    assert "head.weight" not in m.state_dict()
    assert m.num_params(non_embedding=True) == m.num_params() - m.tok_emb.weight.numel()


def test_token_by_token_matches_full():
    m, _ = tiny()
    idx = torch.randint(0, 100, (1, 24))
    full, _ = m(idx)
    c = m.new_cache()
    out = torch.cat([m(idx[:, t:t + 1], cache=c)[0] for t in range(24)], 1)
    assert torch.allclose(out, full, atol=1e-4)
    assert c.length == 24
    assert c.k[0].shape[1] == 2  # GQA-sized


def test_prefill_then_decode_and_last_only():
    m, _ = tiny()
    idx = torch.randint(0, 100, (1, 24))
    full, _ = m(idx)
    c = m.new_cache()
    pre, _ = m(idx[:, :10], cache=c, last_only=True)
    assert pre.shape[1] == 1 and torch.allclose(pre, full[:, 9:10], atol=1e-4)
    rest = torch.cat([m(idx[:, t:t + 1], cache=c)[0] for t in range(10, 24)], 1)
    assert torch.allclose(rest, full[:, 10:], atol=1e-4)


def test_chunked_prefill():
    m, _ = tiny()
    idx = torch.randint(0, 100, (1, 20))
    full, _ = m(idx)
    c = m.new_cache()
    out = torch.cat([m(idx[:, s:s + 7], cache=c)[0] for s in range(0, 20, 7)], 1)
    assert torch.allclose(out, full, atol=1e-4)


def test_overflow_raises():
    m, _ = tiny(block=8)
    c = m.new_cache()
    m(torch.randint(0, 100, (1, 8)), cache=c)
    try:
        m(torch.randint(0, 100, (1, 1)), cache=c)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_loss_paths():
    m, _ = tiny()
    x = torch.randint(0, 100, (3, 16))
    y = torch.randint(0, 100, (3, 16))
    mask = (torch.rand(3, 16) > 0.6).long()
    mask[0, 0] = 1
    y2 = y.clone()
    y2[0, 0] = -100  # ignored target inside the mask
    # masked loss == dense reference
    logits, loss = m(x, targets=y2, loss_mask=mask)
    full, _ = m(x)
    per = torch.nn.functional.cross_entropy(full.reshape(-1, 100), y2.reshape(-1), ignore_index=-100, reduction="none")
    ref = (per * mask.reshape(-1)).sum() / mask.sum()
    assert torch.allclose(loss, ref, atol=1e-5)
    assert logits.shape[0] == int(mask.sum())
    # all-zero mask: finite, zero, still differentiable
    _, z = m(x, targets=y, loss_mask=torch.zeros_like(mask))
    assert z.item() == 0.0
    z.backward()
    # no mask + ignored targets = standard mean over valid targets
    _, l = m(x, targets=y2)
    assert torch.allclose(l, torch.nn.functional.cross_entropy(full.reshape(-1, 100), y2.reshape(-1), ignore_index=-100), atol=1e-5)


def test_half_model_rope_dtype():
    m, _ = tiny()
    m = m.to(torch.bfloat16)
    logits, _ = m(torch.randint(0, 100, (1, 8)))
    assert logits.dtype == torch.bfloat16


def test_greedy_cached_equals_uncached_and_rollover_shape():
    m, cfg = tiny(block=32)
    prompt = [5, 6, 7]
    a = list(stream(m, prompt, max_new_tokens=20, temperature=0, use_cache=True, ban_ids=()))
    b = list(stream(m, prompt, max_new_tokens=20, temperature=0, use_cache=False, ban_ids=()))
    assert a == b
    # rollover: runs past block_size without error and yields the full count
    c = list(stream(m, prompt, max_new_tokens=80, temperature=0, ban_ids=()))
    assert len(c) == 80
    # prompt longer than block is left-truncated, not an error
    long = list(range(1, 90))
    info = {}
    assert len(list(stream(m, long, max_new_tokens=5, temperature=0, info=info))) == 5
    assert info["truncated"] and info["prompt_tokens"] == 31


def test_seed_determinism_and_sampling_options():
    m, _ = tiny()
    kw = dict(max_new_tokens=15, temperature=1.0, top_k=20, top_p=0.9, repetition_penalty=1.2, no_repeat_ngram=2)
    a = list(stream(m, [1, 2, 3], seed=7, **kw))
    b = list(stream(m, [1, 2, 3], seed=7, **kw))
    assert a == b
    ids = [1, 2, 3] + a
    bigrams = [tuple(ids[i:i + 2]) for i in range(len(ids) - 1)]
    assert len(bigrams) == len(set(bigrams))  # no repeated bigram


def test_stop_token_not_yielded_and_banned_pad():
    m, _ = tiny()
    first = next(stream(m, [1, 2], max_new_tokens=1, temperature=0))
    info = {}
    out = list(stream(m, [1, 2], max_new_tokens=5, temperature=0, stop_ids={first}, info=info))
    assert out == [] and info["finish_reason"] == "stop"
    ids = list(stream(m, [1], max_new_tokens=40, temperature=1.5, top_k=0, top_p=None, seed=1))
    assert 0 not in ids
