"""
Namecheap API client for interacting with Namecheap DNS services.
"""
import os
import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any, Union


class NamecheapAPI:
    """Client for the Namecheap API."""

    BASE_URL = "https://api.namecheap.com/xml.response"

    def __init__(
        self,
        api_key: str,
        api_user: str,
        username: str,
        client_ip: str,
        use_sandbox: bool = False,
        debug: bool = False,
    ):
        """
        Initialize the Namecheap API client.

        Args:
            api_key: Namecheap API key
            api_user: Namecheap API user
            username: Namecheap username (usually same as api_user)
            client_ip: Client IP address
            use_sandbox: Whether to use the sandbox environment (default: False)
            debug: Whether to enable debug logging (default: False)
        """
        self.api_key = api_key
        self.api_user = api_user
        self.username = username
        self.client_ip = client_ip
        self.use_sandbox = use_sandbox
        self.debug = debug
        self.namespace = {"nc": "http://api.namecheap.com/xml.response"}

        if use_sandbox:
            self.BASE_URL = "https://api.sandbox.namecheap.com/xml.response"

    def _build_params(self, command: str, extra_params: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Build the parameters for an API request.

        Args:
            command: API command to execute
            extra_params: Additional parameters for the command

        Returns:
            Dict of parameters for the API request
        """
        params = {
            "ApiUser": self.api_user,
            "ApiKey": self.api_key,
            "UserName": self.username,
            "ClientIp": self.client_ip,
            "Command": command,
        }

        if extra_params:
            params.update(extra_params)

        return params

    def _make_request(
        self, command: str, extra_params: Optional[Dict[str, str]] = None
    ) -> ET.Element:
        """
        Make a request to the Namecheap API.

        Args:
            command: API command to execute
            extra_params: Additional parameters for the command

        Returns:
            ElementTree root element containing the API response

        Raises:
            Exception: If the API returns an error
        """
        params = self._build_params(command, extra_params)
        response = requests.get(self.BASE_URL, params=params)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        root = ET.fromstring(response.text)
        status = root.attrib.get("Status")

        if status != "OK":
            error_msg = "Unknown error"
            errors = root.findall(".//nc:Errors/nc:Error", self.namespace)
            if errors:
                error_msg = " | ".join([error.text for error in errors if error.text])
            raise Exception(f"API returned error: {error_msg}")

        return root

    def get_domains(self) -> List[Dict[str, str]]:
        """
        Get a list of domains in the Namecheap account.

        Returns:
            List of dictionaries containing domain information
        """
        command = "namecheap.domains.getList"
        root = self._make_request(command)

        domains = []
        domain_elements = root.findall(".//nc:CommandResponse/nc:DomainGetListResult/nc:Domain", self.namespace)
            
        for domain in domain_elements:
            domains.append({
                "name": domain.attrib.get("Name", ""),
                "id": domain.attrib.get("ID", ""),
                "status": "Active" if domain.attrib.get("IsExpired") == "false" else "Expired",
                "created": domain.attrib.get("Created", ""),
                "expires": domain.attrib.get("Expires", ""),
                "is_locked": domain.attrib.get("IsLocked", ""),
                "auto_renew": domain.attrib.get("AutoRenew", ""),
                "whois_guard": domain.attrib.get("WhoisGuard", ""),
            })

        return domains

    def get_dns_records(self, domain: str) -> List[Dict[str, str]]:
        """
        Get DNS records for a domain.

        Args:
            domain: Domain name (e.g. "example.com")

        Returns:
            List of dictionaries containing DNS record information
        """
        # Split domain into SLD and TLD parts
        domain_parts = domain.split(".")
        sld = domain_parts[0]
        tld = ".".join(domain_parts[1:])

        command = "namecheap.domains.dns.getHosts"
        params = {
            "SLD": sld,
            "TLD": tld,
        }

        root = self._make_request(command, params)

        records = []
        for record in root.findall(".//nc:CommandResponse/nc:DomainDNSGetHostsResult/nc:host", self.namespace):
            records.append({
                "name": record.attrib.get("Name", ""),
                "type": record.attrib.get("Type", ""),
                "address": record.attrib.get("Address", ""),
                "ttl": record.attrib.get("TTL", ""),
                "mxpref": record.attrib.get("MXPref", ""),
            })

        return records

    def set_dns_record(
        self,
        domain: str,
        record_type: str,
        host: str,
        value: str,
        ttl: int = 3600,
        mx_pref: Optional[int] = None,
    ) -> bool:
        """
        Add a DNS record to a domain.

        Args:
            domain: Domain name (e.g. "example.com")
            record_type: DNS record type (e.g. "A", "CNAME", "MX", etc.)
            host: Host name (e.g. "www" for www.example.com)
            value: Record value (e.g. IP address for A records)
            ttl: Time to live in seconds (default: 3600)
            mx_pref: MX preference (only for MX records)

        Returns:
            True if successful, raises exception otherwise
        """
        # Split domain into SLD and TLD parts
        domain_parts = domain.split(".")
        sld = domain_parts[0]
        tld = ".".join(domain_parts[1:])

        # First get existing records
        existing_records = self.get_dns_records(domain)
        
        # Prepare parameters for setHosts command
        command = "namecheap.domains.dns.setHosts"
        params = {
            "SLD": sld,
            "TLD": tld,
        }
        
        # Add existing records as parameters
        for i, record in enumerate(existing_records, 1):
            params[f"HostName{i}"] = record["name"]
            params[f"RecordType{i}"] = record["type"]
            params[f"Address{i}"] = record["address"]
            params[f"TTL{i}"] = record["ttl"]
            if record["type"] == "MX" and record["mxpref"]:
                params[f"MXPref{i}"] = record["mxpref"]
        
        # Add new record
        i = len(existing_records) + 1
        params[f"HostName{i}"] = host
        params[f"RecordType{i}"] = record_type
        params[f"Address{i}"] = value
        params[f"TTL{i}"] = str(ttl)
        if record_type == "MX" and mx_pref is not None:
            params[f"MXPref{i}"] = str(mx_pref)
        
        # Make API request
        self._make_request(command, params)
        return True

    def delete_dns_record(
        self, domain: str, record_type: str, host: str
    ) -> bool:
        """
        Delete a DNS record from a domain.

        Args:
            domain: Domain name (e.g. "example.com")
            record_type: DNS record type (e.g. "A", "CNAME", "MX", etc.)
            host: Host name (e.g. "www" for www.example.com)

        Returns:
            True if successful, raises exception otherwise
        """
        # Split domain into SLD and TLD parts
        domain_parts = domain.split(".")
        sld = domain_parts[0]
        tld = ".".join(domain_parts[1:])

        # First get existing records
        existing_records = self.get_dns_records(domain)
        
        # Filter out the record to delete
        filtered_records = [
            r for r in existing_records
            if not (r["name"] == host and r["type"] == record_type)
        ]
        
        # If no record was filtered out, nothing to delete
        if len(filtered_records) == len(existing_records):
            raise Exception(f"Record not found: {host}.{domain} ({record_type})")
        
        # Prepare parameters for setHosts command
        command = "namecheap.domains.dns.setHosts"
        params = {
            "SLD": sld,
            "TLD": tld,
        }
        
        # Add remaining records as parameters
        for i, record in enumerate(filtered_records, 1):
            params[f"HostName{i}"] = record["name"]
            params[f"RecordType{i}"] = record["type"]
            params[f"Address{i}"] = record["address"]
            params[f"TTL{i}"] = record["ttl"]
            if record["type"] == "MX" and record["mxpref"]:
                params[f"MXPref{i}"] = record["mxpref"]
        
        # Make API request
        self._make_request(command, params)
        return True

    def update_dns_record(
        self,
        domain: str,
        record_type: str,
        host: str,
        value: str,
        ttl: int = 3600,
        mx_pref: Optional[int] = None,
    ) -> bool:
        """
        Update a DNS record for a domain.

        Args:
            domain: Domain name (e.g. "example.com")
            record_type: DNS record type (e.g. "A", "CNAME", "MX", etc.)
            host: Host name (e.g. "www" for www.example.com)
            value: Record value (e.g. IP address for A records)
            ttl: Time to live in seconds (default: 3600)
            mx_pref: MX preference (only for MX records)

        Returns:
            True if successful, raises exception otherwise
        """
        # Split domain into SLD and TLD parts
        domain_parts = domain.split(".")
        sld = domain_parts[0]
        tld = ".".join(domain_parts[1:])

        # First get existing records
        existing_records = self.get_dns_records(domain)
        
        # Prepare parameters for setHosts command
        command = "namecheap.domains.dns.setHosts"
        params = {
            "SLD": sld,
            "TLD": tld,
        }
        
        # Track if we found the record to update
        found = False
        
        # Add existing records as parameters, updating the matched one
        for i, record in enumerate(existing_records, 1):
            if record["name"] == host and record["type"] == record_type:
                # This is the record we want to update
                params[f"HostName{i}"] = host
                params[f"RecordType{i}"] = record_type
                params[f"Address{i}"] = value
                params[f"TTL{i}"] = str(ttl)
                if record_type == "MX" and mx_pref is not None:
                    params[f"MXPref{i}"] = str(mx_pref)
                found = True
            else:
                # Keep this record as is
                params[f"HostName{i}"] = record["name"]
                params[f"RecordType{i}"] = record["type"]
                params[f"Address{i}"] = record["address"]
                params[f"TTL{i}"] = record["ttl"]
                if record["type"] == "MX" and record["mxpref"]:
                    params[f"MXPref{i}"] = record["mxpref"]
        
        # If we didn't find the record to update, add it
        if not found:
            i = len(existing_records) + 1
            params[f"HostName{i}"] = host
            params[f"RecordType{i}"] = record_type
            params[f"Address{i}"] = value
            params[f"TTL{i}"] = str(ttl)
            if record_type == "MX" and mx_pref is not None:
                params[f"MXPref{i}"] = str(mx_pref)
        
        # Make API request
        self._make_request(command, params)
        return True
