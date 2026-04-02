# /rg:verify — Invoke verifier agent to audit implementation

You are running the **verify** step of the ReproGate phase workflow.

## Setup

The phase name is: `$ARGUMENTS`

If `$ARGUMENTS` is empty, show existing phases:
```bash
ls .rg/ 2>/dev/null
```
Then ask: "Which phase do you want to verify? (Usage: /rg:verify <phase-name>)"

## Prerequisite Check

Check if `.rg/$ARGUMENTS/EXECUTION-LOG.md` exists.

If it does NOT exist:
> "❌ EXECUTION-LOG.md not found for phase `$ARGUMENTS`.
> Run `/rg:execute $ARGUMENTS` first to implement the plan."

Stop if EXECUTION-LOG.md is missing.

## Verifier Agent Instructions

Read the file `.claude/agents/verifier.md` now to understand the verifier agent's role, input/output contract, and guardrails.

**You are now acting as the verifier agent.** Follow all rules defined in `.claude/agents/verifier.md` exactly.

Key rules (from verifier.md):
- Read ALL input files: CONTEXT.md, PLAN.md, EXECUTION-LOG.md, and source files changed
- **MUST NOT** modify any source code files
- **MUST NOT** modify PLAN.md or EXECUTION-LOG.md
- **MUST** cover every requirement from CONTEXT.md in `Requirements Coverage`
- **MUST** review every deviation from EXECUTION-LOG.md in `Deviation Review`
- Evidence MUST reference specific files and line numbers
- Overall `Result` is FAIL if ANY requirement has ❌ FAIL status

## Execute Verification

1. Read `.rg/$ARGUMENTS/CONTEXT.md` — extract the full requirements list
2. Read `.rg/$ARGUMENTS/PLAN.md` — understand what was planned
3. Read `.rg/$ARGUMENTS/EXECUTION-LOG.md` — note deviations and any failed tasks
4. Read each source file listed in EXECUTION-LOG.md's "Files changed" sections
5. For each requirement: find evidence, mark PASS with file:line or FAIL with gap
6. For each deviation: assess Acceptable / Concern / Blocking
7. Write `.rg/$ARGUMENTS/VERIFICATION.md` following the standard structure from `docs/spec/agent-contract.md`

## Completion

After writing VERIFICATION.md, show a result summary:

```
✓ Verification complete for phase $ARGUMENTS

Result: PASS ✅  (or FAIL ❌)
Requirements: <N> checked, <P> passed, <F> failed
Deviations: <D> reviewed, <A> acceptable, <C> concerns

Report: .rg/$ARGUMENTS/VERIFICATION.md
```

If FAIL:
```
❌ Blockers:
- <requirement not met>
- <missing file or broken behavior>

Review .rg/$ARGUMENTS/VERIFICATION.md for full details.
```
