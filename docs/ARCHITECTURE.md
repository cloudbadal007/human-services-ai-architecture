# Architecture Deep-Dive

## 1. Problem Statement

Governments face two challenges:

1. **Compliance**: The EU AI Act classifies AI systems that evaluate eligibility for public benefits as High-Risk (Annex III), with obligations effective August 2, 2026. Penalties reach €35M or 7% of global turnover.

2. **Citizen Access**: $140B in benefits go unclaimed annually. Fragmented systems, confusing eligibility rules, and the "wrong door" problem prevent citizens from accessing assistance.

## 2. The Insight

**Compliance is the mechanism for service improvement.** The same architecture that satisfies EU AI Act Articles 9–15 also enables:

- Deterministic eligibility (Art. 15) → predictable, auditable outcomes
- Multi-level explanations (Art. 13) → citizen understanding
- Human oversight (Art. 14) → caseworker control
- Record-keeping (Art. 12) → accountability

## 3. Three-Layer Architecture

### Layer 1: MCP (Model Context Protocol)

Universal adapter for government systems. Maps to Art. 12 (record-keeping) and Art. 15 (robustness).

- `check_eligibility` — Benefit eligibility with compliance logging
- `get_case_history` — Unified cross-program history
- `flag_life_event` — "No Wrong Door" pattern

### Layer 2: OWL + SHACL

- **OWL ontology** — Shared semantic meaning across systems (Art. 10)
- **SHACL shapes** — Deterministic business rules (Art. 9, 11)
- **OntologyFirewall** — Validates every proposed action before execution

### Layer 3: Agentic Orchestration

Neuro-symbolic separation:

- **IntakeAgent** (probabilistic) — Interprets citizen situation
- **RetrievalAgent** (deterministic) — Queries via MCP
- **RulesAgent** (deterministic) — **Only** agent that can make eligibility decisions
- **QAAgent** (deterministic) — Validates against known error patterns
- **OntologyFirewall** — SHACL validation

## 4. EU AI Act Article Mapping

| Article | Component |
|---------|-----------|
| Art. 9 | SHACL constraints, RiskRegistry, QAAgent |
| Art. 10 | OWL ontology, HouseholdDataShape |
| Art. 11 | Versioned SHACL, rule_version in determination |
| Art. 12 | AuditTrailManager, immutable AuditEntry |
| Art. 13 | ExplanationGenerator (3 levels) |
| Art. 14 | AgentSpec.can_make_eligibility_decision, LifeEvent.requires_human_review |
| Art. 15 | RulesAgent (deterministic, zero LLM), FPL thresholds |

## 5. The Neuro-Symbolic Boundary

LLM reasoning must never touch eligibility decisions. Only deterministic agents (RulesAgent) can approve. The ontology firewall enforces this boundary by validating every proposed action against SHACL before it is executed.

## 6. The "Active" Status Trap

Legacy systems often use "Active" for "in progress." AI may misinterpret this as "enrolled." The BenefitApprovalShape SHACL constraint blocks approval unless status is Enrolled or Renewed. This mitigates a documented risk (Art. 9).

## 7. Data Flow

Life event → IntakeAgent (interpret) → For each program: RetrievalAgent → RulesAgent → OntologyFirewall → QAAgent → ExplanationGenerator → Caseworker review flag

## 8. Audit Trail Design

- Immutable Pydantic models (frozen=True)
- Every MCP call logged with input, output, timestamp, agent_id
- Export format for regulators

## 9. "No Wrong Door" Pattern

Life events map to affected programs. Job loss → SNAP, Medicaid, TANF, Housing. One intake triggers cross-program review.

## 10. Scaling

- Add programs: extend ontology, add SHACL shapes
- Add jurisdictions: FPL by state, locale-specific rules
- Add regulations: map new obligations to architectural components
