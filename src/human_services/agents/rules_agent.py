"""
Rules Agent — Deterministic eligibility calculation.

Zero LLM. Same input → same output. Art. 15.
ONLY agent authorized to make eligibility decisions.
"""
from datetime import datetime
from typing import Any

from human_services.models.data_models import (
    ApplicationStatus,
    BenefitProgram,
    EligibilityDetermination,
)
from human_services.utils.fpl_thresholds import FPL_RULE_VERSION, State, get_income_limit


def calculate_eligibility(
    applicant_id: str,
    program: str,
    annual_income: float,
    household_size: int,
    status: str,
    enrollment_complete: bool,
    state: str = "contiguous",
) -> EligibilityDetermination:
    """
    Deterministic eligibility calculation. Zero LLM involvement.
    Same input produces same output every time.
    """
    state_enum = State.CONTIGUOUS
    if state.lower() == "alaska":
        state_enum = State.ALASKA
    elif state.lower() == "hawaii":
        state_enum = State.HAWAII

    try:
        program_enum = BenefitProgram(program)
    except ValueError:
        program_enum = BenefitProgram.SNAP

    try:
        status_enum = ApplicationStatus(status)
    except ValueError:
        status_enum = ApplicationStatus.ACTIVE

    income_limit = get_income_limit(household_size, program, state_enum)
    eligible_by_income = annual_income <= income_limit
    can_approve = status in (ApplicationStatus.ENROLLED.value, ApplicationStatus.RENEWED.value) and enrollment_complete
    eligible = eligible_by_income and can_approve

    return EligibilityDetermination(
        applicant_id=applicant_id,
        program=program_enum,
        eligible=eligible,
        income_limit=income_limit,
        annual_income=annual_income,
        household_size=household_size,
        status=status_enum,
        enrollment_complete=enrollment_complete,
        determination_date=datetime.utcnow().isoformat(),
        rule_version=FPL_RULE_VERSION,
        audit_trail={},
        explanation={},
        compliance={"Art. 15": "deterministic", "rule_version": FPL_RULE_VERSION},
    )
