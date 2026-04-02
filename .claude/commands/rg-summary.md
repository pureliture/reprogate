# /rg:summary — Promote phase artifacts to a tracked summary record

You are running the **summary** step of the ReproGate phase workflow.

## Setup

The phase name is: `$ARGUMENTS`

If `$ARGUMENTS` is empty, show existing phases:
```bash
ls .rg/ 2>/dev/null
```
Then ask: "Which phase do you want to summarize? (Usage: /rg:summary <phase-name>)"

## Prerequisite Check

Check if `.rg/$ARGUMENTS/VERIFICATION.md` exists.

If it does NOT exist:
> "❌ VERIFICATION.md not found for phase `$ARGUMENTS`.
> Run `/rg:verify $ARGUMENTS` first — a summary requires a completed verification."

Stop if VERIFICATION.md is missing.

## Read Phase Artifacts

Read all three phase artifact files:

1. `.rg/$ARGUMENTS/CONTEXT.md` — extract `## Goal`
2. `.rg/$ARGUMENTS/EXECUTION-LOG.md` — extract `## Deviations` table
3. `.rg/$ARGUMENTS/VERIFICATION.md` — extract `## Result` (PASS or FAIL) and `## Summary`

## Determine Output Path

Today's date in YYYY-MM-DD format → use `date +%Y-%m-%d`.

Output file: `records/summaries/<today>-$ARGUMENTS.md`

If that file already exists, ask:
> "records/summaries/<today>-$ARGUMENTS.md already exists. Overwrite? (yes/no)"
Stop if user says no.

## Write the Summary

Create `records/summaries/<today>-$ARGUMENTS.md` following `docs/spec/phase-summary-schema.md` exactly:

```markdown
# Phase Summary: <phase-name>

**Date:** YYYY-MM-DD
**Result:** PASS ✅ | FAIL ❌

## Goal
<Contents of CONTEXT.md ## Goal — verbatim or lightly edited for clarity>

## Outcome
<Contents of VERIFICATION.md ## Summary — what was verified as complete>

## Key Decisions
<Notable decisions or deviations from EXECUTION-LOG.md ## Deviations.
If none: "No notable decisions — implementation followed plan.">

## Deviations
<From EXECUTION-LOG.md ## Deviations table.
If none: "None.">
```

Do NOT include `## Next Steps` unless there is something specific and concrete to document.

## Completion

After writing the summary, show:

```
✓ Phase summary created for $ARGUMENTS

Result: PASS ✅  (or FAIL ❌)
Record:  records/summaries/<today>-$ARGUMENTS.md

The .rg/$ARGUMENTS/ artifacts remain session-local (gitignored).
```

If Result was FAIL:
```
⚠️  Phase ended with FAIL — summary recorded for audit trail.
Review the Outcome section for what was incomplete.
```
