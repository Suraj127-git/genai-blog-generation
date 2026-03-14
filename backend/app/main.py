from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.database.chromadb import chroma_client
from app.routers import auth, blogs, documents, health
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting application...")
    
    # Try to connect to MongoDB but don't fail if it doesn't work
    try:
        await connect_to_mongo()
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.warning(f"MongoDB connection failed: {e}")
    
    # Try to connect to ChromaDB but don't fail if it doesn't work
    try:
        chroma_client.connect()
        logger.info("Connected to ChromaDB")
    except Exception as e:
        logger.warning(f"ChromaDB connection failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    await close_mongo_connection()


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered blog generation platform",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(blogs.router, prefix="/api/v1/blogs")
app.include_router(documents.router, prefix="/api/v1/documents")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Blog Generation API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
