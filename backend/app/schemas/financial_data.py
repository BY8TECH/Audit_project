"""Financial data request/response schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class FinancialDataCreate(BaseModel):
    """Create financial data record."""
    source_platform: str
    data_type: str
    reference_id: str
    reference_number: Optional[str] = None
    date: datetime
    due_date: Optional[datetime] = None
    currency: str = "INR"
    amount: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    party_name: Optional[str] = None
    party_gstin: Optional[str] = None
    description: Optional[str] = None
    line_items: List[Dict[str, Any]] = Field(default_factory=list)
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class FinancialDataResponse(BaseModel):
    """Financial data response."""
    id: str
    connection_id: str
    source_platform: str
    data_type: str
    reference_id: str
    reference_number: Optional[str] = None
    date: datetime
    due_date: Optional[datetime] = None
    currency: str = "INR"
    amount: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    balance_due: float = 0.0
    party_name: Optional[str] = None
    party_gstin: Optional[str] = None
    party_pan: Optional[str] = None
    status: str = "active"
    cgst: float = 0.0
    sgst: float = 0.0
    igst: float = 0.0
    description: Optional[str] = None
    line_items: List[Dict[str, Any]] = []
    synced_at: Optional[datetime] = None


class FinancialDataFilter(BaseModel):
    """Filter for querying financial data."""
    source_platform: Optional[str] = None
    data_type: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    party_name: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    status: Optional[str] = None
    page: int = 1
    page_size: int = 50


class FinancialDataListResponse(BaseModel):
    """Paginated list of financial data."""
    items: List[FinancialDataResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
