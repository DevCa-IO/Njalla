import requests
from .API import NjallaAPI


class NjallaUser:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://njal.la/api/1/"

    def login(self, email, password):
        """
        Login into an existing account (cookie-based session).
        Consider using API tokens instead

        :param email: Email address
        :param password: Password

        """
        data = {
            "method": "login",
            "params": {
                "email": email,
                "password": password
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        result = r.json()["result"]
        if "error" in r.json():
            raise ValueError(r.json()["error"]["message"])
        return result

    def logout(self):
        """
        Logout and end your current session
        """
        data = {
            "method": "logout",
            "params": {
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        result = r.json()["result"]
        if "error" in r.json():
            raise ValueError(r.json()["error"]["message"])
        return result

    def delete_account(self):
        """
        Delete your account.
        You can only delete the account if all domains and servers
        have been removed and your wallet is empty.
        """
        data = {
            "method": "delete-account",
            "params": {
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        result = r.json()["result"]
        if "error" in r.json():
            raise ValueError(r.json()["error"]["message"])
        return result
