"""Dashboard service - aggregate data for dashboard views."""

from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional

from app.core.database import mongodb
from app.schemas.dashboard import (
    DashboardSummary,
    RecentTransaction,
    PlatformBreakdown,
    ChartData,
)


class DashboardService:
    """Service for dashboard data aggregation."""

    @staticmethod
    async def get_summary(user_id: str) -> DashboardSummary:
        """Get dashboard summary statistics."""
        financial_data = mongodb.get_collection("financial_data")
        connections = mongodb.get_collection("connections")

        # Count active connections
        active_connections = await connections.count_documents(
            {"user_id": user_id, "status": "connected"}
        )

        # Aggregate financial data
        pipeline = [
            {"$match": {"user_id": user_id}},
            {
                "$group": {
                    "_id": None,
                    "total_revenue": {
                        "$sum": {
                            "$cond": [
                                {"$in": ["$data_type", ["invoice"]]},
                                "$total_amount",
                                0,
                            ]
                        }
                    },
                    "total_expenses": {
                        "$sum": {
                            "$cond": [
                                {"$in": ["$data_type", ["bill", "voucher"]]},
                                "$total_amount",
                                0,
                            ]
                        }
                    },
                    "total_invoices": {
                        "$sum": {"$cond": [{"$eq": ["$data_type", "invoice"]}, 1, 0]}
                    },
                    "total_bills": {
                        "$sum": {"$cond": [{"$eq": ["$data_type", "bill"]}, 1, 0]}
                    },
                    "outstanding_receivables": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$eq": ["$data_type", "invoice"]},
                                        {"$in": ["$status", ["sent", "overdue", "partially_paid"]]},
                                    ]
                                },
                                "$balance_due",
                                0,
                            ]
                        }
                    },
                    "outstanding_payables": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$eq": ["$data_type", "bill"]},
                                        {"$in": ["$status", ["received", "overdue", "partially_paid"]]},
                                    ]
                                },
                                "$balance_due",
                                0,
                            ]
                        }
                    },
                    "total_records": {"$sum": 1},
                }
            },
        ]

        result = await financial_data.aggregate(pipeline).to_list(1)

        if result:
            data = result[0]
            # Get last sync time
            last_sync = await connections.find_one(
                {"user_id": user_id, "last_sync_at": {"$ne": None}},
                sort=[("last_sync_at", -1)],
            )

            return DashboardSummary(
                total_revenue=data.get("total_revenue", 0),
                total_expenses=data.get("total_expenses", 0),
                total_invoices=data.get("total_invoices", 0),
                total_bills=data.get("total_bills", 0),
                outstanding_receivables=data.get("outstanding_receivables", 0),
                outstanding_payables=data.get("outstanding_payables", 0),
                active_connections=active_connections,
                total_records=data.get("total_records", 0),
                last_sync_at=last_sync.get("last_sync_at") if last_sync else None,
                gst_compliance_score=92.5,
            )

        return DashboardSummary(active_connections=active_connections)

    @staticmethod
    async def get_recent_transactions(
        user_id: str, limit: int = 20
    ) -> List[RecentTransaction]:
        """Get recent transactions for the dashboard."""
        financial_data = mongodb.get_collection("financial_data")

        cursor = financial_data.find(
            {"user_id": user_id, "data_type": {"$in": ["invoice", "bill", "voucher", "payment"]}}
        ).sort("date", -1).limit(limit)

        transactions = []
        async for doc in cursor:
            transactions.append(
                RecentTransaction(
                    id=str(doc["_id"]),
                    date=doc["date"],
                    type=doc["data_type"],
                    reference_number=doc.get("reference_number"),
                    party_name=doc.get("party_name"),
                    amount=doc.get("total_amount", 0),
                    status=doc.get("status", "active"),
                    source_platform=doc.get("source_platform", "unknown"),
                )
            )

        return transactions

    @staticmethod
    async def get_platform_breakdown(user_id: str) -> List[PlatformBreakdown]:
        """Get data breakdown by platform."""
        financial_data = mongodb.get_collection("financial_data")
        connections = mongodb.get_collection("connections")

        pipeline = [
            {"$match": {"user_id": user_id}},
            {
                "$group": {
                    "_id": "$source_platform",
                    "total_records": {"$sum": 1},
                    "total_amount": {"$sum": "$total_amount"},
                }
            },
        ]

        results = await financial_data.aggregate(pipeline).to_list(10)
        breakdowns = []

        platform_display_names = {
            "zoho_books": "Zoho Books",
            "tally_prime": "Tally Prime",
            "gst_portal": "GST Portal",
            "income_tax": "Income Tax Portal",
        }

        for r in results:
            platform = r["_id"]
            conn = await connections.find_one(
                {"user_id": user_id, "platform": platform}
            )

            breakdowns.append(
                PlatformBreakdown(
                    platform=platform,
                    display_name=platform_display_names.get(platform, platform),
                    total_records=r["total_records"],
                    total_amount=r["total_amount"],
                    last_sync_at=conn.get("last_sync_at") if conn else None,
                    status=conn.get("status", "disconnected") if conn else "disconnected",
                )
            )

        return breakdowns

    @staticmethod
    async def get_revenue_trend(user_id: str, months: int = 6) -> ChartData:
        """Get monthly revenue trend for charts."""
        financial_data = mongodb.get_collection("financial_data")

        now = datetime.now(timezone.utc)
        start_date = now - timedelta(days=months * 30)

        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "data_type": "invoice",
                    "date": {"$gte": start_date},
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$date"},
                        "month": {"$month": "$date"},
                    },
                    "revenue": {"$sum": "$total_amount"},
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id.year": 1, "_id.month": 1}},
        ]

        results = await financial_data.aggregate(pipeline).to_list(12)

        month_names = [
            "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ]

        labels = []
        revenue_data = []

        for r in results:
            month_label = f"{month_names[r['_id']['month']]} {r['_id']['year']}"
            labels.append(month_label)
            revenue_data.append(r["revenue"])

        # If no data, provide placeholder labels
        if not labels:
            for i in range(months):
                d = now - timedelta(days=(months - 1 - i) * 30)
                labels.append(f"{month_names[d.month]} {d.year}")
                revenue_data.append(0)

        return ChartData(
            title="Revenue Trend",
            chart_type="line",
            labels=labels,
            datasets=[
                {
                    "label": "Revenue (₹)",
                    "data": revenue_data,
                    "borderColor": "#3B82F6",
                    "backgroundColor": "rgba(59, 130, 246, 0.1)",
                    "fill": True,
                }
            ],
        )

    @staticmethod
    async def get_expense_breakdown(user_id: str) -> ChartData:
        """Get expense breakdown by category for pie chart."""
        financial_data = mongodb.get_collection("financial_data")

        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "data_type": {"$in": ["bill", "voucher"]},
                }
            },
            {
                "$group": {
                    "_id": "$source_platform",
                    "total": {"$sum": "$total_amount"},
                }
            },
        ]

        results = await financial_data.aggregate(pipeline).to_list(10)

        platform_names = {
            "zoho_books": "Zoho Books",
            "tally_prime": "Tally Prime",
            "gst_portal": "GST Portal",
            "income_tax": "Income Tax",
        }
        colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]

        labels = [platform_names.get(r["_id"], r["_id"]) for r in results]
        amounts = [r["total"] for r in results]

        if not labels:
            labels = ["No Data"]
            amounts = [0]

        return ChartData(
            title="Expense Breakdown by Platform",
            chart_type="doughnut",
            labels=labels,
            datasets=[
                {
                    "label": "Expenses (₹)",
                    "data": amounts,
                    "backgroundColor": colors[: len(labels)],
                }
            ],
        )
