# EU AI Act Compliance

## Overview

The EU AI Act classifies AI systems used by public authorities to evaluate eligibility for essential public assistance benefits as **High-Risk** under Annex III. This applies to SNAP, Medicaid, housing assistance, and similar programs.

## Timeline

- **August 2, 2026** — High-risk obligations (Articles 9–15) effective
- **December 2027** — Full backstop
- **2030** — Legacy systems must comply

## Penalties

Up to €35 million or 7% of global annual turnover for non-compliance.

## Article-by-Article Mapping

### Art. 9 — Risk Management

- **BenefitApprovalShape** — Mitigates status misinterpretation (Active ≠ Enrolled)
- **EnrollmentRequiredShape** — Prevents enrollment bypass
- **RiskRegistry** — Documents known risks and SHACL mitigations
- **QAAgent** — Validates determinations against error patterns

### Art. 10 — Data Governance

- **OWL ontology** — Semantic reconciliation across systems
- **HouseholdDataShape** — Validates household size (1–20)
- **ApplicationCompletenessShape** — Required fields

### Art. 11 — Technical Documentation

- **Versioned SHACL shapes** — Every shape has sh:message and version
- **rule_version** in EligibilityDetermination — Tracked in every output

### Art. 12 — Record-Keeping

- **AuditTrailManager** — Every MCP call logged
- **AuditEntry** — Frozen (immutable) Pydantic model
- **export_for_regulator()** — Compliance-ready export

### Art. 13 — Transparency

- **ExplanationGenerator** — Three levels: caseworker, citizen, auditor
- **Citizen level** — Plain language, no jargon (no SHACL, FPL, ontology terms)

### Art. 14 — Human Oversight

- **AgentSpec.can_make_eligibility_decision** — Only RulesAgent = True
- **LifeEvent.requires_human_review** — Always True for life events

### Art. 15 — Accuracy and Robustness

- **RulesAgent** — Deterministic, zero LLM, same input → same output
- **fpl_thresholds.py** — Published HHS FPL data

## Conformity Assessment Checklist

1. Risk management system (Art. 9)
2. Data governance (Art. 10)
3. Technical documentation (Art. 11)
4. Record-keeping (Art. 12)
5. Transparency (Art. 13)
6. Human oversight (Art. 14)
7. Accuracy/robustness (Art. 15)

## How to Run Compliance Check

```bash
make compliance-report
# or
python scripts/compliance_audit.py
```
