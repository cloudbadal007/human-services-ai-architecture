"""End-to-end SNAP determination."""


def test_snap_eligible():
    """Full pipeline: eligible household."""
    from human_services.mcp.eligibility_server import check_eligibility

    r = check_eligibility(
        applicant_id="s1",
        program="SNAP",
        annual_income=35000,
        household_size=4,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert r["eligible"] is True
    assert r["blocked"] is False
    assert "explanation" in r
    assert "audit_trail" in r
    assert "compliance" in r


def test_snap_blocked_active():
    """Full pipeline: blocked by Active status."""
    from human_services.mcp.eligibility_server import check_eligibility

    r = check_eligibility(
        applicant_id="s2",
        program="SNAP",
        annual_income=35000,
        household_size=4,
        status="Active",
        enrollment_complete=True,
    )
    assert r["blocked"] is True
