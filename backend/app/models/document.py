from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    PDF = "pdf"
    TXT = "txt"
    DOCX = "docx"


class DocumentBase(BaseModel):
    filename: str
    file_type: DocumentType
    file_size: int
    content_preview: Optional[str] = None


class DocumentCreate(BaseModel):
    filename: str
    file_type: DocumentType
    file_size: int
    content: str


class DocumentInDB(DocumentBase):
    id: str = Field(alias="_id")
    user_id: str
    file_path: str  # S3 or local path
    content: str  # Full text content
    vector_ids: list[str] = []  # ChromaDB IDs
    uploaded_at: datetime
    
    class Config:
        populate_by_name = True
        use_enum_values = True


class Document(DocumentBase):
    id: str
    user_id: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True


class DocumentList(BaseModel):
    documents: list[Document]
    total: int
