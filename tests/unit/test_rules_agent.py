"""Rules agent determinism tests."""
import pytest

from human_services.agents.rules_agent import calculate_eligibility


def test_rules_agent_deterministic():
    """Same input produces same output."""
    r1 = calculate_eligibility(
        "a1", "SNAP", 30000, 4, "Enrolled", True
    )
    r2 = calculate_eligibility(
        "a1", "SNAP", 30000, 4, "Enrolled", True
    )
    assert r1.eligible == r2.eligible
    assert r1.income_limit == r2.income_limit


def test_rules_agent_active_not_eligible():
    """Status=Active with income OK still not eligible (enrollment workflow)."""
    r = calculate_eligibility(
        "a1", "SNAP", 30000, 4, "Active", True
    )
    assert r.eligible is False


def test_rules_agent_enrolled_eligible():
    """Status=Enrolled, income under limit -> eligible."""
    r = calculate_eligibility(
        "a1", "SNAP", 30000, 4, "Enrolled", True
    )
    assert r.eligible is True


def test_rules_agent_rule_version():
    """Determination includes rule_version."""
    r = calculate_eligibility(
        "a1", "SNAP", 30000, 4, "Enrolled", True
    )
    assert r.rule_version
    assert "2026" in r.rule_version


def test_rules_agent_medicaid():
    """Medicaid calculation."""
    r = calculate_eligibility(
        "a1", "MEDICAID", 35000, 3, "Enrolled", True
    )
    assert hasattr(r, "income_limit")
    assert r.program.value == "MEDICAID"


def test_rules_agent_compliance_field():
    """Determination has compliance field."""
    r = calculate_eligibility(
        "a1", "SNAP", 30000, 4, "Enrolled", True
    )
    assert "compliance" in r.model_dump() or hasattr(r, "compliance")


def test_rules_agent_income_over_limit():
    """Income over limit -> not eligible."""
    r = calculate_eligibility(
        "a1", "SNAP", 100000, 2, "Enrolled", True
    )
    assert r.eligible is False


def test_rules_agent_zero_llm():
    """Rules agent has no LLM—pure calculation. Verify no randomness."""
    results = [
        calculate_eligibility("a1", "SNAP", 32000, 4, "Enrolled", True).eligible
        for _ in range(5)
    ]
    assert all(x == results[0] for x in results)
