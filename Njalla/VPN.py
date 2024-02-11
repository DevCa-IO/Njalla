import requests
from .API import NjallaAPI

class NjallaVPN:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://njal.la/api/1/"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Njalla " + self.api_key,
            "Referer": "https://njal.la/",
        }

    def add_vpn(self, name, autorenew):
        pass

    def edit_vpn(self, vpn_id, name, autorenew, backend, publickey):
        pass

    def get_vpn(self, vpn_id):
        pass

    def list_vpns(self):
        pass

    def remove_vpn(self, vpn_id):
        pass

    def renew_vpn(self, vpn_id, months):
        pass