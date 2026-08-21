#!/bin/bash
# Auto-push v3 checkpoint to GitHub whenever latest_v3.pt is updated.
# Runs alongside training. Each successful push prints one line to stdout,
# which the Monitor tool picks up as a notification.
#
# Usage:  bash scripts/autopush_v3.sh >> autopush_v3.log 2>&1 &

set -euo pipefail
CKPT="checkpoints/latest_v3.pt"
TOUCH=".last_push_v3"
BRANCH=$(git rev-parse --abbrev-ref HEAD)

touch "$TOUCH"

echo "autopush_v3 watching $CKPT on branch $BRANCH"

while true; do
    sleep 90

    # Only act when the checkpoint is newer than our last push
    if [ ! -f "$CKPT" ] || [ ! "$CKPT" -nt "$TOUCH" ]; then
        continue
    fi

    STEP=$(python -c "
import torch, sys
try:
    ck = torch.load('$CKPT', map_location='cpu', weights_only=False)
    print(ck.get('step', '?'))
except Exception as e:
    print('ERR', file=sys.stderr)
    sys.exit(1)
" 2>/dev/null) || continue

    echo "[autopush_v3] halving checkpoint at step $STEP..."
    python -m silicat.halve --src "$CKPT" --dst "$CKPT" 2>/dev/null || true

    echo "[autopush_v3] splitting..."
    cd checkpoints
    rm -f latest_v3.pt.part*
    split -b 45m latest_v3.pt latest_v3.pt.part
    # rename partaa→part00, partab→part01, etc.
    i=0
    for f in $(ls latest_v3.pt.part?? 2>/dev/null | sort); do
        mv "$f" "$(printf 'latest_v3.pt.part%02d' $i)"
        i=$((i + 1))
    done
    cd ..

    echo "[autopush_v3] committing step $STEP..."
    git add checkpoints/latest_v3.pt.part* 2>/dev/null || true
    git diff --cached --quiet && { echo "[autopush_v3] nothing new to commit"; touch "$TOUCH"; continue; }
    git commit -m "pretrain v3 checkpoint step $STEP

https://claude.ai/code/session_01SbbFPVB8fE91W8uChNjk2i" 2>/dev/null || true

    if git push -u origin "$BRANCH" 2>/dev/null; then
        touch "$TOUCH"
        echo "PUSHED v3 checkpoint at step $STEP"  # <-- Monitor picks this up
    else
        echo "[autopush_v3] push failed, will retry"
    fi
done
