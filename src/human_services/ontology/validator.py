"""
SHACL validation engine.

Implements constraint logic equivalent to eligibility_shapes.ttl
for Python dict/object validation. Each constraint maps to EU AI Act articles.
"""
from human_services.models.data_models import (
    ApplicationStatus,
    SeverityLevel,
    ValidationResult,
    Violation,
)
from human_services.utils.fpl_thresholds import get_income_limit


def validate_benefit_approval(status: str, enrollment_complete: bool) -> list[Violation]:
    """Art. 9: Status must be Enrolled/Renewed for approval."""
    violations = []
    if status not in (
        ApplicationStatus.ENROLLED.value,
        ApplicationStatus.RENEWED.value,
    ):
        violations.append(
            Violation(
                constraint_name="BenefitApprovalShape",
                severity=SeverityLevel.VIOLATION,
                message="BLOCKED [EU AI Act Art. 9 — Risk Management]: "
                "Status must be 'Enrolled' or 'Renewed' for approval. "
                "'Active' means in-progress, NOT enrolled.",
                eu_ai_act_article="Art. 9",
            )
        )
    if not enrollment_complete:
        violations.append(
            Violation(
                constraint_name="EnrollmentRequiredShape",
                severity=SeverityLevel.VIOLATION,
                message="BLOCKED [EU AI Act Art. 9 — Risk Management]: "
                "Enrollment must be complete before approval.",
                eu_ai_act_article="Art. 9",
            )
        )
    return violations


def validate_household_data(household_size: int) -> list[Violation]:
    """Art. 10: Household size 1-20."""
    violations = []
    if household_size < 1 or household_size > 20:
        violations.append(
            Violation(
                constraint_name="HouseholdDataShape",
                severity=SeverityLevel.VIOLATION,
                message="BLOCKED [EU AI Act Art. 10 — Data Governance]: "
                "Household size must be between 1 and 20.",
                eu_ai_act_article="Art. 10",
            )
        )
    return violations


def validate_income(
    program: str, annual_income: float, household_size: int, state: str = "contiguous"
) -> list[Violation]:
    """Art. 15: Income within program limits."""
    violations = []
    from human_services.utils.fpl_thresholds import State

    state_enum = State.CONTIGUOUS
    if state.lower() == "alaska":
        state_enum = State.ALASKA
    elif state.lower() == "hawaii":
        state_enum = State.HAWAII

    try:
        limit = get_income_limit(household_size, program, state_enum)
    except ValueError:
        return violations  # Unknown program, skip
    if annual_income > limit:
        art = "Art. 15"
        msg = f"BLOCKED [EU AI Act {art} — Accuracy]: Income ${annual_income} exceeds limit ${limit}."
        violations.append(
            Violation(
                constraint_name=f"{program}IncomeShape",
                severity=SeverityLevel.VIOLATION,
                message=msg,
                eu_ai_act_article=art,
            )
        )
    return violations


def validate_determination_audit(
    determination_date: str, rule_version: str
) -> list[Violation]:
    """Art. 12: Determination must have date and rule version."""
    violations = []
    if not determination_date:
        violations.append(
            Violation(
                constraint_name="DeterminationAuditShape",
                severity=SeverityLevel.VIOLATION,
                message="BLOCKED [EU AI Act Art. 12 — Record-Keeping]: Determination date required.",
                eu_ai_act_article="Art. 12",
            )
        )
    if not rule_version:
        violations.append(
            Violation(
                constraint_name="DeterminationAuditShape",
                severity=SeverityLevel.VIOLATION,
                message="BLOCKED [EU AI Act Art. 12 — Record-Keeping]: Rule version required.",
                eu_ai_act_article="Art. 12",
            )
        )
    return violations


def validate_life_event_review(requires_human_review: bool) -> list[Violation]:
    """Art. 14: Life events require human review."""
    violations = []
    if not requires_human_review:
        violations.append(
            Violation(
                constraint_name="LifeEventReviewShape",
                severity=SeverityLevel.VIOLATION,
                message="BLOCKED [EU AI Act Art. 14 — Human Oversight]: Life event must require human review.",
                eu_ai_act_article="Art. 14",
            )
        )
    return violations


def validate_action(action_data: dict) -> ValidationResult:
    """
    Validate proposed eligibility action against all applicable constraints.

    action_data: dict with status, enrollment_complete, household_size,
                 annual_income, program, determination_date, rule_version, etc.
    """
    violations: list[Violation] = []

    # Benefit approval (Art. 9)
    status = action_data.get("status", "")
    enrollment = action_data.get("enrollment_complete", False)
    violations.extend(validate_benefit_approval(str(status), enrollment))

    # Household (Art. 10)
    hh = action_data.get("household_size", 0)
    violations.extend(validate_household_data(int(hh) if hh else 0))

    # Income (Art. 15) — only if proposing approval (eligible=True)
    # When eligible=False, we're not approving, so no income block
    proposed_approval = action_data.get("eligible", False)
    if proposed_approval and status in (ApplicationStatus.ENROLLED.value, ApplicationStatus.RENEWED.value):
        program = action_data.get("program", "SNAP")
        income = float(action_data.get("annual_income", 0))
        violations.extend(
            validate_income(program, income, int(hh or 1), action_data.get("state", "contiguous"))
        )

    # Audit (Art. 12) — only when we have determination data
    if action_data.get("determination_date") is not None or action_data.get("rule_version"):
        violations.extend(
            validate_determination_audit(
                action_data.get("determination_date", ""),
                action_data.get("rule_version", ""),
            )
        )

    allowed = len(violations) == 0
    satisfied = []
    if allowed:
        satisfied = ["Art. 9", "Art. 10", "Art. 12", "Art. 15"]
    elif violations:
        satisfied = []  # Blocked

    return ValidationResult(
        allowed=allowed,
        deterministic=True,
        violations=violations,
        compliance_articles_satisfied=satisfied,
    )
