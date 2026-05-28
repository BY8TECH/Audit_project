"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Auditor Data Integration Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "audit_platform"

    # JWT Auth
    JWT_SECRET: str = "super-secret-jwt-key-change-in-production-2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://audit-project-blond.vercel.app",
        "*"
    ]

    # Mock Data
    USE_MOCK_DATA: bool = False

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Zoho OAuth Configuration
    ZOHO_CLIENT_ID: str = "1000.XYPLYRU3UM8GAXPR6GJ9M58I4XWOXV"
    ZOHO_CLIENT_SECRET: str = "e3e8ffcbcc1a1abb30ecda680f7d8622fc30d0e3a1"
    ZOHO_REDIRECT_URI: str = "https://audit-project-blond.vercel.app/integrations/zoho/callback"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
