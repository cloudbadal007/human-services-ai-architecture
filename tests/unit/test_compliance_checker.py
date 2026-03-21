"""EU AI Act compliance checker unit tests."""
import pytest

from human_services.compliance.eu_ai_act import EUAIActArticle, COMPLIANCE_REQUIREMENTS
from human_services.compliance.compliance_checker import ComplianceChecker


def test_all_articles_have_requirements():
    """Every Art. 9-15 has at least 1 requirement."""
    articles = {r.article for r in COMPLIANCE_REQUIREMENTS}
    for art in EUAIActArticle:
        assert art in articles


def test_compliance_check_returns_report():
    """check_all() returns ComplianceReport."""
    c = ComplianceChecker()
    r = c.check_all()
    assert r.system_name
    assert r.assessment_date
    assert r.requirements
    assert hasattr(r, "compliant_count")
    assert hasattr(r, "compliance_percentage")


def test_compliant_system_passes():
    """Fully configured system reports COMPLIANT."""
    c = ComplianceChecker(
        has_firewall=True,
        has_audit_trail=True,
        has_explanation=True,
        has_deterministic_rules=True,
    )
    r = c.check_all()
    assert r.overall_status == "COMPLIANT"
    assert r.compliance_percentage == 100


def test_missing_firewall_fails_art9():
    """System without firewall fails Art. 9."""
    c = ComplianceChecker(has_firewall=False)
    r = c.check_all()
    art9_reqs = [x for x in r.requirements if x.article == EUAIActArticle.ART_9_RISK_MANAGEMENT]
    assert any(x.status == "NON_COMPLIANT" for x in art9_reqs)


def test_missing_audit_trail_fails_art12():
    """System without audit fails Art. 12."""
    c = ComplianceChecker(has_audit_trail=False)
    r = c.check_all()
    art12_reqs = [x for x in r.requirements if x.article == EUAIActArticle.ART_12_RECORD_KEEPING]
    assert any(x.status == "NON_COMPLIANT" for x in art12_reqs)


def test_missing_explanation_fails_art13():
    """System without explanations fails Art. 13."""
    c = ComplianceChecker(has_explanation=False)
    r = c.check_all()
    art13_reqs = [x for x in r.requirements if x.article == EUAIActArticle.ART_13_TRANSPARENCY]
    assert any(x.status == "NON_COMPLIANT" for x in art13_reqs)


def test_conformity_report_format():
    """Report includes all required sections."""
    c = ComplianceChecker()
    report = c.generate_conformity_report()
    assert "EU AI Act" in report
    assert "Conformity" in report or "Assessment" in report
    assert "Requirements" in report or "requirement" in report.lower()
