import pandas as pd
import config
import requests
import os
import time
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from tqdm import tqdm

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

ENTITY1_SITE = os.getenv("ENTITY1_CB_SITE")
ENTITY1_KEY = os.getenv("ENTITY1_CB_API_KEY")

ENTITY2_SITE = os.getenv("ENTITY2_CB_SITE")
ENTITY2_KEY = os.getenv("ENTITY2_CB_API_KEY")

# ----------------------------
# SETTINGS
# ----------------------------
TEST_MODE = False
MAX_WORKERS = 10
MAX_RETRIES = 3

# ----------------------------
# Locks
# ----------------------------
cache_lock = Lock()
counter_lock = Lock()

# ----------------------------
# API counter
# ----------------------------
api_call_count = 0

# ----------------------------
# Safe API Request
# ----------------------------
def safe_request(url, key):

    global api_call_count

    for attempt in range(MAX_RETRIES):

        try:

            with counter_lock:
                api_call_count += 1

            r = requests.get(url, auth=(key, ""), timeout=20)

            if r.status_code == 200:
                return r.json()

            if r.status_code == 429:
                print("⚠ Rate limit hit — sleeping 5s")
                time.sleep(5)
                continue

            print("API error:", r.status_code)
            return None

        except Exception as e:

            print(f"Retry {attempt+1}/{MAX_RETRIES} after error:", e)
            time.sleep(2)

    return None


# ----------------------------
# Credentials
# ----------------------------
def get_credentials(entity):

    if entity == "Entity1":
        return ENTITY1_SITE, ENTITY1_KEY

    if entity == "Entity2":
        return ENTITY2_SITE, ENTITY2_KEY

    return None, None


# ----------------------------
# Fetch invoice
# ----------------------------
def fetch_invoice(entity, invoice_id):

    site, key = get_credentials(entity)

    if not site:
        return None

    url = f"https://{site}.chargebee.com/api/v2/invoices/{invoice_id}"

    return safe_request(url, key)


# ----------------------------
# Fetch credit note
# ----------------------------
def fetch_credit_note(entity, credit_note_id):

    site, key = get_credentials(entity)

    if not site:
        return None

    url = f"https://{site}.chargebee.com/api/v2/credit_notes/{credit_note_id}"

    return safe_request(url, key)


# ----------------------------
# Fetch subscription
# ----------------------------
def fetch_subscription(entity, subscription_id):

    site, key = get_credentials(entity)

    if not site:
        return None

    url = f"https://{site}.chargebee.com/api/v2/subscriptions/{subscription_id}"

    return safe_request(url, key)


# ----------------------------
# Fetch customer subscriptions
# ----------------------------
def fetch_customer_subscriptions(entity, customer_id):

    site, key = get_credentials(entity)

    if not site:
        return None

    url = f"https://{site}.chargebee.com/api/v2/customers/{customer_id}/subscriptions"

    data = safe_request(url, key)

    if not data:
        return None

    subs = data.get("list", [])

    if not subs:
        return None

    for s in subs:

        sub = s.get("subscription", {})

        if sub.get("status") == "active":
            return sub

    return subs[0].get("subscription", {})


# ----------------------------
# Caches
# ----------------------------
subscription_cache = {}
customer_subscription_cache = {}

# ----------------------------
# Load Xero file
# ----------------------------
raw = pd.read_excel(config.INPUT_FILE, header=None)

header_row = None

for i in range(len(raw)):

    if "Invoice Number" in raw.iloc[i].astype(str).values:
        header_row = i
        break

if header_row is None:
    raise Exception("Header row not found")

df = pd.read_excel(config.INPUT_FILE, header=header_row)

df = df.dropna(how="all")

df.columns = [str(c).strip() for c in df.columns]

print("Columns detected:", df.columns.tolist())

# ----------------------------
# Required columns
# ----------------------------
ALLOWED_COLS = [
    "Contact",
    "Invoice Date",
    "Due Date",
    "Invoice Number",
    "Invoice Reference",
    "Current",
    "< 1 Month",
    "1 Month",
    "2 Months",
    "3 Months",
    "Older",
    "Total"
]

df = df[[c for c in ALLOWED_COLS if c in df.columns]]

# ----------------------------
# Remove footer
# ----------------------------
df = df[df["Invoice Number"].notna()]
df = df[df["Invoice Number"].astype(str).str.strip() != ""]

