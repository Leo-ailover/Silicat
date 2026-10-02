# Silicat

> A small coding assistant trained entirely from scratch: model, tokenizer, training loop, chat server. No pretrained weights, no HuggingFace models.

Silicat is a GPT-style language model written in plain PyTorch, plus a FastAPI/SSE chat server with a framework-free web UI. The current model ("v3") has **100.7M parameters** and is trained **on CPU only** (4 cores, no GPU) in a cloud container that is wiped periodically, so the repo also contains the machinery that keeps training alive across wipes by committing checkpoints to GitHub.

Figures below are a snapshot (as of the v3 overhaul: 100.7M params, ~8.5 s/step at batch 8 x block 512, 8,478 train / 300 eval chat rows). Check `data/meta_v2.json`, `data/chat_stats.json` and the commands' own output for current values.

## Honest expectations

A 100M-parameter model trained on a ~10M-token, 40 MB corpus for a few thousand CPU steps is a **learning project**, not a replacement for a production coding model (those are 100-10,000x larger and trained on 1,000x more data). Expect it to:

- follow the chat format (`<|user|>...<|end|><|silicat|>...<|end|>`) and stop cleanly,
- answer the kinds of short Python questions present in its chat data, emit code-shaped output and recite common idioms,
- overfit: pretraining sees each token several times; eval loss will sit well above train loss. Read the `gap` printed at each eval.

It will not reliably solve novel programming problems, and it will hallucinate APIs. `python -m silicat.verify` gives a cheap pass/fail check of format and basic behaviour on canned prompts; it is not a benchmark.

## Architecture (`silicat/model_v3.py`)

| Piece | Choice | Why |
|---|---|---|
| Norm | RMSNorm | cheaper than LayerNorm, no bias |
| Positions | RoPE, with **NoPE on every 4th layer** (3:1) | no learned position table; NoPE layers help length generalisation |
| Attention | GQA, 12 query / 4 KV heads, QK-Norm | 3x smaller KV cache; QK-Norm stabilises training |
| MLP | SwiGLU (hidden ~8/3 x n_embd, multiple of 64) | better quality per parameter than GELU |
| Embeddings | tied input/output (one `tok_emb.weight`, no `head.weight` key) | saves 25M parameters |
| Decoding | exact `KVCache` (`GPTV3.new_cache()`) | incremental generation equals the full forward pass (tested) |
| Tokenizer | 32k byte-level BPE, `checkpoints/tokenizer_v2` | specials: `<|pad|>`=0 `<|user|>`=1 `<|silicat|>`=2 `<|end|>`=3 |

Default config: 12 layers, n_embd 768, block size 512, vocab 32,768 (100.7M parameters). Requires **torch >= 2.5** (`enable_gqa` in scaled dot-product attention).

Legacy: `silicat/model.py` is the original GPT-2-style v1 model (13.9M with its default config; an older 182.7M v1 checkpoint exists as `checkpoints/latest.pt.part*`). It is still loadable by the server and trainer (omit `--v3`) but is not the focus.

## Quickstart

```bash
git clone --depth 1 --single-branch --branch claude/recent-conversations-visibility-YdFCm https://github.com/Leo-ailover/Silicat
cd Silicat
```

The full history is ~5 GB (about 800 MB of legacy v1/v2 checkpoint parts); always clone shallow. Then, either by hand:

```bash
pip install -r requirements.txt            # CPU torch is fine; add requirements-dev.txt for tests
python -m silicat.dataset --v2             # tokenize data/corpus_v2.txt -> data/train_v2.bin, val_v2.bin (uint32, ~30 s)
```

or let the recovery script do everything (pip, branch fast-forward, checkpoint assembly from pushed parts, data rebuild, start the watchdog):

```bash
bash scripts/bootstrap.sh                  # ends with "BOOTSTRAP ok step=N"; --dry-run only reports
bash scripts/status.sh                     # one-line STATUS ... summary; exit 0 only if the watchdog is up
```

## Data pipeline

| File | What it is |
|---|---|
| `data/corpus_v2.txt` | 40 MB pretraining corpus: shuffled ~6 KB documents (Python sources, docs, a little prose), separated by blank lines. Built by `data/collect_corpus_v2.py` (defaults to `corpus_v2_rebuild.txt`) and `data/build_corpus.py`; manifest in `data/corpus_v2.manifest.json`. |
| `data/train_v2.bin`, `val_v2.bin` | flat `uint32` token files (gitignored, rebuilt by `python -m silicat.dataset --v2`). Validation is a deterministic **interleaved block split** (4096-token blocks, seed 1234); a candidate val block is rejected when more than 5% of its 32-grams occur in train, so duplicated text cannot leak. Details in `data/meta_v2.json`. |
| `data/silicat_chat_v3.jsonl` | chat fine-tuning set, mostly **LLM-synthesised** (generators and raw output in `data/synth/`) plus a small original seed set. Cleaned by `data/build_chat_dataset.py` (dedupe, template/telegraphic-row removal, fence and syntax repair, length filter to the 512-token block). |
| `data/silicat_chat_eval.jsonl` | 300 held-out rows; no shared prompt with train. |

