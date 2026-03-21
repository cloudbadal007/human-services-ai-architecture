"""SHACL blocking invalid actions."""
from human_services.ontology.firewall import OntologyFirewall


def main():
    f = OntologyFirewall()
    # Invalid: status=Active
    r1 = f.validate_action({"status": "Active", "enrollment_complete": True})
    print(f"Status=Active: allowed={r1.allowed} (violations: {len(r1.violations)})")
    # Valid: status=Enrolled
    r2 = f.validate_action({"status": "Enrolled", "enrollment_complete": True, "household_size": 4})
    print(f"Status=Enrolled: allowed={r2.allowed}")


if __name__ == "__main__":
    main()
