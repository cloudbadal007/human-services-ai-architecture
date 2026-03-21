"""
Agent Specifications — Neuro-Symbolic Separation.

EU AI Act Art. 11 compliance: Each agent's reasoning type is
documented and fixed at design time. No agent crosses the
probabilistic-deterministic boundary without ontology firewall validation.

Key principle: Only DETERMINISTIC agents can make eligibility decisions.
Probabilistic agents handle perception and interpretation.
The ontology firewall enforces the boundary.
"""
from dataclasses import dataclass
from enum import Enum


class ReasoningType(Enum):
    PROBABILISTIC = "probabilistic"  # LLM — interpretation, empathy, context
    DETERMINISTIC = "deterministic"  # Rules engine — calculation, validation


@dataclass
class AgentSpec:
    name: str
    reasoning_type: ReasoningType
    eu_ai_act_articles: list[str]
    eu_ai_act_role: str
    can_make_eligibility_decision: bool
    description: str


INTAKE_AGENT = AgentSpec(
    name="IntakeAgent",
    reasoning_type=ReasoningType.PROBABILISTIC,
    eu_ai_act_articles=["Art. 13"],
    eu_ai_act_role="Interprets citizen situation using natural language understanding",
    can_make_eligibility_decision=False,
    description="Uses LLM reasoning to understand citizen's situation, "
    "map natural language to structured life events, and identify "
    "affected programs. CANNOT make eligibility decisions.",
)

RETRIEVAL_AGENT = AgentSpec(
    name="RetrievalAgent",
    reasoning_type=ReasoningType.DETERMINISTIC,
    eu_ai_act_articles=["Art. 12"],
    eu_ai_act_role="Queries databases via MCP with full audit logging",
    can_make_eligibility_decision=False,
    description="Gathers data from program-specific MCP servers. "
    "Every query is logged with input, output, and timestamp. "
    "CANNOT make eligibility decisions.",
)

RULES_AGENT = AgentSpec(
    name="RulesAgent",
    reasoning_type=ReasoningType.DETERMINISTIC,
    eu_ai_act_articles=["Art. 15"],
    eu_ai_act_role="Applies eligibility rules with zero variance",
    can_make_eligibility_decision=True,
    description="Performs deterministic eligibility calculation using "
    "published federal thresholds. Zero LLM involvement. "
    "Same input produces same output every time. "
    "ONLY agent authorized to make eligibility decisions.",
)

QA_AGENT = AgentSpec(
    name="QAAgent",
    reasoning_type=ReasoningType.DETERMINISTIC,
    eu_ai_act_articles=["Art. 9"],
    eu_ai_act_role="Validates determination against known risk patterns",
    can_make_eligibility_decision=False,
    description="Checks for known error patterns: status misinterpretation, "
    "household size mismatches, FPL version mismatches. "
    "CANNOT make eligibility decisions — can only FLAG issues.",
)

ONTOLOGY_FIREWALL = AgentSpec(
    name="OntologyFirewall",
    reasoning_type=ReasoningType.DETERMINISTIC,
    eu_ai_act_articles=["Art. 9", "Art. 15"],
    eu_ai_act_role="SHACL validation of every proposed agent action",
    can_make_eligibility_decision=False,
    description="Validates every proposed action against SHACL constraints. "
    "Can BLOCK actions but never APPROVE them. "
    "Every constraint maps to a specific EU AI Act article.",
)

ALL_AGENTS = [INTAKE_AGENT, RETRIEVAL_AGENT, RULES_AGENT, QA_AGENT, ONTOLOGY_FIREWALL]


def validate_neuro_symbolic_boundary() -> bool:
    """
    Verify that the neuro-symbolic separation is maintained:
    - Only deterministic agents can make eligibility decisions
    - No probabilistic agent has decision authority
    """
    for agent in ALL_AGENTS:
        if agent.reasoning_type == ReasoningType.PROBABILISTIC:
            assert not agent.can_make_eligibility_decision, (
                f"COMPLIANCE VIOLATION: Probabilistic agent '{agent.name}' "
                f"must not have eligibility decision authority. "
                f"EU AI Act Art. 14 requires human/deterministic oversight."
            )

    decision_makers = [a for a in ALL_AGENTS if a.can_make_eligibility_decision]
    assert len(decision_makers) == 1, (
        f"COMPLIANCE VIOLATION: Exactly one agent should make eligibility decisions. "
        f"Found {len(decision_makers)}: {[a.name for a in decision_makers]}"
    )
    assert decision_makers[0].reasoning_type == ReasoningType.DETERMINISTIC, (
        "COMPLIANCE VIOLATION: The decision-making agent must be deterministic."
    )

    return True
