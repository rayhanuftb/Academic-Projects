import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.vpc_simulator import CloudVPCSimulator
from src.nacl_evaluator import NACLEvaluator


class TestCloudNetworking(unittest.TestCase):
    def test_vpc_subnet_addition(self):
        vpc = CloudVPCSimulator("10.0.0.0/16")
        vpc.add_subnet("Public-1a", "10.0.1.0/24", tier="public")
        summary = vpc.get_topology_summary()
        self.assertEqual(summary["total_subnets"], 1)
        self.assertEqual(summary["subnets"]["Public-1a"]["usable_hosts"], 254)

    def test_invalid_subnet_raises(self):
        vpc = CloudVPCSimulator("10.0.0.0/16")
        with self.assertRaises(ValueError):
            vpc.add_subnet("Invalid", "192.168.1.0/24")

    def test_nacl_rule_evaluation(self):
        rules = [
            {"rule_no": 100, "action": "ALLOW", "protocol": "TCP", "port_range": (443, 443)},
            {"rule_no": 200, "action": "DENY", "protocol": "TCP", "port_range": (23, 23)}
        ]
        res_https = NACLEvaluator.evaluate_traffic(rules, "1.2.3.4", port=443, protocol="TCP")
        self.assertEqual(res_https["action"], "ALLOW")

        res_telnet = NACLEvaluator.evaluate_traffic(rules, "1.2.3.4", port=23, protocol="TCP")
        self.assertEqual(res_telnet["action"], "DENY")

        res_default = NACLEvaluator.evaluate_traffic(rules, "1.2.3.4", port=8080, protocol="TCP")
        self.assertEqual(res_default["action"], "DENY")


if __name__ == "__main__":
    unittest.main()
