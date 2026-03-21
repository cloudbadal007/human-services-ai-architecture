"""MCP eligibility server unit tests."""
import pytest

from human_services.mcp.eligibility_server import check_eligibility, get_case_history, flag_life_event


def test_check_eligibility_eligible_enrolled():
    """Eligible when status=Enrolled, enrollment complete, income under limit."""
    r = check_eligibility(
        applicant_id="a1",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert r["eligible"] is True
    assert r["blocked"] is False
    assert "explanation" in r
    assert "caseworker" in r["explanation"]
    assert "citizen" in r["explanation"]
    assert "auditor" in r["explanation"]


def test_check_eligibility_blocked_active_status():
    """BLOCKED when status=Active (the trap)."""
    r = check_eligibility(
        applicant_id="a1",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Active",
        enrollment_complete=True,
    )
    assert r["blocked"] is True
    assert r["eligible"] is False
    assert "explanation" in r


def test_check_eligibility_deterministic():
    """Response includes deterministic=True."""
    r = check_eligibility(
        applicant_id="a1",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert r["deterministic"] is True


def test_check_eligibility_compliance():
    """Response includes compliance dict."""
    r = check_eligibility(
        applicant_id="a1",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert "compliance" in r


def test_check_eligibility_ineligible_income():
    """Ineligible when income exceeds limit."""
    r = check_eligibility(
        applicant_id="a1",
        program="SNAP",
        annual_income=100000,
        household_size=2,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert r["eligible"] is False
    assert r["blocked"] is False


def test_get_case_history():
    """Case history returns structure."""
    r = get_case_history("a1")
    assert "applicant_id" in r
    assert "entries" in r
    assert r["deterministic"] is True


def test_flag_life_event():
    """Life event creates review tasks with requires_human_review=True."""
    r = flag_life_event("c1", "job_loss", {"note": "test"})
    assert r["requires_human_review"] is True
    assert "affected_programs" in r
    assert "SNAP" in r["affected_programs"]
    assert "review_tasks" in r
    for t in r["review_tasks"]:
        assert t["requires_human_review"] is True


def test_flag_life_event_compliance():
    """Life event response has compliance."""
    r = flag_life_event("c1", "job_loss")
    assert "compliance" in r
    assert "Art. 14" in str(r["compliance"])


def test_check_eligibility_audit_trail():
    """Audit trail present in response."""
    r = check_eligibility(
        applicant_id="a1",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert "audit_trail" in r
    assert "rule_version" in r["audit_trail"]


def test_check_eligibility_medicaid():
    """Medicaid eligibility check."""
    r = check_eligibility(
        applicant_id="a1",
        program="MEDICAID",
        annual_income=35000,
        household_size=3,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert "eligible" in r
    assert "explanation" in r
