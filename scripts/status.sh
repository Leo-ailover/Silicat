#!/bin/bash
# One-screen health report: is training/autopush/watchdog alive, how far, what is on GitHub, disk.
#   bash scripts/status.sh [-n LINES]        exit 0 if the watchdog is up, 1 otherwise
# Last line is a grep-able summary: STATUS watchdog=up|down train=.. autopush=.. local_step=N export_step=N pushed_step=N ...

set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
N=5
[ "${1:-}" = "-n" ] && N="${2:-5}"
up() { is_locked "$1" && echo up || echo down; }

wd=$(up watchdog); tr_=$(up trainer); ap=$(up autopush)
local_step="$(ckpt_step "$LIVE_PT" 2>/dev/null)"; export_step="$(ckpt_step "$EXPORT_PT" 2>/dev/null)"
manifest_step="$(manifest_field step)"
pushed="$(cat "$PUSH_STAMP" 2>/dev/null | tr -dc 0-9)"
pending="no"; [ -f "$PENDING" ] && pending="yes($(cut -d' ' -f1 "$PENDING"))"
branch="$(git -C "$REPO_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
ahead="$(git -C "$REPO_DIR" rev-list --count "$REMOTE/$branch..HEAD" 2>/dev/null || echo '?')"

for f in "$LOG_DIR/watchdog.log" "$LOG_DIR/training_v3_pretrain.log" "$LOG_DIR/autopush_v3.log"; do
    echo "== $(basename "$f") (last $N lines)"
    if [ -f "$f" ]; then tail -n "$N" "$f" | cut -c1-200; else echo "(no such file)"; fi
done
echo "== checkpoints"
ls -lh "$LIVE_PT" "$EXPORT_PT" "$MANIFEST" 2>/dev/null | awk '{print $5, $6, $7, $8, $9}'
echo "== disk"
df -h "$REPO_DIR" | tail -n 1
du -sh "$CKPT_DIR" "$REPO_DIR/.git" 2>/dev/null
echo "STATUS watchdog=$wd train=$tr_ autopush=$ap local_step=${local_step:-none} export_step=${export_step:-none} manifest_step=${manifest_step:-none} pushed_step=${pushed:-none} push_pending=$pending commits_ahead_of_remote=$ahead branch=$branch"
[ "$wd" = up ]
