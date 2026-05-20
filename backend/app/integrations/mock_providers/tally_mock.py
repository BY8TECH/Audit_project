"""Tally Prime mock data provider - Realistic Indian financial data."""

from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
import random

# Tally uses voucher-based system
VOUCHER_TYPES = ["Sales", "Purchase", "Receipt", "Payment", "Journal", "Contra", "Credit Note", "Debit Note"]

PARTY_NAMES = [
    "Reliance Industries Ltd", "Tata Consultancy Services", "HDFC Bank Ltd",
    "Infosys Ltd", "Hindustan Unilever Ltd", "Bharti Airtel Ltd",
    "State Bank of India", "ITC Limited", "Kotak Mahindra Bank",
    "Bajaj Finance Ltd", "Maruti Suzuki India Ltd", "Asian Paints Ltd",
    "Titan Company Ltd", "Nestle India Ltd", "Dabur India Ltd",
    "Godrej Consumer Products", "Cipla Ltd", "Dr Reddy's Laboratories",
    "Adani Green Energy Ltd", "Ambuja Cements Ltd", "Pidilite Industries",
    "Marico Ltd", "Berger Paints India", "Havells India Ltd",
    "Voltas Ltd", "Crompton Greaves", "Blue Star Ltd",
    "Whirlpool India Ltd", "Siemens India Ltd", "ABB India Ltd",
]

TALLY_LEDGERS_DATA = [
    {"name": "Sales Account", "group": "Sales Accounts", "opening_balance": 0, "closing_balance": 15250000.00, "nature": "Credit"},
    {"name": "Purchase Account", "group": "Purchase Accounts", "opening_balance": 0, "closing_balance": 8500000.00, "nature": "Debit"},
    {"name": "Salary Account", "group": "Indirect Expenses", "opening_balance": 0, "closing_balance": 4200000.00, "nature": "Debit"},
    {"name": "Rent Paid", "group": "Indirect Expenses", "opening_balance": 0, "closing_balance": 1080000.00, "nature": "Debit"},
    {"name": "Electricity Charges", "group": "Indirect Expenses", "opening_balance": 0, "closing_balance": 360000.00, "nature": "Debit"},
    {"name": "Telephone Expenses", "group": "Indirect Expenses", "opening_balance": 0, "closing_balance": 145000.00, "nature": "Debit"},
    {"name": "Printing & Stationery", "group": "Indirect Expenses", "opening_balance": 0, "closing_balance": 85000.00, "nature": "Debit"},
    {"name": "Travelling Expenses", "group": "Indirect Expenses", "opening_balance": 0, "closing_balance": 275000.00, "nature": "Debit"},
    {"name": "Professional Charges", "group": "Indirect Expenses", "opening_balance": 0, "closing_balance": 480000.00, "nature": "Debit"},
    {"name": "Depreciation", "group": "Indirect Expenses", "opening_balance": 0, "closing_balance": 620000.00, "nature": "Debit"},
    {"name": "Interest Received", "group": "Indirect Income", "opening_balance": 0, "closing_balance": 285000.00, "nature": "Credit"},
    {"name": "Discount Received", "group": "Indirect Income", "opening_balance": 0, "closing_balance": 125000.00, "nature": "Credit"},
    {"name": "Cash", "group": "Cash-in-Hand", "opening_balance": 350000.00, "closing_balance": 215000.00, "nature": "Debit"},
    {"name": "HDFC Bank Current A/c", "group": "Bank Accounts", "opening_balance": 2800000.00, "closing_balance": 3650000.00, "nature": "Debit"},
    {"name": "SBI Savings A/c", "group": "Bank Accounts", "opening_balance": 1500000.00, "closing_balance": 1180000.00, "nature": "Debit"},
    {"name": "ICICI Bank FD", "group": "Bank Accounts", "opening_balance": 5000000.00, "closing_balance": 5000000.00, "nature": "Debit"},
    {"name": "Sundry Debtors", "group": "Sundry Debtors", "opening_balance": 3200000.00, "closing_balance": 4800000.00, "nature": "Debit"},
    {"name": "Sundry Creditors", "group": "Sundry Creditors", "opening_balance": 2500000.00, "closing_balance": 3100000.00, "nature": "Credit"},
    {"name": "CGST Input", "group": "Duties & Taxes", "opening_balance": 0, "closing_balance": 410000.00, "nature": "Debit"},
    {"name": "SGST Input", "group": "Duties & Taxes", "opening_balance": 0, "closing_balance": 410000.00, "nature": "Debit"},
    {"name": "IGST Input", "group": "Duties & Taxes", "opening_balance": 0, "closing_balance": 195000.00, "nature": "Debit"},
    {"name": "CGST Output", "group": "Duties & Taxes", "opening_balance": 0, "closing_balance": 520000.00, "nature": "Credit"},
    {"name": "SGST Output", "group": "Duties & Taxes", "opening_balance": 0, "closing_balance": 520000.00, "nature": "Credit"},
    {"name": "IGST Output", "group": "Duties & Taxes", "opening_balance": 0, "closing_balance": 310000.00, "nature": "Credit"},
    {"name": "Capital Account", "group": "Capital Account", "opening_balance": 10000000.00, "closing_balance": 10000000.00, "nature": "Credit"},
]


