import requests, json, uuid

url = "https://api.sandbox.transferwise.tech"

with open('token.json') as f:
    token = json.load(f)['token']

headers = {
    "Authorization": token,
    "Content-Type": "application/json"
}

quote_types = ["BALANCE_PAYOUT", "BALANCE_CONVERSION", "REGULAR"]


def tw_request(tw_url, method, data: dict):
    return requests.request(url=tw_url, method=method, headers=headers, data=json.dumps(data)).json()


def create_quote(profile_id: int, source: str, target: str, amount: float, quote_code: int):
    data = {
        "profile": profile_id,
        "source": source,
        "target": target,
        "rateType": "FIXED",
        "type": quote_types[quote_code],
        "targetAmount": amount
    }

    return tw_request(url + "/v1/quotes/", "POST", data)


def create_email_recipient(profile_id: int, email: str, name: str, currency: str):
    data = {
        "profile": profile_id,
        "accountHolderName": name,
        "currency": currency,
        "type": "email",
        "details": {
            "email": email
        }
    }
    return tw_request(url + "/v1/accounts/", "POST", data)


def get_quote(quote_id):
    return tw_request(url + "/v1/quotes/%s" % quote_id, "GET", {})


def get_recipient(recipient_id):
    return tw_request(url + "/v1/accounts/%s" % recipient_id, "GET", {})


def get_profiles():
    return tw_request(url + "/v1/profiles", "GET", {})


def create_transfer(profile_id: int, source: str, target: str, amount: float, quote_code: int, email: str, name: str):
    quote = create_quote(profile_id, source, target, amount, quote_code)
    recipient = create_email_recipient(profile_id, email, name, target)

    data = {
        "targetAccount": recipient["id"],
        "quote": quote["id"],
        "customerTransactionId": str(uuid.uuid4()),
        "details": {
            "reference": "api test",
        }
    }
    return tw_request(url + "/v1/transfers", "POST", data)


def fund_transfer(transfer_id):
    data = {"type": "BALANCE"}
    return tw_request(url + "/v1/transfers/%s/payments" % transfer_id, "POST", data)
