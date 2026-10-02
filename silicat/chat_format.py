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


def _head(m: Message, user: int, sil: int) -> int:
    if m.role == "user":
        return user
    if m.role == "silicat":
        return sil
    raise ValueError(f"unknown role {m.role!r} (expected 'user' or 'silicat')")


def format_prompt(messages: list[Message], tok: Tokenizer) -> list[int]:
    """Render a conversation into token ids, ending with `<|silicat|>` so the
    model is primed to generate its reply."""
    user = tok.special_id("<|user|>")
    sil = tok.special_id("<|silicat|>")
    end = tok.special_id("<|end|>")
    ids: list[int] = []
    for m in messages:
        ids.append(_head(m, user, sil))
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
        ids.append(_head(m, user, sil))
        mask.append(0)
        body = tok.encode(m.content)
        ids.extend(body)
        is_sil = m.role == "silicat"
        mask.extend([1 if is_sil else 0] * len(body))
        ids.append(end)
        mask.append(1 if is_sil else 0)
    return ids, mask


def fit_prompt(
    messages: list[Message], tok: Tokenizer, max_prompt_tokens: int
) -> tuple[list[int], bool]:
    """Like `format_prompt` but guaranteed to be <= max_prompt_tokens ids.

    Drops the oldest turns whole (so the prompt still starts with `<|user|>`),
    always keeps the last turn, and if that alone is too long keeps the TAIL of
    its token ids. Returns (ids, truncated)."""
    user = tok.special_id("<|user|>")
    sil = tok.special_id("<|silicat|>")
    end = tok.special_id("<|end|>")
    turns = [(_head(m, user, sil), tok.encode(m.content)) for m in messages]
    budget = max(max_prompt_tokens, 4) - 1  # trailing <|silicat|>
    sizes = [len(b) + 2 for _, b in turns]
    # candidate start turns: user turns (newest last); the last turn is always allowed
    starts = [i for i, (h, _) in enumerate(turns) if h == user] or [max(len(turns) - 1, 0)]
    start = starts[-1]
    for i in starts:
        if sum(sizes[i:]) <= budget:
            start = i
            break
    kept = turns[start:]
    truncated = start > 0
    if kept and sum(sizes[start:]) > budget:
        truncated = True
        rest = sum(sizes[start + 1:])
        room = max(budget - rest - 2, 0)
        h, body = kept[0]
        kept[0] = (h, body[-room:] if room else [])
        if rest >= budget - 2:  # later turns alone overflow: keep only the tail of the last one
            h, body = kept[-1]
            kept = [(h, body[-max(budget - 2, 0):])]
    ids: list[int] = []
    for h, body in kept:
        ids.append(h)
        ids.extend(body)
        ids.append(end)
    ids.append(sil)
    return ids, truncated
