from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BlogGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=500, description="Blog topic or keywords")
    language: Optional[str] = Field(default="english", description="Target language for blog")
    model: Optional[str] = Field(default=None, description="LLM model to use")
    document_ids: Optional[list[str]] = Field(default=[], description="Document IDs to use as context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "The Future of Artificial Intelligence",
                "language": "english",
                "model": "llama-3.3-70b-versatile",
                "document_ids": []
            }
        }


class BlogResponse(BaseModel):
    id: str
    title: str
    content: str
    topic: str
    topic_category: str
    language: str
    status: str
    generation_time: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class BlogHistoryQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
    search: Optional[str] = None
    topic_category: Optional[str] = None
    sort_by: str = Field(default="created_at", description="Field to sort by")
    sort_order: str = Field(default="desc", description="Sort order: asc or desc")


class BlogHistoryResponse(BaseModel):
    blogs: list[BlogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
