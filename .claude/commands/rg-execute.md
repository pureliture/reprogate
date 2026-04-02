# /rg:execute — Invoke executor agent to implement PLAN.md

You are running the **execute** step of the ReproGate phase workflow.

## Setup

The phase name is: `$ARGUMENTS`

If `$ARGUMENTS` is empty, show existing phases:
```bash
ls .rg/ 2>/dev/null
```
Then ask: "Which phase do you want to execute? (Usage: /rg:execute <phase-name>)"

## Prerequisite Check

Check if `.rg/$ARGUMENTS/PLAN.md` exists.

If it does NOT exist:
> "❌ PLAN.md not found for phase `$ARGUMENTS`.
> Run `/rg:plan $ARGUMENTS` first to create the execution plan."

Stop if PLAN.md is missing.

## Executor Agent Instructions

Read the file `.claude/agents/executor.md` now to understand the executor agent's role, input/output contract, and guardrails.

**You are now acting as the executor agent.** Follow all rules defined in `.claude/agents/executor.md` exactly.

Key rules (from executor.md):
- Read PLAN.md at `.rg/$ARGUMENTS/PLAN.md` fully before starting
- Execute tasks in the order defined in PLAN.md
- Write and incrementally update `.rg/$ARGUMENTS/EXECUTION-LOG.md` after each task
- **MUST NOT** rewrite or modify PLAN.md
- **MUST** record every deviation in the `Deviations` table in EXECUTION-LOG.md
- **MUST** stop and record in `Failed Tasks` on unrecoverable error

## Deviation Guardrail

Any difference from the plan MUST be recorded immediately in EXECUTION-LOG.md:

```markdown
## Deviations

| Task | Plan | Actual | Reason |
|------|------|--------|--------|
| N    | <planned approach> | <actual approach> | <why> |
```

Do NOT rewrite PLAN.md to match what you actually did. Record the deviation in EXECUTION-LOG.md instead.

## Execute

1. Read `.rg/$ARGUMENTS/PLAN.md` fully
2. Create `.rg/$ARGUMENTS/EXECUTION-LOG.md` with:
   ```markdown
   ## Status
   IN_PROGRESS
   ```
3. For each task (in order): implement → verify → record checkpoint in EXECUTION-LOG.md
4. On completion: set status section to:
   ```markdown
   ## Status
   COMPLETE
   ```
5. On unrecoverable error: set status section to:
   ```markdown
   ## Status
   FAILED
   ```
   then record in `## Failed Tasks`, stop

## Completion

Show:
```
✓ Execution complete for phase $ARGUMENTS
  Status: COMPLETE
  Tasks: <N> done, <D> deviations recorded

Next step: /rg:verify $ARGUMENTS
```
