"""MCP Case History Server — Unified cross-program history."""
from typing import Any

from human_services.compliance.audit_trail import get_audit_trail_manager


def get_unified_history(applicant_id: str) -> dict[str, Any]:
    """Reconcile data across program-specific systems using ontology."""
    audit = get_audit_trail_manager()
    entries = audit.get_trail(applicant_id=applicant_id, last_n=100)
    # Group by program
    by_program: dict[str, list] = {}
    for e in entries:
        prog = e.program or "unknown"
        if prog not in by_program:
            by_program[prog] = []
        by_program[prog].append(e.model_dump())
    audit.record(
        agent_id="RetrievalAgent",
        action_type="get_unified_history",
        tool_name="get_unified_history",
        parameters={"applicant_id": applicant_id},
        result={"programs": list(by_program.keys())},
        applicant_id=applicant_id,
    )
    return {
        "applicant_id": applicant_id,
        "by_program": by_program,
        "deterministic": True,
        "compliance": {"Art. 12": "logged"},
    }


def get_program_history(applicant_id: str, program: str) -> dict[str, Any]:
    """Single program history with status timeline."""
    audit = get_audit_trail_manager()
    entries = audit.get_trail(applicant_id=applicant_id, last_n=50)
    program_entries = [e for e in entries if e.program == program]
    audit.record(
        agent_id="RetrievalAgent",
        action_type="get_program_history",
        tool_name="get_program_history",
        parameters={"applicant_id": applicant_id, "program": program},
        result={"entries_count": len(program_entries)},
        applicant_id=applicant_id,
        program=program,
    )
    return {
        "applicant_id": applicant_id,
        "program": program,
        "entries": [e.model_dump() for e in program_entries],
        "deterministic": True,
        "compliance": {"Art. 12": "logged"},
    }
