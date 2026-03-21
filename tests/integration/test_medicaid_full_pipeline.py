"""End-to-end Medicaid determination."""


def test_medicaid_eligible():
    """Full pipeline: eligible for Medicaid expansion."""
    from human_services.mcp.eligibility_server import check_eligibility

    r = check_eligibility(
        applicant_id="m1",
        program="MEDICAID",
        annual_income=40000,
        household_size=3,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert "eligible" in r
    assert "explanation" in r


def test_medicaid_ineligible_income():
    """Income over 138% FPL."""
    from human_services.mcp.eligibility_server import check_eligibility

    r = check_eligibility(
        applicant_id="m2",
        program="MEDICAID",
        annual_income=80000,
        household_size=2,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert r["eligible"] is False
