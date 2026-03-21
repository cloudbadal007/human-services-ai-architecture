# No Wrong Door Pattern

## Problem

Citizens seeking benefits often hit the "wrong door" — they apply to one program but need another, or a life event (job loss, household change) affects multiple programs and they don't know to update each one.

## Solution

One life event triggers **cross-program review**. The architecture maps life event types to affected programs:

- **Job loss** → SNAP, Medicaid, TANF, Housing
- **Income change** → SNAP, Medicaid, TANF, Housing, WIC
- **Household change** → SNAP, Medicaid, TANF, WIC, Childcare
- **Child born** → SNAP, Medicaid, WIC, Childcare

## Implementation

`LifeEventType.affected_programs()` returns the list. `flag_life_event` creates review tasks for each program, all with `requires_human_review=True` (Art. 14).

## Example

```python
from human_services.mcp.eligibility_server import flag_life_event
r = flag_life_event("citizen_001", "job_loss")
# r["affected_programs"] = ["SNAP", "MEDICAID", "TANF", "HOUSING"]
# r["requires_human_review"] = True
```
