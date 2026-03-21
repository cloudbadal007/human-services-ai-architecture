"""
Runnable: Simulated EU AI Act regulator audit.

python -m tests.scenarios.compliance_audit_simulation
"""
from human_services.compliance.compliance_checker import ComplianceChecker


def main():
    print("=== EU AI Act Compliance Audit Simulation ===\n")
    checker = ComplianceChecker()
    report = checker.generate_conformity_report()
    print(report)


if __name__ == "__main__":
    main()
