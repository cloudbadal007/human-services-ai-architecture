"""
OntologyFirewall — SHACL validation with EU AI Act compliance tagging.

Every validation result includes:
- Which SHACL constraints were evaluated
- Which EU AI Act articles each constraint maps to
- Whether the action would be compliant if allowed
- Full reasoning chain for audit trail
"""
from typing import Any, Optional

from human_services.models.data_models import (
    AuditEntry,
    EligibilityDetermination,
    GuardResult,
    ValidationResult,
)
from human_services.ontology.validator import validate_action

# Optional audit trail integration
_audit_trail_manager: Optional[Any] = None


def set_audit_trail_manager(manager: Any) -> None:
    """Inject audit trail manager for logging (optional)."""
    global _audit_trail_manager
    _audit_trail_manager = manager


def _create_action_data(params: dict, determination: Optional[EligibilityDetermination]) -> dict:
    """Build action_data dict for validation from tool params or determination."""
    if determination:
        return {
            "status": (
                determination.status.value
                if hasattr(determination.status, "value")
                else str(determination.status)
            ),
            "enrollment_complete": determination.enrollment_complete,
            "household_size": determination.household_size,
            "annual_income": determination.annual_income,
            "program": (
                determination.program.value
                if hasattr(determination.program, "value")
                else str(determination.program)
            ),
            "determination_date": determination.determination_date,
            "rule_version": determination.rule_version,
            "eligible": determination.eligible,
        }
    return {
        "status": params.get("status", ""),
        "enrollment_complete": params.get("enrollment_complete", False),
        "household_size": params.get("household_size", 1),
        "annual_income": params.get("annual_income", 0),
        "program": params.get("program", "SNAP"),
        "determination_date": params.get("determination_date", ""),
        "rule_version": params.get("rule_version", ""),
        "state": params.get("state", "contiguous"),
    }


class OntologyFirewall:
    """
    Validates every proposed action against SHACL constraints.
    Can BLOCK actions but never APPROVE them.
    Every constraint maps to a specific EU AI Act article.
    """

    def validate_action(self, action_data: dict) -> ValidationResult:
        """Validate action data against constraints."""
        return validate_action(action_data)

    def guard_mcp_tool_call(
        self,
        tool_name: str,
        parameters: dict,
        agent_id: str,
    ) -> GuardResult:
        """
        Guard an MCP tool call before execution.

        Returns GuardResult with status ALLOWED or BLOCKED.
        """
        action_data = _create_action_data(parameters, None)
        validation = self.validate_action(action_data)

        status = "ALLOWED" if validation.allowed else "BLOCKED"
        compliance = {
            "deterministic": True,
            "articles_satisfied": validation.compliance_articles_satisfied,
            "violations": [v.model_dump() for v in validation.violations],
        }

        return GuardResult(
            status=status,
            tool=tool_name,
            agent_id=agent_id,
            validation=validation,
            compliance=compliance,
        )

    def guard_eligibility_determination(
        self,
        determination: EligibilityDetermination,
        agent_id: str = "RulesAgent",
    ) -> GuardResult:
        """Guard an eligibility determination before it is finalized."""
        action_data = _create_action_data({}, determination)
        validation = self.validate_action(action_data)

        status = "ALLOWED" if validation.allowed else "BLOCKED"
        compliance = {
            "deterministic": True,
            "articles_satisfied": validation.compliance_articles_satisfied,
            "violations": [v.model_dump() for v in validation.violations],
        }

        return GuardResult(
            status=status,
            tool="check_eligibility",
            agent_id=agent_id,
            validation=validation,
            compliance=compliance,
        )

    def get_compliance_summary(self) -> dict[str, Any]:
        """Count of constraints by EU AI Act article."""
        return {
            "Art. 9": ["BenefitApprovalShape", "EnrollmentRequiredShape"],
            "Art. 10": ["HouseholdDataShape", "ApplicationCompletenessShape"],
            "Art. 11": ["rule_version in determination"],
            "Art. 12": ["DeterminationAuditShape"],
            "Art. 14": ["LifeEventReviewShape"],
            "Art. 15": ["SNAPIncomeShape", "MedicaidIncomeShape"],
        }

    def get_audit_trail(
        self,
        applicant_id: Optional[str] = None,
        last_n: int = 50,
    ) -> list[AuditEntry]:
        """Get audit trail entries (delegates to audit trail manager if set)."""
        if _audit_trail_manager:
            return _audit_trail_manager.get_trail(applicant_id=applicant_id, last_n=last_n)
        return []
