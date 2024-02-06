import requests

class NjallaAPI:
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