Chat row format: `{"messages":[{"role":"user","content":...},{"role":"silicat","content":...}]}`; roles strictly alternate, start with `user` and end with `silicat`. `silicat/chat_format.py` renders `<|user|>text<|end|><|silicat|>text<|end|>`; training loss is masked to Silicat's tokens (body and the closing `<|end|>`), never the user turns or role markers. Literal `<|end|>` etc. in text encode as ordinary bytes, never as control ids.

Rebuild the chat set: `python data/build_chat_dataset.py` (see `--help`; keep `--block-size` equal to the chat training block size). Pretraining corpus: `python data/build_corpus.py --dry-run`. Any change to `corpus_v2.txt` requires re-running `python -m silicat.dataset --v2` (token ids and the val split change, so do this before a pretraining run, not during one).

## Training

```bash
# Pretrain (v3, the exact configuration the watchdog uses; ~8.5 s/step on 4 CPU cores):
python -m silicat.train --stage pretrain --v3 --n-layer 12 --n-head 12 --n-kv-head 4 --n-embd 768 \
    --block-size 512 --batch-size 8 --lr 3e-4 --warmup 400 --max-steps 10000 --wsd --resume

# Chat fine-tune (uses data/silicat_chat_v3.jsonl and the held-out data/silicat_chat_eval.jsonl by default;
# keeps the best-by-eval-loss weights; writes checkpoints/chat_v3.pt):
python -m silicat.train --stage chat --v3

# Canned-prompt sanity check, then serve:
python -m silicat.verify
python -m silicat serve
```

Notes:

- Without `--v3` the legacy v1 defaults apply (6 layers, n_embd 384, block 256).
- `--resume` continues from `checkpoints/latest_v3.pt` (full fp32 + AdamW state), else from the committed fp16 parts with a fresh optimizer and a short LR re-warmup (`--rewarmup`, default 100 steps). With nothing to resume it starts at step 0 (`--require-resume` makes that an error). Starting **without** `--resume` when a checkpoint exists is refused unless `--fresh` (archives the old one to `checkpoints/old/<timestamp>/`).
- `SIGTERM`/`SIGINT` finish the current step, save and exit 0. Exit code 0 means "finished or cleanly stopped"; any error is non-zero.
- Other flags: `--seed`, `--precision auto|fp32|bf16`, `--grad-accum`, `--save-interval`, `--eval-interval`, `--eval-windows`, `--chat-epochs`, `--patience`, `--chat-data`, `--chat-eval-data`. See `python -m silicat.train --help`.
- Try everything quickly with a toy model: `--n-layer 2 --n-head 4 --n-kv-head 2 --n-embd 32 --block-size 32 --batch-size 2 --max-steps 5` (this is what `tests/test_train_smoke.py` runs).

## Serving

```bash
python -m silicat serve                  # http://127.0.0.1:8000  (same as `python -m silicat`)
python -m silicat serve --ckpt chat_v3   # a path, or a bare checkpoint name under checkpoints/
```

The server picks the best available checkpoint in this order: `chat_v3`, `chat_best_v3`, `chat_latest_v3`, `latest_v3`, `latest_v2`, `latest`; fp16 exports and pushed parts are assembled automatically. `GET /api/health` reports model, step, device and parameter count; `POST /api/chat` streams SSE (`token`, `done`, `error` events) or returns JSON with `"stream": false`.

Environment: `SILICAT_HOST`, `SILICAT_PORT` (default `127.0.0.1:8000`), `SILICAT_CKPT`, `SILICAT_API_KEY` (bearer token for `/api/chat`), `SILICAT_ALLOWED_HOSTS`, `SILICAT_MAX_BODY`, `SILICAT_MAX_CONCURRENCY`, `SILICAT_MAX_QUEUE`. Binding a non-loopback host (e.g. `SILICAT_HOST=0.0.0.0`) allows any Host header: set an API key if the port is reachable by others.

Paths are resolved from the repo root, overridable with `SILICAT_CKPT_DIR` and `SILICAT_DATA_DIR`.

## Persistence across container wipes

The container is wiped every few days, and anything not on GitHub is lost. Only what is needed to resume is committed:

