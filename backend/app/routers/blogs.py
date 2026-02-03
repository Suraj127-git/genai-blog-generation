from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import StreamingResponse
from app.schemas.blog import (
    BlogGenerateRequest,
    BlogResponse,
    BlogHistoryQuery,
    BlogHistoryResponse
)
from app.models.user import User
from app.models.blog import BlogTopic, BlogStatus
from app.auth.dependencies import get_current_active_user
from app.database.mongodb import get_database
from app.services.llm_service import get_llm_service
from app.services.graph_service import get_graph_service
from app.services.export_service import get_export_service
from datetime import datetime
from bson import ObjectId
import time
import logging
import io
import math

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/blogs", tags=["blogs"])


def categorize_topic(topic: str) -> BlogTopic:
    """Categorize topic based on keywords"""
    topic_lower = topic.lower()
    
    tech_keywords = ["ai", "technology", "software", "programming", "computer", "web", "app", "code", "data"]
    health_keywords = ["health", "medical", "fitness", "wellness", "nutrition", "diet", "exercise"]
    finance_keywords = ["finance", "money", "investment", "stock", "cryptocurrency", "business", "economy"]
    education_keywords = ["education", "learning", "teaching", "school", "university", "student"]
    science_keywords = ["science", "research", "physics", "chemistry", "biology", "space"]
    
    if any(keyword in topic_lower for keyword in tech_keywords):
        return BlogTopic.TECHNOLOGY
    elif any(keyword in topic_lower for keyword in health_keywords):
        return BlogTopic.HEALTH
    elif any(keyword in topic_lower for keyword in finance_keywords):
        return BlogTopic.FINANCE
    elif any(keyword in topic_lower for keyword in education_keywords):
        return BlogTopic.EDUCATION
    elif any(keyword in topic_lower for keyword in science_keywords):
        return BlogTopic.SCIENCE
    else:
        return BlogTopic.OTHER


@router.post("/generate", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def generate_blog(
    request: BlogGenerateRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Generate a blog from topic and optional documents"""
    db = get_database()
    start_time = time.time()
    
    try:
        # Categorize topic
        topic_category = categorize_topic(request.topic)
        
        # Create LLM service
        llm_service = get_llm_service(model=request.model)
        
        # Create graph service
        graph_service = get_graph_service(llm_service)
        
        # Generate blog using LangGraph
        result = await graph_service.generate_blog(
            topic=request.topic,
            language=request.language,
            document_ids=request.document_ids
        )
        
        if result.get("error"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating blog: {result['error']}"
            )
        
        generation_time = time.time() - start_time
        
        # Save blog to database
        blog_data = {
            "user_id": current_user.id,
            "title": result["title"],
            "content": result["content"],
            "topic": request.topic,
            "topic_category": topic_category.value,
            "language": request.language,
            "status": BlogStatus.COMPLETED.value,
            "generation_time": generation_time,
            "metadata": {
                "model": request.model or "default",
                "document_ids": request.document_ids
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        blog_result = await db.blogs.insert_one(blog_data)
        blog_id = str(blog_result.inserted_id)
        
        logger.info(f"Blog generated for user {current_user.id}: {blog_id}")
        
        return BlogResponse(
            id=blog_id,
            title=result["title"],
            content=result["content"],
            topic=request.topic,
            topic_category=topic_category.value,
            language=request.language,
            status=BlogStatus.COMPLETED.value,
            generation_time=generation_time,
            created_at=blog_data["created_at"]
        )
    
    except Exception as e:
        logger.error(f"Error generating blog: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/history", response_model=BlogHistoryResponse)
async def get_blog_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    topic_category: str = Query(None),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's blog history with pagination and filtering"""
    db = get_database()
    
    # Build query
    query = {"user_id": current_user.id}
    
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"topic": {"$regex": search, "$options": "i"}}
        ]
    
    if topic_category:
        query["topic_category"] = topic_category
    
    # Get total count
    total = await db.blogs.count_documents(query)
    
    # Get paginated results
    skip = (page - 1) * page_size
    cursor = db.blogs.find(query).sort("created_at", -1).skip(skip).limit(page_size)
    
    blogs = []
    async for blog in cursor:
        blogs.append(BlogResponse(
            id=str(blog["_id"]),
            title=blog["title"],
            content=blog["content"],
            topic=blog["topic"],
            topic_category=blog["topic_category"],
            language=blog.get("language", "english"),
            status=blog.get("status", "completed"),
            generation_time=blog.get("generation_time"),
            created_at=blog["created_at"]
        ))
    
    total_pages = math.ceil(total / page_size)
    
    return BlogHistoryResponse(
        blogs=blogs,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(
    blog_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific blog"""
    db = get_database()
    
    try:
        blog = await db.blogs.find_one({
            "_id": ObjectId(blog_id),
            "user_id": current_user.id
        })
        
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog not found"
            )
        
        return BlogResponse(
            id=str(blog["_id"]),
            title=blog["title"],
            content=blog["content"],
            topic=blog["topic"],
            topic_category=blog["topic_category"],
            language=blog.get("language", "english"),
            status=blog.get("status", "completed"),
            generation_time=blog.get("generation_time"),
            created_at=blog["created_at"]
        )
    except Exception as e:
        logger.error(f"Error getting blog: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a blog"""
    db = get_database()
    
    try:
        result = await db.blogs.delete_one({
            "_id": ObjectId(blog_id),
            "user_id": current_user.id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog not found"
            )
        
        logger.info(f"Blog deleted: {blog_id}")
    except Exception as e:
        logger.error(f"Error deleting blog: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )


@router.get("/{blog_id}/download/{format}")
async def download_blog(
    blog_id: str,
    format: str,
    current_user: User = Depends(get_current_active_user)
):
    """Download blog as PDF or DOCX"""
    if format not in ["pdf", "docx"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format. Use 'pdf' or 'docx'"
        )
    
    db = get_database()
    
    try:
        blog = await db.blogs.find_one({
            "_id": ObjectId(blog_id),
            "user_id": current_user.id
        })
        
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog not found"
            )
        
        export_service = get_export_service()
        
        if format == "pdf":
            file_bytes = export_service.export_to_pdf(
                title=blog["title"],
                content=blog["content"],
                topic=blog["topic"]
            )
            media_type = "application/pdf"
            filename = f"{blog['title'][:50]}.pdf"
        else:  # docx
            file_bytes = export_service.export_to_docx(
                title=blog["title"],
                content=blog["content"],
                topic=blog["topic"]
            )
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"{blog['title'][:50]}.docx"
        
        # Create streaming response
        return StreamingResponse(
            io.BytesIO(file_bytes),
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except Exception as e:
        logger.error(f"Error downloading blog: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating download"
        )
