"""Income Tax Portal mock data provider - Realistic Indian tax data."""

from typing import List, Dict, Any


PAN_RECORDS = [
    {
        "pan": "AABCT1234F",
        "name": "TechNova Solutions Pvt Ltd",
        "type": "Company",
        "status": "Active",
        "aadhaar_linked": True,
        "jurisdiction": "Mumbai",
        "assessment_officer": "Ward 4(3)(2), Mumbai",
        "filing_status": {
            "ay_2025_26": {
                "assessment_year": "2025-26",
                "return_type": "ITR-6",
                "filing_date": "2025-10-15",
                "status": "Filed - Processed",
                "acknowledgement_number": "CPC/2526/A123456789",
                "total_income": 58500000.00,
                "tax_payable": 15210000.00,
                "tax_paid": 15210000.00,
                "refund_amount": 0.00,
                "verification_status": "e-Verified",
            },
            "ay_2024_25": {
                "assessment_year": "2024-25",
                "return_type": "ITR-6",
                "filing_date": "2024-10-31",
                "status": "Filed - Processed",
                "acknowledgement_number": "CPC/2425/B987654321",
                "total_income": 48200000.00,
                "tax_payable": 12532000.00,
                "tax_paid": 12532000.00,
                "refund_amount": 85000.00,
                "verification_status": "e-Verified",
            },
        },
        "tds_summary": {
            "fy_2025_26": {
                "financial_year": "2025-26",
                "total_tds_deducted": 5850000.00,
                "total_tds_deposited": 5850000.00,
                "quarters": [
                    {"quarter": "Q1 (Apr-Jun)", "tds_deducted": 1350000.00, "tds_deposited": 1350000.00, "challan_count": 15, "status": "Filed"},
                    {"quarter": "Q2 (Jul-Sep)", "tds_deducted": 1425000.00, "tds_deposited": 1425000.00, "challan_count": 18, "status": "Filed"},
                    {"quarter": "Q3 (Oct-Dec)", "tds_deducted": 1575000.00, "tds_deposited": 1575000.00, "challan_count": 16, "status": "Filed"},
                    {"quarter": "Q4 (Jan-Mar)", "tds_deducted": 1500000.00, "tds_deposited": 1500000.00, "challan_count": 17, "status": "Filed"},
                ],
            },
        },
        "advance_tax": {
            "fy_2025_26": {
                "financial_year": "2025-26",
                "installments": [
                    {"due_date": "2025-06-15", "amount_due": 2280000.00, "amount_paid": 2280000.00, "challan_number": "BSR-0026-0001", "payment_date": "2025-06-14", "status": "Paid"},
                    {"due_date": "2025-09-15", "amount_due": 3420000.00, "amount_paid": 3420000.00, "challan_number": "BSR-0026-0002", "payment_date": "2025-09-12", "status": "Paid"},
                    {"due_date": "2025-12-15", "amount_due": 5700000.00, "amount_paid": 5700000.00, "challan_number": "BSR-0026-0003", "payment_date": "2025-12-13", "status": "Paid"},
                    {"due_date": "2026-03-15", "amount_due": 3810000.00, "amount_paid": 3810000.00, "challan_number": "BSR-0026-0004", "payment_date": "2026-03-14", "status": "Paid"},
                ],
                "total_due": 15210000.00,
                "total_paid": 15210000.00,
            },
        },
    },
    {
        "pan": "BQJPK5678G",
        "name": "Rajesh Kumar",
        "type": "Individual",
        "status": "Active",
        "aadhaar_linked": True,
        "jurisdiction": "Mumbai",
        "assessment_officer": "Ward 1(1)(1), Mumbai",
        "filing_status": {
            "ay_2025_26": {
                "assessment_year": "2025-26",
                "return_type": "ITR-2",
                "filing_date": "2025-07-28",
                "status": "Filed - Processed",
                "acknowledgement_number": "CPC/2526/C456789012",
                "total_income": 3200000.00,
                "tax_payable": 520000.00,
                "tax_paid": 520000.00,
                "refund_amount": 15000.00,
                "verification_status": "e-Verified",
            },
        },
        "tds_summary": {
            "fy_2025_26": {
                "financial_year": "2025-26",
                "total_tds_deducted": 320000.00,
                "total_tds_deposited": 320000.00,
                "quarters": [
                    {"quarter": "Q1 (Apr-Jun)", "tds_deducted": 80000.00, "tds_deposited": 80000.00, "challan_count": 1, "status": "Filed"},
                    {"quarter": "Q2 (Jul-Sep)", "tds_deducted": 80000.00, "tds_deposited": 80000.00, "challan_count": 1, "status": "Filed"},
                    {"quarter": "Q3 (Oct-Dec)", "tds_deducted": 80000.00, "tds_deposited": 80000.00, "challan_count": 1, "status": "Filed"},
                    {"quarter": "Q4 (Jan-Mar)", "tds_deducted": 80000.00, "tds_deposited": 80000.00, "challan_count": 1, "status": "Filed"},
                ],
            },
        },
        "advance_tax": {"fy_2025_26": {"financial_year": "2025-26", "installments": [], "total_due": 0, "total_paid": 0}},
    },
    {
        "pan": "CXMPD9012H",
        "name": "Priya Desai",
        "type": "Individual",
        "status": "Active",
        "aadhaar_linked": True,
        "jurisdiction": "Bangalore",
        "assessment_officer": "Ward 2(1), Bangalore",
        "filing_status": {
            "ay_2025_26": {
                "assessment_year": "2025-26",
                "return_type": "ITR-1",
                "filing_date": "2025-07-15",
                "status": "Filed - Processed",
                "acknowledgement_number": "CPC/2526/D789012345",
                "total_income": 1850000.00,
                "tax_payable": 195000.00,
                "tax_paid": 195000.00,
                "refund_amount": 0.00,
                "verification_status": "e-Verified",
            },
        },
        "tds_summary": {
            "fy_2025_26": {
                "financial_year": "2025-26",
                "total_tds_deducted": 185000.00,
                "total_tds_deposited": 185000.00,
                "quarters": [
                    {"quarter": "Q1 (Apr-Jun)", "tds_deducted": 46250.00, "tds_deposited": 46250.00, "challan_count": 1, "status": "Filed"},
                    {"quarter": "Q2 (Jul-Sep)", "tds_deducted": 46250.00, "tds_deposited": 46250.00, "challan_count": 1, "status": "Filed"},
                    {"quarter": "Q3 (Oct-Dec)", "tds_deducted": 46250.00, "tds_deposited": 46250.00, "challan_count": 1, "status": "Filed"},
                    {"quarter": "Q4 (Jan-Mar)", "tds_deducted": 46250.00, "tds_deposited": 46250.00, "challan_count": 1, "status": "Filed"},
                ],
            },
        },
        "advance_tax": {"fy_2025_26": {"financial_year": "2025-26", "installments": [], "total_due": 0, "total_paid": 0}},
    },
]


