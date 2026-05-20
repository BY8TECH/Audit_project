"""GST Portal mock data provider - Realistic Indian GST data."""

from datetime import datetime, timezone
from typing import List, Dict, Any


GSTIN_RECORDS = [
    {
        "gstin": "27AABCT1234F1Z5",
        "legal_name": "TechNova Solutions Pvt Ltd",
        "trade_name": "TechNova Solutions",
        "registration_date": "2018-07-01",
        "status": "Active",
        "taxpayer_type": "Regular",
        "constitution": "Private Limited Company",
        "state": "Maharashtra",
        "state_code": "27",
        "principal_place": "301, Tech Park, Bandra Kurla Complex, Mumbai 400051, Maharashtra",
        "additional_places": [
            "5th Floor, IT Tower, Hinjewadi Phase 2, Pune 411057, Maharashtra"
        ],
        "nature_of_business": ["IT Services", "Software Development", "Consulting"],
        "hsn_info": ["998314", "998315", "998316"],
        "filing_frequency": "Monthly",
        "last_return_filed": "GSTR-3B",
        "last_return_period": "March 2026",
        "aadhaar_verified": True,
        "pan": "AABCT1234F",
        "email": "gst@technova.in",
        "mobile": "9876543210",
    },
    {
        "gstin": "29AABCI1234F1Z5",
        "legal_name": "TechNova Solutions Pvt Ltd",
        "trade_name": "TechNova Solutions - Bangalore",
        "registration_date": "2019-01-15",
        "status": "Active",
        "taxpayer_type": "Regular",
        "constitution": "Private Limited Company",
        "state": "Karnataka",
        "state_code": "29",
        "principal_place": "44 Electronics City, Hosur Road, Bangalore 560100, Karnataka",
        "additional_places": [],
        "nature_of_business": ["IT Services", "Software Development"],
        "hsn_info": ["998314", "998315"],
        "filing_frequency": "Monthly",
        "last_return_filed": "GSTR-3B",
        "last_return_period": "March 2026",
        "aadhaar_verified": True,
        "pan": "AABCT1234F",
        "email": "gst.blr@technova.in",
        "mobile": "9876543211",
    },
    {
        "gstin": "07AABCT1234F1Z5",
        "legal_name": "TechNova Solutions Pvt Ltd",
        "trade_name": "TechNova Solutions - Delhi",
        "registration_date": "2019-06-01",
        "status": "Active",
        "taxpayer_type": "Regular",
        "constitution": "Private Limited Company",
        "state": "Delhi",
        "state_code": "07",
        "principal_place": "Tower B, 3rd Floor, Cyber City, Gurgaon 122002, Haryana/Delhi NCR",
        "additional_places": [],
        "nature_of_business": ["IT Services", "Consulting"],
        "hsn_info": ["998314"],
        "filing_frequency": "Monthly",
        "last_return_filed": "GSTR-1",
        "last_return_period": "March 2026",
        "aadhaar_verified": True,
        "pan": "AABCT1234F",
        "email": "gst.del@technova.in",
        "mobile": "9876543212",
    },
    {
        "gstin": "33AABCT1234F1Z5",
        "legal_name": "TechNova Solutions Pvt Ltd",
        "trade_name": "TechNova Solutions - Chennai",
        "registration_date": "2020-04-01",
        "status": "Active",
        "taxpayer_type": "Regular",
        "constitution": "Private Limited Company",
        "state": "Tamil Nadu",
        "state_code": "33",
        "principal_place": "No 12, Rajiv Gandhi Salai, Taramani, Chennai 600113, Tamil Nadu",
        "additional_places": [],
        "nature_of_business": ["IT Services"],
        "hsn_info": ["998314", "998316"],
        "filing_frequency": "Monthly",
        "last_return_filed": "GSTR-3B",
        "last_return_period": "February 2026",
        "aadhaar_verified": True,
        "pan": "AABCT1234F",
        "email": "gst.chn@technova.in",
        "mobile": "9876543213",
    },
    {
        "gstin": "24AABCT1234F1Z5",
        "legal_name": "TechNova Solutions Pvt Ltd",
        "trade_name": "TechNova Solutions - Ahmedabad",
        "registration_date": "2021-01-01",
        "status": "Active",
        "taxpayer_type": "Regular",
        "constitution": "Private Limited Company",
        "state": "Gujarat",
        "state_code": "24",
        "principal_place": "GIFT City, Block 5, Gandhinagar 382355, Gujarat",
        "additional_places": [],
        "nature_of_business": ["IT Services", "Software Development"],
        "hsn_info": ["998314"],
        "filing_frequency": "Monthly",
        "last_return_filed": "GSTR-3B",
        "last_return_period": "March 2026",
        "aadhaar_verified": True,
        "pan": "AABCT1234F",
        "email": "gst.ahd@technova.in",
        "mobile": "9876543214",
    },
]


