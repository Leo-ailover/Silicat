"""Quick automated sanity check: load the model, run a couple of prompts,
print the (decoded) responses. Useful right after training."""
from __future__ import annotations

from pathlib import Path

import torch

from .assemble import ensure_assembled
from .chat_format import Message, format_prompt
from .dataset import TOK_DIR
from .generate import stream
from .model import GPT, GPTConfig
from .tokenizer import Tokenizer


CKPT_DIR = Path("checkpoints")


def _device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def main() -> None:
    device = _device()
    ck_path = ensure_assembled(CKPT_DIR / "latest.pt")
    ck = torch.load(ck_path, map_location=device)
    cfg = GPTConfig(**ck["config"])
    model = GPT(cfg).to(device)
    model.load_state_dict(ck["model"])
    model.eval()
    tok = Tokenizer(TOK_DIR)
    print(f"loaded: {model.num_params():,} params, step {ck.get('step', '?')}, device {device}")
    print("-" * 60)

    prompts = [
        "hi",
        "who are you?",
        "write fizzbuzz",
        "reverse a string in python",
        "what is python",
    ]

    stop_ids = {
        tok.special_id("<|end|>"),
        tok.special_id("<|user|>"),
        tok.special_id("<|silicat|>"),
    }

    for user_msg in prompts:
        prompt_ids = format_prompt([Message(role="user", content=user_msg)], tok)
        out_ids: list[int] = []
        for t in stream(
            model,
            prompt_ids,
            max_new_tokens=128,
            temperature=0.7,
            top_k=40,
            top_p=0.95,
            stop_ids=stop_ids,
            device=device,
        ):
            if t in stop_ids:
                break
            out_ids.append(t)
        reply = tok.decode(out_ids).replace("Ġ", " ")
        print(f"USER:    {user_msg}")
        print(f"SILICAT: {reply}")
        print("-" * 60)


if __name__ == "__main__":
    main()
