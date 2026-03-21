"""
QA Agent — Validates determination against known error patterns.

Deterministic. Art. 9. Can FLAG issues, cannot make eligibility decisions.
"""
from typing import Any, Optional

from human_services.models.data_models import EligibilityDetermination
from human_services.models.agent_specs import QA_AGENT


def validate_determination(determination: EligibilityDetermination) -> dict[str, Any]:
    """
    Check for known error patterns: status misinterpretation, household mismatch, etc.
    Returns flags dict; does not modify determination.
    """
    flags: list[str] = []
    if determination.status.value == "Active" and determination.eligible:
        flags.append("STATUS_TRAP: Eligible=True with status=Active — possible misinterpretation")
    if determination.household_size < 1 or determination.household_size > 20:
        flags.append("HOUSEHOLD_INVALID: Household size out of range")
    if not determination.rule_version:
        flags.append("VERSION_MISSING: Rule version required for Art. 11")
    return {
        "passed": len(flags) == 0,
        "flags": flags,
        "agent": QA_AGENT.name,
        "can_make_eligibility_decision": False,
    }
