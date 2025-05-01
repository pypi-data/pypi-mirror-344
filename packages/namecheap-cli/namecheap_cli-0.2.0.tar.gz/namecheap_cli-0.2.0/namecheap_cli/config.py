"""
Configuration handling for Namecheap CLI.
"""
import os
import json
import getpass
import requests
from pathlib import Path
from typing import Dict, Optional, Any


class Config:
    """Configuration handler for Namecheap CLI."""

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the configuration handler.

        Args:
            config_dir: Directory to store configuration (default: ~/.namecheap)
        """
        if config_dir is None:
            self.config_dir = os.path.expanduser("~/.namecheap")
        else:
            self.config_dir = config_dir

        self.config_file = os.path.join(self.config_dir, "config.json")
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists."""
        os.makedirs(self.config_dir, exist_ok=True)
        # Ensure config directory has proper permissions (700)
        os.chmod(self.config_dir, 0o700)

    def _get_client_ip(self) -> str:
        """
        Get the client's public IP address.

        Returns:
            Client's public IP address
        """
        try:
            response = requests.get("https://api.ipify.org")
            return response.text.strip()
        except Exception:
            # Fall back to a default if we can't get the IP
            return "127.0.0.1"

    def load(self) -> Dict[str, Any]:
        """
        Load configuration.

        Returns:
            Dictionary containing configuration
        """
        if not os.path.exists(self.config_file):
            return {}

        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def save(self, config: Dict[str, Any]) -> None:
        """
        Save configuration.

        Args:
            config: Dictionary containing configuration
        """
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=2)
        
        # Ensure config file has proper permissions (600)
        os.chmod(self.config_file, 0o600)

    def prompt_for_credentials(self) -> Dict[str, str]:
        """
        Prompt user for Namecheap API credentials.

        Returns:
            Dictionary containing API credentials
        """
        print("\nPlease enter your Namecheap API credentials:")
        api_key = getpass.getpass("API Key: ")
        api_user = input("API User: ")
        username = input("Username (leave blank to use API User): ") or api_user
        client_ip = self._get_client_ip()
        
        use_sandbox = input("Use sandbox environment? (y/N): ").lower() == "y"

        credentials = {
            "api_key": api_key,
            "api_user": api_user,
            "username": username,
            "client_ip": client_ip,
            "use_sandbox": use_sandbox,
        }

        return credentials

    def get_credentials(self, force_prompt: bool = False) -> Dict[str, str]:
        """
        Get API credentials, either from environment variables, config, or by prompting.

        Args:
            force_prompt: Whether to force prompting for credentials

        Returns:
            Dictionary containing API credentials
        """
        # Check environment variables first
        if not force_prompt:
            api_key = os.environ.get("NAMECHEAP_API_KEY")
            api_user = os.environ.get("NAMECHEAP_API_USER")
            username = os.environ.get("NAMECHEAP_USERNAME")
            client_ip = os.environ.get("NAMECHEAP_CLIENT_IP")
            use_sandbox = os.environ.get("NAMECHEAP_USE_SANDBOX")

            if api_key and api_user:
                print("Using credentials from environment variables")
                return {
                    "api_key": api_key,
                    "api_user": api_user,
                    "username": username or api_user,
                    "client_ip": client_ip or self._get_client_ip(),
                    "use_sandbox": use_sandbox == "true" if use_sandbox else False,
                }

        # If not in environment variables, check config file
        config = self.load()
        
        if not force_prompt and "credentials" in config:
            return config["credentials"]
        
        # If all else fails, prompt the user
        credentials = self.prompt_for_credentials()
        
        # Update config with new credentials
        config["credentials"] = credentials
        self.save(config)
        
        return credentials


