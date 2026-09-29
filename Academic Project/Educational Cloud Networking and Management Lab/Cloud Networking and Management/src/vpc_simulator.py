import ipaddress
from typing import Dict, List, Any


class CloudVPCSimulator:
    """Simulates a multi-tier educational Cloud Virtual Private Cloud (VPC) topology."""

    def __init__(self, vpc_cidr: str = "10.0.0.0/16", vpc_name: str = "EduCloud-VPC"):
        self.vpc_name = vpc_name
        self.vpc_network = ipaddress.IPv4Network(vpc_cidr)
        self.subnets: Dict[str, Dict[str, Any]] = {}
        self.route_tables: Dict[str, List[Dict[str, str]]] = {}
        self.security_groups: Dict[str, List[Dict[str, Any]]] = {}

    def add_subnet(self, name: str, cidr: str, tier: str = "public", az: str = "us-east-1a") -> None:
        """Adds a structured subnet partition within the VPC."""
        subnet_net = ipaddress.IPv4Network(cidr)
        if not subnet_net.subnet_of(self.vpc_network):
            raise ValueError(f"Subnet CIDR {cidr} is not a valid subset of VPC CIDR {self.vpc_network}")

        self.subnets[name] = {
            "name": name,
            "cidr": str(subnet_net),
            "tier": tier,  # 'public', 'private-app', 'private-db'
            "availability_zone": az,
            "total_ips": subnet_net.num_addresses,
            "usable_hosts": len(list(subnet_net.hosts()))
        }

    def add_route(self, table_name: str, destination_cidr: str, target: str) -> None:
        """Adds a route entry to a VPC route table."""
        if table_name not in self.route_tables:
            self.route_tables[table_name] = []
        self.route_tables[table_name].append({
            "destination": destination_cidr,
            "target": target  # e.g., 'igw-01' (Internet Gateway), 'nat-01' (NAT Gateway), 'local'
        })

    def get_topology_summary(self) -> Dict[str, Any]:
        """Generates a complete architectural summary of the simulated cloud network."""
        return {
            "vpc_name": self.vpc_name,
            "vpc_cidr": str(self.vpc_network),
            "subnets": self.subnets,
            "route_tables": self.route_tables,
            "total_subnets": len(self.subnets)
        }
