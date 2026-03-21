"""MCP Life Event Server — Life event recording and cascade."""
from typing import Any, Optional

from human_services.compliance.audit_trail import get_audit_trail_manager
from human_services.models.data_models import BenefitProgram, LifeEvent, LifeEventType

# In-memory store for life events (production: database)
_life_events: list[LifeEvent] = []
_pending_reviews: list[dict] = []


def record_life_event(
    citizen_id: str,
    event_type: str,
    event_details: Optional[dict] = None,
) -> dict[str, Any]:
    """Record event, map to affected programs, create review tasks."""
    try:
        event_enum = LifeEventType(event_type)
    except ValueError:
        event_enum = LifeEventType.JOB_LOSS
    affected = event_enum.affected_programs()
    review_tasks = [
        {"program": p.value, "requires_human_review": True, "citizen_id": citizen_id}
        for p in affected
    ]
    life_event = LifeEvent(
        event_type=event_enum,
        citizen_id=citizen_id,
        event_details=event_details or {},
        requires_human_review=True,
        affected_programs=affected,
        review_tasks=review_tasks,
    )
    _life_events.append(life_event)
    _pending_reviews.extend(review_tasks)
    audit = get_audit_trail_manager()
    audit.record(
        agent_id="LifeEventAgent",
        action_type="record_life_event",
        tool_name="record_life_event",
        parameters={"citizen_id": citizen_id, "event_type": event_type},
        result=life_event.model_dump(),
        applicant_id=citizen_id,
    )
    return {
        "life_event": life_event.model_dump(),
        "affected_programs": [p.value for p in affected],
        "review_tasks": review_tasks,
        "requires_human_review": True,
        "deterministic": True,
        "compliance": {"Art. 12": "logged", "Art. 14": "human_review"},
    }


def get_pending_reviews(citizen_id: Optional[str] = None) -> dict[str, Any]:
    """Return all reviews awaiting caseworker confirmation."""
    if citizen_id:
        reviews = [r for r in _pending_reviews if r.get("citizen_id") == citizen_id]
    else:
        reviews = list(_pending_reviews)
    return {
        "pending_reviews": reviews,
        "count": len(reviews),
        "deterministic": True,
        "compliance": {"Art. 14": "human_review"},
    }