1. The trainer writes the live checkpoint `checkpoints/latest_v3.pt` (fp32 + AdamW state, gitignored) every `--save-interval` steps, atomically (tmp file + fsync + rename).
2. `scripts/autopush_v3.sh` exports it with `python -m silicat.halve` to `latest_v3.fp16.pt` (weights in fp16, tied embedding stored once, **no optimizer state**), splits it into parts of <= 45 MiB (`latest_v3.fp16.pt.partNN`), writes `checkpoints/latest_v3.manifest.json` (step, per-part and whole-file sha256), and commits and pushes every `PUSH_EVERY_STEPS` (default 500) steps. Each push adds ~100 MB to history, hence the shallow-clone advice.
3. `scripts/watchdog.sh` supervises the trainer and the pusher: restarts them with backoff after crashes, gives up after `MAX_FAST_FAILS` quick failures, and on completion does a final push (exit 0 done, 3 final push pending, 1 error).
4. After a wipe: clone, then `bash scripts/bootstrap.sh`. It verifies the parts against the manifest, assembles `latest_v3.fp16.pt`, rebuilds the token bins if needed and restarts the watchdog; `train.py --resume` continues from the pushed step with a fresh AdamW state (a short LR re-warmup hides the restart). `python -m silicat.assemble [--refresh] <path>` rebuilds a file from its parts by hand.

Check on it any time with `bash scripts/status.sh`. `bash scripts/test_infra.sh` is a ~2 minute end-to-end test of this machinery (needs the token bins). Never `git add checkpoints/` by hand: `.gitignore` un-ignores only the fp16 parts, the manifest, the tokenizers and the legacy v1 parts. `scripts/autopush.sh` and `train_large.sh` from the v2 era are gone; the notebook and `checkpoints/latest*.pt.part*` (v1/v2) are legacy.

## Repository layout

```
silicat/
  model_v3.py      v3 model (RMSNorm, RoPE/NoPE, GQA, QK-Norm, SwiGLU, KVCache)
  model.py         legacy v1 GPT + shared make_adamw
  tokenizer.py     byte-level BPE wrapper (specials at ids 0-3)
  chat_format.py   messages -> ids + loss mask; fit_prompt for long histories
  dataset.py       corpus tokenization, interleaved block split, meta_v2.json
  train.py         pretrain + chat stages, resume, SIGTERM-safe
  checkpoint.py    atomic save/load, resume resolution (local file, fp16 parts, legacy parts)
  halve.py         fp16 export;  assemble.py  split / join <=45 MiB parts;  expand_model.py  add layers
  generate.py      streaming sampler with KV cache; checkpoint + tokenizer discovery
  server.py        FastAPI chat server;  static/  web UI;  verify.py  canned-prompt check
  __main__.py      `python -m silicat {serve,verify,train}`
scripts/           bootstrap.sh, watchdog.sh, autopush_v3.sh, status.sh, common.sh, test_infra.sh
data/              corpus + chat data, builders (build_corpus.py, build_chat_dataset.py), synth/ (LLM-written chat data + generators)
checkpoints/       tokenizer_v2/, pushed fp16 parts + manifest (everything else gitignored)
tests/             pytest suite
notebooks/         legacy Colab notebook (v1 flow)
```

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests          # CPU only, ~35 s: tiny random models and a temp-dir checkpoint/data tree
ruff check silicat tests
```

Covers model shapes/causality/GQA/NoPE/tied weights, KV cache equals full forward, tokenizer round trip on the committed `tokenizer_v2`, chat masking and the train-time shift, block-split disjointness, checkpoint atomicity and resume (optimizer restored; resume from fp16 parts), a 5-step end-to-end pretrain + chat run, deterministic greedy generation, the server (`/api/health`, `/api/chat`), and validators for the committed chat data (schema, no duplicates, every row fits the 512 block, no train/eval prompt overlap). Data tests skip if the files are absent. CI (`.github/workflows/ci.yml`) runs ruff and pytest on pull requests and on pushes that touch code, never on checkpoint commits.

## Licences

Silicat's own code, the chat data and the generators are MIT (see `LICENSE`). `data/corpus_v2.txt` is an **aggregate of third-party material under its original licences and is not relicensed as MIT**: CPython stdlib (PSF), installed site-packages and cloned repositories (Flask, requests, TheAlgorithms/Python, nanoGPT; BSD/Apache/MIT and others), TinyShakespeare, and prose from the Python Data Science Handbook, whose text is CC-BY-NC-ND. Check the licence of anything you redistribute (the corpus file in particular) and do not assume it is permissively licensed.
