"""EU AI Act Article 9 — Risk management validation."""


def test_status_trap_blocked():
    """'Active' status caught and blocked."""
    from human_services.mcp.eligibility_server import check_eligibility

    r = check_eligibility(
        applicant_id="a1",
        program="SNAP",
        annual_income=25000,
        household_size=3,
        status="Active",
        enrollment_complete=True,
    )
    assert r["blocked"] is True


def test_known_risk_has_shacl_constraint():
    """Every registered risk has a constraint."""
    from human_services.compliance.risk_registry import RiskRegistry

    r = RiskRegistry()
    for risk in r.get_risks():
        assert risk.shacl_constraint


def test_qa_agent_catches_error_pattern():
    """QA agent flags known error (status trap)."""
    from human_services.agents.qa_agent import validate_determination
    from human_services.models.data_models import ApplicationStatus, BenefitProgram, EligibilityDetermination

    d = EligibilityDetermination(
        applicant_id="a1",
        program=BenefitProgram.SNAP,
        eligible=True,
        income_limit=40000,
        annual_income=30000,
        household_size=4,
        status=ApplicationStatus.ACTIVE,
        enrollment_complete=True,
        determination_date="2026-01-01",
        rule_version="2026",
    )
    qa = validate_determination(d)
    assert qa["passed"] is False
    assert any("STATUS_TRAP" in f or "Active" in f for f in qa["flags"])


def test_risk_registry_complete():
    """All known risks documented."""
    from human_services.compliance.risk_registry import RiskRegistry

    r = RiskRegistry()
    risks = r.get_risks()
    assert len(risks) >= 5
