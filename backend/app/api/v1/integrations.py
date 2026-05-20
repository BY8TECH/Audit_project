"""Integrations API routes - manage platform connections and sync data."""

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from bson import ObjectId

from app.core.security import get_current_user
from app.core.database import mongodb
from app.schemas.connection import ConnectionCreate, ConnectionResponse
from app.schemas.financial_data import FinancialDataResponse, FinancialDataFilter, FinancialDataListResponse
from app.services.sync_service import SyncService
from app.models.connection import PlatformType, ConnectionStatus

router = APIRouter()

PLATFORM_INFO = {
    "zoho_books": {
        "name": "Zoho Books",
        "description": "Cloud-based accounting software for managing finances, invoicing, and inventory",
        "icon": "zoho",
        "data_types": ["invoices", "bills", "chart_of_accounts", "trial_balance"],
        "supported": True,
    },
    "tally_prime": {
        "name": "Tally Prime",
        "description": "India's most popular business accounting and ERP software",
        "icon": "tally",
        "data_types": ["vouchers", "ledgers", "trial_balance"],
        "supported": True,
    },
    "gst_portal": {
        "name": "GST Portal",
        "description": "Government of India GST compliance portal for returns and filing",
        "icon": "gst",
        "data_types": ["gstin_details", "gstr1_summary", "gstr3b_summary", "filing_history"],
        "supported": True,
    },
    "income_tax": {
        "name": "Income Tax Portal",
        "description": "Income Tax Department portal for PAN verification and filing status",
        "icon": "incometax",
        "data_types": ["pan_verification", "filing_status", "tds_summary"],
        "supported": True,
    },
}


@router.get("/platforms")
async def get_available_platforms(current_user: dict = Depends(get_current_user)):
    """Get list of available integration platforms."""
    return {"platforms": PLATFORM_INFO}


@router.post("/connect", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
async def connect_platform(
    connection_data: ConnectionCreate,
    current_user: dict = Depends(get_current_user),
):
    """Create a new platform connection."""
    connections = mongodb.get_collection("connections")

    # Validate platform
    if connection_data.platform not in PLATFORM_INFO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported platform: {connection_data.platform}",
        )

    # Check for existing active connection to same platform
    existing = await connections.find_one({
        "user_id": current_user["id"],
        "platform": connection_data.platform,
        "is_active": True,
    })
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Active connection to {connection_data.platform} already exists",
        )

    # Create connection document
    now = datetime.now(timezone.utc)
    conn_doc = {
        "user_id": current_user["id"],
        "platform": connection_data.platform,
        "display_name": connection_data.display_name,
        "status": "connected",
        "config": connection_data.config,
        "credentials": connection_data.credentials,
        "last_sync_at": None,
        "last_sync_status": None,
        "sync_frequency_minutes": 60,
        "records_synced": 0,
        "error_message": None,
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }

    result = await connections.insert_one(conn_doc)

    # Log audit
    audit_logs = mongodb.get_collection("audit_logs")
    await audit_logs.insert_one({
        "user_id": current_user["id"],
        "action": "create_connection",
        "resource_type": "connection",
        "resource_id": str(result.inserted_id),
        "details": {"platform": connection_data.platform, "display_name": connection_data.display_name},
        "status": "success",
        "timestamp": now,
    })

    return ConnectionResponse(
        id=str(result.inserted_id),
        platform=connection_data.platform,
        display_name=connection_data.display_name,
        status="connected",
        is_active=True,
        created_at=now,
        updated_at=now,
    )


@router.post("/{connection_id}/sync")
async def sync_connection(
    connection_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Trigger data sync for a connection."""
    # Validate connection belongs to user
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

    # Run sync
    result = await SyncService.sync_connection(current_user["id"], connection_id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Sync failed"),
        )

    return result


@router.get("/{connection_id}/data", response_model=FinancialDataListResponse)
async def get_connection_data(
    connection_id: str,
    data_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
):
    """Get synced data for a specific connection."""
    # Verify connection ownership
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

    financial_data = mongodb.get_collection("financial_data")

    query = {"connection_id": connection_id, "user_id": current_user["id"]}
    if data_type:
        query["data_type"] = data_type

    total = await financial_data.count_documents(query)
    skip = (page - 1) * page_size
    total_pages = max(1, (total + page_size - 1) // page_size)

    cursor = financial_data.find(query).skip(skip).limit(page_size).sort("date", -1)

    items = []
    async for doc in cursor:
        items.append(FinancialDataResponse(
            id=str(doc["_id"]),
            connection_id=doc["connection_id"],
            source_platform=doc["source_platform"],
            data_type=doc["data_type"],
            reference_id=doc.get("reference_id", ""),
            reference_number=doc.get("reference_number"),
            date=doc["date"],
            due_date=doc.get("due_date"),
            currency=doc.get("currency", "INR"),
            amount=doc.get("amount", 0),
            tax_amount=doc.get("tax_amount", 0),
            total_amount=doc.get("total_amount", 0),
            balance_due=doc.get("balance_due", 0),
            party_name=doc.get("party_name"),
            party_gstin=doc.get("party_gstin"),
            party_pan=doc.get("party_pan"),
            status=doc.get("status", "active"),
            cgst=doc.get("cgst", 0),
            sgst=doc.get("sgst", 0),
            igst=doc.get("igst", 0),
            description=doc.get("description"),
            line_items=doc.get("line_items", []),
            synced_at=doc.get("synced_at"),
        ))

    return FinancialDataListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.delete("/{connection_id}", status_code=status.HTTP_200_OK)
async def delete_connection(
    connection_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete a platform connection and its synced data."""
    connections = mongodb.get_collection("connections")
    financial_data = mongodb.get_collection("financial_data")

    # Verify ownership
    conn = await connections.find_one({
        "_id": ObjectId(connection_id),
        "user_id": current_user["id"],
    })
    if not conn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )

    # Soft-delete connection
    await connections.update_one(
        {"_id": ObjectId(connection_id)},
        {
            "$set": {
                "is_active": False,
                "status": "disconnected",
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )

    # Delete synced data
    deleted_data = await financial_data.delete_many({
        "connection_id": connection_id,
        "user_id": current_user["id"],
    })

    # Log audit
    audit_logs = mongodb.get_collection("audit_logs")
    await audit_logs.insert_one({
        "user_id": current_user["id"],
        "action": "delete_connection",
        "resource_type": "connection",
        "resource_id": connection_id,
        "details": {
            "platform": conn["platform"],
            "records_deleted": deleted_data.deleted_count,
        },
        "status": "success",
        "timestamp": datetime.now(timezone.utc),
    })

    return {
        "message": "Connection deleted successfully",
        "records_deleted": deleted_data.deleted_count,
    }
