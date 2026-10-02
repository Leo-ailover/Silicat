# Legacy dataset expanders

`expand_dataset.py` .. `expand_dataset_v5.py` were one-shot scripts that APPENDED hand-written examples to
`data/silicat_chat.jsonl` (they were run once; the result is the committed 1,410-row file; the v5 docstring's
"~2500" was never reached). Re-running them duplicates rows, so each now refuses to run unless `--force-append` is
given. Do not use them: the pipeline is

    data/silicat_chat.jsonl + data/synth/*.jsonl  --(python data/build_chat_dataset.py)-->
        data/silicat_chat_v3.jsonl (train), data/silicat_chat_eval.jsonl (held out), data/chat_stats.json

`data/synth/gen_*.py` regenerate 7 of the 35 synth files (the other `more_*.jsonl` files are committed outputs of
agents and are the source of truth); `gen_identity.py` and `gen_paste_code.py` produce `identity.jsonl` and
`paste_code.jsonl`. Pretraining corpus: `data/build_corpus.py` (see its docstring).
