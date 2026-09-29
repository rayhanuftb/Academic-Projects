# Network Scanning and IP Configuration

**Course:** Cyber Security and Content Management Lab (ICT 4462)  
**Academic Program:** B.Sc. in Educational Technology and Engineering  
**Institution:** University of Frontier Technology, Bangladesh  
**Author:** Rayhanul Islam

---

## 📌 Project Overview

This project implements an educational networking and cybersecurity practical diagnostic suite. It demonstrates IPv4 subnetting calculations, Variable Length Subnet Masking (VLSM) hierarchical addressing design, and non-intrusive TCP port auditing in authorized laboratory environments.

---

## 🎯 Key Objectives

1. **IPv4 Subnetting & CIDR Analysis**: Calculate network IDs, broadcast addresses, wildcard masks, usable host ranges, and RFC 1918 private address verification.
2. **VLSM Optimization**: Compute departmental IP address allocations to eliminate wasted host addresses.
3. **Safe Local Port Diagnostic**: Perform non-intrusive TCP socket connection checks on standard service ports (`80`, `443`, `22`, `3306`, etc.) on authorized local testbeds.
4. **Ethical Security Guardrails**: Built strictly for authorized academic network analysis, avoiding aggressive scanning or unauthorized external reconnaissance.

---

## 🏗️ Project Structure

```
Network Scanning and IP Configuration/
├── src/
│   ├── __init__.py
│   ├── ip_calculator.py    # IPv4 CIDR analysis & parameter calculation
│   ├── subnetter.py        # VLSM hierarchical subnet design
│   └── port_scanner.py     # Safe non-intrusive TCP port diagnostic
├── tests/
│   └── test_network_sec.py # Automated unit tests
├── main.py                 # CLI diagnostic utility
└── README.md
```

---

## 🚀 Execution Instructions

### 1. Calculate IPv4 Subnet Parameters
```bash
python main.py --calc 192.168.10.0/26
```

### 2. Run VLSM Educational Allocation Scheme
```bash
python main.py --vlsm
```

### 3. Run Safe Local Port Audit on Localhost
```bash
python main.py --scan 127.0.0.1 --ports 21,22,80,443,3306,8080
```

### 4. Run Automated Tests
```bash
python -m unittest discover -s tests
```