class IncomeTaxMockProvider:
    """Provides mock Income Tax Portal data."""

    def __init__(self):
        self._pan_records = None

    def get_pan_records(self) -> List[Dict[str, Any]]:
        if self._pan_records is None:
            self._pan_records = PAN_RECORDS
        return self._pan_records

    def verify_pan(self, pan: str) -> Dict[str, Any]:
        """Verify a PAN and return details."""
        for record in PAN_RECORDS:
            if record["pan"] == pan:
                return {
                    "valid": True,
                    "pan": record["pan"],
                    "name": record["name"],
                    "type": record["type"],
                    "status": record["status"],
                    "aadhaar_linked": record["aadhaar_linked"],
                }
        return {"valid": False, "pan": pan, "message": "PAN not found in records"}

    def get_filing_status(self, pan: str) -> Dict[str, Any]:
        """Get filing status for a PAN."""
        for record in PAN_RECORDS:
            if record["pan"] == pan:
                return record.get("filing_status", {})
        return {}

    def get_tds_summary(self, pan: str) -> Dict[str, Any]:
        """Get TDS summary for a PAN."""
        for record in PAN_RECORDS:
            if record["pan"] == pan:
                return record.get("tds_summary", {})
        return {}

    def get_advance_tax(self, pan: str) -> Dict[str, Any]:
        """Get advance tax details for a PAN."""
        for record in PAN_RECORDS:
            if record["pan"] == pan:
                return record.get("advance_tax", {})
        return {}
