"""Zoho Books mock data provider - Realistic Indian financial data."""

from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
import random

# Indian company names for customers/vendors
CUSTOMERS = [
    {"name": "Reliance Industries Ltd", "gstin": "27AABCR5758R1ZP", "pan": "AABCR5758R", "address": "3rd Floor, Maker Chambers IV, Nariman Point, Mumbai 400021, Maharashtra"},
    {"name": "Tata Motors Ltd", "gstin": "27AABCT1424E1ZX", "pan": "AABCT1424E", "address": "Bombay House, 24 Homi Mody Street, Mumbai 400001, Maharashtra"},
    {"name": "Infosys Ltd", "gstin": "29AABCI1234F1Z5", "pan": "AABCI1234F", "address": "44 Electronics City, Hosur Road, Bangalore 560100, Karnataka"},
    {"name": "Wipro Ltd", "gstin": "29AABCW5678G1Z8", "pan": "AABCW5678G", "address": "Doddakannelli, Sarjapur Road, Bangalore 560035, Karnataka"},
    {"name": "HCL Technologies Ltd", "gstin": "09AABCH1234H1Z2", "pan": "AABCH1234H", "address": "Plot No. 3A, Sector 126, Noida 201304, Uttar Pradesh"},
    {"name": "Bharti Airtel Ltd", "gstin": "07AABCB9876J1Z1", "pan": "AABCB9876J", "address": "Bharti Crescent, 1 Nelson Mandela Road, New Delhi 110070"},
    {"name": "Larsen & Toubro Ltd", "gstin": "27AABCL4321K1Z9", "pan": "AABCL4321K", "address": "L&T House, Ballard Estate, Mumbai 400001, Maharashtra"},
    {"name": "Asian Paints Ltd", "gstin": "27AABCA8765L1Z3", "pan": "AABCA8765L", "address": "6A Shantinagar, Santacruz East, Mumbai 400055, Maharashtra"},
    {"name": "Maruti Suzuki India Ltd", "gstin": "06AABCM2345M1Z7", "pan": "AABCM2345M", "address": "1 Nelson Mandela Road, Vasant Kunj, New Delhi 110070"},
    {"name": "Sun Pharmaceutical Industries", "gstin": "24AABCS6789N1Z4", "pan": "AABCS6789N", "address": "SPARC, Tandalja, Vadodara 390012, Gujarat"},
    {"name": "Mahindra & Mahindra Ltd", "gstin": "27AABCM7890P1Z6", "pan": "AABCM7890P", "address": "Gateway Building, Apollo Bunder, Mumbai 400001, Maharashtra"},
    {"name": "ITC Limited", "gstin": "19AABCI5678Q1Z2", "pan": "AABCI5678Q", "address": "Virginia House, 37 J.L. Nehru Road, Kolkata 700071, West Bengal"},
    {"name": "HDFC Bank Ltd", "gstin": "27AABCH3456R1Z8", "pan": "AABCH3456R", "address": "HDFC House, Senapati Bapat Marg, Lower Parel, Mumbai 400013"},
    {"name": "Bajaj Auto Ltd", "gstin": "27AABCB1234S1Z5", "pan": "AABCB1234S", "address": "Mumbai-Pune Road, Akurdi, Pune 411035, Maharashtra"},
    {"name": "Godrej Consumer Products", "gstin": "27AABCG9012T1Z1", "pan": "AABCG9012T", "address": "Godrej One, Pirojshanagar, Vikhroli, Mumbai 400079, Maharashtra"},
]

