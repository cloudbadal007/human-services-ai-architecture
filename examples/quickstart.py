"""5-minute getting started."""
from human_services.mcp.eligibility_server import check_eligibility

# Check SNAP eligibility
result = check_eligibility(
    applicant_id="demo_001",
    program="SNAP",
    annual_income=35000,
    household_size=4,
    status="Enrolled",
    enrollment_complete=True,
)
print(f"Eligible: {result['eligible']}")
print(f"Citizen explanation: {result['explanation']['citizen']}")
