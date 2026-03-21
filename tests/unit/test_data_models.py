"""Pydantic data model tests."""
import pytest

from human_services.models.data_models import (
    ApplicationStatus,
    BenefitProgram,
    LifeEventType,
    EligibilityDetermination,
    LifeEvent,
    AuditEntry,
)
from human_services.utils.fpl_thresholds import FPL_RULE_VERSION


def test_disbursement_permitted():
    """Only Enrolled and Renewed permit disbursement."""
    permitted = ApplicationStatus.disbursement_permitted()
    assert ApplicationStatus.ENROLLED in permitted
    assert ApplicationStatus.RENEWED in permitted
    assert ApplicationStatus.ACTIVE not in permitted


def test_life_event_affected_programs():
    """Job loss affects SNAP, Medicaid, TANF, Housing."""
    progs = LifeEventType.JOB_LOSS.affected_programs()
    assert BenefitProgram.SNAP in progs
    assert BenefitProgram.MEDICAID in progs
    assert BenefitProgram.TANF in progs
    assert BenefitProgram.HOUSING in progs


def test_life_event_requires_human_review():
    """LifeEvent always has requires_human_review=True."""
    e = LifeEvent(
        event_type=LifeEventType.JOB_LOSS,
        citizen_id="c1",
        event_details={},
    )
    assert e.requires_human_review is True


def test_eligibility_determination_explanation_keys():
    """EligibilityDetermination has explanation dict structure."""
    d = EligibilityDetermination(
        applicant_id="a1",
        program=BenefitProgram.SNAP,
        eligible=True,
        income_limit=40000,
        annual_income=30000,
        household_size=4,
        status=ApplicationStatus.ENROLLED,
        enrollment_complete=True,
        determination_date="2026-01-01",
        rule_version=FPL_RULE_VERSION,
        explanation={"caseworker": "x", "citizen": "y", "auditor": "z"},
    )
    assert "caseworker" in d.explanation
    assert "citizen" in d.explanation
    assert "auditor" in d.explanation


def test_audit_entry_frozen():
    """AuditEntry is immutable (frozen)."""
    e = AuditEntry(
        entry_id="e1",
        timestamp="2026-01-01",
        agent_id="A",
        action_type="test",
    )
    with pytest.raises(Exception):
        e.timestamp = "modified"  # type: ignore
