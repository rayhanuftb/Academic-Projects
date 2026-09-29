"""
SafeRx AI - Educational Software Engineering Project

An AI-assisted medication safety checker demonstrating software engineering
principles, testing practices, and quality assurance.

IMPORTANT: This is an EDUCATIONAL project. It does NOT provide real medical
advice and must NOT be used for clinical decision-making.
"""

from .models import Medication, DrugInteraction, PatientProfile
from .safety_checker import SafetyChecker
from .validation import InputValidator

__version__ = "1.0.0"
__author__ = "Rayhanul Islam"
