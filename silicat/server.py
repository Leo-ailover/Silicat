"""FastAPI chat server for Silicat.

- Loads `checkpoints/latest.pt` on startup.
- Serves the static UI at `/`.
- Streams tokens over SSE from `POST /api/chat`.
"""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import torch
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from .chat_format import Message, format_prompt
from .dataset import TOK_DIR
from .generate import stream
from .model import GPT, GPTConfig
from .tokenizer import Tokenizer


CKPT_DIR = Path("checkpoints")
STATIC_DIR = Path(__file__).parent / "static"


class APIMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[APIMessage]
    max_new_tokens: int = 256
    temperature: float = 0.9
    top_k: int = 40
    top_p: float = 0.95


def _device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


class ModelHolder:
    def __init__(self) -> None:
        self.model: GPT | None = None
        self.tok: Tokenizer | None = None
        self.cfg: GPTConfig | None = None
        self.device = _device()
        self.step = 0

    def load(self) -> None:
        ck_path = CKPT_DIR / "latest.pt"
        if not ck_path.exists():
            print(f"[warn] no checkpoint at {ck_path} — chat will return an error")
            return
        if not (TOK_DIR / "vocab.json").exists():
            print(f"[warn] no tokenizer at {TOK_DIR} — chat will return an error")
            return
        ck = torch.load(ck_path, map_location=self.device)
        self.cfg = GPTConfig(**ck["config"])
        self.model = GPT(self.cfg).to(self.device)
        self.model.load_state_dict(ck["model"])
        self.model.eval()
        self.tok = Tokenizer(TOK_DIR)
        self.step = ck.get("step", 0)
        print(
            f"loaded silicat: {self.model.num_params():,} params, "
            f"device={self.device}, step={self.step}"
        )

    @property
    def ready(self) -> bool:
        return self.model is not None and self.tok is not None


app = FastAPI(title="Silicat")
holder = ModelHolder()


@app.on_event("startup")
def _startup() -> None:
    holder.load()


@app.get("/api/health")
def health() -> dict:
    if not holder.ready:
        return {"model_loaded": False}
    assert holder.model is not None and holder.cfg is not None
    return {
        "model_loaded": True,
        "n_params": holder.model.num_params(),
        "device": holder.device,
        "step": holder.step,
        "block_size": holder.cfg.block_size,
        "vocab_size": holder.cfg.vocab_size,
    }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not holder.ready:
        async def err():
            yield {
                "event": "error",
                "data": json.dumps(
                    {
                        "message": (
                            "Silicat has no trained checkpoint yet. "
                            "Run `python -m silicat.dataset` and "
                            "`python -m silicat.train` first."
                        )
                    }
                ),
            }
        return EventSourceResponse(err())

    assert holder.model is not None and holder.tok is not None and holder.cfg is not None
    tok = holder.tok
    msgs = [Message(role=m.role, content=m.content) for m in req.messages]
    prompt_ids = format_prompt(msgs, tok)
    # leave room for max_new_tokens
    max_prompt = holder.cfg.block_size - req.max_new_tokens
    if max_prompt < 16:
        max_prompt = holder.cfg.block_size // 2
    if len(prompt_ids) > max_prompt:
        prompt_ids = prompt_ids[-max_prompt:]

    end_id = tok.special_id("<|end|>")
    user_id = tok.special_id("<|user|>")
    sil_id = tok.special_id("<|silicat|>")
    stop_ids = {end_id, user_id, sil_id}

    async def event_gen():
        buf: list[int] = []
        loop = asyncio.get_event_loop()
        gen = stream(
            holder.model,
            prompt_ids,
            max_new_tokens=req.max_new_tokens,
            temperature=req.temperature,
            top_k=req.top_k,
            top_p=req.top_p,
            stop_ids=stop_ids,
            device=holder.device,
        )

        def _next():
            try:
                return next(gen)
            except StopIteration:
                return None

        while True:
            tid = await loop.run_in_executor(None, _next)
            if tid is None:
                break
            if tid in stop_ids:
                break
            buf.append(tid)
            piece = tok.decode([tid])
            yield {"event": "token", "data": json.dumps({"text": piece})}
        yield {"event": "done", "data": json.dumps({"tokens": len(buf)})}

    return EventSourceResponse(event_gen())


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def main() -> None:
    import uvicorn

    host = os.environ.get("SILICAT_HOST", "127.0.0.1")
    port = int(os.environ.get("SILICAT_PORT", "8000"))
    uvicorn.run("silicat.server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
