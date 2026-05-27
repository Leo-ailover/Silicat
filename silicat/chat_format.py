"""Chat formatting — turn a list of messages into a token stream Silicat understands.

A conversation looks like:
    <|user|>hello<|end|><|silicat|>hi! how can i help?<|end|><|user|>...

For training, `format_for_training` also returns a loss mask so we only train
on Silicat's own tokens, not the user's prompt.
"""
from __future__ import annotations

from dataclasses import dataclass

from .tokenizer import Tokenizer


@dataclass
class Message:
    role: str  # "user" or "silicat"
    content: str


def format_prompt(messages: list[Message], tok: Tokenizer) -> list[int]:
    """Render a conversation into token ids, ending with `<|silicat|>` so the
    model is primed to generate its reply."""
    user = tok.special_id("<|user|>")
    sil = tok.special_id("<|silicat|>")
    end = tok.special_id("<|end|>")
    ids: list[int] = []
    for m in messages:
        head = user if m.role == "user" else sil
        ids.append(head)
        ids.extend(tok.encode(m.content))
        ids.append(end)
    ids.append(sil)
    return ids


def format_for_training(
    messages: list[Message], tok: Tokenizer
) -> tuple[list[int], list[int]]:
    """Return (ids, loss_mask). Loss mask is 1 on Silicat-generated tokens,
    0 on user tokens and on role markers. End-of-turn `<|end|>` after a
    Silicat reply is included in the loss so the model learns to stop."""
    user = tok.special_id("<|user|>")
    sil = tok.special_id("<|silicat|>")
    end = tok.special_id("<|end|>")
    ids: list[int] = []
    mask: list[int] = []
    for m in messages:
        head = user if m.role == "user" else sil
        ids.append(head)
        mask.append(0)
        body = tok.encode(m.content)
        ids.extend(body)
        is_sil = m.role == "silicat"
        mask.extend([1 if is_sil else 0] * len(body))
        ids.append(end)
        mask.append(1 if is_sil else 0)
    return ids, mask
