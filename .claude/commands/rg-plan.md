# /rg:plan — Invoke planner agent to create PLAN.md

You are running the **plan** step of the ReproGate phase workflow.

## Setup

The phase name is: `$ARGUMENTS`

If `$ARGUMENTS` is empty, show existing phases:
```bash
ls .rg/ 2>/dev/null
```
Then ask: "Which phase do you want to plan? (Usage: /rg:plan <phase-name>)"

## Prerequisite Check

Check if `.rg/$ARGUMENTS/CONTEXT.md` exists.

If it does NOT exist:
> "❌ CONTEXT.md not found for phase `$ARGUMENTS`.
> Run `/rg:discuss $ARGUMENTS` first to define the phase goal and requirements."

Stop if CONTEXT.md is missing.

## Planner Agent Instructions

Read the file `.claude/agents/planner.md` now to understand the planner agent's role, input/output contract, and guardrails.

**You are now acting as the planner agent.** Follow all rules defined in `.claude/agents/planner.md` exactly.

Key rules (from planner.md):
- Read CONTEXT.md at `.rg/$ARGUMENTS/CONTEXT.md`
- Read any files listed in `## References`
- Produce exactly one output: `.rg/$ARGUMENTS/PLAN.md`
- **MUST NOT** modify any source code files
- **MUST NOT** create any files other than PLAN.md
- Tasks must be numbered, atomic, and ordered
- Each task must have `What`, `Files`, and `Verification` fields

## Execute Planning

1. Read `.rg/$ARGUMENTS/CONTEXT.md` fully
2. Read any referenced specs or ADRs listed in the `## References` section
3. Break the goal into atomic, ordered tasks
4. Write `.rg/$ARGUMENTS/PLAN.md` following the standard structure from `docs/spec/agent-contract.md`

## Completion

Show:
```
✓ PLAN.md created at .rg/$ARGUMENTS/PLAN.md
  Tasks: <N> tasks planned

Next step: /rg:execute $ARGUMENTS
```
