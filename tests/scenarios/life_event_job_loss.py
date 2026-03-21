"""Runnable: Job loss → 4-program cascade."""
from human_services.mcp.eligibility_server import flag_life_event


def main():
    r = flag_life_event("c1", "job_loss", {"employer": "Acme Corp"})
    print("Affected programs:", r["affected_programs"])
    print("Review tasks:", r["review_tasks"])
    print("Requires human review:", r["requires_human_review"])


if __name__ == "__main__":
    main()
