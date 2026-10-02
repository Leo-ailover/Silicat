#!/bin/bash
# End-to-end test of autopush / bootstrap / watchdog / status against a LOCAL bare repo (never the real remote).
#   bash scripts/test_infra.sh [workdir]        (~2 min on 4 CPU cores; needs data/train_v2.bin + val_v2.bin)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
W="${1:-$(mktemp -d)}"; rm -rf "$W"; mkdir -p "$W"
S="$HERE/scripts"; fails=0
ok()   { echo "  ok   $*"; }
bad()  { echo "  FAIL $*"; fails=$((fails + 1)); }
check() { local d="$1"; shift; if "$@" >/dev/null 2>&1; then ok "$d"; else bad "$d"; fi; }
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
export LOCK_DIR="$W/locks" PART_SIZE=1m PUSH_BACKOFF="1 1" POLL_SECS=1 BRANCH=tb REMOTE=origin
mkdir -p "$LOCK_DIR"

setup_clone() {  # dir
    git clone -q "$W/remote.git" "$1" 2>/dev/null; git -C "$1" checkout -q tb
    mkdir -p "$1/data"; ln -sf "$HERE/data/train_v2.bin" "$1/data/train_v2.bin"; ln -sf "$HERE/data/val_v2.bin" "$1/data/val_v2.bin"
}
env_for() { export REPO_DIR="$1" SILICAT_CKPT_DIR="$1/checkpoints" SILICAT_DATA_DIR="$1/data" LOG_DIR="$1/.logs"; mkdir -p "$LOG_DIR"; }
TRAIN_TINY="python -m silicat.train --stage pretrain --v3 --n-layer 2 --n-head 4 --n-kv-head 2 --n-embd 64 --block-size 64 --batch-size 2 --save-interval 10 --eval-interval 10 --eval-windows 4 --resume"
train_to() { (cd "$HERE" && $TRAIN_TINY --max-steps "$1" >/dev/null 2>&1); }
parts_disk() { ls "$SILICAT_CKPT_DIR" | grep -c '^latest_v3.fp16.pt.part[0-9][0-9]$'; }
parts_head() { git -C "$REPO_DIR" ls-tree -r --name-only HEAD | grep -c 'latest_v3.fp16.pt.part'; }
remote_head() { git -C "$W/remote.git" rev-parse tb; }

echo "== setup"
git init -q --bare "$W/remote.git"; git clone -q "$W/remote.git" "$W/seed" 2>/dev/null
(cd "$W/seed" && git checkout -q -b tb && cp "$HERE/.gitignore" . && mkdir -p checkpoints && cp -r "$HERE/checkpoints/tokenizer_v2" checkpoints/ && git add -A && git commit -qm init && git push -q origin tb 2>/dev/null)
setup_clone "$W/work"; env_for "$W/work"
train_to 20; check "tiny training produced live checkpoint" test -f "$SILICAT_CKPT_DIR/latest_v3.pt"
LIVE_SHA="$(sha256sum "$SILICAT_CKPT_DIR/latest_v3.pt" | cut -d' ' -f1)"

echo "== autopush --once: separate export, parts, manifest, pathspec-limited commit, push"
echo hi > "$W/work/unrelated.txt"; git -C "$W/work" add unrelated.txt
out="$(bash "$S/autopush_v3.sh" --once 2>&1)"; echo "$out" | sed 's/^/    /'
check "prints PUSHED line" grep -q 'PUSHED v3 checkpoint at step 20' <<<"$out"
check "live checkpoint untouched (sha256 equal)" test "$(sha256sum "$SILICAT_CKPT_DIR/latest_v3.pt" | cut -d' ' -f1)" = "$LIVE_SHA"
check "HEAD commit contains only parts+manifest" test -z "$(git -C "$W/work" show --name-only --format= HEAD | grep -v 'latest_v3')"
check "unrelated staged file still staged, not committed" test "$(git -C "$W/work" diff --cached --name-only)" = unrelated.txt
check "remote == local HEAD" test "$(remote_head)" = "$(git -C "$W/work" rev-parse HEAD)"
check ".last_push_v3 content is 20" test "$(cat "$W/work/.last_push_v3")" = 20
check "multiple parts (>=3) at 1m" test "$(parts_disk)" -ge 3
git -C "$W/work" commit -qm "unrelated" ; git -C "$W/work" push -q origin tb 2>/dev/null

echo "== no new checkpoint -> skip, no new commit"
h="$(git -C "$W/work" rev-parse HEAD)"; bash "$S/autopush_v3.sh" --once 2>&1 | sed 's/^/    /'
check "no commit created" test "$(git -C "$W/work" rev-parse HEAD)" = "$h"

