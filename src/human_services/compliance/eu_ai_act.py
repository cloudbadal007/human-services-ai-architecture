"""
EU AI Act — High-Risk AI System Obligations for Public Benefits.

This module codifies Articles 9-15 of the EU AI Act as they apply to
AI systems used by public authorities to evaluate eligibility for
essential public assistance benefits and services (Annex III).

Effective: August 2, 2026
Penalties: Up to €35 million or 7% of global annual turnover

Every component in this project maps to one or more of these obligations.
This module provides:
- Programmatic definitions of each obligation
- Validation functions to check compliance
- Mapping between architectural components and obligations
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EUAIActArticle(Enum):
    """EU AI Act High-Risk obligations (Articles 9-15)."""

    ART_9_RISK_MANAGEMENT = "Article 9 — Risk Management System"
    ART_10_DATA_GOVERNANCE = "Article 10 — Data and Data Governance"
    ART_11_TECHNICAL_DOCUMENTATION = "Article 11 — Technical Documentation"
    ART_12_RECORD_KEEPING = "Article 12 — Record-Keeping / Automatic Logging"
    ART_13_TRANSPARENCY = "Article 13 — Transparency and Information to Deployers"
    ART_14_HUMAN_OVERSIGHT = "Article 14 — Human Oversight"
    ART_15_ACCURACY_ROBUSTNESS = "Article 15 — Accuracy, Robustness and Cybersecurity"


@dataclass
class ComplianceRequirement:
    """A specific compliance requirement derived from the EU AI Act."""

    article: EUAIActArticle
    requirement_id: str
    description: str
    architectural_component: str
    verification_method: str
    status: str = "NOT_VERIFIED"  # NOT_VERIFIED, COMPLIANT, NON_COMPLIANT
    evidence: Optional[str] = None


@dataclass
class ComplianceReport:
    """Complete compliance assessment report for conformity assessment."""

    system_name: str
    assessment_date: str
    assessor: str
    requirements: list[ComplianceRequirement] = field(default_factory=list)
    overall_status: str = "NOT_ASSESSED"

    @property
    def compliant_count(self) -> int:
        return sum(1 for r in self.requirements if r.status == "COMPLIANT")

    @property
    def total_count(self) -> int:
        return len(self.requirements)

    @property
    def compliance_percentage(self) -> float:
        if self.total_count == 0:
            return 0.0
        return (self.compliant_count / self.total_count) * 100


# ── Compliance Requirements Registry ──────────────────────────
# Each requirement maps an EU AI Act obligation to an architectural
# component and a verification method.

COMPLIANCE_REQUIREMENTS = [
    # ARTICLE 9 — Risk Management
    ComplianceRequirement(
        article=EUAIActArticle.ART_9_RISK_MANAGEMENT,
        requirement_id="ART9-001",
        description="Known risks identified and mitigated via SHACL constraints",
        architectural_component="OntologyFirewall + SHACL Shapes",
        verification_method="Count SHACL shapes with sh:Violation severity; "
        "each represents a documented risk mitigation",
    ),
    ComplianceRequirement(
        article=EUAIActArticle.ART_9_RISK_MANAGEMENT,
        requirement_id="ART9-002",
        description="Semantic status misinterpretation risk mitigated",
        architectural_component="BenefitApprovalShape SHACL constraint",
        verification_method="Test: submit action with status='Active'; "
        "verify BLOCKED with correct error message",
    ),
    ComplianceRequirement(
        article=EUAIActArticle.ART_9_RISK_MANAGEMENT,
        requirement_id="ART9-003",
        description="QA Agent validates determinations against known error patterns",
        architectural_component="QAAgent",
        verification_method="Run QA agent against test suite of known failure cases",
    ),
    # ARTICLE 10 — Data Governance
    ComplianceRequirement(
        article=EUAIActArticle.ART_10_DATA_GOVERNANCE,
        requirement_id="ART10-001",
        description="Semantic reconciliation layer for cross-system data",
        architectural_component="OWL Ontology (human_services.ttl)",
        verification_method="Load ontology; verify all cross-system terms "
        "have canonical definitions with rdfs:comment",
    ),
    ComplianceRequirement(
        article=EUAIActArticle.ART_10_DATA_GOVERNANCE,
        requirement_id="ART10-002",
        description="Data validation constraints enforce quality",
        architectural_component="HouseholdDataShape SHACL constraint",
        verification_method="Test: submit household_size=0; verify BLOCKED",
    ),
    # ARTICLE 11 — Technical Documentation
    ComplianceRequirement(
        article=EUAIActArticle.ART_11_TECHNICAL_DOCUMENTATION,
        requirement_id="ART11-001",
        description="All business rules documented as versioned SHACL shapes",
        architectural_component="ontologies/eligibility_shapes.ttl",
        verification_method="Verify every SHACL shape has version annotation "
        "and human-readable sh:message",
    ),
    ComplianceRequirement(
        article=EUAIActArticle.ART_11_TECHNICAL_DOCUMENTATION,
        requirement_id="ART11-002",
        description="Rule version tracked in every determination",
        architectural_component="EligibilityDetermination.rule_version",
        verification_method="Run determination; verify rule_version in output",
    ),
    # ARTICLE 12 — Record-Keeping
    ComplianceRequirement(
        article=EUAIActArticle.ART_12_RECORD_KEEPING,
        requirement_id="ART12-001",
        description="Every MCP tool call logged with full input/output",
        architectural_component="MCP Server audit logging",
        verification_method="Run eligibility check; verify AuditEntry created "
        "with tool name, parameters, result, timestamp",
    ),
    ComplianceRequirement(
        article=EUAIActArticle.ART_12_RECORD_KEEPING,
        requirement_id="ART12-002",
        description="Audit entries are immutable",
        architectural_component="AuditEntry (frozen Pydantic model)",
        verification_method="Attempt to modify AuditEntry; verify exception raised",
    ),
    # ARTICLE 13 — Transparency
    ComplianceRequirement(
        article=EUAIActArticle.ART_13_TRANSPARENCY,
        requirement_id="ART13-001",
        description="Multi-level explanations generated for every determination",
        architectural_component="ExplanationGenerator",
        verification_method="Run determination; verify explanation dict contains "
        "'caseworker', 'citizen', and 'auditor' keys",
    ),
    ComplianceRequirement(
        article=EUAIActArticle.ART_13_TRANSPARENCY,
        requirement_id="ART13-002",
        description="Citizen explanation uses plain language, no technical jargon",
        architectural_component="ExplanationGenerator.citizen_level()",
        verification_method="Run determination; verify citizen explanation "
        "contains no ontology terms, SHACL references, or codes",
    ),
    # ARTICLE 14 — Human Oversight
    ComplianceRequirement(
        article=EUAIActArticle.ART_14_HUMAN_OVERSIGHT,
        requirement_id="ART14-001",
        description="Only deterministic agents can make eligibility decisions",
        architectural_component="AgentSpec.can_make_eligibility_decision",
        verification_method="Verify IntakeAgent (probabilistic) has "
        "can_make_eligibility_decision=False",
    ),
    ComplianceRequirement(
        article=EUAIActArticle.ART_14_HUMAN_OVERSIGHT,
        requirement_id="ART14-002",
        description="Life event changes require caseworker confirmation",
        architectural_component="LifeEvent.requires_human_review",
        verification_method="Trigger life event; verify requires_human_review=True "
        "on all generated review tasks",
    ),
    # ARTICLE 15 — Accuracy and Robustness
    ComplianceRequirement(
        article=EUAIActArticle.ART_15_ACCURACY_ROBUSTNESS,
        requirement_id="ART15-001",
        description="Deterministic: identical inputs produce identical outputs",
        architectural_component="RulesAgent (deterministic, zero LLM)",
        verification_method="Run same determination 100 times; "
        "verify all 100 results are identical",
    ),
    ComplianceRequirement(
        article=EUAIActArticle.ART_15_ACCURACY_ROBUSTNESS,
        requirement_id="ART15-002",
        description="Income threshold calculations use published FPL data",
        architectural_component="fpl_thresholds.py",
        verification_method="Verify FPL values match HHS published guidelines",
    ),
]
