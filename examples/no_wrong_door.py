"""Full 'No Wrong Door' pattern."""
from human_services.agents.orchestrator import HumanServicesOrchestrator


def main():
    orch = HumanServicesOrchestrator()
    result = orch.process_life_event(
        citizen_id="c1",
        event_type="job_loss",
        event_details={"description": "Lost job"},
        annual_income=24000,
        household_size=3,
    )
    print("Program results:", [r["program"] for r in result["program_results"]])
    print("Requires human review:", result["requires_human_review"])


if __name__ == "__main__":
    main()
