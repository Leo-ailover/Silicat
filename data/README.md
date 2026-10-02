# data/

## Chat fine-tuning data (reproducible)

    python data/synth/gen_identity.py      # synth/identity.jsonl   (consistent identity facts)
    python data/synth/gen_paste_code.py    # synth/paste_code.jsonl (verified "fix this code" + multi-turn rows)
    python data/build_chat_dataset.py      # -> silicat_chat_v3.jsonl, silicat_chat_eval.jsonl, chat_stats.json

`silicat_chat.jsonl` + `synth/*.jsonl` are the sources of truth (only 7 of the synth files have generators; the
`more_*.jsonl` files are committed agent output). The builder never reads its own outputs. It validates, normalises,
removes template junk / telegraphic non-answers / unterminated fences / non-compiling python / exact and near duplicates
(one row per prompt cluster), drops rows over 512 tokens (never truncates, so `<|end|>` is always present), and holds out
~300 rows stratified by source. Counts per source and reason: `chat_stats.json`. Details: docstring of
`build_chat_dataset.py`. Tests: `pytest data/test_data_pipeline.py`.

## Pretraining corpus

`corpus_v2.txt` is a frozen raw source (its /tmp clones are gone; `collect_corpus_v2.py` writes
`corpus_v2_rebuild.txt` by default and refuses to overwrite it). `python data/build_corpus.py` cleans it in place
(drops chat transcripts and the 3x-repeated synthetic block, licence headers, charmap tables, emails/home paths, duplicate
paragraphs; chunks and shuffles documents) and records `corpus_v2.manifest.json`; a second run is a no-op. Optional
`--include-synth` (deduped `corpus_synth.txt`), `--add-stdlib` (stdlib remainder beyond the first 8000 chars per file).
After any rewrite rebuild the token bins: `python -m silicat.dataset --v2` (tokenizer_v2 is reused).

`legacy/` holds the one-shot `expand_dataset*.py` scripts (already applied; guarded against re-runs).
