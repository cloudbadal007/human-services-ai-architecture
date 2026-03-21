"""Shared pytest fixtures."""
import pytest

from human_services.compliance.audit_trail import AuditTrailManager


@pytest.fixture
def audit_manager():
    """Fresh audit trail manager."""
    return AuditTrailManager()
