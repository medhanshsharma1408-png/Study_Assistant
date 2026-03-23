from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .routes import chat,history

logging.basicConfig(
    filename="assistant.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="Study Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(history.router, prefix="/api/v1", tags=["history"])