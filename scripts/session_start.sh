#!/bin/bash
# SessionStart hook (.claude/settings.json): auto-resume training after a container restart/wipe.
# Runs scripts/bootstrap.sh fully detached so the session starts instantly; bootstrap is idempotent and
# the watchdog's flock makes a second start a no-op, so this is safe on every session start.
# Opt out with SILICAT_NO_AUTOSTART=1. Log: .logs/session_start.log
[ "${SILICAT_NO_AUTOSTART:-0}" = 1 ] && exit 0
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 0
mkdir -p .logs
nohup setsid bash scripts/bootstrap.sh >> .logs/session_start.log 2>&1 < /dev/null &
echo "silicat: bootstrap started in background (training auto-resume; log .logs/session_start.log)"
exit 0
