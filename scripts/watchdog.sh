#!/bin/bash
# Watchdog: keeps training running by restarting if it dies.
set -euo pipefail

LOG="training_v3_pretrain.log"
TRAIN_CMD="python -m silicat.train --stage pretrain --v3 \
  --n-layer 12 --n-head 12 --n-kv-head 4 --n-embd 768 \
  --block-size 512 --batch-size 8 \
  --lr 3e-4 --warmup 400 --max-steps 10000 \
  --eval-interval 500 --save-interval 50 \
  --wsd --resume"

echo "[watchdog] started at $(date)"

while true; do
    echo "[watchdog] launching training at $(date)" >> "$LOG"
    $TRAIN_CMD >> "$LOG" 2>&1 || true
    echo "[watchdog] training exited at $(date), restarting in 5s..." >> "$LOG"
    sleep 5
done
