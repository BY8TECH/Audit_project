"""Reconciliation request/response schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ReconciliationRequest(BaseModel):
    """Request to run reconciliation between two data sources."""
    source_a_platform: str  # e.g., "zoho_books"
    source_b_platform: str  # e.g., "tally_prime"
    data_type: str = "invoice"  # invoice, bill, ledger
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tolerance_amount: float = 1.0  # Allow small INR differences
    match_by: str = "reference_number"  # reference_number, amount_date, party_name


class MismatchItem(BaseModel):
    """A single mismatch found during reconciliation."""
    mismatch_type: str  # "missing_in_a", "missing_in_b", "amount_mismatch", "date_mismatch"
    reference_number: Optional[str] = None
    party_name: Optional[str] = None
    source_a_amount: Optional[float] = None
    source_b_amount: Optional[float] = None
    difference: Optional[float] = None
    source_a_date: Optional[datetime] = None
    source_b_date: Optional[datetime] = None
    source_a_id: Optional[str] = None
    source_b_id: Optional[str] = None
    severity: str = "medium"  # low, medium, high, critical
    details: Dict[str, Any] = {}


class ReconciliationResult(BaseModel):
    """Result of a reconciliation run."""
    id: str
    source_a_platform: str
    source_b_platform: str
    data_type: str
    run_at: datetime
    status: str = "completed"  # completed, in_progress, failed
    total_source_a: int = 0
    total_source_b: int = 0
    matched: int = 0
    mismatched: int = 0
    missing_in_a: int = 0
    missing_in_b: int = 0
    match_percentage: float = 0.0
    total_difference_amount: float = 0.0
    mismatches: List[MismatchItem] = []
    summary: Dict[str, Any] = {}


class ReconciliationReport(BaseModel):
    """Full reconciliation report."""
    result: ReconciliationResult
    recommendations: List[str] = []
    generated_at: datetime
