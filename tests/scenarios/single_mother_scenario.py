"""
Runnable: The exact closing scenario from the TDS article.

python -m tests.scenarios.single_mother_scenario

Single mother reports job loss → SNAP + Medicaid + TANF + Housing review.
"""
from human_services.agents.orchestrator import HumanServicesOrchestrator


def main():
    print("=== Single Mother Job Loss Scenario ===\n")
    orch = HumanServicesOrchestrator()
    result = orch.single_mother_scenario()
    print(f"Citizen ID: {result['citizen_id']}")
    print(f"Event: {result['event_type']}")
    print(f"Requires human review: {result['requires_human_review']}\n")
    print("Program results:")
    for r in result["program_results"]:
        status = "[OK]" if r["eligible"] else "[--]"
        print(f"  {status} {r['program']}: eligible={r['eligible']}, blocked={r.get('blocked', False)}")
        if r.get("qa_flags"):
            print(f"    QA flags: {r['qa_flags']}")
    print(f"\nCompliance articles: {result['compliance_articles']}")


if __name__ == "__main__":
    main()
