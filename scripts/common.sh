# Shared helpers for the Silicat ops scripts (sourced, not executed).
#
# Environment (all optional):
#   REPO_DIR            git working tree to commit/push from (default: this repo)
#   SILICAT_CKPT_DIR    checkpoint dir, must live inside REPO_DIR (default: <repo>/checkpoints)
#   SILICAT_DATA_DIR    data dir (default: <repo>/data)
#   LOG_DIR             where *.log files go (default: <repo>)
#   LOCK_DIR            where lock files go (default: /tmp)
#   CKPT_NAME           checkpoint base name (default: latest_v3)
#   PYTHON              interpreter (default: python)
#   REMOTE              git remote (default: origin)
#   BRANCH              git branch to push (default: the branch currently checked out)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$(cd "${REPO_DIR:-$ROOT}" && pwd)"
CKPT_DIR="${SILICAT_CKPT_DIR:-$ROOT/checkpoints}"
DATA_DIR="${SILICAT_DATA_DIR:-$ROOT/data}"
LOG_DIR="${LOG_DIR:-$ROOT}"
LOCK_DIR="${LOCK_DIR:-/tmp}"
CKPT_NAME="${CKPT_NAME:-latest_v3}"
PY="${PYTHON:-python}"
REMOTE="${REMOTE:-origin}"
EXPORT_PT="$CKPT_DIR/$CKPT_NAME.fp16.pt"       # derived fp16 export (gitignored)
MANIFEST="$CKPT_DIR/${CKPT_NAME%%.*}.manifest.json"
LIVE_PT="$CKPT_DIR/$CKPT_NAME.pt"              # live fp32 + optimizer (trainer-owned)
PUSH_STAMP="$REPO_DIR/.last_push_${CKPT_NAME#latest_}"   # content = last pushed step
PENDING="$REPO_DIR/.pending_push_${CKPT_NAME#latest_}"   # "<step> <sha>" committed but not pushed
export SILICAT_CKPT_DIR="$CKPT_DIR" SILICAT_DATA_DIR="$DATA_DIR"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

# Key that makes lock names unique per (repo, checkpoint dir) so tests never collide with a real run.
LOCK_KEY="$(printf '%s:%s' "$REPO_DIR" "$CKPT_DIR" | sha1sum | cut -c1-8)"
lock_path() { printf '%s/silicat-%s.%s.lock' "$LOCK_DIR" "$LOCK_KEY" "$1"; }

ts() { date -u +%FT%TZ; }
# log TAG message...   -> "[tag] 2026-.. message"
log() { local tag="$1"; shift; printf '[%s] %s %s\n' "$tag" "$(ts)" "$*"; }

# ckpt_step FILE -> prints the completed-step count of a checkpoint (mmap, cheap), rc!=0 if unreadable
ckpt_step() {
    "$PY" - "$1" <<'PYEOF' 2>/dev/null
import sys, torch
try:
    ck = torch.load(sys.argv[1], map_location="cpu", weights_only=True, mmap=True)
except Exception:
    ck = torch.load(sys.argv[1], map_location="cpu", weights_only=True)
print(int(ck["step"]))
PYEOF
}

# manifest_field KEY -> value of a top-level key of the manifest (empty if missing)
manifest_field() {
    [ -f "$MANIFEST" ] || return 0
    "$PY" -c 'import json,sys; v=json.load(open(sys.argv[1])).get(sys.argv[2]); print("" if v is None else v)' "$MANIFEST" "$1" 2>/dev/null
}

# is_locked NAME -> 0 if some process currently holds the lock
is_locked() {
    local lp; lp="$(lock_path "$1")"
    [ -e "$lp" ] || return 1
    ! flock -n "$lp" true 2>/dev/null
}
