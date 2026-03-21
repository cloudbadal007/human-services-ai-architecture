"""Generate EU AI Act conformity report."""
from human_services.compliance.compliance_checker import ComplianceChecker


def main():
    checker = ComplianceChecker()
    report = checker.generate_conformity_report()
    print(report)


if __name__ == "__main__":
    main()
