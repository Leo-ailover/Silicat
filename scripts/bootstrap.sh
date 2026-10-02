#!/bin/bash
# Idempotent fresh-container recovery. Safe to run any number of times, also while training is live.
#
#   bash scripts/bootstrap.sh [--dry-run] [--no-watchdog] [--no-git] [--no-pip] [--skip-data]
#
# Steps (each is skipped when already satisfied):
#   1 pip     install missing python deps (torch numpy tokenizers tqdm fastapi uvicorn sse-starlette pydantic httpx pytest)
#   2 git     make sure BRANCH (default claude/recent-conversations-visibility-YdFCm) is checked out (never when the tree
#             has tracked modifications) and fast-forward it to the remote. Never reset --hard, never force.
#   3 ckpt    verify checkpoints/latest_v3.fp16.pt.partNN against checkpoints/latest_v3.manifest.json (size + sha256 of
#             every part and of the whole), move part files the manifest does not list to checkpoints/old/, and
#             assemble checkpoints/latest_v3.fp16.pt (tmp + hash check + os.replace). train.py --resume then picks it up
#             (weights are fp16-rounded and the AdamW state restarts: the pushed export has no optimizer state).
#             A local live checkpoints/latest_v3.pt always wins over the export.
#   4 data    rebuild data/train_v2.bin + val_v2.bin (python -m silicat.dataset --v2, ~30 s) when missing/empty, when
#             their size disagrees with data/meta_v2.json, or when corpus_v2.txt changed (sha256 in meta_v2.json)
#   5 start   `nohup setsid bash scripts/watchdog.sh` (unless one is running or --no-watchdog)
#
# --dry-run only reads and prints what it would do (no pip, no git changes, no writes, no processes).
# Last line: "BOOTSTRAP ok step=N" (exit 0) or "BOOTSTRAP FAIL <reason>" (exit 1). step=0 means fresh start.
# Environment: BRANCH, REMOTE, see common.sh (SILICAT_CKPT_DIR, SILICAT_DATA_DIR, LOG_DIR, ...).

set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
TAG=bootstrap
DRY=0; DO_WD=1; DO_GIT=1; DO_PIP=1; DO_DATA=1
for a in "$@"; do
    case "$a" in
        --dry-run) DRY=1 ;;
        --no-watchdog) DO_WD=0 ;;
        --no-git) DO_GIT=0 ;;
        --no-pip) DO_PIP=0 ;;
        --skip-data) DO_DATA=0 ;;
        -h|--help) sed -n '2,/^set -uo/p' "$0" | sed '$d'; exit 0 ;;
        *) echo "unknown argument: $a" >&2; exit 2 ;;
    esac
done
DEFAULT_BRANCH="claude/recent-conversations-visibility-YdFCm"
bl() { log "$TAG" "$@"; }
fail() { echo "BOOTSTRAP FAIL $*"; exit 1; }
would() { bl "DRY-RUN would: $*"; }
g() { git -C "$REPO_DIR" "$@"; }

cd "$REPO_DIR" || fail "cannot cd $REPO_DIR"

# ---------------------------------------------------------------- 1 pip
if [ "$DO_PIP" -eq 1 ]; then
    if "$PY" -c 'import torch, numpy, tokenizers, tqdm, fastapi, uvicorn, sse_starlette, pydantic, httpx' 2>/dev/null; then
        bl "pip: dependencies present"
    elif [ "$DRY" -eq 1 ]; then
        would "pip install -r requirements.txt (without datasets) httpx pytest"
    else
        req="$(mktemp)"; grep -vi '^datasets' "$ROOT/requirements.txt" > "$req"; printf 'httpx\npytest\n' >> "$req"
        bl "pip: installing dependencies"
        "$PY" -m pip install -q -r "$req" || { rm -f "$req"; fail "pip install failed"; }
        rm -f "$req"
    fi
fi

