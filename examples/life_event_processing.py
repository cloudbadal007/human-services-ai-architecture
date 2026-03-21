"""Process life event across programs."""
from human_services.mcp.eligibility_server import flag_life_event


def main():
    r = flag_life_event("citizen_001", "job_loss", {"employer": "Acme"})
    print("Affected programs:", r["affected_programs"])
    print("Requires human review:", r["requires_human_review"])


if __name__ == "__main__":
    main()
