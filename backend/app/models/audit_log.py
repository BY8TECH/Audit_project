"""Audit log model for tracking user actions."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AuditLogModel(BaseModel):
    """Audit log document for MongoDB."""

    user_id: str
    user_email: Optional[str] = None
    action: str  # e.g., "login", "sync_data", "create_connection", "run_reconciliation"
    resource_type: str  # e.g., "connection", "financial_data", "reconciliation"
    resource_id: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    status: str = "success"  # success, failure, error
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
