"""
Input validation module for SafeRx AI.
"""

import re
from typing import List, Optional, Tuple


class InputValidator:
    """Validates user inputs for the safety checker."""

    VALID_MEDICATIONS = [
        "aspirin", "ibuprofen", "acetaminophen", "metformin", "lisinopril",
        "amlodipine", "atorvastatin", "omeprazole", "metoprolol", "losartan",
        "gabapentin", "pantoprazole", "sertraline", "levothyroxine", "montelukast",
        "warfarin", "clopidogrel", "rivaroxaban", "apixaban", "digoxin",
        "methotrexate", "lithium", "phenytoin", "cyclosporine", "amiodarone",
    ]

    @staticmethod
    def validate_medication_name(name: str) -> Tuple[bool, str]:
        """Validate a medication name."""
        if not name or not name.strip():
            return False, "Medication name cannot be empty"
        name = name.strip().lower()
        if len(name) < 2:
            return False, "Medication name too short"
        if not re.match(r'^[a-zA-Z\-]+$', name):
            return False, "Medication name contains invalid characters"
        return True, "Valid"

    @staticmethod
    def validate_age(age: int) -> Tuple[bool, str]:
        """Validate patient age."""
        if not isinstance(age, (int, float)):
            return False, "Age must be a number"
        if age < 0 or age > 150:
            return False, "Age must be between 0 and 150"
        return True, "Valid"

    @staticmethod
    def validate_weight(weight: float) -> Tuple[bool, str]:
        """Validate patient weight."""
        if not isinstance(weight, (int, float)):
            return False, "Weight must be a number"
        if weight <= 0 or weight > 500:
            return False, "Weight must be between 0 and 500 kg"
        return True, "Valid"

    @staticmethod
    def validate_medication_list(medications: List[str]) -> Tuple[bool, str]:
        """Validate a list of medications."""
        if not medications:
            return False, "At least one medication is required"
        for med in medications:
            valid, msg = InputValidator.validate_medication_name(med)
            if not valid:
                return False, f"Invalid medication '{med}': {msg}"
        return True, "Valid"

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize text input."""
        if not text:
            return ""
        text = text.strip()
        text = re.sub(r'[<>"\']', '', text)
        return text
