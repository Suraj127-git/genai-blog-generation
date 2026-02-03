from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class BlogStatus(str, Enum):
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class BlogTopic(str, Enum):
    TECHNOLOGY = "technology"
    HEALTH = "health"
    FINANCE = "finance"
    EDUCATION = "education"
    LIFESTYLE = "lifestyle"
    BUSINESS = "business"
    SCIENCE = "science"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"


class BlogBase(BaseModel):
    title: str
    content: str
    topic: str
    topic_category: Optional[BlogTopic] = BlogTopic.OTHER
    language: str = "english"
    metadata: Optional[Dict[str, Any]] = {}


class BlogCreate(BaseModel):
    topic: str
    language: Optional[str] = "english"
    model: Optional[str] = None
    document_ids: Optional[list[str]] = []


class BlogInDB(BlogBase):
    id: str = Field(alias="_id")
    user_id: str
    status: BlogStatus = BlogStatus.COMPLETED
    generation_time: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        use_enum_values = True


class Blog(BlogBase):
    id: str
    user_id: str
    status: BlogStatus
    generation_time: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True


class BlogHistory(BaseModel):
    blogs: list[Blog]
    total: int
    page: int
    page_size: int
