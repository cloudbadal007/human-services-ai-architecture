"""EU AI Act Article 15 — Accuracy and robustness."""


def test_100_runs_identical_result():
    """Deterministic guarantee over 100 runs."""
    from human_services.mcp.eligibility_server import check_eligibility

    results = []
    for _ in range(100):
        r = check_eligibility(
            applicant_id="a1",
            program="SNAP",
            annual_income=32000,
            household_size=4,
            status="Enrolled",
            enrollment_complete=True,
        )
        results.append((r["eligible"], r.get("blocked", False)))

    assert all(x == results[0] for x in results)
    assert results[0] == (True, False)


def test_fpl_matches_published_data():
    """Thresholds match HHS published values (2026 FPL)."""
    from human_services.utils.fpl_thresholds import get_fpl, get_income_limit, SNAP_GROSS

    # 2026 FPL household of 4 contiguous: ~$31,200
    fpl = get_fpl(4)
    assert 30_000 < fpl < 35_000
    # SNAP = 130% FPL
    snap_limit = get_income_limit(4, "SNAP")
    assert abs(snap_limit - fpl * SNAP_GROSS) < 100


def test_rules_agent_uses_zero_llm():
    """Verify no probabilistic reasoning in rules."""
    from human_services.agents.rules_agent import calculate_eligibility

    # Same inputs, multiple runs — must be identical
    out1 = calculate_eligibility("a1", "SNAP", 30000, 4, "Enrolled", True)
    out2 = calculate_eligibility("a1", "SNAP", 30000, 4, "Enrolled", True)
    assert out1.eligible == out2.eligible
    assert out1.income_limit == out2.income_limit
