"""Authentication service - user registration, login, token management."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any

from fastapi import HTTPException, status

from app.core.database import mongodb
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.config import settings
from app.models.user import UserModel, UserRole
from app.schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    async def register(user_data: UserRegister) -> TokenResponse:
        """Register a new user."""
        users = mongodb.get_collection("users")

        # Check if email already exists
        existing = await users.find_one({"email": user_data.email})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create user model
        user = UserModel(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
            role=UserRole.AUDITOR,
            company_name=user_data.company_name,
            phone=user_data.phone,
        )

        # Insert into MongoDB
        result = await users.insert_one(user.model_dump())
        user_id = str(result.inserted_id)

        # Log audit
        await AuthService._log_audit(user_id, user_data.email, "register")

        # Generate tokens
        token_data = {"sub": user_data.email, "user_id": user_id}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        user_response = UserResponse(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            role=UserRole.AUDITOR.value,
            is_active=True,
            company_name=user_data.company_name,
            phone=user_data.phone,
            created_at=user.created_at,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response,
        )

    @staticmethod
    async def authenticate(login_data: UserLogin) -> TokenResponse:
        """Authenticate a user and return tokens."""
        users = mongodb.get_collection("users")

        user = await users.find_one({"email": login_data.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(login_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is disabled",
            )

        user_id = str(user["_id"])

        # Update last login
        await users.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.now(timezone.utc)}},
        )

        # Log audit
        await AuthService._log_audit(user_id, login_data.email, "login")

        # Generate tokens
        token_data = {"sub": login_data.email, "user_id": user_id}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        user_response = UserResponse(
            id=user_id,
            email=user["email"],
            full_name=user["full_name"],
            role=user.get("role", "auditor"),
            is_active=user.get("is_active", True),
            company_name=user.get("company_name"),
            phone=user.get("phone"),
            created_at=user.get("created_at"),
            last_login=datetime.now(timezone.utc),
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response,
        )

    @staticmethod
    async def refresh_access_token(refresh_token_str: str) -> Dict[str, Any]:
        """Refresh an access token using a refresh token."""
        payload = decode_token(refresh_token_str)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        email = payload.get("sub")
        user_id = payload.get("user_id")

        # Verify user still exists and is active
        users = mongodb.get_collection("users")
        user = await users.find_one({"email": email})
        if not user or not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or disabled",
            )

        token_data = {"sub": email, "user_id": user_id}
        new_access_token = create_access_token(token_data)

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    @staticmethod
    async def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by ID."""
        from bson import ObjectId

        users = mongodb.get_collection("users")
        user = await users.find_one({"_id": ObjectId(user_id)})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
            del user["hashed_password"]
            return user
        return None

    @staticmethod
    async def _log_audit(user_id: str, email: str, action: str) -> None:
        """Log an authentication action."""
        audit_logs = mongodb.get_collection("audit_logs")
        await audit_logs.insert_one({
            "user_id": user_id,
            "user_email": email,
            "action": action,
            "resource_type": "auth",
            "status": "success",
            "timestamp": datetime.now(timezone.utc),
        })
