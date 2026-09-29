import socket
from typing import List, Dict, Any, Optional

# Standard service name mapping
COMMON_SERVICES = {
    21: "FTP (File Transfer)",
    22: "SSH (Secure Shell)",
    23: "Telnet (Unencrypted)",
    25: "SMTP (Simple Mail Transfer)",
    53: "DNS (Domain Name System)",
    80: "HTTP (Hypertext Transfer Protocol)",
    110: "POP3 (Post Office Protocol)",
    143: "IMAP (Internet Message Access)",
    443: "HTTPS (HTTP Secure)",
    445: "SMB (Server Message Block)",
    1433: "MSSQL (Microsoft SQL Server)",
    3306: "MySQL Database",
    5432: "PostgreSQL Database",
    8000: "HTTP Dev Server (Alt)",
    8080: "HTTP Proxy / Web App"
}


class SafePortScanner:
    """
    Educational, safe diagnostic TCP port auditing utility.
    Strictly constrained to authorized hosts (e.g. localhost, private loopback, or user-defined targets).
    """

    def __init__(self, target_host: str = "127.0.0.1", timeout_sec: float = 0.5):
        self.target_host = target_host
        self.timeout_sec = timeout_sec

    def scan_single_port(self, port: int) -> Dict[str, Any]:
        """Performs a non-intrusive TCP connect check on a single port."""
        if not (1 <= port <= 65535):
            return {"port": port, "state": "Invalid", "service": "Unknown"}

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout_sec)
        try:
            res = sock.connect_ex((self.target_host, port))
            state = "Open" if res == 0 else "Closed"
        except socket.gaierror:
            state = "Host Resolution Error"
        except Exception:
            state = "Filtered / Unreachable"
        finally:
            sock.close()

        service = COMMON_SERVICES.get(port, "Custom Service")
        return {
            "port": port,
            "state": state,
            "service": service
        }

    def scan_ports(self, port_list: List[int]) -> List[Dict[str, Any]]:
        """Audits a designated list of ports."""
        results = []
        for p in port_list:
            results.append(self.scan_single_port(p))
        return results
