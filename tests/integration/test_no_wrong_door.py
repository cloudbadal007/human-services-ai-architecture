"""Life event triggers cross-program review."""


def test_job_loss_triggers_four_programs():
    """Job loss triggers SNAP, Medicaid, TANF, Housing review."""
    from human_services.mcp.eligibility_server import flag_life_event

    r = flag_life_event("citizen_001", "job_loss")
    progs = r["affected_programs"]
    assert "SNAP" in progs
    assert "MEDICAID" in progs
    assert "TANF" in progs
    assert "HOUSING" in progs
    assert r["requires_human_review"] is True