VENDORS = [
    {"name": "Tata Steel Ltd", "gstin": "20AABCT5678U1Z4", "pan": "AABCT5678U", "address": "Bombay House, 24 Homi Mody Street, Mumbai 400001, Maharashtra"},
    {"name": "JSW Steel Ltd", "gstin": "27AABCJ2345V1Z7", "pan": "AABCJ2345V", "address": "JSW Centre, Bandra Kurla Complex, Mumbai 400051, Maharashtra"},
    {"name": "Hindustan Unilever Ltd", "gstin": "27AABCH6789W1Z3", "pan": "AABCH6789W", "address": "Unilever House, B.D. Sawant Marg, Chakala, Mumbai 400099"},
    {"name": "Ultratech Cement Ltd", "gstin": "33AABCU1234X1Z9", "pan": "AABCU1234X", "address": "B Wing, Ahura Centre, Mahakali Caves Road, Mumbai 400093"},
    {"name": "ACC Limited", "gstin": "27AABCA4567Y1Z6", "pan": "AABCA4567Y", "address": "Cement House, 121 Maharshi Karve Road, Mumbai 400020"},
    {"name": "Grasim Industries Ltd", "gstin": "23AABCG8901Z1Z2", "pan": "AABCG8901Z", "address": "Birlagram, Nagda 456331, Madhya Pradesh"},
    {"name": "Adani Enterprises Ltd", "gstin": "24AABCA2345A2Z8", "pan": "AABCA2345A", "address": "Adani House, Nr Mithakhali Circle, Ahmedabad 380009, Gujarat"},
    {"name": "Bharat Petroleum Corp", "gstin": "27AABCB6789B2Z5", "pan": "AABCB6789B", "address": "Bharat Bhavan, 4&6 Currimbhoy Road, Ballard Estate, Mumbai 400001"},
    {"name": "Indian Oil Corporation", "gstin": "07AABCI1234C2Z1", "pan": "AABCI1234C", "address": "IndianOil Bhavan, 1 Sri Aurobindo Marg, New Delhi 110001"},
    {"name": "Power Grid Corporation", "gstin": "06AABCP5678D2Z7", "pan": "AABCP5678D", "address": "Plot No. 2, Sector 29, Gurgaon 122001, Haryana"},
]

# Product/Service items
ITEMS = [
    {"name": "IT Consulting Services", "hsn": "998314", "rate": 150000.0, "unit": "hrs"},
    {"name": "Software License - Annual", "hsn": "852392", "rate": 250000.0, "unit": "nos"},
    {"name": "Cloud Hosting - Monthly", "hsn": "998315", "rate": 45000.0, "unit": "nos"},
    {"name": "Data Analytics Services", "hsn": "998316", "rate": 200000.0, "unit": "hrs"},
    {"name": "Cybersecurity Audit", "hsn": "998317", "rate": 350000.0, "unit": "nos"},
    {"name": "ERP Implementation", "hsn": "998318", "rate": 500000.0, "unit": "nos"},
    {"name": "Network Infrastructure Setup", "hsn": "998319", "rate": 175000.0, "unit": "nos"},
    {"name": "Digital Marketing Services", "hsn": "998361", "rate": 85000.0, "unit": "nos"},
    {"name": "Mobile App Development", "hsn": "998314", "rate": 420000.0, "unit": "nos"},
    {"name": "AI/ML Model Training", "hsn": "998316", "rate": 380000.0, "unit": "hrs"},
    {"name": "Database Administration", "hsn": "998315", "rate": 95000.0, "unit": "hrs"},
    {"name": "Quality Assurance Testing", "hsn": "998314", "rate": 120000.0, "unit": "hrs"},
    {"name": "Technical Support - Annual", "hsn": "998318", "rate": 180000.0, "unit": "nos"},
    {"name": "API Integration Services", "hsn": "998314", "rate": 225000.0, "unit": "nos"},
    {"name": "UI/UX Design Services", "hsn": "998314", "rate": 160000.0, "unit": "hrs"},
]

PURCHASE_ITEMS = [
    {"name": "Server Hardware - Dell PowerEdge", "hsn": "847150", "rate": 285000.0, "unit": "nos"},
    {"name": "Office Supplies & Stationery", "hsn": "482090", "rate": 15000.0, "unit": "nos"},
    {"name": "Laptop - ThinkPad X1 Carbon", "hsn": "847130", "rate": 145000.0, "unit": "nos"},
    {"name": "Office Furniture - Workstations", "hsn": "940390", "rate": 45000.0, "unit": "nos"},
    {"name": "UPS System - 10KVA", "hsn": "850440", "rate": 175000.0, "unit": "nos"},
    {"name": "Networking Equipment - Cisco", "hsn": "851762", "rate": 95000.0, "unit": "nos"},
    {"name": "Air Conditioning - Industrial", "hsn": "841582", "rate": 220000.0, "unit": "nos"},
    {"name": "CCTV Security System", "hsn": "852580", "rate": 65000.0, "unit": "nos"},
    {"name": "Diesel Generator - 125KVA", "hsn": "850213", "rate": 850000.0, "unit": "nos"},
    {"name": "Fire Safety Equipment", "hsn": "842490", "rate": 125000.0, "unit": "nos"},
    {"name": "Printer - HP LaserJet Enterprise", "hsn": "844332", "rate": 75000.0, "unit": "nos"},
    {"name": "Software - Microsoft 365 Business", "hsn": "852392", "rate": 35000.0, "unit": "nos"},
]

