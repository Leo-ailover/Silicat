import numpy as np
import pytest

from silicat.dataset import _ngram_hashes, block_split

BLOCK, NGRAM = 64, 8


def rand(n, seed=0):
    return np.random.default_rng(seed).integers(4, 30000, n, dtype=np.uint32)


def test_blocks_are_disjoint_and_cover_everything():
    arr = rand(BLOCK * 40 + 17)
    train, val, info = block_split(arr, 0.1, block=BLOCK, ngram=NGRAM)
    assert len(train) + len(val) == len(arr)
    assert len(val) == info["n_val_blocks"] * BLOCK
    vb = info["val_blocks"]
    assert vb == sorted(set(vb)) and all(0 <= b < info["n_blocks"] for b in vb)
    rebuilt = np.concatenate([val[i * BLOCK:(i + 1) * BLOCK] for i in range(len(vb))])
    assert (rebuilt == val).all()
    for i, b in enumerate(vb):
        assert (arr[b * BLOCK:(b + 1) * BLOCK] == val[i * BLOCK:(i + 1) * BLOCK]).all()
    assert (train[-17:] == arr[-17:]).all()  # partial tail always stays in train


def test_val_is_interleaved_not_tail():
    arr = rand(BLOCK * 100)
    _, _, info = block_split(arr, 0.1, block=BLOCK, ngram=NGRAM)
    assert min(info["val_blocks"]) < 90


def test_deterministic_and_seed_dependent():
    arr = rand(BLOCK * 50)
    a = block_split(arr, 0.1, block=BLOCK, ngram=NGRAM, seed=1)[2]["val_blocks"]
    b = block_split(arr, 0.1, block=BLOCK, ngram=NGRAM, seed=1)[2]["val_blocks"]
    c = block_split(arr, 0.1, block=BLOCK, ngram=NGRAM, seed=2)[2]["val_blocks"]
    assert a == b and a != c


def test_duplicated_text_does_not_leak_into_val():
    half = rand(BLOCK * 30, seed=3)
    arr = np.concatenate([half, rand(BLOCK * 10, seed=4), half])  # 30 blocks have an exact twin
    train, val, info = block_split(arr, 0.2, block=BLOCK, ngram=NGRAM, threshold=0.05)
    tr_h = set(_ngram_hashes(train, NGRAM).tolist())
    va_h = _ngram_hashes(val, NGRAM)
    # windows spanning a block seam are not part of the filter; the rest must not appear in train
    inside = [h for i, h in enumerate(va_h.tolist()) if (i % BLOCK) <= BLOCK - NGRAM]
    leak = sum(h in tr_h for h in inside) / len(inside)
    assert leak <= 0.05 + 1e-9, leak


def test_bad_args():
    with pytest.raises(ValueError):
        block_split(rand(BLOCK * 10), 1.5, block=BLOCK, ngram=NGRAM)
    with pytest.raises(ValueError):
        block_split(rand(BLOCK), 0.1, block=BLOCK, ngram=NGRAM)
