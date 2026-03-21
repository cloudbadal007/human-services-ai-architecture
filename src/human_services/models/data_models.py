"""
Pydantic data models with EU AI Act compliance fields.

Every model that produces output includes a compliance or eu_ai_act field
documenting which articles are satisfied.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

from human_services.compliance.eu_ai_act import EUAIActArticle


class ApplicationStatus(str, Enum):
    """Application/benefit status from legacy systems.

    CRITICAL: 'Active' is a legacy status meaning 'in progress' — NOT 'enrolled'.
    Many systems conflate these, causing the 'contextually insane agent' trap
    where an AI approves benefits for someone who isn't actually receiving them.
    Only ENROLLED and RENEWED permit disbursement.
    """

    ACTIVE = "Active"  # In progress — does NOT permit disbursement
    PENDING = "Pending"
    ENROLLED = "Enrolled"
    RENEWED = "Renewed"
    DENIED = "Denied"
    CLOSED = "Closed"
    SUSPENDED = "Suspended"
    APPEAL = "Appeal"

    @classmethod
    def disbursement_permitted(cls) -> list["ApplicationStatus"]:
        """Statuses that permit benefit disbursement (Art. 15 accuracy)."""
        return [cls.ENROLLED, cls.RENEWED]


class BenefitProgram(str, Enum):
    """Benefit programs supported."""

    SNAP = "SNAP"
    MEDICAID = "MEDICAID"
    TANF = "TANF"
    HOUSING = "HOUSING"
    WIC = "WIC"
    CHILDCARE = "CHILDCARE"
    UNEMPLOYMENT = "UNEMPLOYMENT"
    DISABILITY = "DISABILITY"


class LifeEventType(str, Enum):
    """Life events that trigger cross-program review (No Wrong Door)."""

    JOB_LOSS = "job_loss"
    INCOME_CHANGE = "income_change"
    HOUSEHOLD_CHANGE = "household_change"
    ADDRESS_CHANGE = "address_change"
    HEALTH_CHANGE = "health_change"
    IMMIGRATION_STATUS = "immigration_status"
    DISABILITY_ONSET = "disability_onset"
    CHILD_BORN = "child_born"
    MARITAL_CHANGE = "marital_change"
    INCARCERATION = "incarceration"

    def affected_programs(self) -> list[BenefitProgram]:
        """Map life event to programs that may need review (No Wrong Door)."""
        mapping = {
            LifeEventType.JOB_LOSS: [
                BenefitProgram.SNAP,
                BenefitProgram.MEDICAID,
                BenefitProgram.TANF,
                BenefitProgram.HOUSING,
            ],
            LifeEventType.INCOME_CHANGE: [
                BenefitProgram.SNAP,
                BenefitProgram.MEDICAID,
                BenefitProgram.TANF,
                BenefitProgram.HOUSING,
                BenefitProgram.WIC,
            ],
            LifeEventType.HOUSEHOLD_CHANGE: [
                BenefitProgram.SNAP,
                BenefitProgram.MEDICAID,
                BenefitProgram.TANF,
                BenefitProgram.WIC,
                BenefitProgram.CHILDCARE,
            ],
            LifeEventType.ADDRESS_CHANGE: [
                BenefitProgram.SNAP,
                BenefitProgram.MEDICAID,
                BenefitProgram.HOUSING,
            ],
            LifeEventType.HEALTH_CHANGE: [
                BenefitProgram.MEDICAID,
                BenefitProgram.DISABILITY,
            ],
            LifeEventType.DISABILITY_ONSET: [
                BenefitProgram.MEDICAID,
                BenefitProgram.DISABILITY,
                BenefitProgram.SNAP,
            ],
            LifeEventType.CHILD_BORN: [
                BenefitProgram.SNAP,
                BenefitProgram.MEDICAID,
                BenefitProgram.WIC,
                BenefitProgram.CHILDCARE,
            ],
            LifeEventType.MARITAL_CHANGE: [
                BenefitProgram.SNAP,
                BenefitProgram.MEDICAID,
                BenefitProgram.TANF,
            ],
            LifeEventType.IMMIGRATION_STATUS: [
                BenefitProgram.SNAP,
                BenefitProgram.MEDICAID,
                BenefitProgram.TANF,
            ],
            LifeEventType.INCARCERATION: [
                BenefitProgram.SNAP,
                BenefitProgram.MEDICAID,
                BenefitProgram.HOUSING,
            ],
        }
        return mapping.get(self, [])


class SeverityLevel(str, Enum):
    """SHACL constraint severity."""

    VIOLATION = "Violation"
    WARNING = "Warning"
    INFO = "Info"


class Violation(BaseModel):
    """SHACL validation violation with EU AI Act mapping."""

    constraint_name: str
    severity: SeverityLevel
    message: str
    eu_ai_act_article: Optional[str] = None


class ValidationResult(BaseModel):
    """Result of ontology firewall validation (Art. 9, 15)."""

    allowed: bool
    deterministic: bool = True
    violations: list[Violation] = Field(default_factory=list)
    compliance_articles_satisfied: list[str] = Field(default_factory=list)


class GuardResult(BaseModel):
    """Result of firewall guard on MCP tool call."""

    status: str  # ALLOWED, BLOCKED
    tool: str
    agent_id: str
    validation: ValidationResult
    compliance: dict[str, Any] = Field(default_factory=dict)


class EligibilityDetermination(BaseModel):
    """Eligibility determination with full audit context (Art. 11, 12, 13)."""

    applicant_id: str
    program: BenefitProgram
    eligible: bool
    income_limit: int
    annual_income: float
    household_size: int
    status: ApplicationStatus
    enrollment_complete: bool
    determination_date: str
    rule_version: str
    audit_trail: dict[str, Any] = Field(default_factory=dict)
    explanation: dict[str, str] = Field(
        default_factory=dict,
        description="Art. 13: caseworker, citizen, auditor levels",
    )
    compliance: dict[str, Any] = Field(default_factory=dict)


class LifeEvent(BaseModel):
    """Life event with human review requirement (Art. 14)."""

    event_type: LifeEventType
    citizen_id: str
    event_details: dict[str, Any] = Field(default_factory=dict)
    recorded_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    requires_human_review: bool = True  # Always True per Art. 14
    affected_programs: list[BenefitProgram] = Field(default_factory=list)
    review_tasks: list[dict[str, Any]] = Field(default_factory=list)


class AuditEntry(BaseModel):
    """Immutable audit trail entry (Art. 12)."""

    model_config = {"frozen": True}

    entry_id: str
    timestamp: str
    agent_id: str
    action_type: str
    tool_name: Optional[str] = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    result: Optional[dict[str, Any]] = None
    applicant_id: Optional[str] = None
    program: Optional[str] = None
    eu_ai_act_articles: list[str] = Field(default_factory=list)
    violations: list[dict[str, Any]] = Field(default_factory=list)


class ComplianceTag(BaseModel):
    """Compliance tagging for audit."""

    article: EUAIActArticle
    requirement_id: str
    status: str
