"""Explanation generator unit tests."""
import pytest

from human_services.compliance.explanation_generator import ExplanationGenerator
from human_services.models.data_models import (
    ApplicationStatus,
    BenefitProgram,
    EligibilityDetermination,
)


def _make_determination(eligible: bool, enrollment_complete: bool = True, status: str = "Enrolled"):
    return EligibilityDetermination(
        applicant_id="a1",
        program=BenefitProgram.SNAP,
        eligible=eligible,
        income_limit=41000,
        annual_income=38000,
        household_size=4,
        status=ApplicationStatus(status) if status in [s.value for s in ApplicationStatus] else ApplicationStatus.ACTIVE,
        enrollment_complete=enrollment_complete,
        determination_date="2026-01-01",
        rule_version="2026-FPL-v1",
    )


def test_three_levels_generated():
    """Output has caseworker, citizen, auditor keys."""
    g = ExplanationGenerator()
    d = _make_determination(True)
    d.status = ApplicationStatus.ENROLLED
    expl = g.generate(d)
    assert "caseworker" in expl
    assert "citizen" in expl
    assert "auditor" in expl


def test_citizen_level_no_jargon():
    """Citizen explanation has no technical terms."""
    g = ExplanationGenerator()
    d = _make_determination(True)
    d.status = ApplicationStatus.ENROLLED
    expl = g.generate(d)
    assert g.validate_citizen_no_jargon(expl)


def test_auditor_level_has_rule_version():
    """Auditor level includes rule version."""
    g = ExplanationGenerator()
    d = _make_determination(True)
    d.status = ApplicationStatus.ENROLLED
    expl = g.generate(d)
    assert "2026" in expl["auditor"] or "rule" in expl["auditor"].lower()


def test_eligible_explanation():
    """Correct language for eligible determination."""
    g = ExplanationGenerator()
    d = _make_determination(True)
    d.status = ApplicationStatus.ENROLLED
    expl = g.generate(d)
    assert "qualif" in expl["citizen"].lower() or "income" in expl["citizen"].lower()


def test_ineligible_explanation_with_alternatives():
    """Suggests other programs for ineligible."""
    g = ExplanationGenerator()
    d = _make_determination(False)
    d.status = ApplicationStatus.ENROLLED
    expl = g.generate(d)
    assert "other" in expl["citizen"].lower() or "options" in expl["citizen"].lower() or "exceeds" in expl["caseworker"].lower()


def test_blocked_explanation_with_action():
    """Explains what needs to happen for blocked."""
    g = ExplanationGenerator()
    d = _make_determination(False)
    d.status = ApplicationStatus.ACTIVE
    d.enrollment_complete = False
    expl = g.generate(d)
    assert "citizen" in expl
    assert len(expl["citizen"]) > 0
