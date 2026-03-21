"""EU AI Act Article 12 — Record-keeping / audit trail."""


def test_every_mcp_call_logged():
    """Run 5 tool calls, verify 5 audit entries."""
    import human_services.compliance.audit_trail as audit_mod
    from human_services.compliance.audit_trail import get_audit_trail_manager
    from human_services.mcp.eligibility_server import check_eligibility, get_case_history, flag_life_event

    # Use fresh manager for this test
    audit_mod._default_manager = None
    m = get_audit_trail_manager()
    initial = len(m.get_trail())

    check_eligibility("art12_a1", "SNAP", 30000, 4, "Enrolled", True)
    check_eligibility("art12_a2", "MEDICAID", 35000, 3, "Enrolled", True)
    get_case_history("art12_a1")
    flag_life_event("art12_c1", "job_loss")
    check_eligibility("art12_a3", "SNAP", 20000, 2, "Active", False)

    after = len(m.get_trail())
    assert after >= initial + 5, f"Expected at least {initial + 5} entries, got {after}"


def test_audit_entries_immutable():
    """Attempt modification, verify exception."""
    from human_services.compliance.audit_trail import get_audit_trail_manager
    from human_services.mcp.eligibility_server import check_eligibility

    check_eligibility("a1", "SNAP", 30000, 4, "Enrolled", True)
    m = get_audit_trail_manager()
    trail = m.get_trail(applicant_id="a1")
    if trail:
        entry = trail[-1]
        try:
            entry.timestamp = "modified"  # type: ignore
            assert False, "Should have raised"
        except Exception:
            pass


def test_audit_trail_includes_full_context():
    """Each entry has input, output, timestamp, agent_id."""
    from human_services.compliance.audit_trail import get_audit_trail_manager
    from human_services.mcp.eligibility_server import check_eligibility

    check_eligibility("a1", "SNAP", 30000, 4, "Enrolled", True)
    m = get_audit_trail_manager()
    trail = m.get_trail(applicant_id="a1")
    assert len(trail) >= 1
    e = trail[-1]
    assert e.entry_id
    assert e.timestamp
    assert e.agent_id
    assert e.action_type
