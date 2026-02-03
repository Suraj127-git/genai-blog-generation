from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Session(BaseModel):
    user_id: str
    token: str
    created_at: datetime
    expires_at: datetime
    last_activity: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_active: bool = True


class SessionInDB(Session):
    id: str
    
    class Config:
        populate_by_name = True