# ---------------------------------------------------------------- 2 git
if [ "$DO_GIT" -eq 1 ]; then
    if ! g rev-parse --git-dir >/dev/null 2>&1; then
        fail "$REPO_DIR is not a git repository (clone first: git clone --branch ${BRANCH:-$DEFAULT_BRANCH} <url>)"
    fi
    want="${BRANCH:-$DEFAULT_BRANCH}"
    cur="$(g rev-parse --abbrev-ref HEAD)"
    dirty="$(g status --porcelain --untracked-files=no | head -n 1)"
    if [ "$cur" != "$want" ]; then
        if [ -n "$dirty" ]; then bl "git: on '$cur' (wanted '$want') but tracked files are modified; not switching"
        elif [ "$DRY" -eq 1 ]; then would "git checkout $want"
        else
            g fetch -q "$REMOTE" "$want" 2>&1 | tail -n 2
            if g show-ref --verify -q "refs/heads/$want"; then g checkout -q "$want" || fail "git checkout $want"
            else g checkout -q -b "$want" --track "$REMOTE/$want" || fail "git checkout -b $want"; fi
            cur="$want"; bl "git: checked out $want"
        fi
    fi
    if [ "$DRY" -eq 0 ]; then g fetch -q "$REMOTE" "$cur" 2>&1 | tail -n 2 || bl "git: fetch failed (offline?), continuing"; fi
    if g rev-parse -q --verify "refs/remotes/$REMOTE/$cur" >/dev/null; then
        read -r ahead behind < <(g rev-list --left-right --count "HEAD...$REMOTE/$cur")
        if [ "$behind" -gt 0 ] && [ "$ahead" -eq 0 ]; then
            if [ -n "$dirty" ]; then bl "git: $behind commits behind but tracked files modified; not merging"
            elif [ "$DRY" -eq 1 ]; then would "git merge --ff-only $REMOTE/$cur ($behind commits)"
            else g merge -q --ff-only "$REMOTE/$cur" || fail "git merge --ff-only"; bl "git: fast-forwarded $behind commits"; fi
        elif [ "$behind" -gt 0 ]; then bl "git: DIVERGED ahead=$ahead behind=$behind; leaving the branch alone"
        else bl "git: up to date (ahead=$ahead)"; fi
    else bl "git: no remote ref $REMOTE/$cur yet"; fi
fi

# ---------------------------------------------------------------- 3 checkpoint
verify_ckpt() {   # $1 = checkpoint name, $2 = its manifest
CK_OUT="$("$PY" - "$CKPT_DIR" "$1" "$DRY" "$2" <<'PYEOF'
import hashlib, json, os, re, sys, time
from pathlib import Path
ckdir, name, dry, mpath = Path(sys.argv[1]), sys.argv[2], sys.argv[3] == "1", Path(sys.argv[4])
exp, live = ckdir / f"{name}.fp16.pt", ckdir / f"{name}.pt"
pat = re.compile(re.escape(exp.name) + r"\.part\d+$")

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while c := f.read(1 << 22):
            h.update(c)
    return h.hexdigest()

def step_of(path):
    import torch
    try:
        ck = torch.load(path, map_location="cpu", weights_only=True, mmap=True)
    except Exception:
        ck = torch.load(path, map_location="cpu", weights_only=True)
    return int(ck["step"])

def out(msg): print(msg)
def fail(msg): print("FAIL " + msg); sys.exit(1)

ondisk = sorted(p for p in ckdir.glob(exp.name + ".part*") if pat.match(p.name))
live_step = None
if live.exists():
    try: live_step = step_of(live)
    except Exception as e: out(f"WARN live checkpoint {live.name} unreadable ({str(e)[:80]}); trainer will quarantine it")
if not mpath.exists():
    if ondisk and not live_step:
        fail(f"{len(ondisk)} parts but no manifest {mpath.name}: cannot verify them (git pull? or remove the parts)")
    if ondisk: out("WARN parts present without manifest (ignored: live checkpoint exists)")
    out(f"STEP {live_step or 0}")
    out("INFO " + ("local live checkpoint only" if live_step else "no checkpoint anywhere: fresh start"))
    sys.exit(0)
m = json.loads(mpath.read_text())
listed = [p["name"] for p in m["parts"]]
problems = []
for p in m["parts"]:
    f = ckdir / p["name"]
    if not f.exists(): problems.append(f"{p['name']} missing")
    elif f.stat().st_size != p["size"]: problems.append(f"{p['name']} size {f.stat().st_size} != {p['size']}")
    elif sha(f) != p["sha256"]: problems.append(f"{p['name']} sha256 mismatch")
extras = [p for p in ondisk if p.name not in listed]
if extras:
    msg = f"{len(extras)} stale part(s) not in manifest: " + ", ".join(p.name for p in extras)
    if dry: out("WOULD move " + msg + " to checkpoints/old/")
    else:
        dest = ckdir / "old" / ("stale-parts-" + time.strftime("%Y%m%d-%H%M%S")); dest.mkdir(parents=True, exist_ok=True)
        for p in extras: os.replace(p, dest / p.name)
        out("INFO moved " + msg + f" to {dest}")
mstep = int(m["step"])
if problems:
    if live_step is not None:
        out("WARN parts disagree with manifest (" + "; ".join(problems[:3]) + f"); live checkpoint (step {live_step}) is used, autopush regenerates parts")
        out(f"STEP {live_step}"); sys.exit(0)
    fail("checkpoint parts do not match manifest: " + "; ".join(problems[:3]) + " (try: git checkout -- checkpoints)")
if exp.exists() and sha(exp) == m["sha256"]:
    out(f"INFO export {exp.name} already matches manifest (step {mstep})")
elif dry:
    out(f"WOULD assemble {exp.name} from {len(listed)} parts (step {mstep})")
else:
    tmp = exp.with_name(exp.name + ".assembling"); h = hashlib.sha256()
    try:
        with open(tmp, "wb") as o:
            for n in listed:
                with open(ckdir / n, "rb") as f:
                    while c := f.read(1 << 22):
                        o.write(c); h.update(c)
            o.flush(); os.fsync(o.fileno())
        if h.hexdigest() != m["sha256"]: fail("assembled checkpoint hash differs from manifest")
        os.replace(tmp, exp)
    finally:
        tmp.unlink(missing_ok=True)
    out(f"INFO assembled {exp.name} ({exp.stat().st_size/1e6:.1f} MB, step {mstep})")
if live_step is not None and live_step < mstep:
    out(f"WARN pushed checkpoint (step {mstep}) is newer than live {live.name} (step {live_step}); to use it move the live file aside")
out(f"STEP {live_step if live_step is not None else mstep}")
PYEOF
)" || { echo "$CK_OUT" | sed 's/^/  /'; fail "$(echo "$CK_OUT" | grep '^FAIL ' | head -n 1 | cut -c6-)"; }
echo "$CK_OUT" | grep -v '^STEP ' | sed "s/^/[bootstrap] ckpt: /"
STEP="$(echo "$CK_OUT" | sed -n 's/^STEP //p' | tail -n 1)"
}
verify_ckpt "$CKPT_NAME" "$MANIFEST"
# the chat fine-tune (pushed by scripts/run_chat.sh) is verified/assembled too, but never drives the pretrain STEP
if [ "$CKPT_NAME" != chat_v3 ] && [ -f "$CKPT_DIR/chat_v3.manifest.json" ]; then
    PRE_STEP="$STEP"; verify_ckpt chat_v3 "$CKPT_DIR/chat_v3.manifest.json"; STEP="$PRE_STEP"
