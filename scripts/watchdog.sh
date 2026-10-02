#!/bin/bash
# Supervisor: keeps the v3 pretrain run AND scripts/autopush_v3.sh alive across crashes.
#
#   nohup setsid bash scripts/watchdog.sh >> watchdog.log 2>&1 &        (scripts/bootstrap.sh does this)
#
# - single instance (flock; a second start exits 0 with "already running")
# - on startup runs `bootstrap.sh --no-watchdog --no-git --no-pip` (verify/assemble checkpoint, rebuild bins)
# - trainer crash => restart with exponential backoff 30,60,120,240,300 s (BACKOFF_BASE); a run that lasted >= 600 s resets it;
#   MAX_FAST_FAILS (10) consecutive fast failures => "GIVING_UP", exit 1 (0 = never give up)
# - trainer exit code 0 => finished: stop the autopush loop, run one final `autopush_v3.sh --once`, exit 0
#   (an already-finished run exits 0 immediately from train.py, so a restart after a wipe does not re-train)
# - SIGTERM/SIGINT: forwarded to the trainer (it saves at the next step boundary and exits), then autopush is
#   stopped and a best-effort final push is attempted; a second signal is not intercepted by the trainer
#   (it dies immediately) -- use `kill -9` only as a last resort
# - logs are capped: any log above LOG_MAX_MB (50) is copy-truncated to <log>.1
#
# Environment: MAX_STEPS (10000) SAVE_INTERVAL (100) EVAL_INTERVAL (500) PUSH_EVERY_STEPS (500) POLL_SECS (30)
#   TRAIN_CMD (override the whole trainer command line; flags are still checked against `train --help`)
# Output: "[watchdog] <ISO time> EVENT k=v": START TRAIN_START TRAIN_EXIT AUTOPUSH_START AUTOPUSH_EXIT DONE GIVING_UP ...

set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
TAG=watchdog
wl() { log "$TAG" "$@"; }

POLL_SECS="${POLL_SECS:-30}"
MAX_STEPS="${MAX_STEPS:-10000}"
SAVE_INTERVAL="${SAVE_INTERVAL:-100}"
EVAL_INTERVAL="${EVAL_INTERVAL:-500}"
export PUSH_EVERY_STEPS="${PUSH_EVERY_STEPS:-500}" MAX_STEPS
MAX_FAST_FAILS="${MAX_FAST_FAILS:-10}"
BACKOFF_BASE="${BACKOFF_BASE:-30}"      # restart delays: base, 2x, 4x, 8x, then 10x (300 s)
LOG_MAX_MB="${LOG_MAX_MB:-50}"
FLUSH_TIMEOUT="${FLUSH_TIMEOUT:-600}"
TRAIN_LOG="$LOG_DIR/training_v3_pretrain.log"
PUSH_LOG="$LOG_DIR/autopush_v3.log"

# Flags must exist in silicat.train (a script-vs-CLI mismatch is a bug: see the old halve --ckpt/--out).
if [ -n "${TRAIN_CMD:-}" ]; then
    read -r -a TRAIN_ARGS <<< "$TRAIN_CMD"
else
    TRAIN_ARGS=("$PY" -m silicat.train --stage pretrain --v3
        --n-layer 12 --n-head 12 --n-kv-head 4 --n-embd 768
        --block-size 512 --batch-size 8
        --lr 3e-4 --warmup 400 --max-steps "$MAX_STEPS"
        --eval-interval "$EVAL_INTERVAL" --save-interval "$SAVE_INTERVAL"
        --wsd --resume)
fi

check_flags() {
    local help a bad=0
    help="$("$PY" -m silicat.train --help 2>&1)" || { wl "FLAGCHECK_FAILED err=cannot run silicat.train --help"; return 1; }
    for a in "${TRAIN_ARGS[@]}"; do
        case "$a" in --*) printf '%s' "$help" | grep -qE -- "(^|[^A-Za-z0-9-])${a}([^A-Za-z0-9-]|$)" || { wl "FLAGCHECK_FAILED unknown_flag=$a"; bad=1; } ;; esac
    done
    return "$bad"
}

cap_log() {
    local f
    for f in "$TRAIN_LOG" "$PUSH_LOG" "$LOG_DIR/watchdog.log"; do
        [ -f "$f" ] || continue
        if [ "$(stat -c %s "$f")" -gt $((LOG_MAX_MB * 1024 * 1024)) ]; then
            cp -f "$f" "$f.1" && : > "$f"      # writers use O_APPEND, so truncation is safe
            wl "LOG_TRUNCATED file=$f"
        fi
    done
}

exec 9>"$(lock_path watchdog)"
flock -n 9 || { wl "already running (lock $(lock_path watchdog))"; exit 0; }
cd "$REPO_DIR" || exit 1
mkdir -p "$LOG_DIR"

train_pid=""; push_pid=""; stop=0; sig=""
spid=""
on_sig() { stop=1; sig="$1"; [ -n "$spid" ] && kill "$spid" 2>/dev/null; }
trap 'on_sig TERM' TERM
trap 'on_sig INT' INT

wl "START pid=$$ repo=$REPO_DIR ckpt=$LIVE_PT max_steps=$MAX_STEPS save_every=$SAVE_INTERVAL push_every=$PUSH_EVERY_STEPS"
check_flags || { wl "ABORT reason=flag_mismatch"; exit 1; }
if [ "${SKIP_BOOTSTRAP:-0}" != 1 ]; then
    if ! bash "$SCRIPT_DIR/bootstrap.sh" --no-watchdog --no-git --no-pip; then
        wl "ABORT reason=bootstrap_failed (see output above)"; exit 1
    fi