def generate_gstr1_summary() -> Dict[str, Any]:
    """Generate GSTR-1 summary data (Outward supplies)."""
    return {
        "gstin": "27AABCT1234F1Z5",
        "return_period": "March 2026",
        "filing_status": "Filed",
        "filing_date": "2026-04-11",
        "sections": {
            "b2b": {
                "description": "Invoices for registered recipients (B2B)",
                "number_of_recipients": 28,
                "number_of_invoices": 45,
                "total_taxable_value": 12500000.00,
                "total_igst": 450000.00,
                "total_cgst": 675000.00,
                "total_sgst": 675000.00,
                "total_cess": 0.00,
                "total_invoice_value": 14300000.00,
            },
            "b2cs": {
                "description": "Supplies to unregistered persons (B2CS)",
                "number_of_invoices": 12,
                "total_taxable_value": 850000.00,
                "total_cgst": 76500.00,
                "total_sgst": 76500.00,
                "total_cess": 0.00,
            },
            "b2cl": {
                "description": "Invoices for unregistered persons > 2.5L (B2CL)",
                "number_of_invoices": 3,
                "total_taxable_value": 1200000.00,
                "total_igst": 216000.00,
                "total_cess": 0.00,
            },
            "cdnr": {
                "description": "Credit/Debit Notes (Registered)",
                "number_of_notes": 5,
                "total_taxable_value": -350000.00,
                "total_igst": -12600.00,
                "total_cgst": -25200.00,
                "total_sgst": -25200.00,
            },
            "exp": {
                "description": "Export Invoices",
                "number_of_invoices": 2,
                "total_taxable_value": 2500000.00,
                "total_igst": 0.00,
                "shipping_bill_number": "SB-2026-0045",
                "shipping_bill_date": "2026-03-15",
            },
            "hsn_summary": [
                {"hsn_code": "998314", "description": "IT Consulting Services", "uqc": "OTH", "total_quantity": 150, "taxable_value": 9500000.00, "igst": 342000.00, "cgst": 513000.00, "sgst": 513000.00},
                {"hsn_code": "998315", "description": "Cloud & Hosting Services", "uqc": "OTH", "total_quantity": 85, "taxable_value": 3200000.00, "igst": 115200.00, "cgst": 172800.00, "sgst": 172800.00},
                {"hsn_code": "998316", "description": "Data Analytics Services", "uqc": "OTH", "total_quantity": 45, "taxable_value": 2850000.00, "igst": 102600.00, "cgst": 153900.00, "sgst": 153900.00},
                {"hsn_code": "852392", "description": "Software License", "uqc": "NOS", "total_quantity": 30, "taxable_value": 1500000.00, "igst": 54000.00, "cgst": 81000.00, "sgst": 81000.00},
            ],
        },
        "total_taxable_value": 16700000.00,
        "total_tax": 3006000.00,
        "total_igst": 666000.00,
        "total_cgst": 1170000.00,
        "total_sgst": 1170000.00,
        "total_cess": 0.00,
    }


