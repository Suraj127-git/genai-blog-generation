from datetime import datetime, timedelta
from app.database.mongodb import get_database
from app.models.session import Session
from bson import ObjectId
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class SessionService:
    @staticmethod
    async def create_session(
        user_id: str,
        token: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Session:
        """Create a new session"""
        db = get_database()
        
        session = {
            "user_id": user_id,
            "token": token,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=7),
            "last_activity": datetime.utcnow(),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "is_active": True
        }
        
        result = await db.sessions.insert_one(session)
        session["_id"] = result.inserted_id
        
        logger.info(f"Created session for user: {user_id}")
        return Session(**session, id=str(result.inserted_id))
    
    @staticmethod
    async def get_session_by_token(token: str) -> Optional[Session]:
        """Get session by token"""
        db = get_database()
        session = await db.sessions.find_one({"token": token, "is_active": True})
        
        if not session:
            return None
        
        # Check if expired
        if session["expires_at"] < datetime.utcnow():
            await SessionService.invalidate_session(token)
            return None
        
        # Update last activity
        await db.sessions.update_one(
            {"_id": session["_id"]},
            {"$set": {"last_activity": datetime.utcnow()}}
        )
        
        return Session(**session, id=str(session["_id"]))
    
    @staticmethod
    async def invalidate_session(token: str):
        """Invalidate a session"""
        db = get_database()
        await db.sessions.update_one(
            {"token": token},
            {"$set": {"is_active": False}}
        )
        logger.info("Session invalidated")
    
    @staticmethod
    async def invalidate_user_sessions(user_id: str):
        """Invalidate all sessions for a user"""
        db = get_database()
        await db.sessions.update_many(
            {"user_id": user_id},
            {"$set": {"is_active": False}}
        )
        logger.info(f"Invalidated all sessions for user: {user_id}")
    
    @staticmethod
    async def cleanup_expired_sessions():
        """Clean up expired sessions"""
        db = get_database()
        result = await db.sessions.delete_many({
            "expires_at": {"$lt": datetime.utcnow()}
        })
        logger.info(f"Cleaned up {result.deleted_count} expired sessions")


def get_session_service() -> SessionService:
    """Get session service instance"""
    return SessionService()
