"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
)
from app.services.auth_service import AuthService
from app.core.security import get_current_user

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """Register a new user account."""
    return await AuthService.register(user_data)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin):
    """Login with email and password."""
    return await AuthService.authenticate(login_data)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get the current authenticated user's profile."""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        role=current_user.get("role", "auditor"),
        is_active=current_user.get("is_active", True),
        company_name=current_user.get("company_name"),
        phone=current_user.get("phone"),
        created_at=current_user.get("created_at"),
        last_login=current_user.get("last_login"),
    )


@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):
    """Refresh an access token using a refresh token."""
    return await AuthService.refresh_access_token(request.refresh_token)