STATES_CODES = {
    "Maharashtra": "27", "Karnataka": "29", "Tamil Nadu": "33",
    "Delhi": "07", "Gujarat": "24", "Uttar Pradesh": "09",
    "West Bengal": "19", "Rajasthan": "08", "Haryana": "06",
    "Madhya Pradesh": "23", "Telangana": "36", "Kerala": "32",
}

INVOICE_STATUSES = ["paid", "sent", "overdue", "partially_paid", "draft"]
BILL_STATUSES = ["paid", "received", "overdue", "partially_paid"]


def _base_date() -> datetime:
    return datetime(2026, 5, 20, tzinfo=timezone.utc)


def _random_date_within(months_back: int = 6) -> datetime:
    base = _base_date()
    days_back = random.randint(0, months_back * 30)
    return base - timedelta(days=days_back)


def _calc_gst(amount: float, is_inter_state: bool = False) -> Dict[str, float]:
    """Calculate GST (18%) - split into CGST+SGST or IGST."""
    gst_rate = 0.18
    tax = round(amount * gst_rate, 2)
    if is_inter_state:
        return {"cgst": 0, "sgst": 0, "igst": tax, "cess": 0, "tax_total": tax}
    else:
        half = round(tax / 2, 2)
        return {"cgst": half, "sgst": half, "igst": 0, "cess": 0, "tax_total": tax}


def generate_invoices() -> List[Dict[str, Any]]:
    """Generate 50 realistic Zoho Books invoices."""
    random.seed(42)
    invoices = []

    for i in range(1, 51):
        customer = random.choice(CUSTOMERS)
        item = random.choice(ITEMS)
        qty = random.randint(1, 5)
        is_inter_state = random.random() > 0.5
        date = _random_date_within(6)
        amount = round(item["rate"] * qty, 2)
        gst = _calc_gst(amount, is_inter_state)
        total = round(amount + gst["tax_total"], 2)
        status = random.choice(INVOICE_STATUSES)
        balance = 0.0 if status == "paid" else (round(total * random.uniform(0.3, 1.0), 2) if status == "partially_paid" else total)

        invoice = {
            "invoice_id": f"INV-2026-{i:04d}",
            "invoice_number": f"INV-2026-{i:04d}",
            "date": date.isoformat(),
            "due_date": (date + timedelta(days=random.choice([15, 30, 45, 60]))).isoformat(),
            "customer_name": customer["name"],
            "customer_gstin": customer["gstin"],
            "customer_pan": customer["pan"],
            "customer_address": customer["address"],
            "place_of_supply": random.choice(list(STATES_CODES.keys())),
            "status": status,
            "currency": "INR",
            "sub_total": amount,
            "tax_amount": gst["tax_total"],
            "total": total,
            "balance_due": balance,
            "cgst": gst["cgst"],
            "sgst": gst["sgst"],
            "igst": gst["igst"],
            "cess": gst["cess"],
            "line_items": [
                {
                    "item_name": item["name"],
                    "hsn_code": item["hsn"],
                    "quantity": qty,
                    "rate": item["rate"],
                    "amount": amount,
                    "unit": item["unit"],
                    "tax_percentage": 18.0,
                    "tax_amount": gst["tax_total"],
                }
            ],
            "notes": f"Thank you for your business with {customer['name']}.",
            "terms": "Payment due within 30 days of invoice date.",
            "created_time": date.isoformat(),
            "last_modified_time": date.isoformat(),
        }
        invoices.append(invoice)

    return invoices


