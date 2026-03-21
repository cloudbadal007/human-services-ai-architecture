"""Show deterministic audit trail."""
from human_services.mcp.eligibility_server import check_eligibility
from human_services.compliance.audit_trail import get_audit_trail_manager


def main():
    check_eligibility("a1", "SNAP", 30000, 4, "Enrolled", True)
    m = get_audit_trail_manager()
    trail = m.get_trail(applicant_id="a1")
    print(f"Audit entries for a1: {len(trail)}")
    if trail:
        e = trail[-1]
        print(f"  Latest: {e.agent_id} | {e.action_type} | {e.timestamp}")


if __name__ == "__main__":
    main()
