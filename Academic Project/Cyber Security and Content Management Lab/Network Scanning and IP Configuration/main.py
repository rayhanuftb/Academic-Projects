#!/usr/bin/env python3
"""
CLI Tool for Network Scanning and IP Configuration Practical Lab.
Course: Cyber Security and Content Management Lab (ICT 4462)
"""

import sys
import argparse
from src.ip_calculator import IPCalculator
from src.subnetter import VLSMSubnetter
from src.port_scanner import SafePortScanner


def main():
    parser = argparse.ArgumentParser(description="Network Scanning and IP Configuration Practical Diagnostic Suite")
    parser.add_argument("--calc", type=str, default=None, help="Calculate IPv4 Subnet Parameters (e.g., '192.168.10.0/26')")
    parser.add_argument("--scan", type=str, default=None, help="Authorized Target Host for Port Diagnostic (default: '127.0.0.1')")
    parser.add_argument("--ports", type=str, default="21,22,80,443,3306,8080", help="Comma-separated port numbers to check")
    parser.add_argument("--vlsm", action="store_true", help="Run educational VLSM Departmental Subnet Allocation Demo")

    args = parser.parse_args()

    print("\n================================================================")
    print("  Cyber Security & IP Configuration - Diagnostic Laboratory Tool ")
    print("================================================================")

    if args.calc:
        print(f"\n[+] Computing IPv4 Parameters for CIDR: {args.calc}")
        try:
            res = IPCalculator.calculate_subnet(args.calc)
            print(f"  * Network Address      : {res['network_address']}")
            print(f"  * Broadcast Address    : {res['broadcast_address']}")
            print(f"  * Subnet Mask          : {res['netmask']}")
            print(f"  * Wildcard / Hostmask  : {res['hostmask']}")
            print(f"  * Total Address Space  : {res['total_addresses']} IPs")
            print(f"  * Usable Host Range    : {res['first_usable_host']} -> {res['last_usable_host']} ({res['usable_hosts']} hosts)")
            print(f"  * Private / RFC 1918   : {res['is_private']}")
        except Exception as e:
            print(f"[-] Calculation Error: {e}", file=sys.stderr)

    elif args.vlsm:
        print("\n[+] Designing VLSM Subnet Scheme for University Campus Network:")
        base_net = "192.168.1.0/24"
        departments = [
            {"name": "Computer Science Lab", "hosts_needed": 60},
            {"name": "Faculty & Staff Offices", "hosts_needed": 28},
            {"name": "Smart Classroom IoT", "hosts_needed": 14},
            {"name": "Server & Admin Segment", "hosts_needed": 6}
        ]
        allocations = VLSMSubnetter.design_vlsm(base_net, departments)
        print(f"Base Network: {base_net}\n")
        print(f"{'Department Name':<26} | {'Needed':<6} | {'Allocated CIDR':<16} | {'Subnet Mask':<15} | {'Usable Hosts'}")
        print("-" * 80)
        for alloc in allocations:
            print(f"{alloc['name']:<26} | {alloc['hosts_needed']:<6} | {alloc['allocated_cidr']:<16} | {alloc['netmask']:<15} | {alloc['usable_capacity']}")

    else:
        target = args.scan if args.scan else "127.0.0.1"
        port_nums = [int(p.strip()) for p in args.ports.split(",") if p.strip().isdigit()]
        print(f"\n[+] Running Safe Diagnostic Port Audit on Authorized Host: {target}")
        print("    (Safety notice: Restricted to diagnostic educational monitoring)")
        
        scanner = SafePortScanner(target_host=target, timeout_sec=0.3)
        results = scanner.scan_ports(port_nums)

        print(f"\n{'Port':<8} | {'Service Description':<32} | {'State'}")
        print("-" * 55)
        for r in results:
            print(f"{r['port']:<8} | {r['service']:<32} | {r['state']}")

    print("\n[✓] Diagnostic process completed successfully.\n")


if __name__ == "__main__":
    main()
