from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "Service is running"}
