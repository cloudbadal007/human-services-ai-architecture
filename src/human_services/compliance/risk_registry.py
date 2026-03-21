"""
Risk Registry — Known risks and SHACL constraint mapping (Art. 9).

Maps documented risks to the constraints that mitigate them.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RegisteredRisk:
    """A known risk with mitigation."""

    id: str
    description: str
    shacl_constraint: str
    severity: str
    eu_ai_act_article: str = "Art. 9"


class RiskRegistry:
    """Registry of known risks and their mitigations."""

    def __init__(self) -> None:
        self._risks: list[RegisteredRisk] = []
        self._load_defaults()

    def _load_defaults(self) -> None:
        """Pre-populated known risks."""
        self._risks = [
            RegisteredRisk(
                id="RISK-001",
                description="Semantic status misinterpretation: 'Active' confused with 'Enrolled'",
                shacl_constraint="BenefitApprovalShape",
                severity="HIGH",
            ),
            RegisteredRisk(
                id="RISK-002",
                description="Income threshold drift: using outdated FPL data",
                shacl_constraint="SNAPIncomeShape",
                severity="HIGH",
            ),
            RegisteredRisk(
                id="RISK-003",
                description="Household composition mismatch: invalid household size",
                shacl_constraint="HouseholdDataShape",
                severity="MEDIUM",
            ),
            RegisteredRisk(
                id="RISK-004",
                description="Enrollment workflow bypass: approving before completion",
                shacl_constraint="EnrollmentRequiredShape",
                severity="HIGH",
            ),
            RegisteredRisk(
                id="RISK-005",
                description="Cross-program coverage gap: life event not triggering review",
                shacl_constraint="LifeEventReviewShape",
                severity="MEDIUM",
            ),
        ]

    def get_risks(self) -> list[RegisteredRisk]:
        """List all known risks."""
        return list(self._risks)

    def get_risk_for_constraint(self, constraint_name: str) -> Optional[RegisteredRisk]:
        """Get risk mitigated by a constraint."""
        for r in self._risks:
            if r.shacl_constraint == constraint_name:
                return r
        return None

    def add_risk(
        self,
        description: str,
        shacl_constraint: str,
        severity: str = "MEDIUM",
    ) -> RegisteredRisk:
        """Register new risk."""
        rid = f"RISK-{len(self._risks) + 1:03d}"
        risk = RegisteredRisk(
            id=rid,
            description=description,
            shacl_constraint=shacl_constraint,
            severity=severity,
        )
        self._risks.append(risk)
        return risk
