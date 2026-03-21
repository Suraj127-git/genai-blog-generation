from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from app.schemas.document import DocumentUploadResponse, DocumentListResponse, DocumentDetailResponse
from app.models.user import User
from app.models.document import DocumentType
from app.auth.dependencies import get_current_active_user
from app.database.mongodb import get_database
from app.database.chromadb import get_chroma_client
from app.services.document_service import get_document_service
from app.services.llm_service import get_llm_service
from datetime import datetime
from bson import ObjectId
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a PDF, TXT, or DOCX file"""
    db = get_database()
    chroma_client = get_chroma_client()
    document_service = get_document_service()
    
    # Validate file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    valid_extensions = {".pdf": "pdf", ".txt": "txt", ".docx": "docx"}
    
    if file_extension not in valid_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(valid_extensions.keys())}"
        )
    
    file_type = valid_extensions[file_extension]
    
    try:
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds 10MB limit"
            )
        
        # Extract text from file
        text_content = document_service.extract_text(file_content, file_type)
        
        if not text_content or len(text_content) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract meaningful text from file"
            )
        
        # Create chunks for embedding
        chunks = document_service.create_chunks(text_content)
        
        # Save document to database
        document_data = {
            "user_id": current_user.id,
            "filename": file.filename,
            "file_type": file_type,
            "file_size": file_size,
            "file_path": f"uploads/{current_user.id}/{file.filename}",  # Virtual path
            "content": text_content,
            "content_preview": document_service.get_content_preview(text_content),
            "vector_ids": [],
            "uploaded_at": datetime.utcnow()
        }
        
        result = await db.documents.insert_one(document_data)
        doc_id = str(result.inserted_id)
        
        # Store chunks in ChromaDB
        vector_ids = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            vector_id = f"{doc_id}_chunk_{i}"
            vector_ids.append(vector_id)
            metadatas.append({
                "user_id": current_user.id,
                "doc_id": doc_id,
                "filename": file.filename,
                "chunk_index": i
            })
        
        try:
            chroma_client.add_documents(
                documents=chunks,
                metadatas=metadatas,
                ids=vector_ids
            )
            
            # Update document with vector IDs
            await db.documents.update_one(
                {"_id": ObjectId(doc_id)},
                {"$set": {"vector_ids": vector_ids}}
            )
        except Exception as e:
            logger.warning(f"Error adding to ChromaDB: {e}")
            # Continue even if ChromaDB fails
        
        logger.info(f"Document uploaded: {file.filename} by user {current_user.id}")
        
        return DocumentUploadResponse(
            id=doc_id,
            filename=file.filename,
            file_type=file_type,
            file_size=file_size,
            content_preview=document_data["content_preview"],
            uploaded_at=document_data["uploaded_at"]
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing file"
        )


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    current_user: User = Depends(get_current_active_user)
):
    """List all documents for current user"""
    db = get_database()
    
    cursor = db.documents.find({"user_id": current_user.id}).sort("uploaded_at", -1)
    
    documents = []
    async for doc in cursor:
        documents.append(DocumentUploadResponse(
            id=str(doc["_id"]),
            filename=doc["filename"],
            file_type=doc["file_type"],
            file_size=doc["file_size"],
            content_preview=doc.get("content_preview"),
            uploaded_at=doc["uploaded_at"]
        ))
    
    return DocumentListResponse(
        documents=documents,
        total=len(documents)
    )


@router.get("/{doc_id}", response_model=DocumentDetailResponse)
async def get_document(
    doc_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get document details including full content"""
    db = get_database()
    
    try:
        doc = await db.documents.find_one({
            "_id": ObjectId(doc_id),
            "user_id": current_user.id
        })
        
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        return DocumentDetailResponse(
            id=str(doc["_id"]),
            filename=doc["filename"],
            file_type=doc["file_type"],
            file_size=doc["file_size"],
            content_preview=doc.get("content_preview"),
            uploaded_at=doc["uploaded_at"],
            content=doc["content"]
        )
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    doc_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a document"""
    db = get_database()
    chroma_client = get_chroma_client()
    
    try:
        # Get document to retrieve vector IDs
        doc = await db.documents.find_one({
            "_id": ObjectId(doc_id),
            "user_id": current_user.id
        })
        
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Delete from ChromaDB
        if doc.get("vector_ids"):
            try:
                chroma_client.delete_documents(doc["vector_ids"])
            except Exception as e:
                logger.warning(f"Error deleting from ChromaDB: {e}")
        
        # Delete from MongoDB
        await db.documents.delete_one({"_id": ObjectId(doc_id)})
        
        logger.info(f"Document deleted: {doc_id}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting document"
        )
