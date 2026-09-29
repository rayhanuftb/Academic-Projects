from typing import List, Dict, Any


class NACLEvaluator:
    """Evaluates stateless Network Access Control List (NACL) rule processing."""

    @staticmethod
    def evaluate_traffic(rules: List[Dict[str, Any]], source_ip: str, port: int, protocol: str = "TCP") -> Dict[str, Any]:
        """
        Evaluates incoming traffic against ordered numbered NACL rules (lowest rule number evaluated first).
        Rule format: {'rule_no': 100, 'action': 'ALLOW'/'DENY', 'protocol': 'TCP', 'port_range': (80, 80)}
        """
        sorted_rules = sorted(rules, key=lambda r: r['rule_no'])

        for rule in sorted_rules:
            # Check protocol
            if rule['protocol'] != 'ALL' and rule['protocol'].upper() != protocol.upper():
                continue

            # Check port range
            p_min, p_max = rule.get('port_range', (0, 65535))
            if p_min <= port <= p_max:
                return {
                    "matched_rule": rule['rule_no'],
                    "action": rule['action'],
                    "explanation": f"Traffic on port {port} ({protocol}) matched Rule #{rule['rule_no']} -> {rule['action']}"
                }

        # Default implicit deny
        return {
            "matched_rule": "*",
            "action": "DENY",
            "explanation": "Traffic did not match any explicit rule. Default implicit deny triggered."
        }
