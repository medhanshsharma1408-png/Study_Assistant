from fastapi import APIRouter
from pydantic import BaseModel, field_validator
import logging
from ..router import run

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str

    @field_validator("message")
    def message_must_be_valid(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("message cannot be empty")
        if len(v) > 2000:
            raise ValueError("message too long, max 2000 characters")
        return v.lower()
    
class ChatResponse(BaseModel):
    response: str
    intent: str

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info(f"Received chat request: {request.message}")
    response, intent = run(request.message)
    logger.info(f"Returning response with intent: {intent}")
    return ChatResponse(response=response, intent=intent)