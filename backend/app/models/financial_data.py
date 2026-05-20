"""Normalized financial data model."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class DataType(str, Enum):
    INVOICE = "invoice"
    BILL = "bill"
    PAYMENT = "payment"
    RECEIPT = "receipt"
    JOURNAL = "journal"
    VOUCHER = "voucher"
    LEDGER = "ledger"
    TRIAL_BALANCE = "trial_balance"
    GST_RETURN = "gst_return"
    TAX_FILING = "tax_filing"


class FinancialDataModel(BaseModel):
    """Normalized financial data document for MongoDB."""

    user_id: str
    connection_id: str
    source_platform: str  # e.g., "zoho_books", "tally_prime"
    data_type: DataType
    reference_id: str  # Original ID from the source platform
    reference_number: Optional[str] = None  # Invoice/bill number

    # Date fields
    date: datetime
    due_date: Optional[datetime] = None

    # Amount fields (all in INR)
    currency: str = "INR"
    amount: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    balance_due: float = 0.0

    # Party information
    party_name: Optional[str] = None
    party_gstin: Optional[str] = None
    party_pan: Optional[str] = None
    party_address: Optional[str] = None

    # Status
    status: str = "active"  # active, paid, overdue, cancelled, etc.

    # Line items (for invoices/bills)
    line_items: List[Dict[str, Any]] = Field(default_factory=list)

    # GST details
    cgst: float = 0.0
    sgst: float = 0.0
    igst: float = 0.0
    cess: float = 0.0
    hsn_code: Optional[str] = None
    place_of_supply: Optional[str] = None

    # Additional metadata
    description: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    raw_data: Dict[str, Any] = Field(default_factory=dict)

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    synced_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
