"""
Federal Poverty Level (FPL) Thresholds — 2026.

Source: US Department of Health and Human Services, Federal Register.
Publicly published data for SNAP, Medicaid, TANF, WIC, CHIP calculations.

All values are annual income limits for contiguous US states.
Alaska and Hawaii have higher thresholds.
"""
from enum import Enum
from typing import Optional


class State(Enum):
    """US state/territory for FPL thresholds."""

    CONTIGUOUS = "contiguous"
    ALASKA = "alaska"
    HAWAII = "hawaii"


# 2026 FPL annual income (contiguous US) — HHS published
# Household sizes 1-8
_FPL_CONTIGUOUS = {
    1: 15_060,
    2: 20_440,
    3: 25_820,
    4: 31_200,
    5: 36_580,
    6: 41_960,
    7: 47_340,
    8: 52_720,
}

# Per-additional-person amount for HH > 8
_FPL_PER_ADDITIONAL = 5_380

# Alaska multipliers vs contiguous
_ALASKA_MULTIPLIER = 1.25

# Hawaii multipliers vs contiguous
_HAWAII_MULTIPLIER = 1.15

# Program FPL multipliers (as percentage, e.g., 1.30 = 130%)
# Source: Federal program rules, SNAP gross income 130% FPL, etc.
SNAP_GROSS = 1.30
SNAP_NET = 1.00
MEDICAID_EXPANSION = 1.38
MEDICAID_TRADITIONAL = 0.75
TANF = 0.50
WIC = 1.85
CHIP = 2.00

# Rule version for audit trail (Art. 11)
FPL_RULE_VERSION = "2026-FPL-v1"


def get_fpl(household_size: int, state: State = State.CONTIGUOUS) -> int:
    """
    Get base FPL threshold for household size.

    Args:
        household_size: Number of people in household (1-20).
        state: State for threshold (contiguous, Alaska, Hawaii).

    Returns:
        Annual FPL threshold in dollars.
    """
    if household_size < 1:
        raise ValueError("Household size must be at least 1")
    if household_size > 20:
        raise ValueError("Household size exceeds supported range (1-20)")

    if household_size <= 8:
        base = _FPL_CONTIGUOUS[household_size]
    else:
        base = _FPL_CONTIGUOUS[8] + (household_size - 8) * _FPL_PER_ADDITIONAL

    if state == State.ALASKA:
        return int(base * _ALASKA_MULTIPLIER)
    if state == State.HAWAII:
        return int(base * _HAWAII_MULTIPLIER)
    return base


def get_income_limit(
    household_size: int,
    program: str,
    state: State = State.CONTIGUOUS,
) -> int:
    """
    Get income limit for a benefit program.

    Args:
        household_size: Number of people in household.
        program: Program name (SNAP, MEDICAID, TANF, WIC, CHIP).
        state: State for FPL base.

    Returns:
        Annual income limit in dollars.
    """
    fpl = get_fpl(household_size, state)
    program_upper = program.upper()

    if program_upper == "SNAP":
        return int(fpl * SNAP_GROSS)
    if program_upper in ("MEDICAID", "MEDICAID_EXPANSION"):
        return int(fpl * MEDICAID_EXPANSION)
    if program_upper == "MEDICAID_TRADITIONAL":
        return int(fpl * MEDICAID_TRADITIONAL)
    if program_upper == "TANF":
        return int(fpl * TANF)
    if program_upper == "WIC":
        return int(fpl * WIC)
    if program_upper == "CHIP":
        return int(fpl * CHIP)

    raise ValueError(f"Unknown program: {program}")


def is_income_eligible(
    annual_income: float,
    household_size: int,
    program: str,
    state: State = State.CONTIGUOUS,
) -> bool:
    """
    Check if income is within program limit.

    Returns:
        True if annual_income <= program limit.
    """
    limit = get_income_limit(household_size, program, state)
    return annual_income <= limit
