from fastapi import APIRouter, Depends
from pydantic import BaseModel, field_validator
import logging
from sqlalchemy.orm import Session
from ..router import run
from ..database import get_db
from ..models.db import Session as ChatSession, Message

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

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
        if v == "null" or v == "":
            return None
        return v
    
class ChatResponse(BaseModel):
    response: str
    intent: str
    session_id: str

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if request.session_id is None or request.session_id == "null" or request.session_id == "" or request.session_id == "Null":
        chat_session = ChatSession()
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        session_id = chat_session.id
    else:
        existing = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
        if not existing:
            chat_session = ChatSession()
            db.add(chat_session)
            db.commit()
            db.refresh(chat_session)
            session_id = chat_session.id
        else:
            session_id = request.session_id

    user_message = Message(
        session_id=session_id,
        role="user",
        content=request.message,
        intent=None
    )
    db.add(user_message)
    db.commit()

    logger.info(f"Received chat request: {request.message}")
    response, intent = run(request.message)

    assistant_message = Message(
        session_id=session_id,
        role="assistant",
        content=response,
        intent=intent
    )
    db.add(assistant_message)
    db.commit()

    logger.info(f"Returning response with intent: {intent}")
    return ChatResponse(response=response, intent=intent, session_id=session_id)