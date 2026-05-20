"""User model for MongoDB documents."""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    AUDITOR = "auditor"
    VIEWER = "viewer"


class UserModel(BaseModel):
    """User document model for MongoDB."""

    email: EmailStr
    full_name: str
    hashed_password: str
    role: UserRole = UserRole.AUDITOR
    is_active: bool = True
    company_name: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "auditor@example.com",
                "full_name": "Rajesh Kumar",
                "role": "auditor",
                "is_active": True,
                "company_name": "Kumar & Associates CA",
            }
        }
    }
