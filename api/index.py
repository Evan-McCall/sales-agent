"""HTTP API for the Sales Assistant — the engine behind the React frontend.

A single FastAPI app, served by Vercel's Python runtime (it serves any ASGI `app`)
and runnable locally with `uvicorn api.index:app --reload`.

Endpoints:
- GET  /api/health  → readiness check
- POST /api/chat    → Server-Sent Events stream of the agent's tokens + tool steps

The agent itself lives in `agent/` and is unchanged; this module only adds transport.
"""
import json
import os
import sys

# Vercel bundles each function with its own working dir; make the repo root (one level
# up from api/) importable so `agent` and `config` resolve. Mirrors app/streamlit_app.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from agent.core import build_agent, stream_agent

app = FastAPI(title="Sales Assistant API")

# The Vite dev server runs on a different origin; allow it (and any origin, since there's
# no auth and no cookies — the API is keyed by server-side secrets, not the caller).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build the agent once per warm instance — build_agent() wires up the LLM, Pinecone, and
# Supabase clients and is far too expensive to repeat per request.
_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


def _sse(event: dict) -> str:
    """Encode one event as an SSE frame with a named event type."""
    return f"event: {event['type']}\ndata: {json.dumps(event)}\n\n"


@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/chat")
def chat(req: ChatRequest):
    if not req.messages:
        return JSONResponse({"error": "messages must not be empty"}, status_code=400)

    history = [{"role": m.role, "content": m.content} for m in req.messages]

    def event_stream():
        try:
            for event in stream_agent(get_agent(), history):
                yield _sse(event)
        except Exception as exc:  # surface a clean error to the client, not a 500 HTML page
            yield _sse({"type": "error", "message": str(exc)})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
