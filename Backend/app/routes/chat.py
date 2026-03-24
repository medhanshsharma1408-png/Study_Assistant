from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, field_validator
import logging
import time
from collections import defaultdict
from sqlalchemy.orm import Session
from ..router import run
from ..database import get_db
from ..models.db import Session as ChatSession, Message
from typing import Optional
from app.main import limiter

logger = logging.getLogger(__name__)
router = APIRouter()

# ---------------------------------------------------------------------------
# Simple in-process rate limiter
# Tracks (ip, endpoint) → list of request timestamps in the current window.
# This is intentionally lightweight — no Redis needed for a personal project.
# ---------------------------------------------------------------------------
_rate_store: dict[str, list[float]] = defaultdict(list)

RATE_LIMIT_REQUESTS = 20       # max requests per window
RATE_LIMIT_WINDOW   = 60       # window size in seconds


def _check_rate_limit(key: str):
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    timestamps = _rate_store[key]

    # Drop timestamps outside the current window
    _rate_store[key] = [t for t in timestamps if t > window_start]

    if len(_rate_store[key]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW}s.",
        )
    _rate_store[key].append(now)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
HISTORY_LIMIT = 6   # number of recent messages to feed into the LLM as context


def _get_recent_history(db: Session, session_id: str) -> list[dict]:
    """Return the last HISTORY_LIMIT messages for a session, oldest first."""
    msgs = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.timestamp.desc())
        .limit(HISTORY_LIMIT)
        .all()
    )
    # Reverse so oldest → newest (correct conversation order for the LLM)
    return [{"role": m.role, "content": m.content} for m in reversed(msgs)]


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

    @field_validator("message")
    def message_must_be_valid(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("message cannot be empty")
        if len(v) > 2000:
            raise ValueError("message too long, max 2000 characters")
        return v.lower()

    @field_validator("session_id")
    def clean_session_id(cls, v):
        if v in (None, "null", "", "Null"):
            return None
        return v


class ChatResponse(BaseModel):
    response: str
    intent: str
    session_id: str


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------
@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
def chat(request_body: ChatRequest, request: Request, db: Session = Depends(get_db)):
    # --- Rate limiting (keyed by IP) ---
    client_ip = request.client.host if request.client else "unknown"
    _check_rate_limit(f"chat:{client_ip}")

    # --- Session resolution ---
    session_id = request_body.session_id
    if session_id in (None, "null", "", "Null") or not db.query(ChatSession).filter(ChatSession.id == session_id).first():
        chat_session = ChatSession()
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        session_id = chat_session.id
    
    # --- Fetch recent conversation history BEFORE saving the new user message ---
    history = _get_recent_history(db, session_id)

    # --- Persist user message ---
    user_message = Message(
        session_id=session_id,
        role="user",
        content=request_body.message,
        intent=None,
    )
    db.add(user_message)
    db.commit()

    logger.info(f"Received chat request: {request_body.message} | session: {session_id}")

    # --- Call the router / LLM ---
    response, intent = run(request_body.message, history=history)

    # --- Persist assistant message ---
    assistant_message = Message(
        session_id=session_id,
        role="assistant",
        content=response,
        intent=intent,
    )
    db.add(assistant_message)
    db.commit()

    logger.info(f"Returning response with intent: {intent}")
    return ChatResponse(response=response, intent=intent, session_id=session_id)