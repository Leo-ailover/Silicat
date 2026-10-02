#!/bin/bash
# Persist the v3 training checkpoint to GitHub (the container is wiped without warning).
#
#   bash scripts/autopush_v3.sh            # loop: poll every POLL_SECS (default 90), log to stdout
#   bash scripts/autopush_v3.sh --once     # one cycle that ignores the cadence (final flush), then exit
#
# What a push is
#   1. `silicat.halve` exports the LIVE checkpoint (checkpoints/latest_v3.pt, fp32 + optimizer, owned by
#      the trainer and NEVER modified here) to a separate fp16 file checkpoints/latest_v3.fp16.pt (gitignored).
#   2. That export is split into <=45 MiB parts checkpoints/latest_v3.fp16.pt.partNN (GitHub rejects >100 MB
#      blobs) and described by checkpoints/latest_v3.manifest.json (step, part list, size + sha256 per part,
#      sha256 of the whole export). Stale higher-numbered parts are removed (and the removal is committed).
#   3. ONLY those parts + the manifest are staged and committed (pathspec-limited, so whatever else is staged
#      in the working tree is untouched), then pushed to the CURRENT branch. No force-push, no branch change.
#   Restore: `bash scripts/bootstrap.sh` (verifies parts against the manifest, assembles, trainer resumes
#   from the export with a fresh AdamW state; see silicat/checkpoint.py).
#
# Cadence and git-history growth (read this before lowering PUSH_EVERY_STEPS)
#   A 100.7M-param fp16 export is ~201 MB and is incompressible (zlib ratio ~0.92) and every byte changes
#   between checkpoints, so git cannot delta it: EVERY push adds ~200 MB to .git and to every future clone.
#   PUSH_EVERY_STEPS=500 (default; ~71 min of training at ~8.5 s/step) => 10000 steps = 20 pushes ~ 4 GB.
#   PUSH_EVERY_STEPS=2000 => 5 pushes ~ 1 GB. Every 50 steps (old behaviour) would be ~200 pushes ~ 40 GB.
#   500 is the compromise: a wipe loses at most ~70 min of CPU training. The last step (MAX_STEPS) is
#   always pushed, as is the checkpoint present when training ends (watchdog runs --once). The repo is
#   already ~5 GB from earlier v2 pushes; rewriting history is NOT done here (needs the owner's approval).
#   The save interval of the trainer (--save-interval) is independent: it only controls local saves.
#
# Environment: PUSH_EVERY_STEPS (500), MAX_STEPS (10000), POLL_SECS (90), PART_SIZE (45m), PUSH_BACKOFF ("2 4 8 16"), CKPT_NAME (latest_v3),
#   BRANCH (current branch), REMOTE (origin), CLAUDE_SESSION_URL (optional commit trailer), MIN_FREE_MB (3000; a cycle is
#   skipped below this much free disk), see common.sh.
# Chat stage: the chat fine-tune (the model `serve` prefers) is NOT pushed by the pretrain watchdog. After the chat run use
#   scripts/run_chat.sh, or by hand:  CKPT_NAME=chat_v3 bash scripts/autopush_v3.sh --once
# Output (grep-able): "[autopush_v3] <ISO time> <EVENT> k=v ...", events: START SKIP EXPORTED COMMITTED
#   PUSHED PUSH_FAILED DIVERGED CYCLE_FAILED. Success line: "PUSHED v3 checkpoint at step N ...".

set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

TAG=autopush_v3
POLL_SECS="${POLL_SECS:-90}"
PUSH_EVERY_STEPS="${PUSH_EVERY_STEPS:-500}"
MAX_STEPS="${MAX_STEPS:-10000}"
PUSH_BACKOFF="${PUSH_BACKOFF:-2 4 8 16}"   # seconds before retries 2..5 of a failed push
PART_SIZE="${PART_SIZE:-45m}"   # GitHub blob limit is 100 MB; tests override
ONCE=0
for a in "$@"; do
    case "$a" in
        --once) ONCE=1 ;;
        -h|--help) sed -n '2,/^set -uo/p' "$0" | sed '$d'; exit 0 ;;
        *) echo "unknown argument: $a" >&2; exit 2 ;;
    esac
