"""API v1 router - includes all sub-routers."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.integrations import router as integrations_router
from app.api.v1.connections import router as connections_router
from app.api.v1.reconciliation import router as reconciliation_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(integrations_router, prefix="/integrations", tags=["Integrations"])
api_router.include_router(connections_router, prefix="/connections", tags=["Connections"])
api_router.include_router(reconciliation_router, prefix="/reconciliation", tags=["Reconciliation"])
