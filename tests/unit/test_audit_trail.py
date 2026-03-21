"""Audit trail unit tests."""
import pytest

from human_services.compliance.audit_trail import AuditTrailManager, get_audit_trail_manager


def test_entry_created_on_allow():
    """Allowed actions logged."""
    m = AuditTrailManager()
    e = m.record(
        agent_id="RulesAgent",
        action_type="eligibility_check",
        status="ALLOWED",
    )
    assert e.entry_id
    assert e.agent_id == "RulesAgent"
    trail = m.get_trail()
    assert len(trail) >= 1


def test_entry_created_on_block():
    """Blocked actions logged."""
    m = AuditTrailManager()
    e = m.record(
        agent_id="RulesAgent",
        action_type="eligibility_check",
        status="BLOCKED",
        violations=[{"message": "Status trap"}],
    )
    assert e.violations


def test_entry_is_immutable():
    """Cannot modify audit entry (frozen)."""
    m = AuditTrailManager()
    m.record(agent_id="A", action_type="test")
    trail = m.get_trail()
    entry = trail[-1]
    with pytest.raises(Exception):
        entry.timestamp = "modified"  # type: ignore


def test_entry_includes_compliance_context():
    """Entry includes EU AI Act articles."""
    m = AuditTrailManager()
    m.record(
        agent_id="RulesAgent",
        action_type="eligibility_check",
    )
    entry = m.get_trail()[-1]
    assert "Art. 12" in entry.eu_ai_act_articles


def test_filtering_by_applicant():
    """Filter trail by applicant_id."""
    m = AuditTrailManager()
    m.record(agent_id="A", action_type="test", applicant_id="app1")
    m.record(agent_id="A", action_type="test", applicant_id="app2")
    trail = m.get_trail(applicant_id="app1")
    assert all(e.applicant_id == "app1" for e in trail)


def test_export_for_regulator():
    """Export format includes required fields."""
    m = AuditTrailManager()
    m.record(agent_id="A", action_type="test", applicant_id="app1")
    exported = m.export_for_regulator("json")
    assert "entry_id" in exported or "applicant_id" in exported
