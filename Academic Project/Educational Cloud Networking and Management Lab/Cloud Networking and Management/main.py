#!/usr/bin/env python3
"""
CLI Tool for Educational Cloud Networking & Architecture Validator.
Course: Educational Cloud Networking and Management Lab (ICTE 4342)
"""

import sys
from src.vpc_simulator import CloudVPCSimulator
from src.nacl_evaluator import NACLEvaluator


def main():
    print("\n==============================================================")
    print("  Educational Cloud Networking & Architecture Topology Design ")
    print("==============================================================")

    # 1. Instantiate 3-Tier Educational Cloud VPC
    vpc = CloudVPCSimulator(vpc_cidr="10.0.0.0/16", vpc_name="EduCloud-Production-VPC")
    vpc.add_subnet("Public-Web-1a", "10.0.1.0/24", tier="public", az="us-east-1a")
    vpc.add_subnet("Public-Web-1b", "10.0.2.0/24", tier="public", az="us-east-1b")
    vpc.add_subnet("Private-App-1a", "10.0.10.0/24", tier="private-app", az="us-east-1a")
    vpc.add_subnet("Private-App-1b", "10.0.11.0/24", tier="private-app", az="us-east-1b")
    vpc.add_subnet("Isolated-DB-1a", "10.0.20.0/24", tier="private-db", az="us-east-1a")
    vpc.add_subnet("Isolated-DB-1b", "10.0.21.0/24", tier="private-db", az="us-east-1b")

    vpc.add_route("Public-Route-Table", "0.0.0.0/0", "igw-edu-cloud-01")
    vpc.add_route("Private-Route-Table", "0.0.0.0/0", "nat-gateway-01")

    summary = vpc.get_topology_summary()
    print(f"\n[+] Simulated VPC Name: {summary['vpc_name']} (CIDR: {summary['vpc_cidr']})")
    print(f"[+] Total Configured Subnets: {summary['total_subnets']}\n")

    print(f"{'Subnet Name':<20} | {'Tier':<14} | {'CIDR Block':<16} | {'AZ':<12} | {'Usable IPs'}")
    print("-" * 75)
    for name, s in summary['subnets'].items():
        print(f"{name:<20} | {s['tier']:<14} | {s['cidr']:<16} | {s['availability_zone']:<12} | {s['usable_hosts']}")

    # 2. Test NACL Evaluation
    print("\n[+] Testing Stateless Network Access Control List (NACL) Rules:")
    nacl_rules = [
        {"rule_no": 100, "action": "ALLOW", "protocol": "TCP", "port_range": (80, 80)},
        {"rule_no": 110, "action": "ALLOW", "protocol": "TCP", "port_range": (443, 443)},
        {"rule_no": 120, "action": "ALLOW", "protocol": "TCP", "port_range": (22, 22)},
        {"rule_no": 200, "action": "DENY", "protocol": "TCP", "port_range": (23, 23)}
    ]

    test_checks = [(80, "TCP"), (443, "TCP"), (23, "TCP"), (8080, "TCP")]
    for port, proto in test_checks:
        res = NACLEvaluator.evaluate_traffic(nacl_rules, "0.0.0.0/0", port=port, protocol=proto)
        print(f"  * Port {port:<5} ({proto}): Rule #{res['matched_rule']} -> {res['action']} ({res['explanation']})")

    print("\n[✓] Cloud networking topology validation completed successfully.\n")


if __name__ == "__main__":
    main()
