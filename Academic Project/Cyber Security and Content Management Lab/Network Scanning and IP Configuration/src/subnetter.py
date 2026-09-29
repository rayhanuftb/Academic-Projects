import ipaddress
from typing import List, Dict, Any


class VLSMSubnetter:
    """Computes Variable Length Subnet Masking (VLSM) allocations for departmental networks."""

    @staticmethod
    def design_vlsm(base_network: str, subnets_req: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Allocates subnets sorted in descending order of required hosts.
        subnets_req format: [{'name': 'Lab A', 'hosts_needed': 50}, ...]
        """
        net = ipaddress.IPv4Network(base_network, strict=False)
        # Sort requirements descending by required host count
        sorted_reqs = sorted(subnets_req, key=lambda x: x['hosts_needed'], reverse=True)

        current_ip = int(net.network_address)
        max_ip = int(net.broadcast_address)
        results = []

        for item in sorted_reqs:
            needed = item['hosts_needed']
            # Find smallest power of 2 that accommodates needed + 2 (network & broadcast)
            total_needed = needed + 2
            prefix = 32 - (total_needed - 1).bit_length()
            subnet_size = 2 ** (32 - prefix)

            if current_ip + subnet_size - 1 > max_ip:
                results.append({
                    "name": item['name'],
                    "status": "Failed - Out of Address Space",
                    "hosts_needed": needed
                })
                continue

            sub = ipaddress.IPv4Network((current_ip, prefix))
            hosts = list(sub.hosts())

            results.append({
                "name": item['name'],
                "status": "Allocated",
                "hosts_needed": needed,
                "allocated_cidr": str(sub),
                "network_address": str(sub.network_address),
                "broadcast_address": str(sub.broadcast_address),
                "netmask": str(sub.netmask),
                "usable_capacity": len(hosts),
                "usable_range": f"{hosts[0]} - {hosts[-1]}" if hosts else "None"
            })
            current_ip += subnet_size

        return results
