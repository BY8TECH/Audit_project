"""
Auditor Data Integration Platform - FastAPI Application Entry Point

Run with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import mongodb
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📦 Mock Data Mode: {'ON' if settings.USE_MOCK_DATA else 'OFF'}")
    await mongodb.connect()

    # Create indexes
    try:
        db = mongodb.get_database()
        await db["users"].create_index("email", unique=True)
        await db["connections"].create_index([("user_id", 1), ("platform", 1)])
        await db["financial_data"].create_index([("user_id", 1), ("source_platform", 1)])
        await db["financial_data"].create_index([("user_id", 1), ("data_type", 1)])
        await db["financial_data"].create_index([("connection_id", 1)])
        await db["financial_data"].create_index("date")
        await db["audit_logs"].create_index([("user_id", 1), ("timestamp", -1)])
        await db["reconciliations"].create_index([("user_id", 1), ("run_at", -1)])
        print("📇 Database indexes created")
    except Exception as e:
        print(f"⚠️ Index creation warning: {e}")

    yield

    # Shutdown
    await mongodb.disconnect()
    print("👋 Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for the Auditor Data Integration Platform POC. "
                "Integrates with Zoho Books, Tally Prime, GST Portal, and Income Tax Portal.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


# Root health endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "mock_mode": settings.USE_MOCK_DATA,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    db_healthy = False
    try:
        db = mongodb.get_database()
        await db.command("ping")
        db_healthy = True
    except Exception:
        pass

    return {
        "status": "healthy" if db_healthy else "degraded",
        "database": "connected" if db_healthy else "disconnected",
        "mock_mode": settings.USE_MOCK_DATA,
        "version": settings.APP_VERSION,
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions globally."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred",
        },
    )
