"""EU AI Act Article 13 — Transparency / explanation quality."""


def test_three_level_explanation_for_eligible():
    """All three levels present for approval."""
    from human_services.mcp.eligibility_server import check_eligibility

    r = check_eligibility(
        applicant_id="a1",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Enrolled",
        enrollment_complete=True,
    )
    assert "caseworker" in r["explanation"]
    assert "citizen" in r["explanation"]
    assert "auditor" in r["explanation"]


def test_three_level_explanation_for_blocked():
    """All three levels present for denial/block."""
    from human_services.mcp.eligibility_server import check_eligibility

    r = check_eligibility(
        applicant_id="a1",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Active",
        enrollment_complete=True,
    )
    assert "caseworker" in r["explanation"]
    assert "citizen" in r["explanation"]
    assert "auditor" in r["explanation"]


def test_citizen_explanation_readability():
    """No ontology terms in citizen explanation."""
    from human_services.compliance.explanation_generator import ExplanationGenerator
    from human_services.models.data_models import ApplicationStatus, BenefitProgram, EligibilityDetermination

    d = EligibilityDetermination(
        applicant_id="a1",
        program=BenefitProgram.SNAP,
        eligible=True,
        income_limit=41000,
        annual_income=38000,
        household_size=4,
        status=ApplicationStatus.ENROLLED,
        enrollment_complete=True,
        determination_date="2026-01-01",
        rule_version="2026-FPL-v1",
    )
    g = ExplanationGenerator()
    expl = g.generate(d)
    assert g.validate_citizen_no_jargon(expl)
