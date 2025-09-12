import requests, uuid, base64

BASE_URL = "https://sandbox.momodeveloper.mtn.com"
SUBSCRIPTION_KEY = "70c6cdf2867c4747820230eaed0ea016"  # from your Collection product
API_USER = "5a772898-095a-44a0-b5eb-c6c26f34131c"  # your generated user ID
API_KEY = "b2839e2df8f5444d8707149eb1d3e2da"       # your generated API key
TARGET_ENVIRONMENT = "sandbox"


def get_access_token():
    url = f"{BASE_URL}/collection/token/"  
    auth = base64.b64encode(f"{API_USER}:{API_KEY}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Content-Type": "application/json",  
    }

    res = requests.post(url, headers=headers)
    print("Token response:", res.status_code, res.text)  
    res.raise_for_status()
    return res.json()["access_token"]


def request_to_pay(amount, customer_number, external_id):
    url = f"{BASE_URL}/collection/v1_0/requesttopay"
    ref_id = str(uuid.uuid4())
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Reference-Id": ref_id,
        "X-Target-Environment": TARGET_ENVIRONMENT,
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    }

    payload = {
        "amount": str(amount),
        "currency": "EUR",   # use EUR in sandbox
        "externalId": str(external_id),
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": str(customer_number),  # e.g. "250788123456"
        },
        "payerMessage": "You pay for Ngererayo marketplace",
        "payeeNote": "Thank you for your purchase",
    }

    res = requests.post(url, json=payload, headers=headers)
    print("➡️ Payload Sent:", payload)
    print("➡️ Response Status:", res.status_code)
    print("➡️ Response Body:", res.text)

    res.raise_for_status()
    return ref_id