# ----------------------------
# Normalize
# ----------------------------
df[config.COL_INVOICE_NO] = df[config.COL_INVOICE_NO].astype(str).str.strip()

df[config.COL_TOTAL] = pd.to_numeric(
    df[config.COL_TOTAL],
    errors="coerce"
).fillna(0)

df[config.COL_DUE_DATE] = pd.to_datetime(
    df[config.COL_DUE_DATE],
    errors="coerce"
)

# ----------------------------
# Classify entity
# ----------------------------
entities = []
doc_types = []

for inv in df[config.COL_INVOICE_NO]:

    ent, typ = config.classify_entity_and_type(inv)

    entities.append(ent)
    doc_types.append(typ)

df["Entity"] = entities
df["Doc Type"] = doc_types

# ----------------------------
# Worker
# ----------------------------
def process_row(row):

    invoice_id = row["Invoice Number"]
    entity = row["Entity"]
    doc_type = row["Doc Type"]

    if doc_type not in ["Invoice", "Credit Note"]:
        return None, None, None

    if doc_type == "Invoice":
        data = fetch_invoice(entity, invoice_id)
    else:
        data = fetch_credit_note(entity, invoice_id)

    if not data:
        return "Not Found", None, None

    obj = data.get("invoice", {}) if doc_type == "Invoice" else data.get("credit_note", {})

    payment_status = obj.get("status")

    subscription_id = obj.get("subscription_id")
    customer_id = obj.get("customer_id")

    if subscription_id:

        with cache_lock:

            if subscription_id in subscription_cache:
                sub_obj = subscription_cache[subscription_id]

            else:

                subscription_data = fetch_subscription(entity, subscription_id)

                if not subscription_data:
                    return payment_status, "Not Found", None

                sub_obj = subscription_data.get("subscription", {})

                subscription_cache[subscription_id] = sub_obj

        return payment_status, sub_obj.get("status"), sub_obj.get("cancelled_at")

    if customer_id:

        with cache_lock:

            if customer_id in customer_subscription_cache:

                sub_obj = customer_subscription_cache[customer_id]

            else:

                sub_obj = fetch_customer_subscriptions(entity, customer_id)

                customer_subscription_cache[customer_id] = sub_obj

        if not sub_obj:
            return payment_status, None, None

        return payment_status, sub_obj.get("status"), sub_obj.get("cancelled_at")

    return payment_status, None, None


# ----------------------------
# Process rows
# ----------------------------
rows = [row for _, row in df.iterrows()]

print(f"\nProcessing {len(rows)} invoices...\n")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    results = list(
        tqdm(
            executor.map(process_row, rows),
            total=len(rows),
            desc="Chargebee API"
        )
    )

payments = []
subs = []
cancels = []

for p, s, c in results:

    payments.append(p)
    subs.append(s)
    cancels.append(c)

df["CB Payment Status"] = payments
df["CB Subscription Status"] = subs
df["CB Cancellation Date"] = cancels

# ----------------------------
# Aging calculation
# ----------------------------
report_date = pd.Timestamp.today().normalize()

def aging_bucket(due_date, payment_status):

    if pd.isna(due_date):
        return "Data Issue"

    closed_status = ["paid", "refunded", "voided"]

    if str(payment_status).lower() in closed_status:
        return "Closed"

    days = (report_date - due_date).days

    if days <= 0:
        return "Current"

    for low, high, label in config.AGING_BUCKETS:
        if low <= days <= high:
            return label

    return "90+"

df["Aging Bucket"] = df.apply(
    lambda row: aging_bucket(
        row[config.COL_DUE_DATE],
        row.get("CB Payment Status")
    ),
    axis=1
)

# ----------------------------
# Summary
# ----------------------------
summary = (
    df[df["Doc Type"] == "Invoice"]
    .groupby(["Entity", "Aging Bucket"])[config.COL_TOTAL]
    .sum()
    .reset_index()
)

# ----------------------------
# Write Excel
# ----------------------------
with pd.ExcelWriter(config.OUTPUT_FILE, engine="xlsxwriter") as writer:

    summary.to_excel(writer, sheet_name="Summary", index=False)

    df[df["Entity"] == "Entity1"].to_excel(writer, sheet_name="Entity1", index=False)
    df[df["Entity"] == "Entity2"].to_excel(writer, sheet_name="Entity2", index=False)

print("\nAR_Aging_Report.xlsx created successfully")
print(f"Total Chargebee API calls made: {api_call_count}")