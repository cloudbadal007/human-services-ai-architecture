"""Show multi-level explanations (caseworker/citizen/auditor)."""
from human_services.mcp.eligibility_server import check_eligibility


def main():
    r = check_eligibility(
        "a1", "SNAP", 35000, 4, "Enrolled", True
    )
    print("=== Caseworker (technical) ===")
    print(r["explanation"]["caseworker"])
    print("\n=== Citizen (plain language) ===")
    print(r["explanation"]["citizen"])
    print("\n=== Auditor (full audit) ===")
    print(r["explanation"]["auditor"])


if __name__ == "__main__":
    main()
