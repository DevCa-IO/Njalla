import requests
from .API import NjallaAPI

class NjallaDomain:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://njal.la/api/1/"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Njalla " + self.api_key,
            "Referer": "https://njal.la/"
        }

    def add_dnssec(self, domain, algorithm, digest=None, digest_type=None, key_tag=None, public_key=None):
        """Add DNSSEC record for domain
        
        Args:
            domain (str): Domain name
            algorithm (int): DNSSEC algorithm
            digest (str, optional): DNSSEC digest
            digest_type (int, optional): DNSSEC digest type
            key_tag (int, optional): DNSSEC key tag
            public_key (str, optional): DNSSEC public key
            
        Note:
            Either (digest, digest_type, key_tag) or public_key must be provided
            
        Returns:
            dict: Empty dictionary on success
        """
        params = {
            "domain": domain,
            "algorithm": algorithm
        }
        if digest and digest_type and key_tag:
            params.update({
                "digest": digest,
                "digest_type": digest_type,
                "key_tag": key_tag
            })
        elif public_key:
            params["public_key"] = public_key
        else:
            raise ValueError("Either (digest, digest_type, key_tag) or public_key must be provided")

        data = {"method": "add-dnssec", "params": params}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def add_forward(self, domain, from_, to):
        """Add email forward
        
        Args:
            domain (str): Domain name
            from_ (str): Source email address
            to (str): Destination email address
            
        Returns:
            dict: {
                "domain": str,
                "from": str,
                "to": str
            }
        """
        data = {
            "method": "add-forward",
            "params": {
                "domain": domain,
                "from": from_,
                "to": to
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def add_glue(self, domain, name, address4=None, address6=None):
        """Add glue record for the domain
        
        Args:
            domain (str): Domain name
            name (str): Subdomain name
            address4 (str, optional): IPv4 address
            address6 (str, optional): IPv6 address
            
        Note:
            At least one of address4 or address6 must be provided
            
        Returns:
            dict: Empty dictionary on success
        """
        params = {
            "domain": domain,
            "name": name
        }
        if address4:
            params["address4"] = address4
        if address6:
            params["address6"] = address6
        if not address4 and not address6:
            raise ValueError("At least one of address4 or address6 must be provided")

        data = {"method": "add-glue", "params": params}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def add_record(self, domain, type_, name, content=None, ttl=None, prio=None, weight=None, 
                  port=None, target=None, ssh_algorithm=None, ssh_type=None):
        """Add new DNS Record to domain
        
        Args:
            domain (str): Domain name
            type_ (str): Record type (A, AAAA, ANAME, CAA, CNAME, Dynamic, HTTPS, MX, NAPTR, NS, PTR, SRV, SSHFP, SVCB, TLSA, TXT)
            name (str): Record name
            content (str, optional): Record content (for A, AAAA, ANAME, CAA, CNAME, MX, NAPTR, NS, PTR, Redirect, SRV, SSHFP, Static, TLSA, TXT)
            ttl (int, optional): Time to live (for A, AAAA, ANAME, CAA, CNAME, MX, NAPTR, NS, PTR, Redirect, SRV, SSHFP, TLSA, TXT)
            prio (int, optional): Priority (for HTTPS, MX, Redirect, SRV, SVCB)
            weight (int, optional): Weight (for SRV)
            port (int, optional): Port (for SRV)
            target (str, optional): Target (for HTTPS, SVCB)
            ssh_algorithm (int, optional): SSH algorithm (for SSHFP, values: 1-5 // RSA, DSA, ECDSA, Ed25519, XMSS)
            ssh_type (int, optional): SSH type (for SSHFP, values: 1-2 // SHA-1, SHA-256)
            
        Returns:
            dict: {
                "id": str,
                "domain": str,
                "type": str,
                "name": str,
                "content": str,
                "ttl": int,
                "prio": int,
                "weight": int,
                "port": int,
                "target": str,
                "ssh_algorithm": int,
                "ssh_type": int
            }
        """
        params = {
            "domain": domain,
            "type": type_,
            "name": name
        }
        if content is not None:
            params["content"] = content
        if ttl is not None:
            params["ttl"] = ttl
        if prio is not None:
            params["prio"] = prio
        if weight is not None:
            params["weight"] = weight
        if port is not None:
            params["port"] = port
        if target is not None:
            params["target"] = target
        if ssh_algorithm is not None:
            params["ssh_algorithm"] = ssh_algorithm
        if ssh_type is not None:
            params["ssh_type"] = ssh_type

        data = {"method": "add-record", "params": params}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def edit_domain(self, domain, **kwargs):
        """Edit domain configuration
        
        Args:
            domain (str): Domain name
            **kwargs: Additional parameters
                mailforwarding (bool, optional): Enable/disable mail forwarding
                dnssec (bool, optional): Enable/disable DNSSEC
                lock (bool, optional): Enable/disable domain lock
                contacts (list, optional): Custom whois contact IDs
                nameservers (list, optional): List of custom nameservers or empty list to use our nameservers
                
        Returns:
            dict: {
                "name": str,
                ... (other domain properties)
            }
        """
        params = {"domain": domain}
        valid_keys = ["mailforwarding", "dnssec", "lock", "contacts", "nameservers"]
        for key, value in kwargs.items():
            if key in valid_keys:
                params[key] = value

        data = {"method": "edit-domain", "params": params}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def edit_glue(self, domain, name, address4=None, address6=None):
        """Edit glue record
        
        Args:
            domain (str): Domain name
            name (str): Subdomain name
            address4 (str, optional): IPv4 address
            address6 (str, optional): IPv6 address
            
        Note:
            At least one of address4 or address6 must be provided
            
        Returns:
            dict: Empty dictionary on success
        """
        params = {
            "domain": domain,
            "name": name
        }
        if address4:
            params["address4"] = address4
        if address6:
            params["address6"] = address6
        if not address4 and not address6:
            raise ValueError("At least one of address4 or address6 must be provided")

        data = {"method": "edit-glue", "params": params}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def edit_record(self, id_, domain, type_, name, content=None, ttl=None, prio=None, weight=None,
                   port=None, target=None, ssh_algorithm=None, ssh_type=None):
        """Edit DNS Record
        
        Args:
            id_ (str): Record ID
            domain (str): Domain name
            type_ (str): Record type (A, AAAA, ANAME, CAA, CNAME, Dynamic, HTTPS, MX, NAPTR, NS, PTR, SRV, SSHFP, SVCB, TLSA, TXT)
            name (str): Record name
            content (str, optional): Record content (for A, AAAA, ANAME, CAA, CNAME, MX, NAPTR, NS, PTR, Redirect, SRV, SSHFP, Static, TLSA, TXT)
            ttl (int, optional): Time to live (for A, AAAA, ANAME, CAA, CNAME, MX, NAPTR, NS, PTR, Redirect, SRV, SSHFP, TLSA, TXT)
            prio (int, optional): Priority (for HTTPS, MX, Redirect, SRV, SVCB)
            weight (int, optional): Weight (for SRV)
            port (int, optional): Port (for SRV)
            target (str, optional): Target (for HTTPS, SVCB)
            ssh_algorithm (int, optional): SSH algorithm (for SSHFP, values: 1-5 // RSA, DSA, ECDSA, Ed25519, XMSS)
            ssh_type (int, optional): SSH type (for SSHFP, values: 1-2 // SHA-1, SHA-256)
            
        Returns:
            dict: {
                "domain": str,
                "type": str,
                "name": str,
                "content": str,
                "ttl": int,
                "prio": int,
                "weight": int,
                "port": int,
                "target": str,
                "ssh_algorithm": int,
                "ssh_type": int
            }
        """
        params = {
            "id": id_,
            "domain": domain,
            "type": type_,
            "name": name
        }
        if content is not None:
            params["content"] = content
        if ttl is not None:
            params["ttl"] = ttl
        if prio is not None:
            params["prio"] = prio
        if weight is not None:
            params["weight"] = weight
        if port is not None:
            params["port"] = port
        if target is not None:
            params["target"] = target
        if ssh_algorithm is not None:
            params["ssh_algorithm"] = ssh_algorithm
        if ssh_type is not None:
            params["ssh_type"] = ssh_type

        data = {"method": "edit-record", "params": params}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def find_domains(self, query):
        """Find new domains
        
        Args:
            query (str): Search query
            
        Returns:
            dict: {
                "domains": [
                    {
                        "price": int,
                        "status": str,
                        "name": str
                    }
                ]
            }
        """
        data = {
            "method": "find-domains",
            "params": {"query": query}
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def get_domain(self, domain):
        """Get information about one of your domains
        
        Args:
            domain (str): Domain name
            
        Returns:
            dict: {
                "name": str,
                ... (other domain properties)
            }
        """
        data = {
            "method": "get-domain",
            "params": {"domain": domain}
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def get_tlds(self):
        """Get list of supported TLDs
        
        Returns:
            dict: {
                "tld": {
                    "price": int,
                    "max_year": int,
                    "dnssec": bool
                }
            }
        """
        data = {"method": "get-tlds"}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def import_zone(self, domain, zone):
        """Import BIND zone file
        
        Args:
            domain (str): Domain name
            zone (str): BIND zone file content
            
        Returns:
            dict: Empty dictionary on success
        """
        data = {
            "method": "import-zone",
            "params": {
                "domain": domain,
                "zone": zone
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def list_dnssec(self, domain):
        """List DNSSEC records for domain
        
        Args:
            domain (str): Domain name
            
        Returns:
            dict: {
                "dnssec": list
            }
        """
        data = {
            "method": "list-dnssec",
            "params": {"domain": domain}
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def list_domains(self):
        """Get list of your domains
        
        Returns:
            dict: {
                "domains": list
            }
        """
        data = {"method": "list-domains"}
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def list_forwards(self, domain):
        """List existing email forwards
        
        Args:
            domain (str): Domain name
            
        Returns:
            dict: {
                "forwards": list
            }
        """
        data = {
            "method": "list-forwards",
            "params": {"domain": domain}
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def list_glue(self, domain):
        """List glue records for domain
        
        Args:
            domain (str): Domain name
            
        Returns:
            dict: {
                "glue": list
            }
        """
        data = {
            "method": "list-glue",
            "params": {"domain": domain}
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def list_records(self, domain):
        """List DNS records for given domain
        
        Args:
            domain (str): Domain name
            
        Returns:
            dict: {
                "records": list
            }
        """
        data = {
            "method": "list-records",
            "params": {"domain": domain}
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def register_domain(self, domain, years=1):
        """Register a new domain
        
        Args:
            domain (str): Domain name
            years (int, optional): Number of years to register for. Defaults to 1.
            
        Returns:
            dict: {
                "task": str
            }
        """
        data = {
            "method": "register-domain",
            "params": {
                "domain": domain,
                "years": years
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def remove_dnssec(self, domain, id_):
        """Remove DNSSEC record from domain
        
        Args:
            domain (str): Domain name
            id_ (str): DNSSEC record ID
            
        Returns:
            dict: Empty dictionary on success
        """
        data = {
            "method": "remove-dnssec",
            "params": {
                "domain": domain,
                "id": id_
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def remove_forward(self, domain, from_, to):
        """Remove email forward
        
        Args:
            domain (str): Domain name
            from_ (str): Source email address
            to (str): Destination email address
            
        Returns:
            dict: Empty dictionary on success
        """
        data = {
            "method": "remove-forward",
            "params": {
                "domain": domain,
                "from": from_,
                "to": to
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def remove_glue(self, domain, name):
        """Remove glue record
        
        Args:
            domain (str): Domain name
            name (str): Subdomain name
            
        Returns:
            dict: Empty dictionary on success
        """
        data = {
            "method": "remove-glue",
            "params": {
                "domain": domain,
                "name": name
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def remove_record(self, domain, id_):
        """Remove DNS Record
        
        Args:
            domain (str): Domain name
            id_ (str): Record ID
            
        Returns:
            dict: Empty dictionary on success
        """
        data = {
            "method": "remove-record",
            "params": {
                "domain": domain,
                "id": id_
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

    def renew_domain(self, domain, years=1):
        """Renew one of your domains
        
        Args:
            domain (str): Domain name
            years (int, optional): Number of years to renew for. Defaults to 1.
            
        Returns:
            dict: {
                "task": str
            }
        """
        data = {
            "method": "renew-domain",
            "params": {
                "domain": domain,
                "years": years
            }
        }
        r = requests.post(self.base_url, json=data, headers=self.headers)
        response = r.json()
        if "error" in response:
            raise ValueError(response["error"]["message"])
        return response.get("result", {})

        