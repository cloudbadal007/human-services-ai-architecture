"""Shared MCP tool definitions and schemas."""
from typing import Any

# Tool name constants
CHECK_ELIGIBILITY = "check_eligibility"
GET_CASE_HISTORY = "get_case_history"
FLAG_LIFE_EVENT = "flag_life_event"
GET_UNIFIED_HISTORY = "get_unified_history"
GET_PROGRAM_HISTORY = "get_program_history"
RECORD_LIFE_EVENT = "record_life_event"
GET_PENDING_REVIEWS = "get_pending_reviews"


def tool_response(
    content: Any,
    deterministic: bool = True,
    explanation: dict[str, str] | None = None,
    audit_trail: dict[str, Any] | None = None,
    compliance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build standardized tool response with compliance fields."""
    result = {"content": content, "deterministic": deterministic}
    if explanation:
        result["explanation"] = explanation
    if audit_trail:
        result["audit_trail"] = audit_trail
    if compliance:
        result["compliance"] = compliance
    return result
