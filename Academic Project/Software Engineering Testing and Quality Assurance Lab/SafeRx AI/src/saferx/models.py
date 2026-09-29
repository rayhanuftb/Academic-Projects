"""
Data models for SafeRx AI medication safety checker.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class RiskLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class AllergySeverity(Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    LIFE_THREATENING = "life_threatening"


@dataclass
class Medication:
    """Represents a medication."""
    name: str
    generic_name: str
    category: str
    dosage_form: str
    contraindications: List[str] = field(default_factory=list)
    side_effects: List[str] = field(default_factory=list)
    interactions: List[str] = field(default_factory=list)


@dataclass
class DrugInteraction:
    """Represents a drug-drug interaction."""
    drug1: str
    drug2: str
    severity: RiskLevel
    description: str
    recommendation: str


@dataclass
class Allergy:
    """Represents a patient allergy."""
    allergen: str
    severity: AllergySeverity
    reaction: str


@dataclass
class PatientProfile:
    """Represents a patient profile for safety checking."""
    name: str
    age: int
    weight_kg: float
    allergies: List[Allergy] = field(default_factory=list)
    current_medications: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    is_pregnant: bool = False
    kidney_function_normal: bool = True
    liver_function_normal: bool = True


@dataclass
class SafetyAlert:
    """Represents a safety alert/check result."""
    alert_type: str
    severity: RiskLevel
    message: str
    recommendation: str
    drugs_involved: List[str] = field(default_factory=list)
