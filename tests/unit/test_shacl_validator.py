"""SHACL validator unit tests."""
import pytest

from human_services.ontology.validator import (
    validate_action,
    validate_benefit_approval,
    validate_household_data,
    validate_income,
)


def test_validate_benefit_approval_active_blocked():
    """Status=Active produces violation."""
    v = validate_benefit_approval("Active", True)
    assert len(v) > 0
    assert any("Enrolled" in x.message or "Renewed" in x.message for x in v)


def test_validate_benefit_approval_enrolled_ok():
    """Status=Enrolled, enrollment complete — no violation."""
    v = validate_benefit_approval("Enrolled", True)
    assert len(v) == 0


def test_validate_benefit_approval_enrollment_incomplete():
    """Enrollment incomplete produces violation."""
    v = validate_benefit_approval("Enrolled", False)
    assert len(v) > 0


def test_validate_household_zero_blocked():
    """Household size 0 blocked."""
    v = validate_household_data(0)
    assert len(v) > 0


def test_validate_household_valid():
    """Household size 1-20 valid."""
    v = validate_household_data(4)
    assert len(v) == 0


def test_validate_household_over_20_blocked():
    """Household size > 20 blocked."""
    v = validate_household_data(21)
    assert len(v) > 0


def test_validate_action_status_trap():
    """Action with status=Active blocked."""
    r = validate_action({"status": "Active", "enrollment_complete": True})
    assert r.allowed is False
    assert len(r.violations) > 0


def test_validate_action_household_zero():
    """Action with household_size=0 blocked."""
    r = validate_action({"status": "Enrolled", "household_size": 0})
    assert r.allowed is False


def test_validate_action_allowed():
    """Valid action allowed."""
    r = validate_action({
        "status": "Enrolled",
        "enrollment_complete": True,
        "household_size": 4,
        "annual_income": 30000,
        "program": "SNAP",
    })
    assert r.allowed is True
    assert r.deterministic is True


def test_validate_action_deterministic():
    """Validation result is always deterministic."""
    r = validate_action({"status": "Active"})
    assert r.deterministic is True
