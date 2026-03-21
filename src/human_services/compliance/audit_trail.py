"""
Audit Trail Manager — Immutable logging (Art. 12).

Thread-safe manager creating immutable AuditEntry records for
every MCP tool call and determination.
"""
import threading
import uuid
from datetime import datetime
from typing import Any, Optional

from human_services.models.data_models import AuditEntry


class AuditTrailManager:
    """
    Records audit entries for EU AI Act Art. 12 compliance.
    Entries are immutable. Thread-safe.
    """

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []
        self._lock = threading.Lock()

    def record(
        self,
        agent_id: str,
        action_type: str,
        program: Optional[str] = None,
        status: Optional[str] = None,
        violations: Optional[list[dict]] = None,
        determination: Optional[dict] = None,
        validation_time_ms: Optional[float] = None,
        tool_name: Optional[str] = None,
        parameters: Optional[dict] = None,
        result: Optional[dict] = None,
        applicant_id: Optional[str] = None,
    ) -> AuditEntry:
        """Create and store immutable audit entry."""
        entry_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        articles = ["Art. 12"]
        if violations:
            articles.append("Art. 9")

        entry = AuditEntry(
            entry_id=entry_id,
            timestamp=timestamp,
            agent_id=agent_id,
            action_type=action_type,
            tool_name=tool_name,
            parameters=parameters or {},
            result=result or determination,
            applicant_id=applicant_id,
            program=program,
            eu_ai_act_articles=articles,
            violations=violations or [],
        )

        with self._lock:
            self._entries.append(entry)
        return entry

    def get_trail(
        self,
        applicant_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        last_n: int = 100,
    ) -> list[AuditEntry]:
        """Get filtered audit trail."""
        with self._lock:
            entries = list(self._entries)
        if applicant_id:
            entries = [e for e in entries if e.applicant_id == applicant_id]
        if agent_id:
            entries = [e for e in entries if e.agent_id == agent_id]
        return entries[-last_n:]

    def export_for_regulator(self, format: str = "json") -> str:
        """Export trail for regulator (Art. 12)."""
        import json

        entries = [e.model_dump() for e in self._entries]
        if format == "json":
            return json.dumps(entries, indent=2)
        raise ValueError(f"Unsupported format: {format}")

    def verify_immutability(self) -> bool:
        """Confirm entries are valid AuditEntry instances (frozen per Art. 12)."""
        for entry in self._entries:
            if not isinstance(entry, AuditEntry):
                return False
            try:
                # Frozen model: direct attribute assign raises ValidationError
                entry.timestamp = "modified"  # type: ignore
                return False
            except Exception:
                pass
        return len(self._entries) == 0 or all(isinstance(e, AuditEntry) for e in self._entries)


# Global default instance
_default_manager: Optional[AuditTrailManager] = None


def get_audit_trail_manager() -> AuditTrailManager:
    """Get or create default audit trail manager."""
    global _default_manager
    if _default_manager is None:
        _default_manager = AuditTrailManager()
    return _default_manager
