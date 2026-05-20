"""Reconciliation API routes."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.core.security import get_current_user
from app.schemas.reconciliation import (
    ReconciliationRequest,
    ReconciliationResult,
    ReconciliationReport,
    MismatchItem,
)
from app.services.reconciliation_service import ReconciliationService

from typing import List

router = APIRouter()


@router.post("/compare", response_model=ReconciliationResult)
async def compare_sources(
    request: ReconciliationRequest,
    current_user: dict = Depends(get_current_user),
):
    """Run reconciliation between two data sources."""
    # Validate platforms are different
    if request.source_a_platform == request.source_b_platform:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source A and Source B must be different platforms",
        )

    return await ReconciliationService.compare_sources(current_user["id"], request)


@router.get("/mismatches", response_model=List[MismatchItem])
async def get_mismatches(
    reconciliation_id: Optional[str] = Query(None, description="Specific reconciliation run ID"),
    current_user: dict = Depends(get_current_user),
):
    """Get mismatches from the latest or specific reconciliation run."""
    return await ReconciliationService.get_mismatches(
        current_user["id"], reconciliation_id
    )


@router.get("/report/{reconciliation_id}", response_model=ReconciliationReport)
async def get_reconciliation_report(
    reconciliation_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Get a detailed reconciliation report with recommendations."""
    return await ReconciliationService.generate_report(
        current_user["id"], reconciliation_id
    )
