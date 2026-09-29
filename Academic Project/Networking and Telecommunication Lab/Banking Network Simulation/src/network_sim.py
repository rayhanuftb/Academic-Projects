#!/usr/bin/env python3
"""
Banking Network Topology Simulator

Educational simulation of a banking network infrastructure.
This is a SIMULATION for academic purposes only.
It does NOT represent a real banking network deployment.

Author: Rayhanul Islam
Course: Networking and Telecommunication Lab (ICT 4262)
"""

import json
from dataclasses import dataclass, field
from typing import List, Dict
from pathlib import Path


@dataclass
class Device:
    """Represents a network device."""
    name: str
    device_type: str
    ip_address: str
    subnet_mask: str
    gateway: str
    vlan: int = 0
    status: str = "active"
    interfaces: List[str] = field(default_factory=list)
    connected_to: List[str] = field(default_factory=list)


@dataclass
class VLAN:
    """Represents a VLAN configuration."""
    id: int
    name: str
    subnet: str
    gateway: str
    description: str


@dataclass
class Route:
    """Represents a routing table entry."""
    destination: str
    gateway: str
    interface: str
    metric: int = 1


class BankingNetworkSimulator:
    """Simulates a banking network infrastructure."""

    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.vlans: Dict[int, VLAN] = {}
        self.routes: List[Route] = []
        self._setup_network()

    def _setup_network(self):
        """Configure the banking network topology."""
        self._setup_vlans()
        self._setup_devices()
        self._setup_routing()

    def _setup_vlans(self):
        """Configure VLANs for different departments."""
        self.vlans = {
            10: VLAN(10, "Management", "10.10.10.0/24", "10.10.10.1", "Core banking management"),
            20: VLAN(20, "Teller", "10.10.20.0/24", "10.10.20.1", "Customer service terminals"),
            30: VLAN(30, "ATM", "10.10.30.0/24", "10.10.30.1", "ATM network"),
            40: VLAN(40, "Server", "10.10.40.0/24", "10.10.40.1", "Server farm"),
            50: VLAN(50, "Guest", "10.10.50.0/24", "10.10.50.1", "Guest Wi-Fi"),
        }

    def _setup_devices(self):
        """Configure network devices."""
        self.devices = {
            "core-router": Device(
                name="Core-Router",
                device_type="Router",
                ip_address="10.10.10.1",
                subnet_mask="255.255.255.0",
                gateway="0.0.0.0",
                vlan=10,
                interfaces=["GigE0/0", "GigE0/1", "GigE0/2", "GigE0/3", "GigE0/4"],
            ),
            "core-switch": Device(
                name="Core-Switch",
                device_type="Layer3 Switch",
                ip_address="10.10.10.2",
                subnet_mask="255.255.255.0",
                gateway="10.10.10.1",
                vlan=10,
                interfaces=["GigE1/0-4", "GigE1/5-8"],
            ),
            "firewall": Device(
                name="Firewall",
                device_type="Firewall",
                ip_address="10.10.10.3",
                subnet_mask="255.255.255.0",
                gateway="10.10.10.1",
                vlan=10,
                interfaces=["WAN", "LAN", "DMZ"],
            ),
            "db-server": Device(
                name="DB-Server",
                device_type="Server",
                ip_address="10.10.40.10",
                subnet_mask="255.255.255.0",
                gateway="10.10.40.1",
                vlan=40,
            ),
            "app-server": Device(
                name="App-Server",
                device_type="Server",
                ip_address="10.10.40.20",
                subnet_mask="255.255.255.0",
                gateway="10.10.40.1",
                vlan=40,
            ),
            "teller-switch-1": Device(
                name="Teller-Switch-1",
                device_type="Access Switch",
                ip_address="10.10.20.2",
                subnet_mask="255.255.255.0",
                gateway="10.10.20.1",
                vlan=20,
                interfaces=["Fa0/1-24"],
            ),
            "teller-pc-1": Device(
                name="Teller-PC-1",
                device_type="PC",
                ip_address="10.10.20.101",
                subnet_mask="255.255.255.0",
                gateway="10.10.20.1",
                vlan=20,
            ),
            "teller-pc-2": Device(
                name="Teller-PC-2",
                device_type="PC",
                ip_address="10.10.20.102",
                subnet_mask="255.255.255.0",
                gateway="10.10.20.1",
                vlan=20,
            ),
            "atm-switch": Device(
                name="ATM-Switch",
                device_type="Access Switch",
                ip_address="10.10.30.2",
                subnet_mask="255.255.255.0",
                gateway="10.10.30.1",
                vlan=30,
            ),
            "atm-1": Device(
                name="ATM-Branch-1",
                device_type="ATM",
                ip_address="10.10.30.101",
                subnet_mask="255.255.255.0",
                gateway="10.10.30.1",
                vlan=30,
            ),
            "atm-2": Device(
                name="ATM-Branch-2",
                device_type="ATM",
                ip_address="10.10.30.102",
                subnet_mask="255.255.255.0",
                gateway="10.10.30.1",
                vlan=30,
            ),
        }

        self.devices["core-router"].connected_to = [
            "core-switch", "firewall", "teller-switch-1", "atm-switch"
        ]

    def _setup_routing(self):
        """Configure static routing."""
        self.routes = [
            Route("10.10.10.0/24", "0.0.0.0", "GigE0/0", 0),
            Route("10.10.20.0/24", "10.10.10.2", "GigE0/1", 1),
            Route("10.10.30.0/24", "10.10.10.2", "GigE0/2", 1),
            Route("10.10.40.0/24", "10.10.10.2", "GigE0/3", 1),
            Route("10.10.50.0/24", "10.10.10.2", "GigE0/4", 1),
            Route("0.0.0.0/0", "10.10.10.1", "WAN", 0),
        ]

    def get_topology(self) -> dict:
        """Return the network topology."""
        return {
            "vlans": {k: {"id": v.id, "name": v.name, "subnet": v.subnet, "gateway": v.gateway}
                      for k, v in self.vlans.items()},
            "devices": {k: {"name": v.name, "type": v.device_type, "ip": v.ip_address,
                            "vlan": v.vlan, "status": v.status}
                        for k, v in self.devices.items()},
            "routes": [{"destination": r.destination, "gateway": r.gateway,
                        "interface": r.interface, "metric": r.metric} for r in self.routes],
        }

    def simulate_connectivity(self, source_ip: str, dest_ip: str) -> dict:
        """Simulate ping between two devices."""
        source_device = None
        dest_device = None
        for dev in self.devices.values():
            if dev.ip_address == source_ip:
                source_device = dev
            if dev.ip_address == dest_ip:
                dest_device = dev

        if not source_device or not dest_device:
            return {"success": False, "error": "Device not found"}

        same_vlan = source_device.vlan == dest_device.vlan
        success = True

        return {
            "source": source_device.name,
            "destination": dest_device.name,
            "success": success,
            "hops": 1 if same_vlan else 2,
            "same_vlan": same_vlan,
            "path": f"{source_device.name} -> Core-Switch -> {dest_device.name}" if same_vlan
                    else f"{source_device.name} -> Core-Switch -> Core-Router -> Core-Switch -> {dest_device.name}",
        }

    def generate_config(self, device_name: str) -> str:
        """Generate Cisco-style configuration for a device."""
        device = self.devices.get(device_name)
        if not device:
            return "Device not found"

        config_lines = [
            f"! Configuration for {device.name}",
            f"hostname {device.name.replace('-', '_')}",
            "",
            "interface GigabitEthernet0/0",
            f" ip address {device.ip_address} {device.subnet_mask}",
            " no shutdown",
            "",
        ]

        if device.device_type == "Router":
            config_lines.extend([
                "ip routing",
                "",
            ])
            for route in self.routes:
                config_lines.append(f"ip route {route.destination} {route.gateway}")

        return "\n".join(config_lines)

    def print_summary(self):
        """Print a summary of the network."""
        print("=" * 60)
        print("BANKING NETWORK TOPOLOGY SUMMARY")
        print("=" * 60)

        print(f"\nTotal Devices: {len(self.devices)}")
        print(f"Total VLANs: {len(self.vlans)}")

        print("\nVLAN Configuration:")
        for vlan in self.vlans.values():
            print(f"  VLAN {vlan.id}: {vlan.name} ({vlan.subnet})")

        print("\nDevices:")
        for dev in self.devices.values():
            print(f"  {dev.name} ({dev.device_type}) - {dev.ip_address} [VLAN {dev.vlan}]")

        print("\nRouting Table:")
        for route in self.routes:
            print(f"  {route.destination} via {route.gateway} ({route.interface})")


def save_topology(simulator: BankingNetworkSimulator, output_dir: str = "data") -> str:
    """Save topology to JSON."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    filepath = path / "network_topology.json"
    with open(filepath, "w") as f:
        json.dump(simulator.get_topology(), f, indent=2)
    return str(filepath)


if __name__ == "__main__":
    sim = BankingNetworkSimulator()
    sim.print_summary()

    filepath = save_topology(sim)
    print(f"\nTopology saved to: {filepath}")

    print("\nConnectivity Test:")
    result = sim.simulate_connectivity("10.10.20.101", "10.10.20.102")
    print(f"  {result['source']} -> {result['destination']}: {'UP' if result['success'] else 'DOWN'}")
    print(f"  Path: {result['path']}")

    print("\nRouter Configuration:")
    print(sim.generate_config("core-router"))
