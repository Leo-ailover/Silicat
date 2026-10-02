"""FastAPI chat server for Silicat.

- Loads the best available checkpoint on startup (chat v3 > pretrain v3 > v2 > v1;
  override with SILICAT_CKPT or `python -m silicat serve --ckpt`).
- Serves the static UI at `/`.
- Streams tokens over SSE from `POST /api/chat` (or one JSON object with
  `"stream": false`). Generation is serialised: one request at a time, a short
  bounded queue, 429 beyond it.
- `GET /api/health` reports load state, arch/stage/step/params/device and limits.

Environment: SILICAT_HOST, SILICAT_PORT, SILICAT_CKPT, SILICAT_MAX_BODY (bytes,
default 262144), SILICAT_MAX_CONCURRENCY (1), SILICAT_MAX_QUEUE (4),
SILICAT_ALLOWED_HOSTS (comma list), SILICAT_API_KEY (optional bearer token for
/api/chat).
"""
from __future__ import annotations

import asyncio
import hmac
import json
import os
import threading
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, model_validator
from sse_starlette.sse import EventSourceResponse
from starlette.background import BackgroundTask
from starlette.middleware.trustedhost import TrustedHostMiddleware

from . import checkpoint as ckpt_mod
from .chat_format import Message, fit_prompt
from .generate import Engine, IncrementalDecoder, load_engine, pick_device, stream

CKPT_DIR = ckpt_mod.CKPT_DIR
STATIC_DIR = Path(__file__).parent / "static"
MIN_REPLY = 64  # tokens always reserved for the reply when budgeting the prompt


class APIMessage(BaseModel):
    role: Literal["user", "silicat", "assistant"]
    content: str = Field(max_length=32_000)


class ChatRequest(BaseModel):
    messages: list[APIMessage] = Field(min_length=1, max_length=64)
    max_new_tokens: int = Field(256, ge=1, le=4096)
    temperature: float = Field(0.9, ge=0, le=5, allow_inf_nan=False)
    top_k: int = Field(40, ge=0, le=100_000)
    top_p: float = Field(0.95, ge=0, le=1, allow_inf_nan=False)
    repetition_penalty: float = Field(1.0, ge=1, le=2, allow_inf_nan=False)
    no_repeat_ngram: int = Field(0, ge=0, le=16)
    seed: int | None = Field(None, ge=0, le=2**31 - 1)
    stream: bool = True

    @model_validator(mode="after")
    def _last_is_user(self) -> "ChatRequest":
        if self.messages[-1].role != "user":
            raise ValueError("the last message must have role 'user'")
        return self


class ModelHolder:
    """Holds the loaded engine (or the reason it failed to load)."""

    def __init__(self, ckpt_path: str | os.PathLike | None = None, device: str | None = None) -> None:
        self.ckpt_path = ckpt_path
        self.device = device or pick_device()
        self.engine: Engine | None = None
        self.error: str | None = None

    def load(self) -> None:
        try:
            self.engine = load_engine(self.ckpt_path, self.device)
            self.error = None
            e = self.engine
            print(
                f"loaded silicat {e.arch}/{e.stage}: {e.model.num_params():,} params, "
                f"step={e.step}, device={e.device}, file={e.path.name}"
            )
            if e.arch == "v1":
                print("[warn] serving a v1/v2 (GPT) checkpoint; no v3 checkpoint was found")
        except Exception as ex:  # surfaced via /api/health and chat errors
            self.engine = None
            self.error = f"{type(ex).__name__}: {ex}"
            print(f"[warn] model not loaded: {self.error}")

    @property
    def ready(self) -> bool:
        return self.engine is not None

    # convenience accessors (kept for older callers)
    @property
    def model(self):
        return self.engine.model if self.engine else None

    @property
    def tok(self):
        return self.engine.tok if self.engine else None

    @property
    def cfg(self):
        return self.engine.cfg if self.engine else None

    @property
    def step(self) -> int:
        return self.engine.step if self.engine else 0


