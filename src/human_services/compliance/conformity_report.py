"""Generate conformity assessment report for EU AI Act."""
from human_services.compliance.compliance_checker import ComplianceChecker


def generate_report() -> str:
    """Generate full conformity report."""
    checker = ComplianceChecker()
    return checker.generate_conformity_report()
