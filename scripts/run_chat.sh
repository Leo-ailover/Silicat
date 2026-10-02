#!/bin/bash
# Run the chat fine-tune stage and persist the result (the pretrain watchdog only pushes latest_v3).
#
#   bash scripts/run_chat.sh [extra silicat.train args...]
#
# Runs `python -m silicat.train --stage chat --v3 --resume`-style (CHAT_CMD overrides the whole command), then
# CKPT_NAME=chat_v3 scripts/autopush_v3.sh --once, which halves/splits/commits/pushes checkpoints/chat_v3.pt
# as chat_v3.fp16.pt.partNN + chat_v3.manifest.json. Restore after a wipe: scripts/bootstrap.sh.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
if [ -n "${CHAT_CMD:-}" ]; then read -r -a CMD <<< "$CHAT_CMD"
else CMD=("$PY" -m silicat.train --stage chat --v3 "$@"); fi
cd "$ROOT" && "${CMD[@]}" || { echo "[run_chat] training failed rc=$?" >&2; exit 1; }
# a fresh chat run restarts step counting: forget the previous chat push markers
rm -f "$REPO_DIR/.last_push_chat_v3" "$REPO_DIR/.last_push_chat_v3.seen"
CKPT_NAME=chat_v3 bash "$ROOT/scripts/autopush_v3.sh" --once
