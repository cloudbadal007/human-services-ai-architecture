"""
Runnable: The "Active" status trap.

python -m tests.scenarios.contextually_insane_agent
"""
from human_services.mcp.eligibility_server import check_eligibility


def main():
    print("=== The Contextually Insane Agent ===\n")
    print("Scenario: Agent proposes approval for status 'Active'")
    print("(Active = in progress, NOT enrolled)\n")
    r = check_eligibility(
        applicant_id="victim_001",
        program="SNAP",
        annual_income=30000,
        household_size=4,
        status="Active",
        enrollment_complete=True,
    )
    print(f"BLOCKED: {r['blocked']}")
    print(f"Eligible: {r['eligible']}")
    print(f"\nCitizen explanation: {r['explanation']['citizen']}")
    print(f"\nCompliance: {r.get('compliance', {})}")


if __name__ == "__main__":
    main()
