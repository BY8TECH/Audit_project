"""Connection model for platform integrations."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class PlatformType(str, Enum):
    ZOHO_BOOKS = "zoho_books"
    TALLY_PRIME = "tally_prime"
    GST_PORTAL = "gst_portal"
    INCOME_TAX = "income_tax"


class ConnectionStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    SYNCING = "syncing"
    ERROR = "error"
    PENDING = "pending"


class ConnectionModel(BaseModel):
    """Connection document model for MongoDB."""

    user_id: str
    platform: PlatformType
    display_name: str
    status: ConnectionStatus = ConnectionStatus.PENDING
    config: Dict[str, Any] = Field(default_factory=dict)
    credentials: Dict[str, Any] = Field(default_factory=dict)
    last_sync_at: Optional[datetime] = None
    last_sync_status: Optional[str] = None
    sync_frequency_minutes: int = 60
    records_synced: int = 0
    error_message: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "60f7b2c8e13c...",
                "platform": "zoho_books",
                "display_name": "Zoho Books - Main",
                "status": "connected",
            }
        }
    }
