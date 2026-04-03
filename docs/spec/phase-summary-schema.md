# Phase Summary Schema

This document defines the standard structure for phase summaries stored in `records/summaries/`.

Phase summaries are the "promoted" form of phase artifact packets: once a phase is complete (VERIFICATION.md exists), `/rg:summary` converts the `.rg/<phase>/` artifacts into a tracked, shareable record.

## File Naming Convention

```
records/summaries/<YYYY-MM-DD>-<phase-name>.md
```

Examples:
- `records/summaries/2026-04-02-add-auth.md`
- `records/summaries/2026-04-15-refactor-db.md`

The date is the day `/rg:summary` is run (not when the phase started).

## Schema

```markdown
# Phase Summary: <phase-name>

**Date:** YYYY-MM-DD
**Result:** PASS ✅ | FAIL ❌

## Goal
<From CONTEXT.md ## Goal — what the phase set out to achieve>

## Outcome
<From VERIFICATION.md ## Summary — what was actually achieved and verified>

## Key Decisions
<Notable decisions or approaches from EXECUTION-LOG.md ## Deviations, if any.
If no deviations, write "No notable decisions — implementation followed plan.">

## Deviations
<From EXECUTION-LOG.md ## Deviations table.
Format: "N deviations recorded: <brief description>. All acceptable." or list concerns.
If no deviations: "None.">

## Next Steps
<Optional. What should follow this phase, if known. Omit if not applicable.>
```

## Required Fields

| Field | Source | Required |
|-------|--------|----------|
| `**Date:**` | Today's date | Yes |
| `**Result:**` | VERIFICATION.md `## Result` | Yes |
| `## Goal` | CONTEXT.md `## Goal` | Yes |
| `## Outcome` | VERIFICATION.md `## Summary` | Yes |
| `## Key Decisions` | EXECUTION-LOG.md `## Deviations` | Yes (write "None" if absent) |
| `## Deviations` | EXECUTION-LOG.md `## Deviations` | Yes (write "None" if absent) |
| `## Next Steps` | Author judgment | No |

## Relationship to .rg/ Artifacts

```
.rg/<phase>/CONTEXT.md       →  ## Goal
.rg/<phase>/VERIFICATION.md  →  **Result:** and ## Outcome
.rg/<phase>/EXECUTION-LOG.md →  ## Key Decisions and ## Deviations
```

Phase summaries are stored in `records/summaries/` (tracked in git).  
The source artifacts in `.rg/` remain gitignored (session-local).

## Usage

```
/rg:summary <phase-name>
```

Requires VERIFICATION.md to exist. Creates `records/summaries/<today>-<phase-name>.md`.
