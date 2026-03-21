from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.db import Session as ChatSession, Message

router = APIRouter()

@router.get("/history/{session_id}")
def get_history(session_id: str, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = [
        {
            "role": m.role,
            "content": m.content,
            "intent": m.intent,
            "timestamp": m.timestamp.isoformat()
        }
        for m in session.messages
    ]

    return {"session_id": session_id, "messages": messages}

@router.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    return [
        {
            "session_id": s.id,
            "created_at": s.created_at.isoformat(),
            "message_count": len(s.messages)
        }
        for s in sessions
    ]