#!/bin/bash
# Runs sequentially after 91M v4 fine-tune:
# 1. Save the 91M v4 weights.
# 2. Expand to 176M via layer-doubling.
# 3. Fine-tune the 176M model on the chat dataset.
set -e

echo "=== Waiting for 91M fine-tune (PID 5736) to finish ===" | tee -a training_176M.log
while kill -0 5736 2>/dev/null; do
    sleep 30
done
echo "=== 91M fine-tune done ===" | tee -a training_176M.log

echo "=== Saving 91M v4 checkpoint ===" | tee -a training_176M.log
cp checkpoints/latest.pt checkpoints/chat_v4_91M.pt

echo "=== Expanding 91M → 176M via layer doubling ===" | tee -a training_176M.log
python -m silicat.expand_model \
    --src checkpoints/chat_v4_91M.pt \
    --dst checkpoints/latest.pt \
    --n-layer 24 2>&1 | tee -a training_176M.log

echo "=== Starting 176M chat fine-tune ===" | tee -a training_176M.log
python -m silicat.train \
    --stage chat \
    --batch-size 2 \
    --block-size 256 \
    --dropout 0.1 \
    --lr 1e-4 \
    --max-steps 3000 \
    --warmup 150 \
    --save-interval 250 \
    --log-interval 10 \
    --chat-data data/silicat_chat.jsonl \
    >> training_176M.log 2>&1

echo "=== 176M done. Saving versioned copy ===" | tee -a training_176M.log
cp checkpoints/latest.pt checkpoints/chat_v4_176M.pt
echo "=== All done ===" | tee -a training_176M.log
