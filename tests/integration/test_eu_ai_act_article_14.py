"""EU AI Act Article 14 — Human oversight enforcement."""


def test_probabilistic_agent_cannot_decide():
    """IntakeAgent blocked from making determination."""
    from human_services.models.agent_specs import INTAKE_AGENT

    assert INTAKE_AGENT.can_make_eligibility_decision is False


def test_life_event_requires_human_review():
    """All review tasks have human_review=True."""
    from human_services.mcp.eligibility_server import flag_life_event

    r = flag_life_event("c1", "job_loss")
    for t in r["review_tasks"]:
        assert t["requires_human_review"] is True


def test_only_rules_agent_can_decide():
    """Only RulesAgent has decision authority."""
    from human_services.models.agent_specs import ALL_AGENTS

    decision_makers = [a for a in ALL_AGENTS if a.can_make_eligibility_decision]
    assert len(decision_makers) == 1
    assert decision_makers[0].name == "RulesAgent"
