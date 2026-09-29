import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ip_calculator import IPCalculator
from src.subnetter import VLSMSubnetter
from src.port_scanner import SafePortScanner


class TestNetworkSecurity(unittest.TestCase):
    def test_ip_validation(self):
        self.assertTrue(IPCalculator.validate_ip("192.168.1.1"))
        self.assertTrue(IPCalculator.validate_ip("10.0.0.1"))
        self.assertFalse(IPCalculator.validate_ip("999.999.999.999"))
        self.assertFalse(IPCalculator.validate_ip("invalid-ip"))

    def test_subnet_calculator(self):
        res = IPCalculator.calculate_subnet("192.168.10.0/24")
        self.assertEqual(res["network_address"], "192.168.10.0")
        self.assertEqual(res["broadcast_address"], "192.168.10.255")
        self.assertEqual(res["netmask"], "255.255.255.0")
        self.assertEqual(res["usable_hosts"], 254)
        self.assertEqual(res["first_usable_host"], "192.168.10.1")
        self.assertEqual(res["last_usable_host"], "192.168.10.254")
        self.assertTrue(res["is_private"])

    def test_vlsm_subnetter(self):
        base_net = "192.168.1.0/24"
        departments = [
            {"name": "Lab A", "hosts_needed": 60},
            {"name": "Lab B", "hosts_needed": 25}
        ]
        allocations = VLSMSubnetter.design_vlsm(base_net, departments)
        self.assertEqual(len(allocations), 2)
        self.assertEqual(allocations[0]["status"], "Allocated")
        self.assertEqual(allocations[0]["allocated_cidr"], "192.168.1.0/26")
        self.assertEqual(allocations[1]["allocated_cidr"], "192.168.1.64/27")

    def test_safe_port_scanner_single(self):
        scanner = SafePortScanner(target_host="127.0.0.1", timeout_sec=0.1)
        res = scanner.scan_single_port(80)
        self.assertIn("state", res)
        self.assertIn(res["state"], ["Open", "Closed", "Filtered / Unreachable"])


if __name__ == "__main__":
    unittest.main()
