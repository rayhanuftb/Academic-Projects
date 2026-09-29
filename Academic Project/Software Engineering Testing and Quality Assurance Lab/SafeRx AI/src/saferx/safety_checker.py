"""
Core safety checker module for SafeRx AI.

Performs medication safety checks including drug interactions,
allergy screening, and contraindication analysis.

IMPORTANT: This is for EDUCATIONAL purposes only.
"""

from typing import List, Dict
from .models import (
    Medication, DrugInteraction, PatientProfile, SafetyAlert, RiskLevel, AllergySeverity
)


class SafetyChecker:
    """Performs medication safety checks."""

    KNOWN_INTERACTIONS: List[DrugInteraction] = [
        DrugInteraction(
            "warfarin", "aspirin", RiskLevel.HIGH,
            "Combined use increases bleeding risk significantly.",
            "Avoid combination or monitor INR closely."
        ),
        DrugInteraction(
            "warfarin", "ibuprofen", RiskLevel.HIGH,
            "NSAIDs increase bleeding risk with warfarin.",
            "Use acetaminophen as alternative analgesic."
        ),
        DrugInteraction(
            "metformin", "lisinopril", RiskLevel.LOW,
            "Generally safe combination.",
            "Monitor kidney function periodically."
        ),
        DrugInteraction(
            "lisinopril", "potassium", RiskLevel.MODERATE,
            "ACE inhibitors can increase potassium levels.",
            "Monitor serum potassium regularly."
        ),
        DrugInteraction(
            "sertraline", "warfarin", RiskLevel.MODERATE,
            "SSRIs may increase anticoagulant effect.",
            "Monitor INR and watch for signs of bleeding."
        ),
        DrugInteraction(
            "metformin", "alcohol", RiskLevel.HIGH,
            "Alcohol increases risk of lactic acidosis.",
            "Limit alcohol consumption."
        ),
        DrugInteraction(
            "omeprazole", "clopidogrel", RiskLevel.MODERATE,
            "PPIs may reduce antiplatelet effect of clopidogrel.",
            "Consider pantoprazole as alternative PPI."
        ),
        DrugInteraction(
            "digoxin", "amiodarone", RiskLevel.CRITICAL,
            "Amiodarone significantly increases digoxin levels.",
            "Reduce digoxin dose by 50% and monitor levels."
        ),
        DrugInteraction(
            "methotrexate", "ibuprofen", RiskLevel.HIGH,
            "NSAIDs can increase methotrexate toxicity.",
            "Use acetaminophen for pain relief instead."
        ),
        DrugInteraction(
            "lithium", "ibuprofen", RiskLevel.HIGH,
            "NSAIDs can increase lithium levels to toxic range.",
            "Avoid NSAIDs; use acetaminophen instead."
        ),
    ]

    CATEGORY_MAP: Dict[str, List[str]] = {
        "nsaid": ["aspirin", "ibuprofen"],
        "ace_inhibitor": ["lisinopril"],
        "arb": ["losartan"],
        "statin": ["atorvastatin"],
        "ppi": ["omeprazole", "pantoprazole"],
        "ssri": ["sertraline"],
        "beta_blocker": ["metoprolol"],
        "anticoagulant": ["warfarin", "rivaroxaban", "apixaban"],
        "antiplatelet": ["clopidogrel"],
        "antidiabetic": ["metformin"],
        "thyroid": ["levothyroxine"],
        "cardiac_glycoside": ["digoxin"],
    }

    def check_interactions(self, medications: List[str]) -> List[SafetyAlert]:
        """Check for drug-drug interactions."""
        alerts = []
        meds_lower = [m.lower().strip() for m in medications]

        for interaction in self.KNOWN_INTERACTIONS:
            if interaction.drug1 in meds_lower and interaction.drug2 in meds_lower:
                alerts.append(SafetyAlert(
                    alert_type="drug_interaction",
                    severity=interaction.severity,
                    message=f"{interaction.drug1.title()} + {interaction.drug2.title()}: {interaction.description}",
                    recommendation=interaction.recommendation,
                    drugs_involved=[interaction.drug1, interaction.drug2],
                ))
        return alerts

    def check_allergies(self, patient: PatientProfile, medications: List[str]) -> List[SafetyAlert]:
        """Check for allergy conflicts with medications."""
        alerts = []
        for allergy in patient.allergies:
            allergen = allergy.allergen.lower()
            for med in medications:
                med_lower = med.lower().strip()
                if allergen in med_lower or med_lower in allergen:
                    severity_map = {
                        AllergySeverity.MILD: RiskLevel.MODERATE,
                        AllergySeverity.MODERATE: RiskLevel.HIGH,
                        AllergySeverity.SEVERE: RiskLevel.CRITICAL,
                        AllergySeverity.LIFE_THREATENING: RiskLevel.CRITICAL,
                    }
                    alerts.append(SafetyAlert(
                        alert_type="allergy_conflict",
                        severity=severity_map[allergy.severity],
                        message=f"Allergy to {allergy.allergen} detected. {med} may cause {allergy.reaction}.",
                        recommendation=f"Avoid {med}. Consult physician for alternative.",
                        drugs_involved=[med],
                    ))
        return alerts

    def check_contraindications(self, patient: PatientProfile, medications: List[str]) -> List[SafetyAlert]:
        """Check for patient-specific contraindications."""
        alerts = []
        meds_lower = [m.lower().strip() for m in medications]

        if not patient.kidney_function_normal:
            kidney_sensitive = ["metformin", "gabapentin", "lisinopril", "losartan"]
            for med in meds_lower:
                if med in kidney_sensitive:
                    alerts.append(SafetyAlert(
                        alert_type="contraindication",
                        severity=RiskLevel.HIGH,
                        message=f"{med.title()} requires dose adjustment with impaired kidney function.",
                        recommendation=f"Consult physician for {med.title()} dosing with renal impairment.",
                        drugs_involved=[med],
                    ))

        if not patient.liver_function_normal:
            liver_sensitive = ["atorvastatin", "omeprazole", "sertraline"]
            for med in meds_lower:
                if med in liver_sensitive:
                    alerts.append(SafetyAlert(
                        alert_type="contraindication",
                        severity=RiskLevel.MODERATE,
                        message=f"{med.title()} may require dose adjustment with impaired liver function.",
                        recommendation=f"Monitor liver function if taking {med.title()}.",
                        drugs_involved=[med],
                    ))

        if patient.is_pregnant:
            pregnancy_contraindicated = ["warfarin", "ibuprofen", "methotrexate", "lisinopril"]
            for med in meds_lower:
                if med in pregnancy_contraindicated:
                    alerts.append(SafetyAlert(
                        alert_type="contraindication",
                        severity=RiskLevel.CRITICAL,
                        message=f"{med.title()} is contraindicated during pregnancy.",
                        recommendation=f"Avoid {med.title()} during pregnancy. Consult OB/GYN.",
                        drugs_involved=[med],
                    ))

        if patient.age > 65:
            elderly_sensitive = ["gabapentin", "omeprazole", "metformin"]
            for med in meds_lower:
                if med in elderly_sensitive:
                    alerts.append(SafetyAlert(
                        alert_type="age_warning",
                        severity=RiskLevel.MODERATE,
                        message=f"{med.title()} may require dose adjustment for patients over 65.",
                        recommendation=f"Consider lower starting dose for {med.title()}.",
                        drugs_involved=[med],
                    ))

        return alerts

    def full_safety_check(
        self, patient: PatientProfile, medications: List[str]
    ) -> Dict:
        """Perform complete safety check."""
        all_alerts = []
        all_alerts.extend(self.check_interactions(medications))
        all_alerts.extend(self.check_allergies(patient, medications))
        all_alerts.extend(self.check_contraindications(patient, medications))

        severity_order = {
            RiskLevel.CRITICAL: 0,
            RiskLevel.HIGH: 1,
            RiskLevel.MODERATE: 2,
            RiskLevel.LOW: 3,
        }
        all_alerts.sort(key=lambda a: severity_order.get(a.severity, 99))

        critical_count = sum(1 for a in all_alerts if a.severity == RiskLevel.CRITICAL)
        high_count = sum(1 for a in all_alerts if a.severity == RiskLevel.HIGH)

        overall_risk = RiskLevel.LOW
        if critical_count > 0:
            overall_risk = RiskLevel.CRITICAL
        elif high_count > 0:
            overall_risk = RiskLevel.HIGH
        elif len(all_alerts) > 0:
            overall_risk = RiskLevel.MODERATE

        return {
            "patient": patient.name,
            "medications": medications,
            "total_alerts": len(all_alerts),
            "overall_risk": overall_risk.value,
            "alerts": [
                {
                    "type": a.alert_type,
                    "severity": a.severity.value,
                    "message": a.message,
                    "recommendation": a.recommendation,
                }
                for a in all_alerts
            ],
        }
