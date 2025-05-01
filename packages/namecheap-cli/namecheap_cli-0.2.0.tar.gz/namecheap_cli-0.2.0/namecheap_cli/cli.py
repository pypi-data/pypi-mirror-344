"""
Command-line interface for Namecheap API.
"""
import sys
import argparse
import textwrap
from typing import Dict, List, Optional, Any, NoReturn, Tuple

from .api import NamecheapAPI
from .config import Config
from .utils import (
    print_table,
    is_valid_domain,
    validate_record_type,
    validate_ttl,
    confirm_action,
    handle_error,
)


class NamecheapCLI:
    """Command-line interface for Namecheap API."""

    def __init__(self):
        """Initialize the CLI."""
        self.config = Config()
        self.api = None
        self.debug = False

    def _initialize_api(self, force_prompt: bool = False, debug: bool = False) -> NamecheapAPI:
        """
        Initialize the Namecheap API client.

        Args:
            force_prompt: Whether to force prompting for credentials
            debug: Whether to enable debug logging

        Returns:
            Initialized NamecheapAPI instance
        """
        credentials = self.config.get_credentials(force_prompt)
        self.api = NamecheapAPI(
            api_key=credentials["api_key"],
            api_user=credentials["api_user"],
            username=credentials["username"],
            client_ip=credentials["client_ip"],
            use_sandbox=credentials.get("use_sandbox", False),
            debug=debug,
        )
        return self.api

    def list_domains(self) -> None:
        """List all domains in the Namecheap account."""
        try:
            BLUE = "\033[0;34m"
            GREEN = "\033[0;32m"
            YELLOW = "\033[1;33m"
            NC = "\033[0m"  # No Color
            
            api = self._initialize_api(debug=self.debug)
            print(f"{BLUE}Fetching domains from Namecheap...{NC}")
            domains = api.get_domains()

            if not domains:
                print(f"{YELLOW}No domains found.{NC}")
                return

            headers = ["DOMAIN", "STATUS", "EXPIRY DATE"]
            rows = [[d["name"], d["status"], d["expires"]] for d in domains]
            print_table(headers, rows)
        except Exception as e:

            handle_error(e)

    def list_records(self, domain: str) -> None:
        """
        List DNS records for a domain.

        Args:
            domain: Domain name
        """
        try:
            BLUE = "\033[0;34m"
            GREEN = "\033[0;32m"
            YELLOW = "\033[1;33m"
            RED = "\033[0;31m"
            NC = "\033[0m"  # No Color
            
            if not is_valid_domain(domain):
                print(f"{RED}Invalid domain: {domain}{NC}")
                return

            api = self._initialize_api(debug=self.debug)
            print(f"{BLUE}Fetching DNS records for {domain}...{NC}")
            records = api.get_dns_records(domain)

            if not records:
                print(f"{YELLOW}No DNS records found for {domain}.{NC}")
                return

            headers = ["HOST", "TYPE", "VALUE", "TTL"]
            rows = [[r["name"], r["type"], r["address"], r["ttl"]] for r in records]
            print_table(headers, rows)
        except Exception as e:

            handle_error(e)

    def add_record(
        self,
        domain: str,
        record_type: str,
        host: str,
        value: str,
        ttl: str = "3600",
        mx_pref: Optional[str] = None,
    ) -> None:
        """
        Add a DNS record to a domain.

        Args:
            domain: Domain name
            record_type: DNS record type
            host: Host name
            value: Record value
            ttl: Time to live
            mx_pref: MX preference (only for MX records)
        """
        try:
            if not is_valid_domain(domain):
                print(f"Invalid domain: {domain}")
                return

            record_type = record_type.upper()
            if not validate_record_type(record_type):
                print(f"Invalid record type: {record_type}")
                return

            if not validate_ttl(ttl):
                print(f"Invalid TTL: {ttl} (must be between 60 and 86400)")
                return

            # Convert ttl and mx_pref to integers
            ttl_int = int(ttl)
            mx_pref_int = int(mx_pref) if mx_pref is not None else None

            api = self._initialize_api(debug=self.debug)
            print(f"Adding DNS record to {domain}...")
            print(f"Type: {record_type}, Host: {host}, Value: {value}, TTL: {ttl}")

            if api.set_dns_record(
                domain=domain,
                record_type=record_type,
                host=host,
                value=value,
                ttl=ttl_int,
                mx_pref=mx_pref_int,
            ):
                print("DNS record added successfully.")
            else:
                print("Failed to add DNS record.")
        except Exception as e:
            handle_error(e)

    def update_record(
        self,
        domain: str,
        record_type: str,
        host: str,
        value: str,
        ttl: str = "3600",
        mx_pref: Optional[str] = None,
    ) -> None:
        """
        Update a DNS record for a domain.

        Args:
            domain: Domain name
            record_type: DNS record type
            host: Host name
            value: Record value
            ttl: Time to live
            mx_pref: MX preference (only for MX records)
        """
        try:
            if not is_valid_domain(domain):
                print(f"Invalid domain: {domain}")
                return

            record_type = record_type.upper()
            if not validate_record_type(record_type):
                print(f"Invalid record type: {record_type}")
                return

            if not validate_ttl(ttl):
                print(f"Invalid TTL: {ttl} (must be between 60 and 86400)")
                return

            # Convert ttl and mx_pref to integers
            ttl_int = int(ttl)
            mx_pref_int = int(mx_pref) if mx_pref is not None else None

            api = self._initialize_api(debug=self.debug)
            print(f"Updating DNS record for {domain}...")
            print(f"Type: {record_type}, Host: {host}, Value: {value}, TTL: {ttl}")

            if api.update_dns_record(
                domain=domain,
                record_type=record_type,
                host=host,
                value=value,
                ttl=ttl_int,
                mx_pref=mx_pref_int,
            ):
                print("DNS record updated successfully.")
            else:
                print("Failed to update DNS record.")
        except Exception as e:
            handle_error(e)

    def delete_record(
        self, domain: str, record_type: str, host: str
    ) -> None:
        """
        Delete a DNS record from a domain.

        Args:
            domain: Domain name
            record_type: DNS record type
            host: Host name
        """
        try:
            if not is_valid_domain(domain):
                print(f"Invalid domain: {domain}")
                return

            record_type = record_type.upper()
            if not validate_record_type(record_type):
                print(f"Invalid record type: {record_type}")
                return

            api = self._initialize_api(debug=self.debug)
            print(f"Deleting DNS record from {domain}...")
            print(f"Type: {record_type}, Host: {host}")

            if not confirm_action(f"Are you sure you want to delete {host}.{domain} ({record_type})?"):
                print("Operation cancelled.")
                return

            if api.delete_dns_record(
                domain=domain,
                record_type=record_type,
                host=host,
            ):
                print("DNS record deleted successfully.")
            else:
                print("Failed to delete DNS record.")
        except Exception as e:
            handle_error(e)

    def interactive_menu(self) -> None:
        """Display an interactive menu."""
        try:
            self._initialize_api(force_prompt=True, debug=self.debug)
            
            BLUE = "\033[0;34m"
            GREEN = "\033[0;32m"
            YELLOW = "\033[1;33m"
            CYAN = "\033[0;36m"
            RED = "\033[0;31m"
            NC = "\033[0m"  # No Color
            
            while True:
                # Clear screen
                print("\n" * 2)
                
                # Display menu with nice formatting
                print(f"{CYAN}╭────────────────╮{NC}")
                print(f"{CYAN}│{GREEN} Namecheap CLI {CYAN}│{NC}")
                print(f"{CYAN}╰────────────────╯{NC}")
                print("\n" + f"{YELLOW}Please select an option:{NC}\n")
                print(f"{BLUE}[1]{NC} List domains")
                print(f"{BLUE}[2]{NC} View DNS records")
                print(f"{BLUE}[3]{NC} Add DNS record")
                print(f"{BLUE}[4]{NC} Update DNS record")
                print(f"{BLUE}[5]{NC} Delete DNS records")
                print(f"{BLUE}[0]{NC} Exit")
                
                choice = input(f"\n{YELLOW}Enter your choice {BLUE}[0/1/2/3/4/5]{YELLOW} (0):{NC} ") or "0"
                
                if choice == "0":
                    break
                elif choice == "1":
                    self.list_domains()
                    input(f"\n{BLUE}Press Enter to continue...{NC}")
                elif choice == "2":
                    domain = input(f"{YELLOW}Enter domain name:{NC} ")
                    self.list_records(domain)
                    input(f"\n{BLUE}Press Enter to continue...{NC}")
                elif choice == "3":
                    domain = input(f"{YELLOW}Enter domain name:{NC} ")
                    record_type = input(f"{YELLOW}Enter record type (A, CNAME, MX, TXT, etc.):{NC} ")
                    host = input(f"{YELLOW}Enter host (e.g. www, @ for root):{NC} ")
                    value = input(f"{YELLOW}Enter value:{NC} ")
                    ttl = input(f"{YELLOW}Enter TTL (default: 3600):{NC} ") or "3600"
                    mx_pref = None
                    if record_type.upper() == "MX":
                        mx_pref = input(f"{YELLOW}Enter MX preference (default: 10):{NC} ") or "10"
                    self.add_record(domain, record_type, host, value, ttl, mx_pref)
                    input(f"\n{BLUE}Press Enter to continue...{NC}")
                elif choice == "4":
                    domain = input(f"{YELLOW}Enter domain name:{NC} ")
                    record_type = input(f"{YELLOW}Enter record type (A, CNAME, MX, TXT, etc.):{NC} ")
                    host = input(f"{YELLOW}Enter host (e.g. www, @ for root):{NC} ")
                    value = input(f"{YELLOW}Enter new value:{NC} ")
                    ttl = input(f"{YELLOW}Enter TTL (default: 3600):{NC} ") or "3600"
                    mx_pref = None
                    if record_type.upper() == "MX":
                        mx_pref = input(f"{YELLOW}Enter MX preference (default: 10):{NC} ") or "10"
                    self.update_record(domain, record_type, host, value, ttl, mx_pref)
                    input(f"\n{BLUE}Press Enter to continue...{NC}")
                elif choice == "5":
                    domain = input(f"{YELLOW}Enter domain name:{NC} ")
                    record_type = input(f"{YELLOW}Enter record type (A, CNAME, MX, TXT, etc.):{NC} ")
                    host = input(f"{YELLOW}Enter host (e.g. www, @ for root):{NC} ")
                    self.delete_record(domain, record_type, host)
                    input(f"\n{BLUE}Press Enter to continue...{NC}")
                else:
                    print(f"{RED}Invalid choice. Please try again.{NC}")
                    input(f"\n{BLUE}Press Enter to continue...{NC}")
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:

            handle_error(e)

    def run(self) -> None:
        """Run the CLI."""
        parser = argparse.ArgumentParser(
            description="Namecheap DNS Manager CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent("""
                Examples:
                  namecheap domains
                  namecheap records example.com
                  namecheap add -d example.com -t A -H www -v 192.168.1.1 -l 3600
                  namecheap update -d example.com -t A -H www -v 192.168.1.2 -l 3600
                  namecheap delete -d example.com -t A -H www
                """),
        )
        
        # Add global flags
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
        
        # Initialize subparsers
        subparsers = parser.add_subparsers(dest="command", help="Command to execute")
        
        # Initialize command
        parser_init = subparsers.add_parser("init", help="Initialize Namecheap API credentials")
        
        # Domains command
        parser_domains = subparsers.add_parser("domains", help="List all domains")
        
        # Records command
        parser_records = subparsers.add_parser("records", help="List DNS records for a domain")
        parser_records.add_argument("domain", help="Domain name")
        
        # Add record command
        parser_add = subparsers.add_parser("add", help="Add a DNS record")
        parser_add.add_argument("-d", "--domain", required=True, help="Domain name")
        parser_add.add_argument("-t", "--type", required=True, help="Record type (A, CNAME, MX, TXT, etc.)")
        parser_add.add_argument("-H", "--host", required=True, help="Host name (e.g. www, @ for root)")
        parser_add.add_argument("-v", "--value", required=True, help="Record value")
        parser_add.add_argument("-l", "--ttl", default="3600", help="Time to live (default: 3600)")
        parser_add.add_argument("-p", "--priority", help="MX preference (only for MX records)")
        
        # Update record command
        parser_update = subparsers.add_parser("update", help="Update a DNS record")
        parser_update.add_argument("-d", "--domain", required=True, help="Domain name")
        parser_update.add_argument("-t", "--type", required=True, help="Record type (A, CNAME, MX, TXT, etc.)")
        parser_update.add_argument("-H", "--host", required=True, help="Host name (e.g. www, @ for root)")
        parser_update.add_argument("-v", "--value", required=True, help="Record value")
        parser_update.add_argument("-l", "--ttl", default="3600", help="Time to live (default: 3600)")
        parser_update.add_argument("-p", "--priority", help="MX preference (only for MX records)")
        
        # Delete record command
        parser_delete = subparsers.add_parser("delete", help="Delete a DNS record")
        parser_delete.add_argument("-d", "--domain", required=True, help="Domain name")
        parser_delete.add_argument("-t", "--type", required=True, help="Record type (A, CNAME, MX, TXT, etc.)")
        parser_delete.add_argument("-H", "--host", required=True, help="Host name (e.g. www, @ for root)")
        
        # Interactive mode command
        parser_interactive = subparsers.add_parser("interactive", help="Interactive mode")
        
        # Parse arguments
        args = parser.parse_args()
        
        # Check for verbose flag
        if args.verbose:
            self.debug = True
        
        if args.command is None or args.command == "help":
            parser.print_help()
            return
        
        if args.command == "init":
            self._initialize_api(force_prompt=True, debug=self.debug)
            print("Namecheap API credentials initialized.")
        elif args.command == "domains":
            self.list_domains()
        elif args.command == "records":
            self.list_records(args.domain)
        elif args.command == "add":
            self.add_record(
                domain=args.domain,
                record_type=args.type,
                host=args.host,
                value=args.value,
                ttl=args.ttl,
                mx_pref=args.priority,
            )
        elif args.command == "update":
            self.update_record(
                domain=args.domain,
                record_type=args.type,
                host=args.host,
                value=args.value,
                ttl=args.ttl,
                mx_pref=args.priority,
            )
        elif args.command == "delete":
            self.delete_record(
                domain=args.domain,
                record_type=args.type,
                host=args.host,
            )
        elif args.command == "interactive":
            self.interactive_menu()


def main() -> None:
    """Entry point for the namecheap command."""
    cli = NamecheapCLI()
    
    # Check for verbose flag
    if "-v" in sys.argv or "--verbose" in sys.argv:
        cli.debug = True
        # Remove the flag so it doesn't interfere with command parsing
        if "-v" in sys.argv:
            sys.argv.remove("-v")
        if "--verbose" in sys.argv:
            sys.argv.remove("--verbose")
    
    # If no arguments were provided, launch interactive mode
    if len(sys.argv) == 1:
        cli.interactive_menu()
    else:
        cli.run()


if __name__ == "__main__":
    main()
