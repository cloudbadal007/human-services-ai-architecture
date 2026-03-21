"""Configuration management."""
import os
from pathlib import Path


def get_ontology_path() -> Path:
    """Get ontology directory path."""
    return Path(
        os.environ.get("ONTOLOGY_PATH", "ontologies")
    ).resolve()


def get_log_level() -> str:
    """Get log level from environment."""
    return os.environ.get("LOG_LEVEL", "INFO")


def get_compliance_assessor() -> str:
    """Get compliance assessor name for reports."""
    return os.environ.get("COMPLIANCE_ASSESSOR", "Default Assessor")
