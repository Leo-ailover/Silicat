#!/bin/bash
# Watchdog: keeps training AND autopush running, restarting either if it dies.
set -uo pipefail

LOG="training_v3_pretrain.log"
TRAIN_CMD="python -m silicat.train --stage pretrain --v3 \
  --n-layer 12 --n-head 12 --n-kv-head 4 --n-embd 768 \
  --block-size 512 --batch-size 8 \
  --lr 3e-4 --warmup 400 --max-steps 10000 \
  --eval-interval 500 --save-interval 50 \
  --wsd --resume"

echo "[watchdog] started at $(date)"

train_pid=""
push_pid=""

while true; do
    if [ -z "$train_pid" ] || ! kill -0 "$train_pid" 2>/dev/null; then
        echo "[watchdog] (re)starting training at $(date)" >> "$LOG"
        $TRAIN_CMD >> "$LOG" 2>&1 &
        train_pid=$!
        echo "[watchdog] training pid $train_pid"
    fi
    if [ -z "$push_pid" ] || ! kill -0 "$push_pid" 2>/dev/null; then
        echo "[watchdog] (re)starting autopush at $(date)"
        bash scripts/autopush_v3.sh >> autopush_v3.log 2>&1 &
        push_pid=$!
        echo "[watchdog] autopush pid $push_pid"
    fi
    sleep 30
done
