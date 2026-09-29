# Cloud Networking and Management Practical Work

**Course:** Educational Cloud Networking and Management Lab (ICTE 4342)  
**Academic Program:** B.Sc. in Educational Technology and Engineering  
**Institution:** University of Frontier Technology, Bangladesh  
**Author:** Rayhanul Islam

---

## 📌 Project Overview

This project provides a comprehensive architectural blueprint, simulation framework, and Infrastructure as Code (IaC) specification for a highly available, multi-tier **Educational Virtual Private Cloud (VPC)**.

---

## 🎯 Architectural Design

```
                     Internet (0.0.0.0/0)
                              │
                    [ Internet Gateway ]
                              │
    ┌─────────────────────────┴─────────────────────────┐
    │ Public Subnet (10.0.1.0/24 & 10.0.2.0/24)         │
    │  - Application Load Balancers                     │
    │  - NAT Gateways                                   │
    └─────────────────────────┬─────────────────────────┘
                              │
    ┌─────────────────────────┴─────────────────────────┐
    │ Private Application Subnet (10.0.10.0/24 & 11.0)  │
    │  - Educational LMS Containers                     │
    │  - Auto-scaling Microservices                     │
    └─────────────────────────┬─────────────────────────┘
                              │
    ┌─────────────────────────┴─────────────────────────┐
    │ Isolated Database Subnet (10.0.20.0/24 & 21.0)    │
    │  - PostgreSQL / MySQL Multi-AZ Primary & Replica  │
    └───────────────────────────────────────────────────┘
```

---

## 🏗️ Project Structure

```
Cloud Networking and Management/
├── iac/
│   └── vpc_architecture.tf     # Terraform HCL cloud infrastructure specification
├── src/
│   ├── __init__.py
│   ├── vpc_simulator.py        # Multi-tier subnetting and route table simulator
│   └── nacl_evaluator.py       # Stateless NACL network firewall rule engine
├── tests/
│   └── test_cloud_networking.py# Automated unit tests
├── main.py                     # CLI topology validator
└── README.md
```

---

## 🚀 Execution Instructions

### 1. Run Network Topology Simulator
```bash
python main.py
```

### 2. Run Automated Unit Tests
```bash
python -m unittest discover -s tests
```