def generate_gstr3b_summary() -> Dict[str, Any]:
    """Generate GSTR-3B summary data."""
    return {
        "gstin": "27AABCT1234F1Z5",
        "return_period": "March 2026",
        "filing_status": "Filed",
        "filing_date": "2026-04-20",
        "sections": {
            "3_1": {
                "description": "Details of Outward Supplies and Inward Supplies liable to reverse charge",
                "outward_taxable": {
                    "taxable_value": 14550000.00,
                    "igst": 523800.00,
                    "cgst": 784200.00,
                    "sgst": 784200.00,
                    "cess": 0.00,
                },
                "outward_zero_rated": {
                    "taxable_value": 2500000.00,
                    "igst": 0.00,
                    "cgst": 0.00,
                    "sgst": 0.00,
                    "cess": 0.00,
                },
                "outward_nil_rated": {
                    "taxable_value": 150000.00,
                    "igst": 0.00,
                    "cgst": 0.00,
                    "sgst": 0.00,
                    "cess": 0.00,
                },
                "inward_reverse_charge": {
                    "taxable_value": 500000.00,
                    "igst": 18000.00,
                    "cgst": 27000.00,
                    "sgst": 27000.00,
                    "cess": 0.00,
                },
            },
            "3_2": {
                "description": "Inter-State Supplies",
                "supplies_to_unregistered": 850000.00,
                "supplies_to_composition": 0.00,
                "supplies_to_uin_holders": 0.00,
            },
            "4": {
                "description": "Eligible ITC",
                "itc_available": {
                    "igst": 295000.00,
                    "cgst": 380000.00,
                    "sgst": 380000.00,
                    "cess": 0.00,
                },
                "itc_reversed": {
                    "igst": 12000.00,
                    "cgst": 15000.00,
                    "sgst": 15000.00,
                    "cess": 0.00,
                },
                "net_itc": {
                    "igst": 283000.00,
                    "cgst": 365000.00,
                    "sgst": 365000.00,
                    "cess": 0.00,
                },
            },
            "5": {
                "description": "Values of exempt, nil-rated and non-GST inward supplies",
                "from_registered": 250000.00,
                "from_unregistered": 75000.00,
            },
            "6_1": {
                "description": "Payment of Tax",
                "igst": {"tax_payable": 240800.00, "paid_through_itc": 195000.00, "paid_in_cash": 45800.00},
                "cgst": {"tax_payable": 419200.00, "paid_through_itc": 320000.00, "paid_in_cash": 99200.00},
                "sgst": {"tax_payable": 419200.00, "paid_through_itc": 320000.00, "paid_in_cash": 99200.00},
                "cess": {"tax_payable": 0.00, "paid_through_itc": 0.00, "paid_in_cash": 0.00},
            },
        },
        "total_tax_liability": 1079200.00,
        "total_itc_claimed": 835000.00,
        "total_cash_paid": 244200.00,
        "late_fee": {"cgst": 0.00, "sgst": 0.00},
        "interest": 0.00,
    }


def generate_gstr1_monthly_history() -> List[Dict[str, Any]]:
    """Generate 6-month GSTR-1 filing history."""
    months = [
        ("October 2025", "2025-11-10", 11800000.00),
        ("November 2025", "2025-12-09", 13200000.00),
        ("December 2025", "2026-01-11", 14500000.00),
        ("January 2026", "2026-02-10", 12900000.00),
        ("February 2026", "2026-03-11", 15100000.00),
        ("March 2026", "2026-04-11", 16700000.00),
    ]

    history = []
    for period, filing_date, taxable_value in months:
        tax = round(taxable_value * 0.18, 2)
        history.append({
            "return_period": period,
            "filing_status": "Filed",
            "filing_date": filing_date,
            "total_taxable_value": taxable_value,
            "total_tax": tax,
            "total_invoices": 40 + hash(period) % 20,
            "arn": f"AA270526{hash(period) % 100000:06d}",
        })
    return history


class GSTMockProvider:
    """Provides mock GST Portal data."""

    def __init__(self):
        self._gstin_records = None
        self._gstr1_summary = None
        self._gstr3b_summary = None
        self._gstr1_history = None

    def get_gstin_records(self) -> List[Dict[str, Any]]:
        if self._gstin_records is None:
            self._gstin_records = GSTIN_RECORDS
        return self._gstin_records

    def get_gstr1_summary(self) -> Dict[str, Any]:
        if self._gstr1_summary is None:
            self._gstr1_summary = generate_gstr1_summary()
        return self._gstr1_summary

    def get_gstr3b_summary(self) -> Dict[str, Any]:
        if self._gstr3b_summary is None:
            self._gstr3b_summary = generate_gstr3b_summary()
        return self._gstr3b_summary

    def get_filing_history(self) -> List[Dict[str, Any]]:
        if self._gstr1_history is None:
            self._gstr1_history = generate_gstr1_monthly_history()
        return self._gstr1_history

    def verify_gstin(self, gstin: str) -> Dict[str, Any]:
        """Verify a GSTIN and return details."""
        for record in GSTIN_RECORDS:
            if record["gstin"] == gstin:
                return {"valid": True, "details": record}
        return {"valid": False, "details": None, "message": "GSTIN not found"}
