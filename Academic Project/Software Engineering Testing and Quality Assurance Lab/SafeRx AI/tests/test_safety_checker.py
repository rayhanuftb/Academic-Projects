"""Tests for SafeRx AI safety checker module."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest
from saferx.models import PatientProfile, Allergy, AllergySeverity, RiskLevel
from saferx.safety_checker import SafetyChecker


@pytest.fixture
def checker():
    return SafetyChecker()


@pytest.fixture
def basic_patient():
    return PatientProfile(
        name="Test Patient",
        age=45,
        weight_kg=70,
    )


@pytest.fixture
def complex_patient():
    return PatientProfile(
        name="Complex Patient",
        age=70,
        weight_kg=60,
        allergies=[
            Allergy("aspirin", AllergySeverity.SEVERE, "anaphylaxis"),
        ],
        current_medications=["warfarin"],
        conditions=["hypertension"],
        is_pregnant=False,
        kidney_function_normal=False,
        liver_function_normal=True,
    )


class TestSafetyChecker:
    def test_no_interactions(self, checker, basic_patient):
        result = checker.check_interactions(["aspirin", "metformin"])
        assert len(result) == 0

    def test_warfarin_aspirin_interaction(self, checker, basic_patient):
        alerts = checker.check_interactions(["warfarin", "aspirin"])
        assert len(alerts) == 1
        assert alerts[0].severity == RiskLevel.HIGH
        assert alerts[0].alert_type == "drug_interaction"

    def test_multiple_interactions(self, checker, basic_patient):
        alerts = checker.check_interactions(["warfarin", "aspirin", "ibuprofen"])
        assert len(alerts) >= 2

    def test_allergy_conflict(self, checker, basic_patient):
        basic_patient.allergies = [
            Allergy("aspirin", AllergySeverity.SEVERE, "rash")
        ]
        alerts = checker.check_allergies(basic_patient, ["aspirin", "metformin"])
        assert len(alerts) == 1
        assert alerts[0].alert_type == "allergy_conflict"

    def test_no_allergy_conflict(self, checker, basic_patient):
        basic_patient.allergies = [
            Allergy("penicillin", AllergySeverity.MILD, "rash")
        ]
        alerts = checker.check_allergies(basic_patient, ["aspirin", "metformin"])
        assert len(alerts) == 0

    def test_pregnancy_contraindication(self, checker):
        patient = PatientProfile(
            name="Pregnant", age=28, weight_kg=65, is_pregnant=True
        )
        alerts = checker.check_contraindications(patient, ["warfarin", "ibuprofen"])
        assert len(alerts) >= 2
        assert any(a.severity == RiskLevel.CRITICAL for a in alerts)

    def test_kidney_function_warning(self, checker):
        patient = PatientProfile(
            name="Renal", age=55, weight_kg=70, kidney_function_normal=False
        )
        alerts = checker.check_contraindications(patient, ["metformin", "lisinopril"])
        assert len(alerts) >= 1

    def test_elderly_warning(self, checker):
        patient = PatientProfile(
            name="Elderly", age=75, weight_kg=60
        )
        alerts = checker.check_contraindications(patient, ["gabapentin", "omeprazole"])
        assert len(alerts) >= 1

    def test_full_safety_check(self, checker, complex_patient):
        result = checker.full_safety_check(
            complex_patient, ["warfarin", "aspirin", "metformin"]
        )
        assert "alerts" in result
        assert "overall_risk" in result
        assert result["total_alerts"] > 0
        assert result["overall_risk"] in ["low", "moderate", "high", "critical"]

    def test_full_safety_check_clean(self, checker, basic_patient):
        result = checker.full_safety_check(basic_patient, ["metformin", "lisinopril"])
        assert result["total_alerts"] == 0
        assert result["overall_risk"] == "low"
