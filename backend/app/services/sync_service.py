"""Sync service - orchestrate data synchronization from connectors to MongoDB."""

from datetime import datetime, timezone
from typing import Dict, Any, Optional

from app.core.database import mongodb
from app.integrations.zoho_connector import ZohoConnector
from app.integrations.tally_connector import TallyConnector
from app.integrations.gst_connector import GSTConnector
from app.integrations.income_tax_connector import IncomeTaxConnector
from app.services.normalizer_service import NormalizerService


class SyncService:
    """Service to orchestrate data sync from platform connectors to MongoDB."""

    # Connector registry
    CONNECTORS = {
        "zoho_books": ZohoConnector,
        "tally_prime": TallyConnector,
        "gst_portal": GSTConnector,
        "income_tax": IncomeTaxConnector,
    }

    @staticmethod
    async def sync_connection(user_id: str, connection_id: str) -> Dict[str, Any]:
        """Sync data for a specific connection."""
        connections = mongodb.get_collection("connections")
        from bson import ObjectId

        # Get connection details
        conn = await connections.find_one({"_id": ObjectId(connection_id), "user_id": user_id})
        if not conn:
            return {"success": False, "error": "Connection not found"}

        platform = conn["platform"]

        # Update status to syncing
        await connections.update_one(
            {"_id": ObjectId(connection_id)},
            {"$set": {"status": "syncing", "updated_at": datetime.now(timezone.utc)}},
        )

        try:
            # Get the appropriate connector
            connector_class = SyncService.CONNECTORS.get(platform)
            if not connector_class:
                raise ValueError(f"Unknown platform: {platform}")

            connector = connector_class(
                config=conn.get("config", {}),
                credentials=conn.get("credentials", {}),
            )

            # Connect
            await connector.connect()

            # Sync based on platform
            records_synced = 0
            if platform == "zoho_books":
                records_synced = await SyncService._sync_zoho(connector, user_id, connection_id)
            elif platform == "tally_prime":
                records_synced = await SyncService._sync_tally(connector, user_id, connection_id)
            elif platform == "gst_portal":
                records_synced = await SyncService._sync_gst(connector, user_id, connection_id)
            elif platform == "income_tax":
                records_synced = await SyncService._sync_income_tax(connector, user_id, connection_id)

            # Disconnect
            await connector.disconnect()

            # Update connection status
            await connections.update_one(
                {"_id": ObjectId(connection_id)},
                {
                    "$set": {
                        "status": "connected",
                        "last_sync_at": datetime.now(timezone.utc),
                        "last_sync_status": "success",
                        "records_synced": records_synced,
                        "error_message": None,
                        "updated_at": datetime.now(timezone.utc),
                    }
                },
            )

            # Log audit
            await SyncService._log_audit(user_id, connection_id, platform, records_synced, "success")

            return {
                "success": True,
                "platform": platform,
                "records_synced": records_synced,
                "synced_at": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            # Update connection with error
            await connections.update_one(
                {"_id": ObjectId(connection_id)},
                {
                    "$set": {
                        "status": "error",
                        "last_sync_status": "failed",
                        "error_message": str(e),
                        "updated_at": datetime.now(timezone.utc),
                    }
                },
            )

            await SyncService._log_audit(user_id, connection_id, platform, 0, "failure", str(e))

            return {"success": False, "error": str(e)}

    @staticmethod
    async def _sync_zoho(connector: ZohoConnector, user_id: str, connection_id: str) -> int:
        """Sync Zoho Books data."""
        financial_data = mongodb.get_collection("financial_data")
        count = 0

        # Clear existing data for this connection
        await financial_data.delete_many({"connection_id": connection_id, "user_id": user_id})

        # Fetch and normalize invoices
        invoices = await connector.fetch_invoices()
        for inv in invoices:
            normalized = NormalizerService.normalize_zoho_invoice(inv, user_id, connection_id)
            await financial_data.insert_one(normalized)
            count += 1

        # Fetch and normalize bills
        bills = await connector.fetch_bills()
        for bill in bills:
            normalized = NormalizerService.normalize_zoho_bill(bill, user_id, connection_id)
            await financial_data.insert_one(normalized)
            count += 1

        return count

    @staticmethod
    async def _sync_tally(connector: TallyConnector, user_id: str, connection_id: str) -> int:
        """Sync Tally Prime data."""
        financial_data = mongodb.get_collection("financial_data")
        count = 0

        await financial_data.delete_many({"connection_id": connection_id, "user_id": user_id})

        # Fetch and normalize all vouchers
        vouchers = await connector.fetch_all_vouchers()
        for voucher in vouchers:
            normalized = NormalizerService.normalize_tally_voucher(voucher, user_id, connection_id)
            await financial_data.insert_one(normalized)
            count += 1

        # Fetch and normalize ledgers
        ledgers = await connector.fetch_ledgers()
        for ledger in ledgers:
            normalized = NormalizerService.normalize_tally_ledger(ledger, user_id, connection_id)
            await financial_data.insert_one(normalized)
            count += 1

        return count

    @staticmethod
    async def _sync_gst(connector: GSTConnector, user_id: str, connection_id: str) -> int:
        """Sync GST Portal data."""
        financial_data = mongodb.get_collection("financial_data")
        count = 0

        await financial_data.delete_many({"connection_id": connection_id, "user_id": user_id})

        # Fetch GSTR-1 summary
        gstr1 = await connector.fetch_gstr1_summary()
        if gstr1:
            normalized = NormalizerService.normalize_gst_data(gstr1, user_id, connection_id)
            normalized["description"] = "GSTR-1 Summary"
            await financial_data.insert_one(normalized)
            count += 1

        # Fetch GSTR-3B summary
        gstr3b = await connector.fetch_gstr3b_summary()
        if gstr3b:
            normalized = NormalizerService.normalize_gst_data(gstr3b, user_id, connection_id)
            normalized["description"] = "GSTR-3B Summary"
            await financial_data.insert_one(normalized)
            count += 1

        # Fetch GSTIN details
        gstin_records = await connector.fetch_gstin_details()
        for record in gstin_records:
            normalized = NormalizerService.normalize_gst_data(record, user_id, connection_id)
            normalized["data_type"] = "gst_return"
            normalized["description"] = f"GSTIN: {record.get('gstin', '')} - {record.get('trade_name', '')}"
            await financial_data.insert_one(normalized)
            count += 1

        return count

    @staticmethod
    async def _sync_income_tax(connector: IncomeTaxConnector, user_id: str, connection_id: str) -> int:
        """Sync Income Tax Portal data."""
        financial_data = mongodb.get_collection("financial_data")
        count = 0

        await financial_data.delete_many({"connection_id": connection_id, "user_id": user_id})

        # Fetch PAN records
        pan_records = await connector.fetch_pan_records()
        for record in pan_records:
            normalized = NormalizerService.normalize_income_tax_data(record, user_id, connection_id)
            await financial_data.insert_one(normalized)
            count += 1

        return count

    @staticmethod
    async def _log_audit(
        user_id: str, connection_id: str, platform: str, records: int,
        status: str, error: Optional[str] = None,
    ) -> None:
        """Log sync action to audit log."""
        audit_logs = mongodb.get_collection("audit_logs")
        await audit_logs.insert_one({
            "user_id": user_id,
            "action": "sync_data",
            "resource_type": "connection",
            "resource_id": connection_id,
            "details": {
                "platform": platform,
                "records_synced": records,
            },
            "status": status,
            "error_message": error,
            "timestamp": datetime.now(timezone.utc),
        })
