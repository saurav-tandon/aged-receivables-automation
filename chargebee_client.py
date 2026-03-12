import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# Environment Variables
# ----------------------------
ENTITY1_SITE = os.getenv("ENTITY1_CB_SITE")
ENTITY1_KEY = os.getenv("ENTITY1_CB_API_KEY")

ENTITY2_SITE = os.getenv("ENTITY2_CB_SITE")
ENTITY2_KEY = os.getenv("ENTITY2_CB_API_KEY")


# ----------------------------
# Site Configuration
# ----------------------------
def get_site_config(entity):

    if entity == "Entity1":
        return ENTITY1_SITE, ENTITY1_KEY

    elif entity == "Entity2":
        return ENTITY2_SITE, ENTITY2_KEY

    return None, None


# ----------------------------
# Fetch Invoice
# ----------------------------
def fetch_invoice(entity, invoice_id):

    site, key = get_site_config(entity)

    if not site or not key:
        return None

    url = f"https://{site}.chargebee.com/api/v2/invoices/{invoice_id}"

    response = requests.get(url, auth=(key, ""))

    if response.status_code != 200:
        return None

    return response.json()


# ----------------------------
# Fetch Subscription
# ----------------------------
def fetch_subscription(entity, subscription_id):

    site, key = get_site_config(entity)

    if not site or not key:
        return None

    url = f"https://{site}.chargebee.com/api/v2/subscriptions/{subscription_id}"

    response = requests.get(url, auth=(key, ""))

    if response.status_code != 200:
        return None

    return response.json()