"""End-to-end CLI runs on a temp bin with a ~100k-param model (each run is a few seconds)."""
import json
import subprocess
import sys

import torch

from silicat import checkpoint as C

PRE = ["--stage", "pretrain", "--v3", "--n-layer", "2", "--n-head", "4", "--n-kv-head", "2", "--n-embd", "32",
       "--block-size", "32", "--batch-size", "2", "--eval-windows", "4", "--device", "cpu", "--precision", "fp32",
       "--log-interval", "1", "--eval-interval", "1000"]


def run(env, *args, ok=True):
    r = subprocess.run([sys.executable, "-m", "silicat.train", *args], env=env, capture_output=True, text=True, timeout=300)
    assert (r.returncode == 0) == ok, r.stdout[-1500:] + r.stderr[-1500:]
    return r.stdout + r.stderr


def test_pretrain_resume_with_optimizer_then_guards(tiny_env):
    env, ck, _ = tiny_env
    out = run(env, *PRE, "--max-steps", "5", "--save-interval", "2")
    assert "saved" in out
    live = C.load_checkpoint(ck / "latest_v3.pt")
    assert live["step"] == 5 and live["stage"] == "pretrain" and live["optim"]["state"]
    losses = [json.loads(line) for line in (ck / "metrics_latest_v3.jsonl").read_text().splitlines()]
    assert all(torch.isfinite(torch.tensor(r["loss"])) for r in losses if "loss" in r)

    out = run(env, *PRE, "--max-steps", "8", "--resume", "--save-interval", "2")
    assert "optimizer state restored" in out and "resumed from step 5" in out
    assert C.load_checkpoint(ck / "latest_v3.pt")["step"] == 8

    # re-running without --resume must not clobber an existing run
    out = run(env, *PRE, "--max-steps", "8", ok=False)
    assert "--resume" in out and "--fresh" in out
    # finished run: nothing to do, still exit 0 (the watchdog treats 0 as "finished")
    assert "nothing to do" in run(env, *PRE, "--max-steps", "8", "--resume")


def test_resume_from_fp16_parts_after_wipe(tiny_env):
    from silicat.assemble import split_checkpoint
    from silicat.halve import export

    env, ck, _ = tiny_env
    run(env, *PRE, "--max-steps", "3", "--save-interval", "3")
    exp = ck / "latest_v3.fp16.pt"
    export(ck / "latest_v3.pt", exp)
    split_checkpoint(exp, part_bytes=30_000)
    for f in (ck / "latest_v3.pt", exp):
        f.unlink()
    out = run(env, *PRE, "--max-steps", "5", "--resume", "--rewarmup", "2")
    assert "resumed from step 3" in out and "NO optimizer state" in out


def test_chat_stage_end_to_end_keeps_pretrain_checkpoint(tiny_env, tmp_path):
    env, ck, data = tiny_env
    run(env, *PRE, "--max-steps", "2", "--save-interval", "2")
    before = (ck / "latest_v3.pt").read_bytes()
    rows = [{"messages": [{"role": "user", "content": f"say number {i}"},
                          {"role": "silicat", "content": f"```python\nprint({i})\n```"}]} for i in range(16)]
    train, ev = data / "chat_train.jsonl", data / "chat_eval.jsonl"
    train.write_text("\n".join(json.dumps(r) for r in rows[:12]) + "\n")
    ev.write_text("\n".join(json.dumps(r) for r in rows[12:]) + "\n")
    out = run(env, "--stage", "chat", "--v3", "--device", "cpu", "--precision", "fp32", "--batch-size", "4",
              "--chat-data", str(train), "--chat-eval-data", str(ev), "--max-steps", "3", "--eval-interval", "2",
              "--log-interval", "1", "--warmup", "1")
    assert "held-out eval file" in out
    final = C.load_checkpoint(ck / "chat_v3.pt")
    assert final["stage"] == "chat" and final["pretrain_step"] == 2
    assert (ck / "latest_v3.pt").read_bytes() == before  # pretrain weights untouched
    # a chat model must be refused as a pretrain resume source / chat base
    (ck / "latest_v3.pt").unlink()
    (ck / "chat_v3.pt").rename(ck / "latest_v3.pt")
    out = run(env, *PRE, "--max-steps", "4", "--resume", ok=False)
    assert "chat weights" in out
