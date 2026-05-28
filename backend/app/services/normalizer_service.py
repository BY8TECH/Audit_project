"""Normalizer service - transform source-specific data to unified schema."""

from datetime import datetime, timezone
from typing import Dict, Any, List
from dateutil import parser as date_parser


class NormalizerService:
    """Service to normalize data from different platforms into unified format."""

    @staticmethod
    def normalize_zoho_invoice(raw: Dict[str, Any], user_id: str, connection_id: str) -> Dict[str, Any]:
        """Normalize a Zoho Books invoice to unified format."""
        date = NormalizerService._parse_date(raw.get("date"))
        due_date = NormalizerService._parse_date(raw.get("due_date"))

        return {
            "user_id": user_id,
            "connection_id": connection_id,
            "source_platform": "zoho_books",
            "data_type": "invoice",
            "reference_id": raw.get("invoice_id", ""),
            "reference_number": raw.get("invoice_number", ""),
            "date": date,
            "due_date": due_date,
            "currency": raw.get("currency", "INR"),
            "amount": raw.get("sub_total", 0),
            "tax_amount": raw.get("tax_amount", 0),
            "total_amount": raw.get("total", 0),
            "balance_due": raw.get("balance", raw.get("balance_due", 0)),
            "party_name": raw.get("customer_name", ""),
            "party_gstin": raw.get("customer_gstin", ""),
            "party_pan": raw.get("customer_pan", ""),
            "party_address": raw.get("customer_address", ""),
            "status": raw.get("status", "active"),
            "line_items": raw.get("line_items", []),
            "cgst": raw.get("cgst", 0),
            "sgst": raw.get("sgst", 0),
            "igst": raw.get("igst", 0),
            "cess": raw.get("cess", 0),
            "place_of_supply": raw.get("place_of_supply", ""),
            "description": raw.get("notes", ""),
            "raw_data": raw,
            "synced_at": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

    @staticmethod
    def normalize_zoho_bill(raw: Dict[str, Any], user_id: str, connection_id: str) -> Dict[str, Any]:
        """Normalize a Zoho Books bill to unified format."""
        date = NormalizerService._parse_date(raw.get("date"))
        due_date = NormalizerService._parse_date(raw.get("due_date"))

        return {
            "user_id": user_id,
            "connection_id": connection_id,
            "source_platform": "zoho_books",
            "data_type": "bill",
            "reference_id": raw.get("bill_id", ""),
            "reference_number": raw.get("bill_number", ""),
            "date": date,
            "due_date": due_date,
            "currency": raw.get("currency", "INR"),
            "amount": raw.get("sub_total", 0),
            "tax_amount": raw.get("tax_amount", 0),
            "total_amount": raw.get("total", 0),
            "balance_due": raw.get("balance", raw.get("balance_due", 0)),
            "party_name": raw.get("vendor_name", ""),
            "party_gstin": raw.get("vendor_gstin", ""),
            "party_pan": raw.get("vendor_pan", ""),
            "party_address": raw.get("vendor_address", ""),
            "status": raw.get("status", "active"),
            "line_items": raw.get("line_items", []),
            "cgst": raw.get("cgst", 0),
            "sgst": raw.get("sgst", 0),
            "igst": raw.get("igst", 0),
            "cess": raw.get("cess", 0),
            "place_of_supply": raw.get("place_of_supply", ""),
            "description": raw.get("notes", ""),
            "raw_data": raw,
            "synced_at": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

    @staticmethod
    def normalize_tally_voucher(raw: Dict[str, Any], user_id: str, connection_id: str) -> Dict[str, Any]:
        """Normalize a Tally Prime voucher to unified format."""
        date = NormalizerService._parse_date(raw.get("date"))
        v_type = raw.get("voucher_type", "").lower()

        # Map voucher types to our data types
        type_map = {
            "sales": "invoice",
            "purchase": "bill",
            "receipt": "payment",
            "payment": "payment",
            "journal": "journal",
            "contra": "journal",
            "credit note": "invoice",
            "debit note": "bill",
        }

        data_type = type_map.get(v_type, "voucher")

        return {
            "user_id": user_id,
            "connection_id": connection_id,
            "source_platform": "tally_prime",
            "data_type": data_type,
            "reference_id": raw.get("voucher_id", ""),
            "reference_number": raw.get("reference_number", raw.get("voucher_number", "")),
            "date": date,
            "due_date": None,
            "currency": "INR",
            "amount": raw.get("amount", 0),
            "tax_amount": raw.get("tax_amount", 0),
            "total_amount": raw.get("total_amount", 0),
            "balance_due": 0,
            "party_name": raw.get("party_name", ""),
            "party_gstin": "",
            "party_pan": "",
            "party_address": "",
            "status": "cancelled" if raw.get("is_cancelled") else "active",
            "line_items": raw.get("inventory_entries", []),
            "cgst": raw.get("cgst", 0),
            "sgst": raw.get("sgst", 0),
            "igst": raw.get("igst", 0),
            "cess": 0,
            "place_of_supply": "",
            "description": raw.get("narration", ""),
            "notes": f"Voucher Type: {raw.get('voucher_type', '')}",
            "tags": [raw.get("voucher_type", "")],
            "raw_data": raw,
            "synced_at": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

    @staticmethod
    def normalize_tally_ledger(raw: Dict[str, Any], user_id: str, connection_id: str) -> Dict[str, Any]:
        """Normalize a Tally ledger to unified format."""
        return {
            "user_id": user_id,
            "connection_id": connection_id,
            "source_platform": "tally_prime",
            "data_type": "ledger",
            "reference_id": raw.get("ledger_id", ""),
            "reference_number": raw.get("ledger_name", ""),
            "date": datetime.now(timezone.utc),
            "currency": "INR",
            "amount": raw.get("closing_balance", 0),
            "tax_amount": 0,
            "total_amount": raw.get("closing_balance", 0),
            "balance_due": 0,
            "party_name": raw.get("ledger_name", ""),
            "status": "active",
            "description": f"Group: {raw.get('parent_group', '')}",
            "raw_data": raw,
            "synced_at": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

    @staticmethod
    def normalize_gst_data(raw: Dict[str, Any], user_id: str, connection_id: str) -> Dict[str, Any]:
        """Normalize GST return data to unified format."""
        return {
            "user_id": user_id,
            "connection_id": connection_id,
            "source_platform": "gst_portal",
            "data_type": "gst_return",
            "reference_id": raw.get("gstin", ""),
            "reference_number": raw.get("return_period", ""),
            "date": datetime.now(timezone.utc),
            "currency": "INR",
            "amount": raw.get("total_taxable_value", 0),
            "tax_amount": raw.get("total_tax", 0),
            "total_amount": raw.get("total_taxable_value", 0) + raw.get("total_tax", 0),
            "balance_due": 0,
            "party_name": "GST Portal",
            "status": raw.get("filing_status", "unknown"),
            "description": f"GSTR Summary - {raw.get('return_period', '')}",
            "raw_data": raw,
            "synced_at": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

    @staticmethod
    def normalize_income_tax_data(raw: Dict[str, Any], user_id: str, connection_id: str) -> Dict[str, Any]:
        """Normalize Income Tax data to unified format."""
        return {
            "user_id": user_id,
            "connection_id": connection_id,
            "source_platform": "income_tax",
            "data_type": "tax_filing",
            "reference_id": raw.get("pan", ""),
            "reference_number": raw.get("pan", ""),
            "date": datetime.now(timezone.utc),
            "currency": "INR",
            "amount": 0,
            "tax_amount": 0,
            "total_amount": 0,
            "balance_due": 0,
            "party_name": raw.get("name", ""),
            "party_pan": raw.get("pan", ""),
            "status": raw.get("status", "unknown"),
            "description": f"PAN: {raw.get('pan', '')} - {raw.get('name', '')}",
            "raw_data": raw,
            "synced_at": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

    @staticmethod
    def _parse_date(date_value) -> datetime:
        """Parse various date formats into datetime."""
        if date_value is None:
            return datetime.now(timezone.utc)
        if isinstance(date_value, datetime):
            return date_value
        if isinstance(date_value, str):
            try:
                return date_parser.parse(date_value)
            except (ValueError, TypeError):
                return datetime.now(timezone.utc)
        return datetime.now(timezone.utc)
