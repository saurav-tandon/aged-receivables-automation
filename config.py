from datetime import datetime

# --- FILES ---
INPUT_FILE = "sample aged for chatgpt.xlsx"
OUTPUT_FILE = "AR_Aging_Report.xlsx"

# --- COLUMN NAMES (from your sheet) ---
COL_INVOICE_NO = "Invoice Number"
COL_CONTACT = "Contact"
COL_INVOICE_DATE = "Invoice Date"
COL_DUE_DATE = "Due Date"
COL_TOTAL = "Total"

# --- AGING BUCKETS ---
AGING_BUCKETS = [
    (0, 0, "Current"),
    (1, 30, "1–30"),
    (31, 60, "31–60"),
    (61, 90, "61–90"),
    (91, 99999, "90+"),
]

# --- ENTITY CLASSIFICATION RULES ---
def classify_entity_and_type(invoice_no: str):
    s = str(invoice_no).strip()

    # -------- Credit Notes --------
    if s.startswith("CN-"):
        digits = s.replace("CN-", "").strip()

        # Agorapulse CNs are long date-style numbers (6+ digits)
        if digits.isdigit() and len(digits) >= 6:
            return "Agorapulse", "Credit Note"

        # Mention CNs are short numbers (usually 4 digits)
        if digits.isdigit() and len(digits) <= 5:
            return "Mention", "Credit Note"

        return "Unknown", "Credit Note"

    # -------- Invoices --------
    if s.startswith("INV-"):
        return "Agorapulse", "Invoice"

    if s.isdigit():
        n = int(s)

        # Manual invoices are small numbers
        if n < 100000:
            return "Manual", "Invoice"

        # Mention invoices are large numeric IDs
        return "Mention", "Invoice"

    return "Unknown", "Unknown"

