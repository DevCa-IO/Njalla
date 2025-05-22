import requests
from .API import NjallaAPI

class NjallaVPN:
    def __init__(self, api_key):
        """Initialize NjallaVPN client
        
        Args:
            api_key (str): Njalla API key
        """
        self.api_key = api_key
        self.base_url = "https://njal.la/api/1/"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Njalla " + self.api_key,
            "Referer": "https://njal.la/",
        }

    def add_vpn(self, name, autorenew):
        """Add a new VPN client
        
        Args:
            name (str): Name of the VPN client
            autorenew (bool): Whether to automatically renew the VPN
            
        Returns:
            dict: {
                "id": str,
                ... (other VPN properties)
            }
        """
        data = {
            "method": "add-vpn",
            "params": {
                "name": name,
                "autorenew": autorenew
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def edit_vpn(self, vpn_id, name, autorenew, backend, publickey):
        """Edit an existing VPN client
        
        Args:
            vpn_id (str): ID of the VPN client to edit
            name (str): New name for the VPN client
            autorenew (bool): Whether to automatically renew the VPN
            backend (str): VPN backend type (wireguard|openvpn)
            publickey (str): WireGuard PublicKey, set to your public key or null to generate a new one
            
        Returns:
            dict: {
                ... (VPN properties)
            }
        """
        data = {
            "method": "edit-vpn",
            "params": {
                "id": vpn_id,
                "name": name,
                "autorenew": autorenew,
                "backend": backend,
                "publickey": publickey
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def get_vpn(self, vpn_id):
        """Get information about a specific VPN client
        
        Args:
            vpn_id (str): ID of the VPN client
            
        Returns:
            dict: {
                ... (VPN properties)
            }
        """
        data = {
            "method": "get-vpn",
            "params": {
                "id": vpn_id
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def list_vpns(self):
        """List all VPN clients
        
        Returns:
            list: List of VPN clients with their properties
        """
        data = {
            "method": "list-vpns"
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]["vpns"]

    def remove_vpn(self, vpn_id):
        """Remove an existing VPN client
        
        Args:
            vpn_id (str): ID of the VPN client to remove
            
        Returns:
            dict: {
                ... (operation result)
            }
        """
        data = {
            "method": "remove-vpn",
            "params": {
                "id": vpn_id
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def renew_vpn(self, vpn_id, months):
        """Renew an existing VPN client
        
        Args:
            vpn_id (str): ID of the VPN client to renew
            months (int): Number of months to renew for
            
        Note:
            Your wallet must have enough credit to complete this operation
            
        Returns:
            dict: {
                ... (renewal result)
            }
        """
        data = {
            "method": "renew-vpn",
            "params": {
                "id": vpn_id,
                "months": months
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]