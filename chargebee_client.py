import requests
import os
from dotenv import load_dotenv

load_dotenv()

AGORA_SITE = os.getenv("AGORA_CB_SITE")
AGORA_KEY = os.getenv("AGORA_CB_API_KEY")

MENTION_SITE = os.getenv("MENTION_CB_SITE")
MENTION_KEY = os.getenv("MENTION_CB_API_KEY")


def get_site_config(entity):
    if entity == "Agorapulse":
        return AGORA_SITE, AGORA_KEY
    elif entity == "Mention":
        return MENTION_SITE, MENTION_KEY
    return None, None


def fetch_invoice(entity, invoice_id):
    site, key = get_site_config(entity)
    if not site or not key:
        return None

    url = f"https://{site}.chargebee.com/api/v2/invoices/{invoice_id}"

    response = requests.get(url, auth=(key, ""))

    if response.status_code != 200:
        return None

    return response.json()


def fetch_subscription(entity, subscription_id):
    site, key = get_site_config(entity)
    if not site or not key:
        return None

    url = f"https://{site}.chargebee.com/api/v2/subscriptions/{subscription_id}"

    response = requests.get(url, auth=(key, ""))

    if response.status_code != 200:
        return None

    return response.json()