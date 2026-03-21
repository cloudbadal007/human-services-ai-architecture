"""FPL thresholds unit tests."""
import pytest

from human_services.utils.fpl_thresholds import (
    State,
    get_fpl,
    get_income_limit,
    is_income_eligible,
    SNAP_GROSS,
)


def test_get_fpl_household_1():
    """FPL for household of 1."""
    fpl = get_fpl(1)
    assert fpl > 0
    assert fpl < 20000


def test_get_fpl_household_4():
    """FPL for household of 4."""
    fpl = get_fpl(4)
    assert fpl > 20000


def test_get_fpl_household_8():
    """FPL for household of 8."""
    fpl = get_fpl(8)
    assert fpl > 40000


def test_get_fpl_alaska_higher():
    """Alaska FPL higher than contiguous."""
    c = get_fpl(4, State.CONTIGUOUS)
    a = get_fpl(4, State.ALASKA)
    assert a > c


def test_get_income_limit_snap():
    """SNAP limit is 130% FPL."""
    limit = get_income_limit(4, "SNAP")
    fpl = get_fpl(4)
    assert abs(limit - fpl * SNAP_GROSS) < 10


def test_is_income_eligible():
    """Income eligible check."""
    assert is_income_eligible(30000, 4, "SNAP") is True
    assert is_income_eligible(100000, 2, "SNAP") is False
