"""Checkpoint I/O shared by training, export and (future) serving code.

Checkpoint dict layout (all values are tensors / plain python so that
`torch.load(weights_only=True)` works):

    model   state_dict (fp32 for live checkpoints, fp16 for exports)
    config  dataclass fields of GPTConfig / GPTConfigV3 (v3 has `n_kv_head`)
    step    number of COMPLETED optimizer steps
    optim   AdamW state_dict or None            (absent / None in fp16 exports)
    rng     {"torch": ByteTensor} or None
    arch    "v1" | "v3"
    stage   "pretrain" | "chat"   (top level, via `extra`)
    dtype   "float16" only in exports

Resumable-checkpoint resolution order (see `resolve_resumable`):
  1. full local `<name>.pt` (fp32 + optimizer)
  2. fp16 export assembled from committed parts `<name>.fp16.pt.partNN`
  3. legacy parts `<name>.pt.partNN` (assembled to `<name>.pt`)
Exports have no optimizer state: resuming from them uses a fresh optimizer but
the correct step / LR-schedule position.

Environment: SILICAT_CKPT_DIR overrides the checkpoint directory.
"""
from __future__ import annotations

import dataclasses
import os
import pickle
import time
from pathlib import Path
from typing import Any

import torch

from .assemble import ensure_assembled, list_parts

ROOT = Path(__file__).resolve().parents[1]
CKPT_DIR = Path(os.environ.get("SILICAT_CKPT_DIR", ROOT / "checkpoints"))

ARCH_KEYS = ("n_layer", "n_head", "n_kv_head", "n_embd", "vocab_size")


