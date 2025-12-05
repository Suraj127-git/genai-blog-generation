from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    provider: str
    model: str
    usecase: str
    message: str
    embedding_model: Optional[str] = "nomic-embed-text"

class ChatResponse(BaseModel):
    content: str
    from_cache: bool = False

class NewsRequest(BaseModel):
    timeframe: str
    embedding_model: Optional[str] = "nomic-embed-text"

class NewsResponse(BaseModel):
    summary: str
    saved_file: Optional[str] = None
    from_cache: bool = False
