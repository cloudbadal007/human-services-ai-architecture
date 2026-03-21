"""Check SNAP/Medicaid eligibility."""
from human_services.mcp.eligibility_server import check_eligibility


def main():
    print("=== Benefit Eligibility Check ===\n")
    for program in ["SNAP", "MEDICAID"]:
        r = check_eligibility(
            applicant_id="demo",
            program=program,
            annual_income=38000,
            household_size=4,
            status="Enrolled",
            enrollment_complete=True,
        )
        print(f"{program}: eligible={r['eligible']}, blocked={r.get('blocked', False)}")
        print(f"  {r['explanation']['citizen']}\n")


if __name__ == "__main__":
    main()
