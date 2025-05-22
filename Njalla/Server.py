import requests
from .API import NjallaAPI

class NjallaServer:
    def __init__(self, api_key):
        """Initialize NjallaServer client
        
        Args:
            api_key (str): Njalla API key
        """
        self.api_key = api_key
        self.base_url = "https://njal.la/api/1/"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Njalla " + self.api_key,
            "Referer": "https://njal.la/"
        }

    def add_server(self, name, type_, os_, ssh_key, months=1, autorenew=False):
        """Create a new server
        
        Args:
            name (str): Name of the server
            type_ (str): Server type
            os_ (str): Operating system
            ssh_key (str): SSH public key
            months (int, optional): Number of months to rent. Defaults to 1. Max 12.
            autorenew (bool, optional): Whether to automatically renew. Defaults to False.
            
        Returns:
            dict: {
                "id": str,
                ... (other server properties)
            }
        """
        data = {
            "method": "add-server",
            "params": {
                "name": name,
                "type": type_,
                "os": os_,
                "ssh_key": ssh_key,
                "months": months,
                "autorenew": autorenew
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def add_traffic(self, id_, amount, months, starts_today=False):
        """Add extra traffic package
        
        Args:
            id_ (str): Server ID
            amount (int): Amount of traffic to add
            months (int): Number of months
            starts_today (bool, optional): Whether to start today. Defaults to False.
            
        Returns:
            dict: Operation result
        """
        data = {
            "method": "add-traffic",
            "params": {
                "id": id_,
                "amount": amount,
                "months": months,
                "starts_today": starts_today
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def edit_server(self, id_, name=None, type_=None, ssh_key=None, reverse_name=None, autorenew=None):
        """Edit an existing server
        
        Args:
            id_ (str): Server ID
            name (str, optional): New server name
            type_ (str, optional): New server type
            ssh_key (str, optional): New SSH public key
            reverse_name (str, optional): New reverse DNS name
            autorenew (bool, optional): New autorenew setting
            
        Returns:
            dict: Updated server properties
        """
        params = {"id": id_}
        if name is not None:
            params["name"] = name
        if type_ is not None:
            params["type"] = type_
        if ssh_key is not None:
            params["ssh_key"] = ssh_key
        if reverse_name is not None:
            params["reverse_name"] = reverse_name
        if autorenew is not None:
            params["autorenew"] = autorenew
            
        data = {"method": "edit-server", "params": params}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def get_server(self, id_):
        """Get information about a server
        
        Args:
            id_ (str): Server ID
            
        Returns:
            dict: Server information
        """
        data = {
            "method": "get-server",
            "params": {
                "id": id_
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def list_server_images(self):
        """List available server images
        
        Returns:
            list: List of available server images
        """
        data = {"method": "list-server-images"}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]["images"]

    def list_server_types(self):
        """List available server types
        
        Returns:
            list: List of available server types
        """
        data = {"method": "list-server-types"}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]["types"]

    def list_servers(self):
        """List all servers
        
        Returns:
            list: List of servers
        """
        data = {"method": "list-servers"}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]["servers"]

    def list_traffic(self, id_):
        """List extra traffic packages for a server
        
        Args:
            id_ (str): Server ID
            
        Returns:
            list: List of traffic packages
        """
        data = {
            "method": "list-traffic",
            "params": {
                "id": id_
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]["traffic"]

    def remove_server(self, id_):
        """Remove a server
        
        Args:
            id_ (str): Server ID
            
        Returns:
            dict: {
                "task": str  # Task ID for tracking removal progress
            }
        """
        data = {
            "method": "remove-server",
            "params": {
                "id": id_
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def renew_server(self, id_, months):
        """Renew a server
        
        Args:
            id_ (str): Server ID
            months (int): Number of months to renew for
            
        Note:
            Your wallet must have enough credit to complete this operation
            
        Returns:
            dict: Renewal result
        """
        data = {
            "method": "renew-server",
            "params": {
                "id": id_,
                "months": months
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def reset_server(self, id_, os_, ssh_key, type_):
        """Reset and reinstall a server
        
        Args:
            id_ (str): Server ID
            os_ (str): New operating system
            ssh_key (str): New SSH public key
            type_ (str): New server type
            
        Note:
            All data will be lost
            
        Returns:
            dict: Reset operation result
        """
        data = {
            "method": "reset-server",
            "params": {
                "id": id_,
                "os": os_,
                "ssh_key": ssh_key,
                "type": type_
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def restart_server(self, id_):
        """Restart a server
        
        Args:
            id_ (str): Server ID
            
        Returns:
            dict: Restart operation result
        """
        data = {
            "method": "restart-server",
            "params": {
                "id": id_
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def start_server(self, id_):
        """Start a server
        
        Args:
            id_ (str): Server ID
            
        Returns:
            dict: Start operation result
        """
        data = {
            "method": "start-server",
            "params": {
                "id": id_
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def stop_server(self, id_):
        """Stop a server
        
        Args:
            id_ (str): Server ID
            
        Returns:
            dict: Stop operation result
        """
        data = {
            "method": "stop-server",
            "params": {
                "id": id_
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]