"""
THE scenario: "Active" ≠ "Enrolled".

Agent proposes approval for status "Active" — must be BLOCKED.
"""


def test_active_status_blocked():
    """Status=Active with eligible income must be BLOCKED (not approved)."""
    from human_services.mcp.eligibility_server import check_eligibility

    r = check_eligibility(
        applicant_id="victim_001",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Active",
        enrollment_complete=True,
    )
    assert r["blocked"] is True
    assert r["eligible"] is False
    assert "explanation" in r
    assert "citizen" in r["explanation"]


def test_enrolled_status_allowed():
    """Same case with status=Enrolled — ALLOWED."""
    from human_services.mcp.eligibility_server import check_eligibility

    r = check_eligibility(
        applicant_id="victim_001",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert r["blocked"] is False
    assert r["eligible"] is True