fi

train_start=0; fails=0; next_train=0; next_push=0; train_done=0

start_train() {
    wl "TRAIN_START cmd=${TRAIN_ARGS[*]}"
    echo "[watchdog] $(ts) (re)starting training" >> "$TRAIN_LOG"
    # fd 9 (watchdog lock) is closed for children so an orphan can never keep the watchdog lock held
    # the subshell takes the trainer lock on fd 8, then exec()s the trainer, so $! IS the trainer pid and the
    # trainer itself holds the lock (an orphan survives a SIGKILLed watchdog but cannot be started twice)
    ( exec 8>"$(lock_path trainer)"; flock -n 8 || exit 75; exec "${TRAIN_ARGS[@]}" ) >> "$TRAIN_LOG" 2>&1 9>&- &
    train_pid=$!; train_start=$SECONDS
}

while [ "$stop" -eq 0 ]; do
    now=$SECONDS
    # ---- trainer
    if [ "$train_done" -eq 0 ]; then
        if [ -n "$train_pid" ] && ! kill -0 "$train_pid" 2>/dev/null; then
            wait "$train_pid"; rc=$?
            ran=$((SECONDS - train_start)); train_pid=""
            cs=""; [ "$rc" -eq 0 ] && cs="$(ckpt_step "$LIVE_PT" 2>/dev/null)"
            if [ "$rc" -eq 0 ] && [ "${cs:-0}" -ge "$MAX_STEPS" ]; then
                wl "TRAIN_EXIT rc=0 ran=${ran}s step=$cs -> finished, not restarting"
                train_done=1
            elif [ "$rc" -eq 0 ]; then
                wl "TRAIN_EXIT rc=0 early_stop step=${cs:-?} ran=${ran}s restart_in=${BACKOFF_BASE}s"
                next_train=$((SECONDS + BACKOFF_BASE))
            elif [ "$rc" -eq 75 ]; then
                wl "TRAIN_EXIT rc=75 another trainer holds $(lock_path trainer); retry in 60s"
                next_train=$((SECONDS + 60))
            else
                if [ "$ran" -ge 600 ]; then fails=1; else fails=$((fails + 1)); fi
                delay=$((BACKOFF_BASE << (fails - 1 > 4 ? 4 : fails - 1))); [ "$delay" -gt $((BACKOFF_BASE * 10)) ] && delay=$((BACKOFF_BASE * 10))
                wl "TRAIN_EXIT rc=$rc ran=${ran}s fast_fails=$fails restart_in=${delay}s"
                next_train=$((SECONDS + delay))
                if [ "$MAX_FAST_FAILS" -gt 0 ] && [ "$fails" -ge "$MAX_FAST_FAILS" ]; then
                    wl "GIVING_UP after $fails consecutive failed runs; fix the cause then restart bootstrap.sh"
                    stop=2; break
                fi
            fi
        fi
        if [ "$train_done" -eq 0 ] && [ -z "$train_pid" ] && [ "$SECONDS" -ge "$next_train" ]; then
            start_train
        fi
    fi
    if [ "$train_done" -eq 1 ]; then break; fi
    # ---- autopush
    if [ -n "$push_pid" ] && ! kill -0 "$push_pid" 2>/dev/null; then
        wait "$push_pid"; wl "AUTOPUSH_EXIT rc=$?"; push_pid=""; next_push=$((SECONDS + 60))
    fi
    if [ -z "$push_pid" ] && [ "$SECONDS" -ge "$next_push" ]; then
        bash "$SCRIPT_DIR/autopush_v3.sh" >> "$PUSH_LOG" 2>&1 9>&- &
        push_pid=$!; wl "AUTOPUSH_START pid=$push_pid"
    fi
    cap_log
    sleep "$POLL_SECS" & spid=$!
    wait "$spid"; spid=""
done

# ---- shutdown (finished, signalled or gave up)
if [ -n "$train_pid" ] && kill -0 "$train_pid" 2>/dev/null; then
    wl "FORWARD signal=${sig:-TERM} to trainer pid=$train_pid (waiting up to 120s for its final save)"
    kill -TERM "$train_pid" 2>/dev/null
    for _ in $(seq 120); do kill -0 "$train_pid" 2>/dev/null || break; sleep 1; done
    kill -0 "$train_pid" 2>/dev/null && { wl "KILL trainer pid=$train_pid did not exit"; kill -KILL "$train_pid" 2>/dev/null; }
    wait "$train_pid" 2>/dev/null
fi
if [ -n "$push_pid" ]; then
    kill -TERM "$push_pid" 2>/dev/null; wait "$push_pid" 2>/dev/null
fi
if [ "$stop" -ne 2 ]; then
    wl "FINAL_PUSH start"
    ok=0
    for attempt in 1 2 3 4 5; do
        if timeout "$FLUSH_TIMEOUT" bash "$SCRIPT_DIR/autopush_v3.sh" --once >> "$PUSH_LOG" 2>&1 9>&-; then ok=1; break; fi
        [ "$stop" -ne 0 ] && break      # signalled: one best-effort try only
        wl "FINAL_PUSH attempt=$attempt failed; retry in 30s"; sleep 30
    done
    if [ "$ok" -eq 1 ]; then wl "DONE final checkpoint pushed (step=$(manifest_field step))"
    else wl "FINAL_PUSH_PENDING the last checkpoint is NOT on GitHub; run: bash scripts/autopush_v3.sh --once"; exit 3; fi
fi
[ "$stop" -eq 2 ] && exit 1
[ -n "$sig" ] && exit 143
exit 0
