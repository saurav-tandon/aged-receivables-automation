from datetime import datetime

# --- FILES ---
INPUT_FILE = "sample_ar_aging.xlsx"
OUTPUT_FILE = "AR_Aging_Report.xlsx"

# --- COLUMN NAMES ---
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

        if digits.isdigit() and len(digits) >= 6:
            return "Entity1", "Credit Note"

        if digits.isdigit() and len(digits) <= 5:
            return "Entity2", "Credit Note"

        return "Unknown", "Credit Note"

    # -------- Invoices --------
    if s.startswith("INV-"):
        return "Entity1", "Invoice"

    if s.isdigit():

        n = int(s)

        if n < 100000:
            return "Manual", "Invoice"

        return "Entity2", "Invoice"

    return "Unknown", "Unknown"