#!/bin/bash
# Auto-push checkpoint to GitHub whenever latest_v2.pt is updated.
# Runs alongside training. Each successful push prints one line to stdout,
# which the Monitor tool picks up as a notification.
#
# Usage:  bash scripts/autopush.sh >> autopush.log 2>&1 &

set -euo pipefail
CKPT="checkpoints/latest_v2.pt"
TOUCH=".last_push_v2"
BRANCH=$(git rev-parse --abbrev-ref HEAD)

touch "$TOUCH"

echo "autopush watching $CKPT on branch $BRANCH"

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

    echo "[autopush] halving checkpoint at step $STEP..."
    python -m silicat.halve --ckpt "$CKPT" --out "$CKPT" 2>/dev/null || \
        python -m silicat.halve 2>/dev/null || true

    echo "[autopush] splitting..."
    cd checkpoints
    rm -f latest_v2.pt.part*
    split -b 45m latest_v2.pt latest_v2.pt.part
    # rename partaa→part00, partab→part01, etc.
    i=0
    for f in $(ls latest_v2.pt.part?? 2>/dev/null | sort); do
        mv "$f" "$(printf 'latest_v2.pt.part%02d' $i)"
        i=$((i + 1))
    done
    cd ..

    echo "[autopush] committing step $STEP..."
    git add checkpoints/latest_v2.pt.part* 2>/dev/null || true
    git diff --cached --quiet && { echo "[autopush] nothing new to commit"; touch "$TOUCH"; continue; }
    git commit -m "pretrain v2 checkpoint step $STEP

https://claude.ai/code/session_01SbbFPVB8fE91W8uChNjk2i" 2>/dev/null || true

    if git push -u origin "$BRANCH" 2>/dev/null; then
        touch "$TOUCH"
        echo "PUSHED checkpoint at step $STEP"  # <-- Monitor picks this up
    else
        echo "[autopush] push failed, will retry"
    fi
done
