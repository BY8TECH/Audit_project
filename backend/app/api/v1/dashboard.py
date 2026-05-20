"""Dashboard API routes."""

from fastapi import APIRouter, Depends, Query

from app.core.security import get_current_user
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import DashboardSummary, RecentTransaction, PlatformBreakdown, ChartData

from typing import List

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(current_user: dict = Depends(get_current_user)):
    """Get dashboard summary statistics."""
    return await DashboardService.get_summary(current_user["id"])


@router.get("/recent-transactions", response_model=List[RecentTransaction])
async def get_recent_transactions(
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    """Get recent transactions for the dashboard."""
    return await DashboardService.get_recent_transactions(current_user["id"], limit)


@router.get("/platform-breakdown", response_model=List[PlatformBreakdown])
async def get_platform_breakdown(current_user: dict = Depends(get_current_user)):
    """Get data breakdown by connected platform."""
    return await DashboardService.get_platform_breakdown(current_user["id"])


@router.get("/charts/revenue-trend", response_model=ChartData)
async def get_revenue_trend(
    months: int = Query(6, ge=1, le=24),
    current_user: dict = Depends(get_current_user),
):
    """Get monthly revenue trend data for charts."""
    return await DashboardService.get_revenue_trend(current_user["id"], months)


@router.get("/charts/expense-breakdown", response_model=ChartData)
async def get_expense_breakdown(current_user: dict = Depends(get_current_user)):
    """Get expense breakdown data for pie/doughnut charts."""
    return await DashboardService.get_expense_breakdown(current_user["id"])
