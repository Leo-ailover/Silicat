"""Shared fixtures. Everything runs on CPU with tiny models; no network, no GPU."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import numpy as np
import pytest
import torch

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

torch.set_num_threads(2)

REAL_TOK = REPO / "checkpoints" / "tokenizer_v2"


@pytest.fixture(scope="session")
def real_tok():
    """The committed 32k tokenizer (skipped only if the files are absent)."""
    if not (REAL_TOK / "vocab.json").exists():
        pytest.skip("checkpoints/tokenizer_v2 not present")
    from silicat.tokenizer import Tokenizer

    return Tokenizer(REAL_TOK)


@pytest.fixture
def tiny_env(tmp_path, real_tok):
    """A throw-away repo-like env: $SILICAT_CKPT_DIR with the real tokenizer, $SILICAT_DATA_DIR
    with tiny random uint32 train/val bins. Returns (env dict for subprocesses, ckpt, data)."""
    ck, data = tmp_path / "checkpoints", tmp_path / "data"
    ck.mkdir()
    data.mkdir()
    shutil.copytree(REAL_TOK, ck / "tokenizer_v2")
    rng = np.random.default_rng(0)
    rng.integers(4, 2000, 6000, dtype=np.uint32).tofile(data / "train_v2.bin")
    rng.integers(4, 2000, 1500, dtype=np.uint32).tofile(data / "val_v2.bin")
    import os

    env = dict(os.environ, SILICAT_CKPT_DIR=str(ck), SILICAT_DATA_DIR=str(data), PYTHONPATH=str(REPO))
    return env, ck, data


def tiny_v3(vocab: int = 100, block: int = 32, n_layer: int = 4, n_head: int = 4, n_kv_head: int = 2, n_embd: int = 32):
    from silicat.model_v3 import GPTConfigV3, GPTV3

    torch.manual_seed(0)
    cfg = GPTConfigV3(vocab_size=vocab, block_size=block, n_layer=n_layer, n_head=n_head,
                      n_kv_head=n_kv_head, n_embd=n_embd)
    return GPTV3(cfg).eval(), cfg
