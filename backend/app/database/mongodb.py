from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Connect to MongoDB"""
    try:
        mongodb.client = AsyncIOMotorClient(settings.mongodb_url)
        mongodb.db = mongodb.client[settings.mongodb_db_name]
        
        # Test connection
        await mongodb.client.admin.command('ping')
        logger.info(f"Connected to MongoDB: {settings.mongodb_db_name}")
        
        # Create indexes
        await create_indexes()
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    if mongodb.client:
        mongodb.client.close()
        logger.info("Closed MongoDB connection")


async def create_indexes():
    """Create database indexes"""
    # Users collection indexes
    await mongodb.db.users.create_index("email", unique=True)
    await mongodb.db.users.create_index("username", unique=True)
    
    # Blogs collection indexes
    await mongodb.db.blogs.create_index("user_id")
    await mongodb.db.blogs.create_index("created_at")
    await mongodb.db.blogs.create_index([("user_id", 1), ("created_at", -1)])
    
    # Documents collection indexes
    await mongodb.db.documents.create_index("user_id")
    await mongodb.db.documents.create_index("filename")
    
    # Sessions collection indexes
    await mongodb.db.sessions.create_index("user_id")
    await mongodb.db.sessions.create_index("token", unique=True)
    await mongodb.db.sessions.create_index("expires_at", expireAfterSeconds=0)
    
    logger.info("Database indexes created")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return mongodb.db
