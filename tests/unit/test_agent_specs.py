"""Agent reasoning type enforcement tests."""
import pytest

from human_services.models.agent_specs import (
    ALL_AGENTS,
    INTAKE_AGENT,
    RULES_AGENT,
    validate_neuro_symbolic_boundary,
    ReasoningType,
)


def test_intake_agent_probabilistic():
    """IntakeAgent is probabilistic."""
    assert INTAKE_AGENT.reasoning_type == ReasoningType.PROBABILISTIC


def test_intake_agent_cannot_decide():
    """IntakeAgent cannot make eligibility decision."""
    assert INTAKE_AGENT.can_make_eligibility_decision is False


def test_rules_agent_deterministic():
    """RulesAgent is deterministic."""
    assert RULES_AGENT.reasoning_type == ReasoningType.DETERMINISTIC


def test_rules_agent_can_decide():
    """RulesAgent can make eligibility decision."""
    assert RULES_AGENT.can_make_eligibility_decision is True


def test_only_one_decision_maker():
    """Exactly one agent has decision authority."""
    decision_makers = [a for a in ALL_AGENTS if a.can_make_eligibility_decision]
    assert len(decision_makers) == 1
    assert decision_makers[0].name == "RulesAgent"


def test_validate_neuro_symbolic_boundary():
    """Validation passes for correct configuration."""
    assert validate_neuro_symbolic_boundary() is True
