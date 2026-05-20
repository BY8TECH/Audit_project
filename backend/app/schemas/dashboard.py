"""Dashboard response schemas."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class DashboardSummary(BaseModel):
    """Main dashboard summary stats."""
    total_revenue: float = 0.0
    total_expenses: float = 0.0
    total_invoices: int = 0
    total_bills: int = 0
    outstanding_receivables: float = 0.0
    outstanding_payables: float = 0.0
    active_connections: int = 0
    total_records: int = 0
    last_sync_at: Optional[datetime] = None
    gst_compliance_score: float = 0.0  # percentage


class RecentTransaction(BaseModel):
    """A recent transaction for dashboard display."""
    id: str
    date: datetime
    type: str  # invoice, bill, payment, etc.
    reference_number: Optional[str] = None
    party_name: Optional[str] = None
    amount: float
    status: str
    source_platform: str


class PlatformBreakdown(BaseModel):
    """Data breakdown by platform."""
    platform: str
    display_name: str
    total_records: int
    total_amount: float
    last_sync_at: Optional[datetime] = None
    status: str


class ChartDataPoint(BaseModel):
    """Single data point for charts."""
    label: str
    value: float
    metadata: Dict[str, Any] = {}


class ChartData(BaseModel):
    """Chart data with labels and datasets."""
    title: str
    chart_type: str  # bar, line, pie, doughnut
    labels: List[str]
    datasets: List[Dict[str, Any]]


class DashboardResponse(BaseModel):
    """Complete dashboard response."""
    summary: DashboardSummary
    recent_transactions: List[RecentTransaction]
    platform_breakdown: List[PlatformBreakdown]
