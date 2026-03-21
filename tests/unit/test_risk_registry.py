"""Risk registry unit tests."""
from human_services.compliance.risk_registry import RiskRegistry


def test_get_risks():
    """Registry returns known risks."""
    r = RiskRegistry()
    risks = r.get_risks()
    assert len(risks) >= 5


def test_get_risk_for_constraint():
    """Can find risk for constraint."""
    r = RiskRegistry()
    risk = r.get_risk_for_constraint("BenefitApprovalShape")
    assert risk is not None
    assert "Active" in risk.description or "status" in risk.description.lower()


def test_add_risk():
    """Can add new risk."""
    r = RiskRegistry()
    before = len(r.get_risks())
    r.add_risk("Test risk", "TestShape", "LOW")
    after = len(r.get_risks())
    assert after == before + 1