def generate_bills() -> List[Dict[str, Any]]:
    """Generate 30 realistic Zoho Books bills."""
    random.seed(84)
    bills = []

    for i in range(1, 31):
        vendor = random.choice(VENDORS)
        item = random.choice(PURCHASE_ITEMS)
        qty = random.randint(1, 10)
        is_inter_state = random.random() > 0.5
        date = _random_date_within(6)
        amount = round(item["rate"] * qty, 2)
        gst = _calc_gst(amount, is_inter_state)
        total = round(amount + gst["tax_total"], 2)
        status = random.choice(BILL_STATUSES)
        balance = 0.0 if status == "paid" else (round(total * random.uniform(0.3, 1.0), 2) if status == "partially_paid" else total)

        bill = {
            "bill_id": f"BILL-2026-{i:04d}",
            "bill_number": f"BILL-2026-{i:04d}",
            "reference_number": f"VND-REF-{random.randint(10000,99999)}",
            "date": date.isoformat(),
            "due_date": (date + timedelta(days=random.choice([15, 30, 45]))).isoformat(),
            "vendor_name": vendor["name"],
            "vendor_gstin": vendor["gstin"],
            "vendor_pan": vendor["pan"],
            "vendor_address": vendor["address"],
            "place_of_supply": random.choice(list(STATES_CODES.keys())),
            "status": status,
            "currency": "INR",
            "sub_total": amount,
            "tax_amount": gst["tax_total"],
            "total": total,
            "balance_due": balance,
            "cgst": gst["cgst"],
            "sgst": gst["sgst"],
            "igst": gst["igst"],
            "cess": gst["cess"],
            "line_items": [
                {
                    "item_name": item["name"],
                    "hsn_code": item["hsn"],
                    "quantity": qty,
                    "rate": item["rate"],
                    "amount": amount,
                    "unit": item["unit"],
                    "tax_percentage": 18.0,
                    "tax_amount": gst["tax_total"],
                }
            ],
            "notes": f"Purchase from {vendor['name']}.",
            "created_time": date.isoformat(),
        }
        bills.append(bill)

    return bills


def generate_chart_of_accounts() -> List[Dict[str, Any]]:
    """Generate Zoho Books chart of accounts."""
    accounts = [
        {"account_id": "ACC001", "account_name": "Sales Revenue", "account_type": "income", "account_code": "4000", "balance": 12500000.00, "currency": "INR"},
        {"account_id": "ACC002", "account_name": "Service Revenue", "account_type": "income", "account_code": "4100", "balance": 8750000.00, "currency": "INR"},
        {"account_id": "ACC003", "account_name": "Interest Income", "account_type": "income", "account_code": "4200", "balance": 325000.00, "currency": "INR"},
        {"account_id": "ACC004", "account_name": "Other Income", "account_type": "income", "account_code": "4300", "balance": 175000.00, "currency": "INR"},
        {"account_id": "ACC005", "account_name": "Cost of Goods Sold", "account_type": "expense", "account_code": "5000", "balance": 5200000.00, "currency": "INR"},
        {"account_id": "ACC006", "account_name": "Salaries & Wages", "account_type": "expense", "account_code": "5100", "balance": 4800000.00, "currency": "INR"},
        {"account_id": "ACC007", "account_name": "Rent Expense", "account_type": "expense", "account_code": "5200", "balance": 1200000.00, "currency": "INR"},
        {"account_id": "ACC008", "account_name": "Utilities", "account_type": "expense", "account_code": "5300", "balance": 450000.00, "currency": "INR"},
        {"account_id": "ACC009", "account_name": "Depreciation", "account_type": "expense", "account_code": "5400", "balance": 680000.00, "currency": "INR"},
        {"account_id": "ACC010", "account_name": "Travel & Conveyance", "account_type": "expense", "account_code": "5500", "balance": 325000.00, "currency": "INR"},
        {"account_id": "ACC011", "account_name": "Professional Fees", "account_type": "expense", "account_code": "5600", "balance": 550000.00, "currency": "INR"},
        {"account_id": "ACC012", "account_name": "Insurance", "account_type": "expense", "account_code": "5700", "balance": 280000.00, "currency": "INR"},
        {"account_id": "ACC013", "account_name": "Marketing & Advertising", "account_type": "expense", "account_code": "5800", "balance": 420000.00, "currency": "INR"},
        {"account_id": "ACC014", "account_name": "Office Supplies", "account_type": "expense", "account_code": "5900", "balance": 95000.00, "currency": "INR"},
        {"account_id": "ACC015", "account_name": "Cash in Hand", "account_type": "asset", "account_code": "1000", "balance": 250000.00, "currency": "INR"},
        {"account_id": "ACC016", "account_name": "HDFC Bank Current A/c", "account_type": "asset", "account_code": "1100", "balance": 3450000.00, "currency": "INR"},
        {"account_id": "ACC017", "account_name": "ICICI Bank Savings A/c", "account_type": "asset", "account_code": "1110", "balance": 1250000.00, "currency": "INR"},
        {"account_id": "ACC018", "account_name": "Accounts Receivable", "account_type": "asset", "account_code": "1200", "balance": 4500000.00, "currency": "INR"},
        {"account_id": "ACC019", "account_name": "Fixed Deposits", "account_type": "asset", "account_code": "1300", "balance": 5000000.00, "currency": "INR"},
        {"account_id": "ACC020", "account_name": "Furniture & Fixtures", "account_type": "asset", "account_code": "1400", "balance": 850000.00, "currency": "INR"},
        {"account_id": "ACC021", "account_name": "Computer Equipment", "account_type": "asset", "account_code": "1410", "balance": 1200000.00, "currency": "INR"},
        {"account_id": "ACC022", "account_name": "Accounts Payable", "account_type": "liability", "account_code": "2000", "balance": 3200000.00, "currency": "INR"},
        {"account_id": "ACC023", "account_name": "GST Payable", "account_type": "liability", "account_code": "2100", "balance": 850000.00, "currency": "INR"},
        {"account_id": "ACC024", "account_name": "TDS Payable", "account_type": "liability", "account_code": "2200", "balance": 420000.00, "currency": "INR"},
        {"account_id": "ACC025", "account_name": "Capital Account", "account_type": "equity", "account_code": "3000", "balance": 10000000.00, "currency": "INR"},
        {"account_id": "ACC026", "account_name": "Retained Earnings", "account_type": "equity", "account_code": "3100", "balance": 5500000.00, "currency": "INR"},
        {"account_id": "ACC027", "account_name": "CGST Input Credit", "account_type": "asset", "account_code": "1500", "balance": 380000.00, "currency": "INR"},
        {"account_id": "ACC028", "account_name": "SGST Input Credit", "account_type": "asset", "account_code": "1510", "balance": 380000.00, "currency": "INR"},
        {"account_id": "ACC029", "account_name": "IGST Input Credit", "account_type": "asset", "account_code": "1520", "balance": 220000.00, "currency": "INR"},
        {"account_id": "ACC030", "account_name": "Provision for Bad Debts", "account_type": "liability", "account_code": "2300", "balance": 150000.00, "currency": "INR"},
    ]
    return accounts


