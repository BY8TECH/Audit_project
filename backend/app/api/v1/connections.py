"""Connections API routes - view and manage connection statuses."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.core.security import get_current_user
from app.core.database import mongodb
from app.schemas.connection import (
    ConnectionResponse,
    ConnectionStatusResponse,
    ConnectionStatusSummary,
)
from app.services.sync_service import SyncService

router = APIRouter()


@router.get("/", response_model=List[ConnectionResponse])
async def list_connections(current_user: dict = Depends(get_current_user)):
    """List all connections for the current user."""
    connections = mongodb.get_collection("connections")

    cursor = connections.find({
        "user_id": current_user["id"],
        "is_active": True,
    }).sort("created_at", -1)

    result = []
    async for conn in cursor:
        result.append(ConnectionResponse(
            id=str(conn["_id"]),
            platform=conn["platform"],
            display_name=conn["display_name"],
            status=conn.get("status", "disconnected"),
            last_sync_at=conn.get("last_sync_at"),
            last_sync_status=conn.get("last_sync_status"),
            records_synced=conn.get("records_synced", 0),
            sync_frequency_minutes=conn.get("sync_frequency_minutes", 60),
            error_message=conn.get("error_message"),
            is_active=conn.get("is_active", True),
            created_at=conn.get("created_at"),
            updated_at=conn.get("updated_at"),
        ))

    return result


@router.get("/status-summary", response_model=ConnectionStatusSummary)
async def get_status_summary(current_user: dict = Depends(get_current_user)):
    """Get summary of all connection statuses."""
    connections = mongodb.get_collection("connections")

    cursor = connections.find({
        "user_id": current_user["id"],
        "is_active": True,
    })

    all_connections = []
    connected = 0
    disconnected = 0
    syncing = 0
    error = 0

    async for conn in cursor:
        conn_status = conn.get("status", "disconnected")

        if conn_status == "connected":
            connected += 1
        elif conn_status == "disconnected":
            disconnected += 1
        elif conn_status == "syncing":
            syncing += 1
        elif conn_status == "error":
            error += 1

        all_connections.append(ConnectionStatusResponse(
            id=str(conn["_id"]),
            platform=conn["platform"],
            display_name=conn["display_name"],
            status=conn_status,
            is_healthy=conn_status in ["connected"],
            last_sync_at=conn.get("last_sync_at"),
            records_synced=conn.get("records_synced", 0),
            error_message=conn.get("error_message"),
        ))

    return ConnectionStatusSummary(
        total=len(all_connections),
        connected=connected,
        disconnected=disconnected,
        syncing=syncing,
        error=error,
        connections=all_connections,
    )


@router.get("/{connection_id}/health")
async def check_connection_health(
    connection_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Check health of a specific connection."""
    connections = mongodb.get_collection("connections")

    conn = await connections.find_one({
        "_id": ObjectId(connection_id),
        "user_id": current_user["id"],
    })

    if not conn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )

    platform = conn["platform"]

    # Get the connector and run health check
    connector_class = SyncService.CONNECTORS.get(platform)
    if not connector_class:
        return {
            "healthy": False,
            "message": f"Unknown platform: {platform}",
            "platform": platform,
        }

    connector = connector_class(
        config=conn.get("config", {}),
        credentials=conn.get("credentials", {}),
    )

    health = await connector.health_check()

    return {
        "connection_id": connection_id,
        "platform": platform,
        "display_name": conn["display_name"],
        **health,
    }