echo "== part count shrinks -> stale parts deleted in git too"
n_before="$(parts_disk)"; train_to 40
PART_SIZE=4m bash "$S/autopush_v3.sh" --once 2>&1 | sed 's/^/    /'
check "fewer parts than before ($n_before -> $(parts_disk))" test "$(parts_disk)" -lt "$n_before"
check "parts in HEAD == parts on disk" test "$(parts_head)" = "$(parts_disk)"
check "git status clean for checkpoint paths" test -z "$(git -C "$W/work" status --porcelain -- checkpoints/latest_v3.fp16.pt.part00 checkpoints/latest_v3.manifest.json)"
check "pushed step 40" test "$(cat "$W/work/.last_push_v3")" = 40

echo "== loop mode: cadence skip, single instance, SIGTERM"
train_to 60
PUSH_EVERY_STEPS=500 MAX_STEPS=10000 bash "$S/autopush_v3.sh" >"$W/loop.log" 2>&1 & lp=$!
sleep 4
check "second instance exits 75" bash -c "bash '$S/autopush_v3.sh' >/dev/null 2>&1; test \$? -eq 75"
check "cadence skip logged" grep -q 'SKIP reason=cadence step=60' "$W/loop.log"
check "no commit for step 60" test "$(cat "$W/work/.last_push_v3")" = 40
kill -TERM "$lp"; sleep 2; check "SIGTERM stops loop" bash -c "! kill -0 $lp"
cat "$W/loop.log" | sed 's/^/    /'

echo "== push failure -> stranded commit is retried later (hook rejects, then removed)"
printf '#!/bin/sh\necho rejected-by-test >&2\nexit 1\n' > "$W/remote.git/hooks/pre-receive"; chmod +x "$W/remote.git/hooks/pre-receive"
train_to 80
PUSH_EVERY_STEPS=1 bash "$S/autopush_v3.sh" --once 2>&1 | sed 's/^/    /'
check "pending marker exists" test -f "$W/work/.pending_push_v3"
check "stamp still 40" test "$(cat "$W/work/.last_push_v3")" = 40
check "remote did not advance" test "$(remote_head)" != "$(git -C "$W/work" rev-parse HEAD)"
rm "$W/remote.git/hooks/pre-receive"
PUSH_EVERY_STEPS=500 bash "$S/autopush_v3.sh" >"$W/loop2.log" 2>&1 & lp=$!; sleep 6; kill -TERM "$lp"; sleep 1
cat "$W/loop2.log" | sed 's/^/    /'
check "next tick pushed it" test "$(remote_head)" = "$(git -C "$W/work" rev-parse HEAD)"
check "pending cleared, stamp 80" test ! -f "$W/work/.pending_push_v3" -a "$(cat "$W/work/.last_push_v3")" = 80

echo "== bootstrap on a fresh clone (container wipe)"
setup_clone "$W/fresh"; env_for "$W/fresh"; rm -f "$W/fresh/data/"*.bin; ln -sf "$HERE/data/corpus_v2.txt" "$W/fresh/data/corpus_v2.txt"
dr="$(bash "$S/bootstrap.sh" --dry-run --no-watchdog 2>&1)"; echo "$dr" | sed 's/^/    /'
check "dry-run: would assemble + rebuild bins, ends ok" bash -c 'grep -q "WOULD assemble" <<<"$0" && grep -q "would: python -m silicat.dataset" <<<"$0" && grep -q "BOOTSTRAP ok step=80" <<<"$0"' "$dr"
check "dry-run wrote nothing" test ! -e "$W/fresh/checkpoints/latest_v3.fp16.pt"
ln -sf "$HERE/data/train_v2.bin" "$W/fresh/data/train_v2.bin"; ln -sf "$HERE/data/val_v2.bin" "$W/fresh/data/val_v2.bin"
echo junk > "$W/fresh/checkpoints/latest_v3.fp16.pt.part09"
out="$(bash "$S/bootstrap.sh" --no-watchdog --no-pip --no-git 2>&1)"; echo "$out" | sed 's/^/    /'
check "BOOTSTRAP ok step=80" grep -q '^BOOTSTRAP ok step=80' <<<"$out"
check "stale part moved away" test ! -e "$W/fresh/checkpoints/latest_v3.fp16.pt.part09"
check "export sha == manifest sha" test "$(sha256sum "$W/fresh/checkpoints/latest_v3.fp16.pt" | cut -d' ' -f1)" = "$(python -c "import json;print(json.load(open('$W/fresh/checkpoints/latest_v3.manifest.json'))['sha256'])")"
out2="$(bash "$S/bootstrap.sh" --no-watchdog --no-pip --no-git 2>&1)"; check "idempotent second run" grep -q 'already matches manifest' <<<"$out2"
printf 'X' | dd of="$W/fresh/checkpoints/latest_v3.fp16.pt.part01" bs=1 seek=100 conv=notrunc 2>/dev/null
out3="$(bash "$S/bootstrap.sh" --no-watchdog --no-pip --no-git 2>&1)"; rc=$?
check "corrupt part => BOOTSTRAP FAIL, rc 1" bash -c 'test '$rc' -eq 1 && grep -q "^BOOTSTRAP FAIL.*sha256 mismatch" <<<"$0"' "$out3"
git -C "$W/fresh" checkout -q -- checkpoints; rm -f "$W/fresh/checkpoints/latest_v3.fp16.pt"
bash "$S/bootstrap.sh" --no-watchdog --no-pip --no-git >/dev/null 2>&1
echo "== resume from restored export + watchdog end-to-end (finish at step 100, final push)"
export TRAIN_CMD="$TRAIN_TINY --max-steps 100" MAX_STEPS=100 SAVE_INTERVAL=10 POLL_SECS=1 PUSH_EVERY_STEPS=500
timeout 170 bash "$S/watchdog.sh" >"$W/wd.log" 2>&1; rc=$?; sed 's/^/    /' "$W/wd.log" | cut -c1-220
check "watchdog exit 0" test "$rc" -eq 0
check "resumed from step 80" grep -q 'resumed from step 80' "$LOG_DIR/training_v3_pretrain.log"
check "TRAIN_EXIT rc=0 not restarted" grep -q 'TRAIN_EXIT rc=0' "$W/wd.log"
check "DONE + final push of step 100" bash -c 'grep -q "DONE final checkpoint pushed (step=100)" "$0"' "$W/wd.log"
check "remote has step-100 manifest" bash -c "git -C $W/remote.git show tb:checkpoints/latest_v3.manifest.json | grep -q '\"step\": 100'"

