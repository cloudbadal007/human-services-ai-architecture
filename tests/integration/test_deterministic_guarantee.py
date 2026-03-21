"""Same input → same output, 100 runs."""


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
        results.append((r["eligible"], r["blocked"]))

    first = results[0]
    assert all(x == first for x in results)
    assert first == (True, False)
