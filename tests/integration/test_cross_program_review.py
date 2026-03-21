"""Single life event → multiple programs."""


def test_cross_program_review():
    """Job loss triggers 4 program reviews."""
    from human_services.agents.orchestrator import HumanServicesOrchestrator

    orch = HumanServicesOrchestrator()
    result = orch.single_mother_scenario()
    assert "program_results" in result
    assert len(result["program_results"]) >= 4
    assert result["requires_human_review"] is True
    programs = {r["program"] for r in result["program_results"]}
    assert "SNAP" in programs
    assert "MEDICAID" in programs
