"""Ontology firewall unit tests."""
import pytest

from human_services.models.data_models import EligibilityDetermination
from human_services.ontology.firewall import OntologyFirewall
from human_services.utils.fpl_thresholds import FPL_RULE_VERSION


def test_firewall_validate_action_blocked():
    """Firewall blocks invalid action."""
    f = OntologyFirewall()
    r = f.validate_action({"status": "Active", "enrollment_complete": True})
    assert r.allowed is False


def test_firewall_validate_action_allowed():
    """Firewall allows valid action."""
    f = OntologyFirewall()
    r = f.validate_action({
        "status": "Enrolled",
        "enrollment_complete": True,
        "household_size": 4,
    })
    assert r.allowed is True


def test_firewall_guard_mcp_tool_call():
    """Guard MCP tool call returns GuardResult."""
    f = OntologyFirewall()
    r = f.guard_mcp_tool_call(
        "check_eligibility",
        {"status": "Active"},
        "RulesAgent",
    )
    assert r.status == "BLOCKED"
    assert r.tool == "check_eligibility"
    assert r.agent_id == "RulesAgent"
    assert r.validation.deterministic is True


def test_firewall_guard_eligibility_determination_blocked():
    """Guard blocks determination with Active status."""
    f = OntologyFirewall()
    d = EligibilityDetermination(
        applicant_id="a1",
        program="SNAP",
        eligible=True,
        income_limit=40000,
        annual_income=30000,
        household_size=4,
        status="Active",
        enrollment_complete=True,
        determination_date="2026-01-01T00:00:00",
        rule_version=FPL_RULE_VERSION,
    )
    r = f.guard_eligibility_determination(d)
    assert r.status == "BLOCKED"


def test_firewall_guard_eligibility_determination_allowed():
    """Guard allows determination with Enrolled status."""
    from human_services.models.data_models import ApplicationStatus, BenefitProgram

    f = OntologyFirewall()
    d = EligibilityDetermination(
        applicant_id="a1",
        program=BenefitProgram.SNAP,
        eligible=True,
        income_limit=40000,
        annual_income=30000,
        household_size=4,
        status=ApplicationStatus.ENROLLED,
        enrollment_complete=True,
        determination_date="2026-01-01T00:00:00",
        rule_version=FPL_RULE_VERSION,
    )
    r = f.guard_eligibility_determination(d)
    assert r.status == "ALLOWED"


def test_firewall_get_compliance_summary():
    """Compliance summary returns article mapping."""
    f = OntologyFirewall()
    s = f.get_compliance_summary()
    assert "Art. 9" in s
    assert "Art. 15" in s


def test_firewall_compliance_in_guard_result():
    """GuardResult includes compliance dict."""
    f = OntologyFirewall()
    r = f.guard_mcp_tool_call("check_eligibility", {"status": "Active"}, "agent1")
    assert "compliance" in r.model_dump()
    assert r.compliance