done

lg() { log "$TAG" "$@"; }
g() { git -C "$REPO_DIR" "$@"; }
CK_REL="$(realpath --relative-to="$REPO_DIR" "$CKPT_DIR")"
case "$CK_REL" in ..*) echo "checkpoint dir $CKPT_DIR is outside the git tree $REPO_DIR" >&2; exit 2 ;; esac
PARTS_GLOB="$CK_REL/$CKPT_NAME.fp16.pt.part*"
MANIFEST_REL="$CK_REL/${CKPT_NAME}.manifest.json"
PATHSPECS=("$PARTS_GLOB" "$MANIFEST_REL")
SEEN="$PUSH_STAMP.seen"      # "mtime:size" of the live checkpoint last examined
STAGE="$CKPT_DIR/.push_tmp"

branch_now() {
    local b="${BRANCH:-$(g rev-parse --abbrev-ref HEAD 2>/dev/null)}"
    [ -n "$b" ] && [ "$b" != HEAD ] && echo "$b"
}

write_atomic() { local tmp="$2.tmp.$$"; printf '%s\n' "$1" > "$tmp" && mv -f "$tmp" "$2"; }

last_pushed() {
    local v; v="$(cat "$PUSH_STAMP" 2>/dev/null | tr -dc 0-9)"
    [ -n "$v" ] || v="$(manifest_field step)"
    echo "${v:--1}"
}

# Push the committed-but-unpushed checkpoint commit. 5 attempts, backoff 2/4/8/16 s. Never forces.
push_pending() {
    [ -f "$PENDING" ] || return 0
    local pstep psha br d attempt=0 err rc
    read -r pstep psha < "$PENDING"
    if ! g merge-base --is-ancestor "$psha" HEAD 2>/dev/null; then
        lg "SKIP reason=pending_commit_not_in_HEAD step=$pstep sha=${psha:0:7} (dropping marker)"
        rm -f "$PENDING"; return 0
    fi
    br="$(branch_now)" || { lg "PUSH_FAILED step=$pstep err=detached_HEAD"; return 1; }
    for d in 0 $PUSH_BACKOFF; do
        [ "$d" -gt 0 ] && sleep "$d"
        attempt=$((attempt + 1))
        err="$(GIT_HTTP_LOW_SPEED_LIMIT=1000 GIT_HTTP_LOW_SPEED_TIME=120 \
               g -c http.postBuffer=524288000 push "$REMOTE" "HEAD:refs/heads/$br" 2>&1)"; rc=$?
        if [ "$rc" -eq 0 ]; then
            write_atomic "$pstep" "$PUSH_STAMP"
            rm -f "$PENDING"
            lg "PUSHED v3 checkpoint at step $pstep sha=${psha:0:7} branch=$br attempts=$attempt"
            return 0
        fi
        lg "PUSH_FAILED step=$pstep attempt=$attempt err=$(printf '%s' "$err" | tail -n 1 | cut -c1-200)"
        if printf '%s' "$err" | grep -qiE 'non-fast-forward|fetch first|stale info'; then
            lg "DIVERGED step=$pstep branch=$br (remote has commits we lack; rebasing, never forcing)"
            if g fetch -q "$REMOTE" "$br" && g rebase --autostash "$REMOTE/$br" >/dev/null 2>&1; then
                psha="$(g rev-parse HEAD)"; write_atomic "$pstep $psha" "$PENDING"
                lg "REBASED step=$pstep new_sha=${psha:0:7}"
                continue
            fi
            g rebase --abort 2>/dev/null
            lg "DIVERGED_UNRESOLVED step=$pstep (rebase failed; reconcile manually)"
            return 1
        fi
    done
    lg "PUSH_FAILED step=$pstep giving_up_until_next_cycle=1"
    return 1
}

# git command that tolerates a short-lived index.lock held by another git process
git_retry() {
    local i out rc
    for i in 1 2 3; do
        out="$(g "$@" 2>&1)"; rc=$?
        [ "$rc" -eq 0 ] && { [ -n "$out" ] && echo "$out" >&2; return 0; }
        printf '%s' "$out" | grep -q 'index.lock' || break
        sleep 2
    done
    printf '%s\n' "$out" >&2
    return "$rc"
}

