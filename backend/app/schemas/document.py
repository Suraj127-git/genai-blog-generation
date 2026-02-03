from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    content_preview: Optional[str] = None
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    documents: list[DocumentUploadResponse]
    total: int


class DocumentDetailResponse(DocumentUploadResponse):
    content: str
