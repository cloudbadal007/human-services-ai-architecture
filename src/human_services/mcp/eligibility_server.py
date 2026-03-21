"""
MCP Eligibility Server — Benefit eligibility with compliance logging.

Tools: check_eligibility, get_case_history, flag_life_event
Every response includes deterministic, explanation, audit_trail, compliance.
"""
from datetime import datetime
from typing import Any, Optional

from human_services.compliance.audit_trail import get_audit_trail_manager
from human_services.compliance.explanation_generator import ExplanationGenerator
from human_services.models.data_models import (
    ApplicationStatus,
    BenefitProgram,
    EligibilityDetermination,
    LifeEvent,
    LifeEventType,
)
from human_services.ontology.firewall import OntologyFirewall
from human_services.utils.fpl_thresholds import FPL_RULE_VERSION, get_income_limit
from human_services.utils.fpl_thresholds import State


def check_eligibility(
    applicant_id: str,
    program: str,
    annual_income: float,
    household_size: int,
    status: str = "Active",
    enrollment_complete: bool = False,
    state: str = "contiguous",
) -> dict[str, Any]:
    """
    Check benefit eligibility with compliance logging and status trap validation.

    Returns dict with deterministic, explanation (caseworker/citizen/auditor),
    audit_trail, and compliance.
    """
    firewall = OntologyFirewall()
    audit = get_audit_trail_manager()
    explainer = ExplanationGenerator()

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
        income_limit = get_income_limit(household_size, program, state_enum)
    except ValueError:
        income_limit = get_income_limit(household_size, "SNAP", state_enum)

    # Build determination for firewall validation
    eligible_by_income = annual_income <= income_limit
    can_approve = status in (ApplicationStatus.ENROLLED.value, ApplicationStatus.RENEWED.value) and enrollment_complete
    eligible = eligible_by_income and can_approve

    try:
        status_enum = ApplicationStatus(status)
    except ValueError:
        status_enum = ApplicationStatus.ACTIVE

    determination = EligibilityDetermination(
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
        compliance={"Art. 12": "logged", "Art. 15": "deterministic"},
    )

    # Firewall guard — BLOCK if status trap
    guard = firewall.guard_eligibility_determination(determination)
    if guard.status == "BLOCKED":
        explanation = explainer.generate(determination)
        # Override citizen for blocked case
        explanation["citizen"] = (
            "Your application is still being processed. "
            "We need to complete a few more steps before we can finalize your eligibility."
        )
        audit.record(
            agent_id="RulesAgent",
            action_type="eligibility_check",
            tool_name="check_eligibility",
            parameters={"applicant_id": applicant_id, "program": program, "status": status},
            result={"eligible": False, "blocked": True, "reason": "Firewall validation"},
            applicant_id=applicant_id,
            program=program,
            violations=[v.model_dump() for v in guard.validation.violations],
        )
        return {
            "eligible": False,
            "blocked": True,
            "deterministic": True,
            "explanation": explanation,
            "audit_trail": {"rule_version": FPL_RULE_VERSION, "timestamp": determination.determination_date},
            "compliance": guard.compliance,
        }

    determination.explanation = explainer.generate(determination)
    audit.record(
        agent_id="RulesAgent",
        action_type="eligibility_check",
        tool_name="check_eligibility",
        parameters={"applicant_id": applicant_id, "program": program},
        result=determination.model_dump(),
        applicant_id=applicant_id,
        program=program,
    )
    return {
        "eligible": determination.eligible,
        "blocked": False,
        "deterministic": True,
        "explanation": determination.explanation,
        "audit_trail": {"rule_version": FPL_RULE_VERSION, "timestamp": determination.determination_date},
        "compliance": {"Art. 12": "logged", "Art. 13": "explanation", "Art. 15": "deterministic"},
        "determination": determination.model_dump(),
    }


def get_case_history(applicant_id: str) -> dict[str, Any]:
    """Unified cross-program case history with audit logging."""
    audit = get_audit_trail_manager()
    entries = audit.get_trail(applicant_id=applicant_id, last_n=50)
    audit.record(
        agent_id="RetrievalAgent",
        action_type="get_case_history",
        tool_name="get_case_history",
        parameters={"applicant_id": applicant_id},
        result={"entries_count": len(entries)},
        applicant_id=applicant_id,
    )
    return {
        "applicant_id": applicant_id,
        "entries": [e.model_dump() for e in entries],
        "deterministic": True,
        "compliance": {"Art. 12": "logged"},
    }


def flag_life_event(
    citizen_id: str,
    event_type: str,
    event_details: Optional[dict] = None,
) -> dict[str, Any]:
    """No Wrong Door: record life event, create review tasks with requires_human_review=True."""
    event_enum = LifeEventType(event_type) if event_type in [e.value for e in LifeEventType] else LifeEventType.JOB_LOSS
    affected = event_enum.affected_programs()
    review_tasks = [
        {"program": p.value, "requires_human_review": True, "event_type": event_type}
        for p in affected
    ]
    life_event = LifeEvent(
        event_type=event_enum,
        citizen_id=citizen_id,
        event_details=event_details or {},
        requires_human_review=True,
        affected_programs=affected,
        review_tasks=review_tasks,
    )
    audit = get_audit_trail_manager()
    audit.record(
        agent_id="LifeEventAgent",
        action_type="flag_life_event",
        tool_name="flag_life_event",
        parameters={"citizen_id": citizen_id, "event_type": event_type},
        result=life_event.model_dump(),
        applicant_id=citizen_id,
    )
    return {
        "life_event": life_event.model_dump(),
        "affected_programs": [p.value for p in affected],
        "review_tasks": review_tasks,
        "requires_human_review": True,
        "deterministic": True,
        "compliance": {"Art. 12": "logged", "Art. 14": "human_review"},
    }
