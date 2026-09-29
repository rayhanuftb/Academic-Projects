# Design and Simulation of a Banking Network System

> Academic Project / Practical Work

## 📚 Course Information

- **Course Title:** Networking and Telecommunication Lab
- **Course Code:** ICT 4262
- **Student:** Rayhanul Islam
- **Institution:** University of Frontier Technology, Bangladesh

---

## ⚠️ DISCLAIMER

This is a SIMULATION for academic purposes only. It does NOT represent a real banking network deployment. All IP addresses, configurations, and topologies are simulated.

---

## 📌 Overview

A documented banking network simulation demonstrating network topology design, VLAN configuration, IP addressing, subnetting, routing, and connectivity testing. The project includes a Python-based network simulator and Cisco-style configuration templates.

---

## 🎯 Learning Objectives

1. Design a hierarchical network topology for a banking environment
2. Configure VLANs for departmental segmentation
3. Implement IP addressing and subnetting schemes
4. Configure static routing between VLANs
5. Test network connectivity and analyze traffic paths

---

## 🏗️ Network Architecture

### Topology Design

```
                    [Internet]
                        |
                  [Firewall]
                        |
                  [Core Router]
                        |
                  [Core Switch]
                   /    |    \
          [Teller SW] [ATM SW] [Server Farm]
           /    \       |    \       |
       [PC1] [PC2]  [ATM1] [ATM2]  [DB/App]
```

### VLAN Design

| VLAN ID | Name | Subnet | Gateway | Purpose |
|---------|------|--------|---------|---------|
| 10 | Management | 10.10.10.0/24 | 10.10.10.1 | Core banking management |
| 20 | Teller | 10.10.20.0/24 | 10.10.20.1 | Customer service terminals |
| 30 | ATM | 10.10.30.0/24 | 10.10.30.1 | ATM network |
| 40 | Server | 10.10.40.0/24 | 10.10.40.1 | Server farm |
| 50 | Guest | 10.10.50.0/24 | 10.10.50.1 | Guest Wi-Fi |

### IP Addressing

| Device | IP Address | VLAN | Type |
|--------|------------|------|------|
| Core-Router | 10.10.10.1 | 10 | Router |
| Core-Switch | 10.10.10.2 | 10 | L3 Switch |
| Firewall | 10.10.10.3 | 10 | Firewall |
| DB-Server | 10.10.40.10 | 40 | Server |
| App-Server | 10.10.40.20 | 40 | Server |
| Teller-PC-1 | 10.10.20.101 | 20 | PC |
| Teller-PC-2 | 10.10.20.102 | 20 | PC |
| ATM-Branch-1 | 10.10.30.101 | 30 | ATM |
| ATM-Branch-2 | 10.10.30.102 | 30 | ATM |

---

## 📁 Project Structure

```
Banking Network Simulation/
├── README.md
├── src/
│   └── network_sim.py          Network topology simulator
├── configs/
│   └── router_config.txt       Cisco router configuration
├── data/
│   └── network_topology.json   Topology data
└── docs/
    └── topology_diagram.md     Network diagram description
```

---

## 🚀 How to Run

```bash
python src/network_sim.py
```

---

## 🎓 Academic Note

This project demonstrates networking concepts including hierarchical topology design, VLAN segmentation, IP subnetting, static routing, and configuration generation. All components are simulated for educational purposes.

---

## 👤 Author

**Rayhanul Islam**  
Educational Technology and Engineering  
University of Frontier Technology, Bangladesh
