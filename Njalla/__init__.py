from .API import NjallaAPI
from .Domain import NjallaDomain
from .Server import NjallaServer
from .VPN import NjallaVPN
from .Wallet import NjallaWallet
import requests

class Client:
    def __init__(self, api_key):
        """
        Initialize the Njalla API.
        We are initializing the API, Domain, Server, User, VPN, and Wallet classes here and use the same API key for all of them.

        Example:
        >>> from Njalla import Njalla
        >>> njalla = Njalla("API_KEY")
        >>> njalla.API_CLASS.method(parameters)

        :param api_key: Your Njalla API key.
        :type api_key: str

        """

        r = requests.post("https://njal.la/api/1/", headers={"Authorization": "Njalla " + api_key}, timeout=30)
        if "error" in r.json():
            if r.json()["error"]["code"] == 403:
                raise ValueError("Invalid API key.")

        self.API = NjallaAPI(api_key)
        self.Domain = NjallaDomain(api_key)
        self.Server = NjallaServer(api_key)
        self.VPN = NjallaVPN(api_key)
        self.Wallet = NjallaWallet(api_key)