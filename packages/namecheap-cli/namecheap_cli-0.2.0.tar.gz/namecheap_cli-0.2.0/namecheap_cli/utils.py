"""
Utility functions for Namecheap CLI.
"""
import sys
import re
from typing import Dict, List, Any, Optional


def print_table(headers: List[str], rows: List[List[str]], colors: bool = True) -> None:
    """
    Print a formatted table with nice borders.

    Args:
        headers: List of column headers
        rows: List of rows, each row is a list of values
        colors: Whether to use colors in output
    """
    if colors:
        BLUE = "\033[0;34m"
        GREEN = "\033[0;32m"
        CYAN = "\033[0;36m"
        NC = "\033[0m"  # No Color
    else:
        BLUE = ""
        GREEN = ""
        CYAN = ""
        NC = ""

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Calculate total width
    total_width = sum(col_widths) + (len(col_widths) * 3) - 1

    # Print top border
    print(f"{CYAN}╭{'─' * total_width}╮{NC}")

    # Print headers
    header_format = "│ " + " │ ".join([f"{{:{w}}}" for w in col_widths]) + " │"
    print(f"{CYAN}│{GREEN}{header_format.format(*headers)}{CYAN}│{NC}")

    # Print separator
    print(f"{CYAN}├{'─' * total_width}┤{NC}")

    # Print rows
    row_format = "│ " + " │ ".join([f"{{:{w}}}" for w in col_widths]) + " │"
    for row in rows:
        print(f"{CYAN}{row_format.format(*[str(val) for val in row])}{NC}")

    # Print bottom border
    print(f"{CYAN}╰{'─' * total_width}╯{NC}")


def is_valid_domain(domain: str) -> bool:
    """
    Validate a domain name.

    Args:
        domain: Domain name to validate

    Returns:
        True if the domain is valid, False otherwise
    """
    pattern = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    return bool(re.match(pattern, domain))


def validate_record_type(record_type: str) -> bool:
    """
    Validate a DNS record type.

    Args:
        record_type: DNS record type to validate

    Returns:
        True if the record type is valid, False otherwise
    """
    valid_types = ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SRV", "URL"]
    return record_type.upper() in valid_types


def validate_ttl(ttl: str) -> bool:
    """
    Validate a TTL value.

    Args:
        ttl: TTL value to validate

    Returns:
        True if the TTL is valid, False otherwise
    """
    try:
        ttl_int = int(ttl)
        return ttl_int >= 60 and ttl_int <= 86400
    except ValueError:
        return False


def confirm_action(message: str) -> bool:
    """
    Ask for confirmation before proceeding with an action.

    Args:
        message: Message to display

    Returns:
        True if confirmed, False otherwise
    """
    YELLOW = "\033[1;33m"
    NC = "\033[0m"  # No Color
    response = input(f"{YELLOW}{message} (y/N): {NC}").lower()
    return response == "y"


def handle_error(e: Exception, exit_on_error: bool = False) -> None:
    """
    Handle an error.

    Args:
        e: Exception that was raised
        exit_on_error: Whether to exit the program on error
    """
    RED = "\033[0;31m"
    NC = "\033[0m"  # No Color
    print(f"{RED}Error: {str(e)}{NC}", file=sys.stderr)
    if exit_on_error:
        sys.exit(1)