# ---------------------------------------------------------------- atomic I/O
def atomic_save(obj: Any, path: str | Path) -> None:
    """torch.save to `<path>.tmp`, fsync, then os.replace -> never a torn file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    try:
        with open(tmp, "wb") as f:
            torch.save(obj, f)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    try:  # make the rename itself durable
        fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        pass


def _cfg_dict(cfg: Any) -> dict:
    if dataclasses.is_dataclass(cfg):
        return dataclasses.asdict(cfg)
    return dict(cfg)


def detect_arch(config: dict) -> str:
    return "v3" if "n_kv_head" in config else "v1"


def save_checkpoint(
    path: str | Path,
    model: torch.nn.Module,
    cfg: Any,
    step: int,
    optim: torch.optim.Optimizer | None = None,
    extra: dict | None = None,
) -> None:
    config = _cfg_dict(cfg)
    obj: dict[str, Any] = {
        "model": model.state_dict(),
        "config": config,
        "step": int(step),
        "optim": optim.state_dict() if optim is not None else None,
        "rng": {"torch": torch.get_rng_state()},
        "arch": detect_arch(config),
    }
    if extra:
        obj.update(extra)
    atomic_save(obj, path)
    print(f"saved {path} (step {step})", flush=True)


def load_checkpoint(path: str | Path, map_location: str = "cpu", validate: bool = True) -> dict:
    """Safe load (`weights_only=True`). Raises on unreadable / structurally wrong files."""
    try:
        ck = torch.load(path, map_location=map_location, weights_only=True)
    except pickle.UnpicklingError as e:
        raise RuntimeError(
            f"{path}: checkpoint contains non-tensor objects; refusing to unpickle ({e})"
        ) from e
    if validate:
        if not isinstance(ck, dict) or "model" not in ck or "config" not in ck:
            raise RuntimeError(f"{path}: not a Silicat checkpoint (need 'model' and 'config')")
        ck.setdefault("arch", detect_arch(ck["config"]))  # legacy files lack it
    return ck


# ------------------------------------------------------------------- models
def build_model(config: dict, dropout: float | None = None):
    """Instantiate the right architecture from a checkpoint config dict."""
    from .model import GPT, GPTConfig
    from .model_v3 import GPTConfigV3, GPTV3

    config = dict(config)
    if dropout is not None:
        config["dropout"] = dropout
    if detect_arch(config) == "v3":
        cfg = GPTConfigV3(**config)
        return GPTV3(cfg), cfg, "v3"
    cfg = GPTConfig(**config)
    return GPT(cfg), cfg, "v1"


def state_to_fp32(sd: dict) -> dict:
    return {k: (v.float() if torch.is_tensor(v) and v.is_floating_point() else v) for k, v in sd.items()}


def load_model(path: str | Path, device: str = "cpu", dropout: float | None = None):
    """Load any checkpoint (assembling committed parts if needed).

    Returns (model, cfg, ckpt). fp16 exports are upcast to fp32. The ckpt dict
    keeps its (possibly fp16) 'model' entry for inspection."""
    path = _materialize(Path(path))
    ck = load_checkpoint(path, map_location="cpu")
    model, cfg, _ = build_model(ck["config"], dropout)
    model.load_state_dict(state_to_fp32(ck["model"]))
    return model.to(device), cfg, ck


# ------------------------------------------------------------- resolution
def export_path(name: str, ckpt_dir: Path | None = None) -> Path:
    return (ckpt_dir or CKPT_DIR) / f"{name}.fp16.pt"


def _materialize(path: Path) -> Path:
    """Return a loadable local file for `path`, assembling parts if it is missing."""
    if path.exists():
        return path
    exp = path.with_name(path.name.removesuffix(".pt") + ".fp16.pt")
    if list_parts(exp):
        return ensure_assembled(exp, refresh=True)
    return ensure_assembled(path)


def checkpoint_exists(name: str, ckpt_dir: Path | None = None) -> bool:
    d = ckpt_dir or CKPT_DIR
    p = d / f"{name}.pt"
    return p.exists() or bool(list_parts(p)) or bool(list_parts(export_path(name, d)))


def resolve_resumable(
    name: str, ckpt_dir: Path | None = None, map_location: str = "cpu"
) -> tuple[dict, Path] | None:
    """Find the best resumable checkpoint for `name` (e.g. 'latest_v3').

    Returns (ckpt, source_path) or None if NOTHING exists. If candidates exist but
    none can be read, raises RuntimeError (callers must not silently restart)."""
    d = ckpt_dir or CKPT_DIR
    local = d / f"{name}.pt"
    errors: list[str] = []

    if local.exists():
        try:
            return load_checkpoint(local, map_location), local
        except Exception as e:  # truncated / corrupt
            bad = local.with_name(local.name + ".corrupt")
            print(f"WARNING: {local} unreadable ({e}); moving to {bad}", flush=True)
            os.replace(local, bad)
            errors.append(f"{local}: {e}")

    exp = export_path(name, d)
    if list_parts(exp) or exp.exists():
        try:
            return load_checkpoint(ensure_assembled(exp, refresh=True), map_location), exp
        except Exception as e:
            errors.append(f"{exp}: {e}")
    if list_parts(local):
        try:
            return load_checkpoint(ensure_assembled(local), map_location), local
        except Exception as e:
            errors.append(f"{local} (parts): {e}")
    if errors:
        raise RuntimeError("checkpoint(s) exist but none could be loaded: " + "; ".join(errors))
    return None


def archive_existing(name: str, ckpt_dir: Path | None = None) -> Path | None:
    """Move the checkpoint, optimizer-independent exports and parts for `name`
    into `<ckpt_dir>/old/<timestamp>/` (never deletes). Used by `--fresh`."""
    d = ckpt_dir or CKPT_DIR
    victims = [p for p in (d / f"{name}.pt", export_path(name, d)) if p.exists()]
    victims += list_parts(d / f"{name}.pt") + list_parts(export_path(name, d))
    if not victims:
        return None
    dest = d / "old" / time.strftime("%Y%m%d-%H%M%S")
    dest.mkdir(parents=True, exist_ok=True)
    for p in victims:
        os.replace(p, dest / p.name)
    print(f"--fresh: moved {len(victims)} existing checkpoint file(s) to {dest}", flush=True)
    return dest