# Export + split + manifest + commit for the current live checkpoint (force=1 ignores the cadence)
maybe_export() {
    local force="$1" sig step last half n i total f
    [ -f "$LIVE_PT" ] || return 0
    sig="$(stat -c '%Y:%s' "$LIVE_PT")"
    if [ "$force" -eq 0 ] && [ "$sig" = "$(cat "$SEEN" 2>/dev/null)" ]; then return 0; fi
    step="$(ckpt_step "$LIVE_PT")" || { lg "SKIP reason=unreadable_checkpoint file=$LIVE_PT"; return 1; }
    last="$(last_pushed)"
    if [ -f "$PENDING" ]; then lg "SKIP reason=push_pending step=$step"; return 1; fi
    if [ "$step" -le "$last" ]; then
        lg "SKIP reason=already_pushed step=$step last_pushed=$last"; write_atomic "$sig" "$SEEN"; return 0
    fi
    if [ "$force" -eq 0 ] && [ "$step" -lt "$MAX_STEPS" ] && [ "$step" -lt $((last + PUSH_EVERY_STEPS)) ]; then
        lg "SKIP reason=cadence step=$step last_pushed=$last every=$PUSH_EVERY_STEPS"
        write_atomic "$sig" "$SEEN"; return 0
    fi

    free="$(df -Pk "$CKPT_DIR" | awk 'NR==2{print int($4/1024)}')"
    if [ "${free:-0}" -lt "${MIN_FREE_MB:-3000}" ]; then
        lg "SKIP reason=low_disk free_mb=$free min_free_mb=${MIN_FREE_MB:-3000} step=$step"; return 1
    fi
    rm -rf "$STAGE"; mkdir -p "$STAGE"
    if ! "$PY" -m silicat.halve --src "$LIVE_PT" --dst "$EXPORT_PT" >"$STAGE/halve.out" 2>&1; then
        lg "CYCLE_FAILED reason=halve step=$step err=$(tail -n 1 "$STAGE/halve.out" | cut -c1-200)"
        rm -rf "$STAGE"; return 1
    fi
    step="$(ckpt_step "$EXPORT_PT")" || { lg "CYCLE_FAILED reason=export_unreadable"; rm -rf "$STAGE"; return 1; }
    lg "EXPORTED step=$step bytes=$(stat -c %s "$EXPORT_PT")"

    split -b "$PART_SIZE" -d -a 2 "$EXPORT_PT" "$STAGE/$CKPT_NAME.fp16.pt.part" || { lg "CYCLE_FAILED reason=split"; rm -rf "$STAGE"; return 1; }
    n=0; total=0
    for f in "$STAGE/$CKPT_NAME.fp16.pt.part"[0-9][0-9]; do
        [ -f "$f" ] || continue
        n=$((n + 1)); total=$((total + $(stat -c %s "$f")))
    done
    if [ "$n" -eq 0 ] || [ "$total" -ne "$(stat -c %s "$EXPORT_PT")" ]; then
        lg "CYCLE_FAILED reason=split_size_mismatch parts=$n"; rm -rf "$STAGE"; return 1
    fi
    "$PY" - "$STAGE" "$CKPT_NAME" "$step" "$STAGE/manifest.json" <<'PYEOF' || { lg "CYCLE_FAILED reason=manifest"; rm -rf "$STAGE"; return 1; }
import hashlib, json, os, re, sys, time
stage, name, step, out = sys.argv[1:5]
pat = re.compile(re.escape(f"{name}.fp16.pt.part") + r"\d\d$")
names = sorted(f for f in os.listdir(stage) if pat.match(f))
whole, parts = hashlib.sha256(), []
for f in names:
    h = hashlib.sha256()
    with open(os.path.join(stage, f), "rb") as fh:
        while c := fh.read(1 << 22):
            h.update(c); whole.update(c)
    parts.append({"name": f, "size": os.path.getsize(os.path.join(stage, f)), "sha256": h.hexdigest()})
m = {"version": 1, "name": name, "file": f"{name}.fp16.pt", "step": int(step), "n_parts": len(parts),
     "total_bytes": sum(p["size"] for p in parts), "sha256": whole.hexdigest(),
     "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "parts": parts}
tmp = out + ".tmp"
with open(tmp, "w") as fh:
    json.dump(m, fh, indent=1); fh.write("\n"); fh.flush(); os.fsync(fh.fileno())
os.replace(tmp, out)
PYEOF
    # swap in: old parts (any count) are removed only now that the new set is complete
    rm -f "$CKPT_DIR/$CKPT_NAME.fp16.pt.part"[0-9][0-9]
    mv -f "$STAGE/$CKPT_NAME.fp16.pt.part"[0-9][0-9] "$CKPT_DIR/" && mv -f "$STAGE/manifest.json" "$MANIFEST" \
        || { lg "CYCLE_FAILED reason=install_parts"; return 1; }
    touch "$EXPORT_PT"   # export is at least as new as the parts: assemble --refresh will not redo it
    rm -rf "$STAGE"

    git_retry add -f -A -- "${PATHSPECS[@]}" || { lg "CYCLE_FAILED reason=git_add"; return 1; }
    if g diff --cached --quiet -- "${PATHSPECS[@]}"; then
        lg "SKIP reason=identical_to_HEAD step=$step"
        write_atomic "$step" "$PUSH_STAMP"; write_atomic "$sig" "$SEEN"; return 0
    fi
    local kind=pretrain; case "$CKPT_NAME" in chat*) kind=chat ;; esac
    local msg="$kind v3 checkpoint $CKPT_NAME step $step (fp16, $n parts)"
    [ -n "${CLAUDE_SESSION_URL:-}" ] && msg="$msg

$CLAUDE_SESSION_URL"
    git_retry commit -q -m "$msg" -- "${PATHSPECS[@]}" || { lg "CYCLE_FAILED reason=git_commit step=$step"; return 1; }
    local sha; sha="$(g rev-parse HEAD)"
    write_atomic "$step $sha" "$PENDING"; write_atomic "$sig" "$SEEN"
    lg "COMMITTED step=$step sha=${sha:0:7} parts=$n bytes=$total (adds ~$((total / 1000000)) MB to git history)"
}

