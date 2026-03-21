"""
Intake Agent — Probabilistic interpretation.

Uses LLM reasoning to understand citizen situation, map natural language
to structured life events, and identify affected programs.
CANNOT make eligibility decisions (Art. 14).
"""
from human_services.models.data_models import LifeEventType
from human_services.models.agent_specs import INTAKE_AGENT


def interpret_situation(natural_language_input: str) -> dict:
    """
    Interpret citizen situation (stub: would use LLM in production).

    Returns structured representation: life_event_type, affected_programs.
    For demo, maps common phrases to LifeEventType and programs.
    """
    text = natural_language_input.lower()
    # Simple deterministic mapping for demo (production: LLM)
    if "job" in text and ("lost" in text or "loss" in text or "laid off" in text):
        return {
            "life_event_type": LifeEventType.JOB_LOSS.value,
            "affected_programs": [p.value for p in LifeEventType.JOB_LOSS.affected_programs()],
            "agent": INTAKE_AGENT.name,
            "can_make_eligibility_decision": False,
        }
    if "income" in text and "change" in text:
        return {
            "life_event_type": LifeEventType.INCOME_CHANGE.value,
            "affected_programs": [p.value for p in LifeEventType.INCOME_CHANGE.affected_programs()],
            "agent": INTAKE_AGENT.name,
            "can_make_eligibility_decision": False,
        }
    if "baby" in text or "child" in text and "born" in text:
        return {
            "life_event_type": LifeEventType.CHILD_BORN.value,
            "affected_programs": [p.value for p in LifeEventType.CHILD_BORN.affected_programs()],
            "agent": INTAKE_AGENT.name,
            "can_make_eligibility_decision": False,
        }
    # Default: job loss
    return {
        "life_event_type": LifeEventType.JOB_LOSS.value,
        "affected_programs": [p.value for p in LifeEventType.JOB_LOSS.affected_programs()],
        "agent": INTAKE_AGENT.name,
        "can_make_eligibility_decision": False,
    }
