# Silicat

> An AI for code, trained from scratch.

Silicat is a small GPT-style language model written in PyTorch from the ground up, plus a chat web UI to talk to it. The whole thing — model code, tokenizer, training loop, chat server — lives in this repo. You clone it, train it, and chat with it locally.

## What you get

- **A from-scratch transformer** (`silicat/model.py`) — about 200 lines, no `transformers.AutoModel`.
- **A from-scratch training pipeline** — BPE tokenizer, data prep, two-stage training (pretrain on Python code, then chat fine-tune).
- **A browser chat UI** with streaming responses, served by FastAPI.

## Honest expectations

The default ~10M-parameter Silicat is for **learning how an AI is built**, not for replacing GPT-4 or Claude. Production coding models are **10,000–100,000× larger** and trained on **10,000× more data**. Out of the box, Silicat will:

- speak in the chat format it was trained on,
- recognise basic prompts from the seed dataset,
- emit code-shaped output for short prompts.

It will **not** solve hard, novel programming problems. To make it stronger: increase `n_layer` / `n_embd` / `block_size` in `silicat/model.py`, train on more data, train for more steps.

## Setup

```bash
git clone https://github.com/leo-ailover/silicat
cd silicat
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Training

Three steps:

```bash
# 1) Download + tokenize a Python code corpus (writes data/train.bin, data/val.bin,
#    and checkpoints/tokenizer/).
python -m silicat.dataset --max-samples 5000

# 2) Pretrain (next-token on Python code). On a Colab T4: ~2hr at 3000 steps.
#    On CPU it's slow — use --max-steps 200 just to see it work.
python -m silicat.train --stage pretrain --max-steps 3000 --amp

# 3) Chat fine-tune on data/silicat_chat.jsonl. Loss is masked so the model
#    only learns to produce Silicat's replies, not the user's prompts.
python -m silicat.train --stage chat --max-steps 500 --lr 1e-4
```

Don't have a GPU? Open `notebooks/train.ipynb` in [Google Colab](https://colab.research.google.com), pick a GPU runtime, and `Runtime → Run all`. Download `checkpoints/latest.pt` and `checkpoints/tokenizer/` when done.

## Chat

```bash
python -m silicat.server
# open http://127.0.0.1:8000
```

The status bar at the top shows whether a checkpoint is loaded, how many parameters, and the device. Adjust temperature / top-k / top-p in the right-hand panel.

By default Silicat binds to `127.0.0.1` only. If you want LAN access:

```bash
SILICAT_HOST=0.0.0.0 SILICAT_PORT=8000 python -m silicat.server
```

## Repository layout

```
silicat/
├── silicat/
│   ├── model.py         from-scratch GPT (PyTorch)
│   ├── tokenizer.py     byte-level BPE wrapper
│   ├── chat_format.py   message → token formatting + loss mask
│   ├── dataset.py       corpus download + tokenization
│   ├── generate.py      sampling: temperature / top-k / top-p / streaming
│   ├── train.py         two-stage training loop
│   ├── server.py        FastAPI chat server
│   └── static/          chat UI (no framework)
├── data/
│   └── silicat_chat.jsonl   hand-written chat fine-tune dataset
├── notebooks/train.ipynb    one-click Colab training
├── requirements.txt
└── LICENSE
```

## How it works (one paragraph)

`model.py` defines a standard decoder-only transformer: token + positional embeddings, N pre-LayerNorm blocks of causal multi-head attention + GELU MLP, final LayerNorm, tied linear head. `dataset.py` streams a small slice of `codeparrot-clean-valid`, trains a byte-level BPE on it, and writes the encoded corpus as a flat `uint16` memmap. `train.py` samples random windows of length `block_size` for next-token loss, then in stage two reads `silicat_chat.jsonl`, formats each conversation with `<|user|>` / `<|silicat|>` / `<|end|>` special tokens, and trains with a loss mask so only Silicat's tokens contribute. `server.py` loads `checkpoints/latest.pt`, takes a list of messages, formats them with the same special tokens ending in `<|silicat|>`, and streams sampled tokens over SSE.

## License

MIT.