def _base_date() -> datetime:
    return datetime(2026, 5, 20, tzinfo=timezone.utc)


def _random_date_within(months_back: int = 6) -> datetime:
    base = _base_date()
    days_back = random.randint(0, months_back * 30)
    return base - timedelta(days=days_back)


def generate_vouchers() -> List[Dict[str, Any]]:
    """Generate 40 realistic Tally Prime vouchers."""
    random.seed(55)
    vouchers = []

    for i in range(1, 41):
        v_type = random.choice(VOUCHER_TYPES)
        party = random.choice(PARTY_NAMES)
        date = _random_date_within(6)

        # Different amounts based on voucher type
        if v_type == "Sales":
            amount = round(random.uniform(50000, 1500000), 2)
            debit_ledger = "Sundry Debtors"
            credit_ledger = "Sales Account"
        elif v_type == "Purchase":
            amount = round(random.uniform(25000, 800000), 2)
            debit_ledger = "Purchase Account"
            credit_ledger = "Sundry Creditors"
        elif v_type == "Receipt":
            amount = round(random.uniform(50000, 2000000), 2)
            debit_ledger = "HDFC Bank Current A/c"
            credit_ledger = "Sundry Debtors"
        elif v_type == "Payment":
            amount = round(random.uniform(25000, 1000000), 2)
            debit_ledger = "Sundry Creditors"
            credit_ledger = "HDFC Bank Current A/c"
        elif v_type == "Journal":
            amount = round(random.uniform(10000, 500000), 2)
            debit_ledger = random.choice(["Salary Account", "Rent Paid", "Professional Charges"])
            credit_ledger = random.choice(["HDFC Bank Current A/c", "SBI Savings A/c"])
        elif v_type == "Contra":
            amount = round(random.uniform(100000, 2000000), 2)
            debit_ledger = "HDFC Bank Current A/c"
            credit_ledger = "Cash"
        elif v_type == "Credit Note":
            amount = round(random.uniform(5000, 200000), 2)
            debit_ledger = "Sales Account"
            credit_ledger = "Sundry Debtors"
        else:  # Debit Note
            amount = round(random.uniform(5000, 150000), 2)
            debit_ledger = "Sundry Creditors"
            credit_ledger = "Purchase Account"

        # Calculate GST
        is_inter_state = random.random() > 0.6
        gst_rate = 0.18
        tax_amount = round(amount * gst_rate, 2)
        total = round(amount + tax_amount, 2)

        voucher = {
            "voucher_id": f"V-{date.strftime('%Y%m%d')}-{i:04d}",
            "voucher_number": f"{i}",
            "voucher_type": v_type,
            "date": date.isoformat(),
            "reference_number": f"REF/{v_type[:3].upper()}/{date.strftime('%y%m')}/{i:04d}",
            "party_name": party,
            "amount": amount,
            "tax_amount": tax_amount,
            "total_amount": total,
            "narration": f"{v_type} - {party} - {date.strftime('%B %Y')}",
            "is_cancelled": False,
            "is_optional": False,
            "ledger_entries": [
                {"ledger_name": debit_ledger, "amount": total, "type": "Debit"},
                {"ledger_name": credit_ledger, "amount": total, "type": "Credit"},
            ],
            "cgst": 0 if is_inter_state else round(tax_amount / 2, 2),
            "sgst": 0 if is_inter_state else round(tax_amount / 2, 2),
            "igst": tax_amount if is_inter_state else 0,
            "inventory_entries": [],
            "created_time": date.isoformat(),
        }

        # Add inventory entries for Sales and Purchase vouchers
        if v_type in ["Sales", "Purchase"]:
            items_list = [
                "Computer Hardware", "Software License", "Networking Equipment",
                "Office Furniture", "Consulting Services", "Cloud Services",
                "Training Services", "Maintenance Contract", "Security Solutions",
            ]
            item_name = random.choice(items_list)
            qty = random.randint(1, 20)
            rate = round(amount / qty, 2)
            voucher["inventory_entries"] = [
                {
                    "item_name": item_name,
                    "quantity": qty,
                    "rate": rate,
                    "amount": amount,
                    "godown": "Main Godown",
                }
            ]

        vouchers.append(voucher)

    return vouchers


