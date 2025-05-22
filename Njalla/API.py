import requests

class NjallaAPI:
    def __init__(self, api_key):
        """Initialize NjallaAPI client
        
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

    def add_token(self, comment=None, from_=None, allowed_domains=None, allowed_servers=None, allowed_methods=None, allowed_prefixes=None, allowed_types=None, acme=None):
        """Add a new API token
        
        Args:
            comment (str, optional): Comment describing the token's purpose
            from_ (list, optional): Array of IPv4 or IPv6 IPs or networks that are allowed to use the token.
                                  i.e.: ['8.8.8.8', '192.168.0.0/24']
            allowed_domains (list, optional): Restrict token to subset of your domains
            allowed_servers (list, optional): Restrict token to subset of your servers by id
            allowed_methods (list, optional): Restrict token to subset of possible API calls
            allowed_prefixes (list, optional): Restrict token to DNS record name prefixes
            allowed_types (list, optional): Restrict token to subset of possible types of DNS records
            acme (bool, optional): Syntax sugar adding allowed_methods, allowed_prefixes and allowed_types
                                 needed for ACME DNS challenge
            
        Returns:
            dict: Empty dictionary on success
        """
        if acme:
            allowed_methods = ["add-record", "edit-record", "remove-record", "list-records"]
            allowed_types = ["TXT"]
            allowed_prefixes = ["_acme-challenge"]
        data = {
            "method": "add-token",
            "params": {
                "comment": comment,
                "from": from_,
                "allowed_domains": allowed_domains,
                "allowed_servers": allowed_servers,
                "allowed_methods": allowed_methods,
                "allowed_prefixes": allowed_prefixes,
                "allowed_types": allowed_types,
                "acme": acme
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def check_task(self, task_id):
        """Check status of a long running task
        
        Args:
            task_id (str): ID of the task to check
            
        Returns:
            dict: {
                "id": str,
                "status": object
            }
        """
        data = {
            "method": "check-task",
            "params": {
                "id": task_id
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def edit_token(self, key, comment=None, from_=None, allowed_domains=None, allowed_servers=None, allowed_methods=None, allowed_prefixes=None, allowed_types=None):
        """Edit API token
        
        Args:
            key (str): Token key to edit
            comment (str, optional): Comment describing the token's purpose
            from_ (list, optional): Array of IPv4 or IPv6 IPs or networks that are allowed to use the token.
                                  i.e.: ['8.8.8.8', '192.168.0.0/24']
            allowed_domains (list, optional): Restrict token to subset of your domains
            allowed_servers (list, optional): Restrict token to subset of your servers by id
            allowed_methods (list, optional): Restrict token to subset of possible API calls
            allowed_prefixes (list, optional): Restrict token to DNS record name prefixes
            allowed_types (list, optional): Restrict token to subset of possible types of DNS records
            
        Returns:
            dict: Empty dictionary on success
        """
        params = {"key": key}
        if comment is not None:
            params["comment"] = comment
        if from_ is not None:
            params["from"] = from_
        if allowed_domains is not None:
            params["allowed_domains"] = allowed_domains
        if allowed_servers is not None:
            params["allowed_servers"] = allowed_servers
        if allowed_methods is not None:
            params["allowed_methods"] = allowed_methods
        if allowed_prefixes is not None:
            params["allowed_prefixes"] = allowed_prefixes
        if allowed_types is not None:
            params["allowed_types"] = allowed_types
        data = {"method": "edit-token", "params": params}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]

    def list_tokens(self):
        """List existing API authorization tokens
        
        Returns:
            list: List of tokens with their properties
        """
        data = {"method": "list-tokens"}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response["result"]["tokens"]

    def remove_token(self, key):
        """Remove an existing API token
        
        Args:
            key (str): Token key to remove
            
        Returns:
            dict: {
                "success": bool
            }
        """
        data = {"method": "remove-token", "params": {"key": key}}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        res = response.get("result", {})
        if isinstance(res, dict) and res.get("status") == "removed":
            return {"success": True}
        return res
