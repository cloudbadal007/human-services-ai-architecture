"""
Explanation Generator — Multi-level explanations (Art. 13).

Generates three levels for every determination:
- caseworker: Technical but readable
- citizen: Plain language, no jargon
- auditor: Full audit format with rule version
"""
import re

from human_services.models.data_models import EligibilityDetermination


# Technical terms that must NOT appear in citizen explanation
_JARGON_PATTERNS = [
    r"SHACL",
    r"ontology",
    r"FPL",
    r"constraint",
    r"Art\.\s*\d+",
    r"130%",
    r"138%",
    r"rdfs:",
    r"deterministic",
    r"eligibility\s*determination",
    r"rule_version",
    r"BLOCKED",
    r"Risk Management",
    r"Data Governance",
]


def _has_jargon(text: str) -> bool:
    """Check if text contains technical jargon."""
    lower = text.lower()
    for pattern in _JARGON_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


class ExplanationGenerator:
    """Generates Art. 13 compliant multi-level explanations."""

    def generate(self, determination: EligibilityDetermination) -> dict[str, str]:
        """Generate three-level explanation dict."""
        return {
            "caseworker": self._caseworker_level(determination),
            "citizen": self._citizen_level(determination),
            "auditor": self._auditor_level(determination),
        }

    def _caseworker_level(self, d: EligibilityDetermination) -> str:
        """Technical but readable for caseworkers."""
        if d.eligible:
            return (
                f"Household of {d.household_size} with income ${d.annual_income:,.0f} "
                f"is within {d.program.value} threshold of ${d.income_limit:,} "
                f"({d.rule_version}). All criteria satisfied."
            )
        if not d.enrollment_complete:
            return (
                f"Income and household criteria met, but enrollment is incomplete. "
                f"Status: {d.status}. Cannot approve until enrollment complete."
            )
        if d.status not in ("Enrolled", "Renewed"):
            return (
                f"Status '{d.status}' does not permit approval. "
                f"Only Enrolled or Renewed status allows disbursement."
            )
        return (
            f"Household of {d.household_size} with income ${d.annual_income:,.0f} "
            f"exceeds {d.program.value} limit of ${d.income_limit:,}. "
            f"Consider WIC, TANF, or other programs."
        )

    def _citizen_level(self, d: EligibilityDetermination) -> str:
        """Plain language, no technical jargon. Art. 13 compliance."""
        if d.eligible:
            return (
                "Your household qualifies for this assistance program. "
                "Your income is within the program limit."
            )
        if not d.enrollment_complete:
            return (
                "We need to complete your application before we can finalize "
                "your eligibility. A caseworker will contact you."
            )
        if d.status not in ("Enrolled", "Renewed"):
            return (
                "Your application is still being processed. "
                "You will receive notification when it is complete."
            )
        return (
            "Based on the information provided, your income exceeds the limit "
            "for this program. You may qualify for other assistance programs "
            "— a caseworker can help you explore options."
        )

    def _auditor_level(self, d: EligibilityDetermination) -> str:
        """Full audit format for regulators."""
        return (
            f"Rule: ELIGIBILITY_CHECK | "
            f"Input: income={d.annual_income}, hh={d.household_size}, "
            f"limit={d.income_limit} | "
            f"Result: {'PASS' if d.eligible else 'FAIL'} | "
            f"Version: {d.rule_version} | "
            f"Date: {d.determination_date}"
        )

    def validate_citizen_no_jargon(self, explanation: dict[str, str]) -> bool:
        """Verify citizen explanation has no technical terms (Art. 13)."""
        citizen = explanation.get("citizen", "")
        return not _has_jargon(citizen)