class BodyLimit:
    """Pure-ASGI request body cap (also counts chunked bodies)."""

    def __init__(self, app, max_bytes: int) -> None:
        self.app, self.max = app, max_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope["headers"])
        cl = headers.get(b"content-length")
        too_big = JSONResponse({"detail": "request body too large"}, status_code=413)
        if cl and cl.isdigit() and int(cl) > self.max:
            return await too_big(scope, receive, send)
        seen = 0

        async def limited_receive():
            nonlocal seen
            msg = await receive()
            if msg["type"] == "http.request":
                seen += len(msg.get("body", b""))
                if seen > self.max:
                    raise _TooLarge()
            return msg

        try:
            await self.app(scope, limited_receive, send)
        except _TooLarge:
            await too_big(scope, receive, send)


class _TooLarge(Exception):
    pass


def _loopback(host: str) -> bool:
    return host in ("127.0.0.1", "localhost", "::1")


def create_app(
    ckpt_path: str | os.PathLike | None = None,
    device: str | None = None,
    holder: ModelHolder | None = None,
    load: bool = True,
) -> FastAPI:
    """Build the app. `holder` may be pre-filled (tests); `load=False` skips loading."""
    holder = holder or ModelHolder(ckpt_path, device)
    max_conc = max(1, int(os.environ.get("SILICAT_MAX_CONCURRENCY", "1")))
    max_queue = max(0, int(os.environ.get("SILICAT_MAX_QUEUE", "4")))
    api_key = os.environ.get("SILICAT_API_KEY") or None

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if load and not holder.ready:
            await asyncio.to_thread(holder.load)
        yield

    app = FastAPI(title="Silicat", lifespan=lifespan)
    app.state.holder = holder

    @app.exception_handler(RequestValidationError)
    async def _bad_request(request: Request, exc: RequestValidationError):
        # the default handler echoes the offending input, which breaks on NaN/inf
        errs = [{"loc": list(e.get("loc", ())), "msg": str(e.get("msg", ""))} for e in exc.errors()]
        return JSONResponse({"detail": errs}, status_code=422)
    sem = asyncio.Semaphore(max_conc)
    counter = {"n": 0}  # admitted (running + waiting) requests

    @app.get("/api/health")
    def health() -> dict:
        base = {"model_loaded": holder.ready, "error": holder.error, "auth_required": bool(api_key)}
        if not holder.ready:
            return base
        e = holder.engine
        return {**base, **e.info(), "max_new_tokens": e.cfg.block_size - 16}

    def _check_auth(request: Request) -> None:
        if not api_key:
            return
        got = request.headers.get("authorization", "")
        want = f"Bearer {api_key}"
        if not hmac.compare_digest(got.encode(), want.encode()):
            raise HTTPException(401, "missing or invalid API key", headers={"WWW-Authenticate": "Bearer"})

    @app.post("/api/chat")
    async def chat(req: ChatRequest, request: Request):
        _check_auth(request)
        if not holder.ready:
            raise HTTPException(503, holder.error or "model not loaded")
        e = holder.engine
        block = e.cfg.block_size
        if counter["n"] >= max_conc + max_queue:
            return JSONResponse(
                {"detail": "server busy, try again shortly"}, status_code=429,
                headers={"Retry-After": "5"},
            )
        counter["n"] += 1
        released = threading.Event()

        def release() -> None:
            if not released.is_set():
                released.set()
                counter["n"] -= 1

        try:
            # tail of each message only: tokenising 100k chars to discard them is wasteful
            msgs = [
                Message(role="silicat" if m.role == "assistant" else m.role, content=m.content[-block * 8:])
                for m in req.messages
            ]
            want_new = min(req.max_new_tokens, block - 16)
            max_prompt = min(max(16, block - min(want_new, block // 2)), block - min(MIN_REPLY, block // 4))
            prompt_ids, truncated = await asyncio.to_thread(fit_prompt, msgs, e.tok, max_prompt)
        except BaseException:
            release()
            raise
        budget = max(1, min(want_new, block - len(prompt_ids)))
        tok = e.tok
        stop_ids = {tok.special_id(t) for t in ("<|end|>", "<|user|>", "<|silicat|>")}
        kw = dict(
            max_new_tokens=budget, temperature=req.temperature, top_k=req.top_k, top_p=req.top_p,
            repetition_penalty=req.repetition_penalty, no_repeat_ngram=req.no_repeat_ngram,
            stop_ids=stop_ids, seed=req.seed,
        )

        async def run():
            """Yield ('tok', id) ... then ('end', info) or ('err', msg). One generation at a time."""
            loop = asyncio.get_running_loop()
            q: asyncio.Queue = asyncio.Queue()
            halt = threading.Event()
            info: dict = {}

            def work() -> None:
                try:
                    for tid in stream(e.model, prompt_ids, info=info, device=e.device, **kw):
                        if halt.is_set():
                            return
                        loop.call_soon_threadsafe(q.put_nowait, ("tok", tid))
                    loop.call_soon_threadsafe(q.put_nowait, ("end", info))
                except Exception as ex:
                    loop.call_soon_threadsafe(q.put_nowait, ("err", f"{type(ex).__name__}: {ex}"))

            async with sem:
                fut = loop.run_in_executor(None, work)
                try:
                    while True:
                        kind, val = await q.get()
                        yield kind, val
                        if kind != "tok":
                            break
                finally:
                    halt.set()
                    try:  # worker exits after its current token; keep the slot until then
                        await asyncio.shield(fut)
                    except BaseException:
                        pass

        def done_payload(n: int, info: dict, reason: str | None = None) -> dict:
            return {
                "tokens": n, "prompt_tokens": len(prompt_ids), "truncated": truncated,
                "finish_reason": reason or info.get("finish_reason", "length"),
            }

        if not req.stream:
            try:
                ids: list[int] = []
                final: dict = {}
                async for kind, val in run():
                    if kind == "tok":
                        ids.append(val)
                    elif kind == "err":
                        raise HTTPException(500, val)
                    else:
                        final = val
                dec = IncrementalDecoder(tok)
                text = "".join(dec.push(t) for t in ids) + dec.flush()
                return {"text": text, **done_payload(len(ids), final)}
            finally:
                release()

        async def event_gen():
            dec = IncrementalDecoder(tok)
            n = 0
            try:
                async for kind, val in run():
                    if kind == "tok":
                        n += 1
                        piece = dec.push(val)
                        if piece:
                            yield {"event": "token", "data": json.dumps({"text": piece})}
                    elif kind == "err":
                        yield {"event": "error", "data": json.dumps({"message": val})}
                        yield {"event": "done", "data": json.dumps(done_payload(n, {}, "error"))}
                        return
                    else:
                        rest = dec.flush()
                        if rest:
                            yield {"event": "token", "data": json.dumps({"text": rest})}
                        yield {"event": "done", "data": json.dumps(done_payload(n, val))}
            finally:
                release()

        return EventSourceResponse(event_gen(), background=BackgroundTask(release))

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    bind = os.environ.get("SILICAT_HOST", "127.0.0.1")
    hosts = os.environ.get("SILICAT_ALLOWED_HOSTS")
    if hosts:
        allowed = [h.strip() for h in hosts.split(",") if h.strip()]
    elif _loopback(bind):
        allowed = ["localhost", "127.0.0.1", "[::1]", "testserver"]
    else:
        allowed = ["*"]  # remote bind: Host is the LAN name; rely on SILICAT_API_KEY
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed)
    app.add_middleware(BodyLimit, max_bytes=int(os.environ.get("SILICAT_MAX_BODY", "262144")))
    return app


app = create_app()


def main(host: str | None = None, port: int | None = None, ckpt: str | None = None) -> None:
    import uvicorn

    host = host or os.environ.get("SILICAT_HOST", "127.0.0.1")
    port = port or int(os.environ.get("SILICAT_PORT", "8000"))
    if ckpt:
        os.environ["SILICAT_CKPT"] = ckpt
    if not _loopback(host) and not os.environ.get("SILICAT_API_KEY"):
        print(
            f"[WARNING] binding to {host} with no SILICAT_API_KEY: anyone who can reach "
            "this port can use the model. Set SILICAT_API_KEY.", flush=True,
        )
    os.environ["SILICAT_HOST"] = host  # picked up by create_app (allowed hosts)
    uvicorn.run(create_app(), host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