def generate_ledgers() -> List[Dict[str, Any]]:
    """Generate 25 realistic Tally Prime ledgers."""
    ledgers = []
    for idx, ledger_data in enumerate(TALLY_LEDGERS_DATA, 1):
        ledger = {
            "ledger_id": f"LDG-{idx:04d}",
            "ledger_name": ledger_data["name"],
            "parent_group": ledger_data["group"],
            "opening_balance": ledger_data["opening_balance"],
            "closing_balance": ledger_data["closing_balance"],
            "debit_total": ledger_data["closing_balance"] if ledger_data["nature"] == "Debit" else 0,
            "credit_total": ledger_data["closing_balance"] if ledger_data["nature"] == "Credit" else 0,
            "nature": ledger_data["nature"],
            "currency": "INR",
            "is_revenue": ledger_data["group"] in ["Sales Accounts", "Indirect Income"],
            "is_expense": ledger_data["group"] in ["Purchase Accounts", "Indirect Expenses"],
            "address": "",
            "gstin": "",
            "pan": "",
        }
        ledgers.append(ledger)
    return ledgers


def generate_tally_trial_balance() -> Dict[str, Any]:
    """Generate Tally Prime trial balance."""
    ledgers = generate_ledgers()
    debit_total = sum(l["closing_balance"] for l in ledgers if l["nature"] == "Debit")
    credit_total = sum(l["closing_balance"] for l in ledgers if l["nature"] == "Credit")

    entries = []
    for l in ledgers:
        entries.append({
            "ledger_name": l["ledger_name"],
            "parent_group": l["parent_group"],
            "debit": l["closing_balance"] if l["nature"] == "Debit" else 0,
            "credit": l["closing_balance"] if l["nature"] == "Credit" else 0,
        })

    return {
        "report_name": "Trial Balance",
        "company_name": "TechNova Solutions Pvt Ltd",
        "from_date": "2025-11-01",
        "to_date": "2026-04-30",
        "currency": "INR",
        "entries": entries,
        "total_debit": round(debit_total, 2),
        "total_credit": round(credit_total, 2),
        "difference": round(debit_total - credit_total, 2),
    }


class TallyMockProvider:
    """Provides mock Tally Prime data."""

    def __init__(self):
        self._vouchers = None
        self._ledgers = None
        self._trial_balance = None

    def get_vouchers(self) -> List[Dict[str, Any]]:
        if self._vouchers is None:
            self._vouchers = generate_vouchers()
        return self._vouchers

    def get_ledgers(self) -> List[Dict[str, Any]]:
        if self._ledgers is None:
            self._ledgers = generate_ledgers()
        return self._ledgers

    def get_trial_balance(self) -> Dict[str, Any]:
        if self._trial_balance is None:
            self._trial_balance = generate_tally_trial_balance()
        return self._trial_balance
