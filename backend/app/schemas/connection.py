"""Connection request/response schemas."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class ConnectionCreate(BaseModel):
    """Create a new platform connection."""
    platform: str  # zoho_books, tally_prime, gst_portal, income_tax
    display_name: str = Field(..., min_length=2, max_length=100)
    config: Dict[str, Any] = Field(default_factory=dict)
    credentials: Dict[str, Any] = Field(default_factory=dict)


class ConnectionUpdate(BaseModel):
    """Update an existing connection."""
    display_name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    credentials: Optional[Dict[str, Any]] = None
    sync_frequency_minutes: Optional[int] = None
    is_active: Optional[bool] = None


class ConnectionResponse(BaseModel):
    """Connection response."""
    id: str
    platform: str
    display_name: str
    status: str
    last_sync_at: Optional[datetime] = None
    last_sync_status: Optional[str] = None
    records_synced: int = 0
    sync_frequency_minutes: int = 60
    error_message: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ConnectionStatusResponse(BaseModel):
    """Connection health/status response."""
    id: str
    platform: str
    display_name: str
    status: str
    is_healthy: bool
    last_sync_at: Optional[datetime] = None
    records_synced: int = 0
    error_message: Optional[str] = None


class ConnectionStatusSummary(BaseModel):
    """Summary of all connection statuses."""
    total: int
    connected: int
    disconnected: int
    syncing: int
    error: int
    connections: List[ConnectionStatusResponse]