tick() { push_pending; maybe_export "$1"; push_pending; }

cycle_locked() {   # one serialized cycle (shared lock with --once runs)
    ( flock -w 3600 8 || { lg "CYCLE_FAILED reason=lock_timeout"; exit 1; }; tick "$1" ) 8>"$(lock_path gitcycle)"
}

if [ "$ONCE" -eq 1 ]; then
    cycle_locked 1; rc=$?
    [ -f "$PENDING" ] && { lg "CYCLE_FAILED reason=push_still_pending"; exit 1; }
    exit "$rc"
fi

exec 9>"$(lock_path autopush)"
flock -n 9 || { lg "SKIP reason=already_running"; exit 75; }

stop=0; cpid=""; spid=""
on_term() {
    stop=1
    [ -n "$spid" ] && kill "$spid" 2>/dev/null
    if [ -n "$cpid" ]; then pkill -TERM -P "$cpid" 2>/dev/null; kill "$cpid" 2>/dev/null; fi
}
trap on_term TERM INT

lg "START ckpt=$LIVE_PT branch=$(branch_now || echo '?') push_every=$PUSH_EVERY_STEPS max_steps=$MAX_STEPS poll=${POLL_SECS}s last_pushed=$(last_pushed)"
rm -rf "$STAGE"
g config gc.auto 0 2>/dev/null   # never auto-gc ~200 MB blobs mid-training
while [ "$stop" -eq 0 ]; do
    cycle_locked 0 & cpid=$!
    wait "$cpid"; rc=$?
    cpid=""
    [ "$stop" -eq 1 ] && break
    [ "$rc" -ne 0 ] && lg "CYCLE_FAILED rc=$rc (will retry next poll)"
    sleep "$POLL_SECS" & spid=$!
    wait "$spid"
    spid=""
done
lg "STOP"
exit 143
