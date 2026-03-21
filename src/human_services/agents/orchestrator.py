"""
HumanServicesOrchestrator — Compliance pipeline with checkpoints.

Coordinates all agents: Intake (prob) → Retrieval → Rules → Firewall → QA → Explanation.
Art. 12 audit, Art. 13 explanation, Art. 14 human review flagging.
"""
from typing import Any

from human_services.agents.intake_agent import interpret_situation
from human_services.agents.qa_agent import validate_determination
from human_services.compliance.audit_trail import get_audit_trail_manager
from human_services.models.data_models import LifeEventType
from human_services.compliance.explanation_generator import ExplanationGenerator
from human_services.mcp.eligibility_server import check_eligibility, flag_life_event
from human_services.ontology.firewall import OntologyFirewall


class HumanServicesOrchestrator:
    """Orchestrates agents with EU AI Act compliance checkpoints."""

    def __init__(self) -> None:
        self.firewall = OntologyFirewall()
        self.explainer = ExplanationGenerator()
        self.audit = get_audit_trail_manager()

    def process_life_event(
        self,
        citizen_id: str,
        event_type: str,
        event_details: dict | None = None,
        annual_income: float = 0,
        household_size: int = 1,
    ) -> dict[str, Any]:
        """
        Full pipeline: interpret → per-program eval → firewall → QA → explanation.
        All results flagged for caseworker review (Art. 14).
        """
        event_details = event_details or {}
        # 1. IntakeAgent interprets (stub uses simple mapping)
        interpreted = interpret_situation(
            event_details.get("description", f"Life event: {event_type}")
        )
        try:
            ev = LifeEventType(event_type)
            programs = [p.value for p in ev.affected_programs()]
        except ValueError:
            programs = interpreted.get("affected_programs", ["SNAP", "MEDICAID", "TANF", "HOUSING"])

        results = []
        compliance_articles = set()

        for program in programs:
            # 2. Retrieval + Rules: get eligibility via MCP
            det = check_eligibility(
                applicant_id=citizen_id,
                program=program,
                annual_income=annual_income,
                household_size=household_size,
                status="Active",
                enrollment_complete=False,
            )
            determination_data = det.get("explanation", {})
            qa_flags: list[str] = []
            if det.get("determination"):
                from human_services.models.data_models import EligibilityDetermination

                det_obj = EligibilityDetermination(**det["determination"])
                det_obj.explanation = self.explainer.generate(det_obj)
                qa = validate_determination(det_obj)
                qa_flags = qa.get("flags", [])
                determination_data = det_obj.explanation
                compliance_articles.update(["Art. 12", "Art. 13", "Art. 14", "Art. 15"])

            results.append({
                "program": program,
                "eligible": det.get("eligible", False),
                "blocked": det.get("blocked", False),
                "explanation": determination_data,
                "qa_flags": qa_flags,
            })

        # 4. Flag life event for human review
        flag_result = flag_life_event(citizen_id=citizen_id, event_type=event_type, event_details=event_details)

        return {
            "citizen_id": citizen_id,
            "event_type": event_type,
            "program_results": results,
            "requires_human_review": True,
            "life_event": flag_result.get("life_event"),
            "compliance_articles": list(compliance_articles),
            "audit_trail": "generated",
        }

    def single_mother_scenario(self) -> dict[str, Any]:
        """
        The exact closing scenario from the TDS article:
        Job loss → SNAP + Medicaid + TANF + Housing review.
        """
        return self.process_life_event(
            citizen_id="single_mother_001",
            event_type="job_loss",
            event_details={"description": "Lost job, single mother with 2 children"},
            annual_income=24000,
            household_size=3,
        )
