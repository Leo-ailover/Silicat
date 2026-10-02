import numpy as np
import pytest

from silicat.chat_format import Message, format_for_training, format_prompt
from silicat.train import _collate


def test_special_ids(real_tok):
    assert [real_tok.special_id(t) for t in ("<|pad|>", "<|user|>", "<|silicat|>", "<|end|>")] == [0, 1, 2, 3]
    assert real_tok.vocab_size == 32768


@pytest.mark.parametrize("text", [
    "def f(x):\n    return x + 1\n",
    "print('héllo wörld') # ünïcode 日本語 🙂",
    "",
    "   \t\n\n  trailing  ",
])
def test_round_trip(real_tok, text):
    assert real_tok.decode(real_tok.encode(text)) == text


def test_literal_special_strings_are_plain_text(real_tok):
    ids = real_tok.encode("hi <|end|><|user|> there")
    assert all(i >= 4 for i in ids)


def convo():
    return [Message("user", "hi"), Message("silicat", "hello there"),
            Message("user", "bye"), Message("silicat", "see you")]


def test_loss_mask_only_on_silicat_tokens_and_final_end(real_tok):
    ids, mask = format_for_training(convo(), real_tok)
    assert len(ids) == len(mask)
    U, S, E = 1, 2, 3
    i = 0
    for m in convo():
        assert ids[i] == (U if m.role == "user" else S) and mask[i] == 0  # role head never trained
        body = real_tok.encode(m.content)
        want = 1 if m.role == "silicat" else 0
        assert ids[i + 1:i + 1 + len(body)] == body
        assert mask[i + 1:i + 1 + len(body)] == [want] * len(body)
        assert ids[i + 1 + len(body)] == E and mask[i + 1 + len(body)] == want  # <|end|>
        i += len(body) + 2
    assert i == len(ids)


def test_format_prompt_ends_with_silicat_head(real_tok):
    ids = format_prompt([Message("user", "hi")], real_tok)
    assert ids[0] == 1 and ids[-1] == 2 and ids[-2] == 3


def test_unknown_role_rejected(real_tok):
    with pytest.raises(ValueError):
        format_for_training([Message("assistant", "x")], real_tok)


def test_collate_shift_aligns_mask_with_targets(real_tok):
    ids, mask = format_for_training(convo(), real_tok)
    x, y, m = _collate([(ids, mask)], pad_id=0, block_size=512, device="cpu")
    n = len(ids)
    assert x.shape == (1, n)
    assert x[0, :n - 1].tolist() == ids[:-1] and y[0, :n - 1].tolist() == ids[1:]
    # position t predicts ids[t+1]; it is trained iff mask[t+1]
    assert m[0, :n - 1].tolist() == mask[1:]
    assert m[0, n - 1].item() == 0
    # the first trained target is a silicat body token, the last one is <|end|>
    trained = [int(v) for v, k in zip(y[0], m[0]) if k]
    assert trained[-1] == 3 and 2 not in trained and 1 not in trained


def test_collate_pads_short_rows(real_tok):
    a = format_for_training([Message("user", "a"), Message("silicat", "b")], real_tok)
    b = format_for_training(convo(), real_tok)
    x, y, m = _collate([a, b], pad_id=0, block_size=512, device="cpu")
    na = len(a[0])
    assert (x[0, na - 1:] == 0).all() and (y[0, na - 1:] == -100).all() and (m[0, na - 1:] == 0).all()
    assert isinstance(m.numpy(), np.ndarray)