fi

# ---------------------------------------------------------------- 4 data
if [ "$DO_DATA" -eq 1 ]; then
    NEED="$("$PY" - "$DATA_DIR" <<'PYEOF'
import hashlib, json, sys
from pathlib import Path
d = Path(sys.argv[1]); tr, va, corpus, meta = d/"train_v2.bin", d/"val_v2.bin", d/"corpus_v2.txt", d/"meta_v2.json"
if not tr.exists() or not va.exists() or tr.stat().st_size == 0 or va.stat().st_size == 0:
    print("missing bins"); sys.exit()
if meta.exists():
    m = json.loads(meta.read_text())
    if m.get("n_train_tokens") is not None and tr.stat().st_size != 4 * m["n_train_tokens"]:
        print("train_v2.bin size disagrees with meta_v2.json"); sys.exit()
    if m.get("n_val_tokens") is not None and va.stat().st_size != 4 * m["n_val_tokens"]:
        print("val_v2.bin size disagrees with meta_v2.json"); sys.exit()
    if m.get("corpus_sha256") and corpus.exists():
        h = hashlib.sha256(corpus.read_bytes()).hexdigest()
        if h != m["corpus_sha256"]: print("corpus_v2.txt changed since the bins were built"); sys.exit()
PYEOF
)"
    if [ -z "$NEED" ]; then bl "data: token bins present and consistent"
    elif [ ! -s "$DATA_DIR/corpus_v2.txt" ]; then fail "data: $NEED and $DATA_DIR/corpus_v2.txt is missing (git checkout?)"
    elif [ "$DRY" -eq 1 ]; then would "python -m silicat.dataset --v2   ($NEED)"
    else
        bl "data: rebuilding bins ($NEED)"
        "$PY" -m silicat.dataset --v2 >&2 || fail "data: silicat.dataset --v2 failed"
        [ -s "$DATA_DIR/train_v2.bin" ] && [ -s "$DATA_DIR/val_v2.bin" ] || fail "data: bins still missing after build"
    fi
fi

# ---------------------------------------------------------------- 5 watchdog
if [ "$DO_WD" -eq 1 ]; then
    if is_locked watchdog; then bl "watchdog: already running"
    elif [ "$DRY" -eq 1 ]; then would "nohup setsid bash scripts/watchdog.sh >> $LOG_DIR/watchdog.log"
    else
        mkdir -p "$LOG_DIR"
        # the watchdog re-runs this script with --no-watchdog; SKIP_BOOTSTRAP avoids doing the work twice
        SKIP_BOOTSTRAP=1 nohup setsid bash "$SCRIPT_DIR/watchdog.sh" >> "$LOG_DIR/watchdog.log" 2>&1 < /dev/null &
        disown
        sleep 3
        is_locked watchdog || fail "watchdog did not stay up; see $LOG_DIR/watchdog.log"
        bl "watchdog: started"
    fi
fi

[ "$DRY" -eq 1 ] && bl "dry-run: nothing was changed"
free_gb=$(( $(df -Pk "$REPO_DIR" | awk 'NR==2{print $4}') / 1048576 ))
[ "$free_gb" -lt 6 ] && bl "WARN only ${free_gb} GB free disk"
echo "BOOTSTRAP ok step=${STEP:-0}"
