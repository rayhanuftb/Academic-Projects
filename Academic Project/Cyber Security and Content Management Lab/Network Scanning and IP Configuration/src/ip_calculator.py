import ipaddress
from typing import Dict, Any, List, Optional


class IPCalculator:
    """Calculates IPv4 subnet parameters, network addresses, broadcast, and valid host ranges."""

    @staticmethod
    def calculate_subnet(cidr_str: str) -> Dict[str, Any]:
        """Parses a CIDR notation (e.g. '192.168.1.0/24') and returns detailed networking metrics."""
        if not cidr_str or not isinstance(cidr_str, str):
            raise ValueError("CIDR string must be a non-empty string.")

        try:
            network = ipaddress.IPv4Network(cidr_str.strip(), strict=False)
        except Exception as e:
            raise ValueError(f"Invalid IPv4 CIDR notation: {str(e)}")

        hosts = list(network.hosts())
        total_addresses = network.num_addresses
        usable_hosts = len(hosts)

        return {
            "cidr": str(network),
            "network_address": str(network.network_address),
            "broadcast_address": str(network.broadcast_address),
            "netmask": str(network.netmask),
            "hostmask": str(network.hostmask),
            "prefix_length": network.prefixlen,
            "total_addresses": total_addresses,
            "usable_hosts": usable_hosts,
            "first_usable_host": str(hosts[0]) if hosts else "None",
            "last_usable_host": str(hosts[-1]) if hosts else "None",
            "is_private": network.is_private,
            "is_loopback": network.is_loopback
        }

    @staticmethod
    def validate_ip(ip_str: str) -> bool:
        """Validates if a string is a well-formed IPv4 address."""
        if not ip_str or not isinstance(ip_str, str):
            return False
        try:
            ipaddress.IPv4Address(ip_str.strip())
            return True
        except ValueError:
            return False