echo "== watchdog: finished run is not re-trained / re-saved after a wipe-restart"
m1="$(stat -c %Y "$SILICAT_CKPT_DIR/latest_v3.pt")"; sleep 1
timeout 100 bash "$S/watchdog.sh" >"$W/wd2.log" 2>&1; check "second launch exits 0 immediately" test $? -eq 0
check "checkpoint not rewritten" test "$(stat -c %Y "$SILICAT_CKPT_DIR/latest_v3.pt")" = "$m1"

echo "== watchdog: flag mismatch, crash loop backoff, single instance, SIGTERM"
TRAIN_CMD="python -m silicat.train --bogus-flag 1" timeout 60 bash "$S/watchdog.sh" >"$W/wd3.log" 2>&1; rc=$?
check "unknown flag aborts rc 1" bash -c "test $rc -eq 1 && grep -q 'unknown_flag=--bogus-flag' $W/wd3.log"
TRAIN_CMD="false" SKIP_BOOTSTRAP=1 BACKOFF_BASE=1 MAX_FAST_FAILS=3 timeout 60 bash "$S/watchdog.sh" >"$W/wd4.log" 2>&1; rc=$?
check "crash loop: backoff 1s,2s then GIVING_UP rc 1" bash -c "test $rc -eq 1 && grep -q 'restart_in=1s' $W/wd4.log && grep -q 'restart_in=2s' $W/wd4.log && grep -q GIVING_UP $W/wd4.log"
export TRAIN_CMD="$TRAIN_TINY --max-steps 100000" SKIP_BOOTSTRAP=1
rm -f "$SILICAT_CKPT_DIR/latest_v3.pt" "$SILICAT_CKPT_DIR"/latest_v3.fp16.pt*; git -C "$REPO_DIR" checkout -q -- checkpoints
bash "$S/watchdog.sh" >"$W/wd5.log" 2>&1 & wp=$!; sleep 12
check "second watchdog refused" bash -c "bash '$S/watchdog.sh' 2>&1 | grep -q 'already running'"
check "status.sh sees it up" bash -c "bash '$S/status.sh' | grep -q 'STATUS watchdog=up train=up autopush=up'"
kill -TERM "$wp"; wait "$wp"; rc=$?
check "SIGTERM: watchdog exits 143" test "$rc" -eq 143
check "trainer got the signal and saved" bash -c "grep -q 'finishing the current step' '$LOG_DIR/training_v3_pretrain.log'"
check "no stray trainer/autopush left" test -z "$(ps -eo args | grep -E '^(python -m silicat\.train|bash .*autopush_v3)' )"
sed 's/^/    /' "$W/wd5.log" | cut -c1-200
echo; [ "$fails" -eq 0 ] && echo "ALL INFRA TESTS PASSED" || echo "$fails INFRA TEST(S) FAILED"
exit "$fails"
