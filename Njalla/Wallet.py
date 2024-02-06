import requests
from .API import NjallaAPI


class NjallaWallet:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://njal.la/api/1/"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Njalla " + self.api_key,
            "Referer": "https://njal.la/",
        }
        self.payment_shorts = {
            "bitcoin": "btc",
            "litecoin": "ltc",
            "monero": "xmr",
            "zcash": "zec",
            "ethereum": "eth",
            "paypal": "paypal"
        }

    def add_payment(self, amount, via):
        # Possible via: paypal, bitcoin, litecoin, monero, zcash, ethereum
        """
            Add a payment to the account.
            :param amount: Amount to add in EUR. (int) 5 or multiple of 15, max: 300
            :param via: Payment method. Possible values: paypal, bitcoin, litecoin, monero, zcash, ethereum
            :return: amount (int), address (string, payment address), url (string, for paypal)
            """
        if amount < 5 or amount > 300:
            raise ValueError("Amount must be 5 or multiple of 15, max: 300")
        if via not in ["paypal", "bitcoin", "litecoin", "monero", "zcash", "ethereum"]:
            raise ValueError(
                "Invalid payment method. Possible values: paypal, bitcoin, litecoin, monero, zcash, ethereum")
        data = {
            "method": "add-payment",
            "params": {
                "amount": amount,
                "via": via
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        result = r.json()["result"]
        if "error" in r.json():
            raise ValueError(r.json()["error"]["message"])
        if via == "paypal":
            json_obj = {
                "eur_amount": result["amount"],
                "url": result["url"]
            }
        else:
            json_obj = {
                "eur_amount": result["amount"],
                "crypto_amount": result["amount_" + self.payment_shorts[via]],
                "address": result["address"]
            }

        return json_obj

    def get_balance(self):
        """
            Get the balance of the account.

            :return: Balance (int) in EUR.
            """
        data = {
            "method": "get-balance"
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        result = r.json()["result"]
        if "error" in r.json():
            raise ValueError(r.json()["error"]["message"])
        return result["balance"]

    def get_payment(self, payment_id):
        """
            Get details about a payment

            :param payment_id: ID of the payment.
            :return: JSON object with the details of the payment.
            """
        data = {
            "method": "get-payment",
            "params": {
                "id": payment_id
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        result = r.json()["result"]
        if "error" in r.json():
            raise ValueError(r.json()["error"]["message"])
        return result

    def list_transactions(self):
        """
            List transactions (payments, registrations, renewals, etc.) of the last 90 days

            :return: JSON object with the details of the transactions.
            """
        data = {
            "method": "list-transactions",
            "params": {}
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        result = r.json()["result"]
        if "error" in r.json():
            raise ValueError(r.json()["error"]["message"])
        return result