def generate_trial_balance() -> Dict[str, Any]:
    """Generate Zoho Books trial balance."""
    accounts = generate_chart_of_accounts()
    debit_total = sum(a["balance"] for a in accounts if a["account_type"] in ["asset", "expense"])
    credit_total = sum(a["balance"] for a in accounts if a["account_type"] in ["liability", "equity", "income"])

    trial_balance_entries = []
    for acc in accounts:
        if acc["account_type"] in ["asset", "expense"]:
            trial_balance_entries.append({
                **acc,
                "debit": acc["balance"],
                "credit": 0.0,
            })
        else:
            trial_balance_entries.append({
                **acc,
                "debit": 0.0,
                "credit": acc["balance"],
            })

    return {
        "report_name": "Trial Balance",
        "organization_name": "TechNova Solutions Pvt Ltd",
        "from_date": "2025-11-01",
        "to_date": "2026-04-30",
        "currency": "INR",
        "entries": trial_balance_entries,
        "total_debit": round(debit_total, 2),
        "total_credit": round(credit_total, 2),
        "difference": round(debit_total - credit_total, 2),
    }


class ZohoMockProvider:
    """Provides mock Zoho Books data."""

    def __init__(self):
        self._invoices = None
        self._bills = None
        self._chart_of_accounts = None
        self._trial_balance = None

    def get_invoices(self) -> List[Dict[str, Any]]:
        if self._invoices is None:
            self._invoices = generate_invoices()
        return self._invoices

    def get_bills(self) -> List[Dict[str, Any]]:
        if self._bills is None:
            self._bills = generate_bills()
        return self._bills

    def get_chart_of_accounts(self) -> List[Dict[str, Any]]:
        if self._chart_of_accounts is None:
            self._chart_of_accounts = generate_chart_of_accounts()
        return self._chart_of_accounts

    def get_trial_balance(self) -> Dict[str, Any]:
        if self._trial_balance is None:
            self._trial_balance = generate_trial_balance()
        return self._trial_balance
