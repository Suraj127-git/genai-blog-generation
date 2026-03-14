from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserProfile
from app.models.user import UserCreate, User, get_password_hash, verify_password
from app.auth.jwt import create_access_token
from app.auth.dependencies import get_current_active_user
from app.database.mongodb import get_database
from app.services.session_service import SessionService
from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, req: Request):
    """Register a new user"""
    db = get_database()
    
    # Check if email already exists
    existing_user = await db.users.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = await db.users.find_one({"username": request.username})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    hashed_password = get_password_hash(request.password)
    user_data = {
        "email": request.email,
        "username": request.username,
        "full_name": request.full_name,
        "hashed_password": hashed_password,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_data)
    user_id = str(result.inserted_id)
    
    # Create access token
    access_token = create_access_token(data={"sub": user_id})
    
    # Create session
    ip_address = req.client.host if req.client else None
    user_agent = req.headers.get("user-agent")
    
    await SessionService.create_session(
        user_id=user_id,
        token=access_token,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    logger.info(f"User registered: {request.email}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user_id,
            "email": request.email,
            "username": request.username,
            "full_name": request.full_name
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, req: Request):
    """Login user"""
    db = get_database()
    
    # Find user by email
    user = await db.users.find_one({"email": request.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    user_id = str(user["_id"])
    
    # Create access token
    access_token = create_access_token(data={"sub": user_id})
    
    # Create session
    ip_address = req.client.host if req.client else None
    user_agent = req.headers.get("user-agent")
    
    await SessionService.create_session(
        user_id=user_id,
        token=access_token,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    logger.info(f"User logged in: {request.email}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user_id,
            "email": user["email"],
            "username": user["username"],
            "full_name": user.get("full_name")
        }
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Logout user"""
    # In a real implementation, you would invalidate the token
    # For now, we'll just return success
    logger.info(f"User logged out: {current_user.email}")
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat()
    )
