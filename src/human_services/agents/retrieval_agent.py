"""
Retrieval Agent — Deterministic data gathering.

Queries via MCP with full audit logging. Art. 12.
CANNOT make eligibility decisions.
"""
from human_services.mcp.case_history_server import get_unified_history
from human_services.mcp.eligibility_server import check_eligibility
from human_services.models.agent_specs import RETRIEVAL_AGENT


def get_eligibility_data(
    applicant_id: str,
    program: str,
    annual_income: float,
    household_size: int,
    status: str = "Active",
    enrollment_complete: bool = False,
) -> dict:
    """Retrieve eligibility determination via MCP (logged)."""
    return check_eligibility(
        applicant_id=applicant_id,
        program=program,
        annual_income=annual_income,
        household_size=household_size,
        status=status,
        enrollment_complete=enrollment_complete,
    )


def get_history(applicant_id: str) -> dict:
    """Retrieve unified case history via MCP (logged)."""
    return get_unified_history(applicant_id=applicant_id)
