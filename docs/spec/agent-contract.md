# Agent Contract: Specialist Agent Handoff Schema

This document defines the artifact-based handoff contract between ReproGate's specialist agents. All three agents (planner, executor, verifier) communicate exclusively through files — no session state, no memory dependencies.

## Handoff Pipeline

```
CONTEXT.md
    │
    ▼
[planner agent]
    │
    ▼
PLAN.md
    │
    ▼
[executor agent]
    │
    ├── code changes (in-place)
    ▼
EXECUTION-LOG.md
    │
    ▼
[verifier agent]
    │
    ▼
VERIFICATION.md
```

Each agent is **stateless**: it reads its designated input files and produces its designated output files. A phase directory (`.rg/<phase-name>/`) holds all artifacts for one unit of work.

---

## CONTEXT.md

**Produced by**: developer (or Phase Workflow command)
**Consumed by**: planner

```markdown
# Context: <phase-name>

## Goal
One-paragraph description of what this phase achieves.

## Requirements
- Requirement 1 (SHALL)
- Requirement 2 (SHALL)
- ...

## Constraints
- Constraint 1
- Constraint 2

## References
- path/to/relevant/spec.md
- records/adr/ADR-NNN-*.md
```

**Required fields**: `Goal`, `Requirements`
**Optional fields**: `Constraints`, `References`

---

## PLAN.md

**Produced by**: planner agent
**Consumed by**: executor

```markdown
# Plan: <phase-name>

## Tasks

1. **<task-title>**
   - What: <description of what to implement>
   - Files: <list of files to create/modify>
   - Verification: <how to verify this task is complete>

2. **<task-title>**
   - What: ...
   - Files: ...
   - Verification: ...

## Expected Outputs
- <file-or-artifact-1>: <description>
- <file-or-artifact-2>: <description>

## Completion Criteria
<How to determine the plan is fully executed>
```

**Required fields**: `Tasks` (numbered list, each with What/Files/Verification), `Expected Outputs`
**Constraints**: planner MUST NOT modify any code files

---

## EXECUTION-LOG.md

**Produced by**: executor agent (incrementally during execution)
**Consumed by**: verifier

```markdown
# Execution Log: <phase-name>

## Status
IN_PROGRESS | COMPLETE | FAILED

## Completed Tasks

### Task 1: <task-title>
- **Status**: DONE
- **Files changed**: path/to/file.py (+N lines), path/to/other.py (modified)
- **Notes**: <optional notes>

### Task 2: <task-title>
- **Status**: DONE | DEVIATED | FAILED
- **Files changed**: ...
- **Deviation**: <if DEVIATED — what changed from plan and why>

## Deviations

| Task | Plan | Actual | Reason |
|------|------|--------|--------|
| 2    | Create X using approach A | Used approach B | Approach A incompatible with existing Y |

## Failed Tasks

### Task N: <task-title>
- **Status**: FAILED
- **Error**: <error message or description>
- **Impact**: <what cannot proceed without this>
```

**Required fields**: `Status`, task entries with status
**Deviation rule**: ANY deviation from PLAN.md MUST be recorded in the `Deviations` table
**Failure rule**: On unrecoverable error, executor stops and records in `Failed Tasks`; does NOT attempt to rewrite PLAN.md

---

## VERIFICATION.md

**Produced by**: verifier agent
**Consumed by**: developer (and Phase Workflow)

```markdown
# Verification: <phase-name>

## Result
PASS | FAIL

## Requirements Coverage

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Requirement 1 | ✅ PASS | path/to/file.py:42 — implements X |
| Requirement 2 | ❌ FAIL | Not found in codebase |

## Deviation Review

| Deviation | Assessment | Impact |
|-----------|------------|--------|
| Task 2 used approach B | ✅ Acceptable — equivalent outcome | None |

## Summary
<2–3 sentences summarizing the overall assessment>

## Blockers (if FAIL)
- <specific requirement not met>
- <missing file or broken behavior>
```

**Required fields**: `Result` (PASS or FAIL), `Requirements Coverage`
**Constraints**: verifier MUST NOT modify any code files
**Deviation review**: ALL deviations from EXECUTION-LOG.md MUST be assessed

---

## Rules

1. **File-only communication**: agents read and write files; no session memory
2. **Stateless execution**: any agent can be re-run given the same input files
3. **Single responsibility**: planner plans, executor executes, verifier verifies — no role crossing
4. **Record deviations**: executor records any deviation; verifier reviews all deviations
5. **Guardrails**:
   - Planner: MUST NOT modify code or non-PLAN.md files
   - Executor: MUST NOT rewrite PLAN.md; MUST record all deviations
   - Verifier: MUST NOT modify code; MUST review all deviations from EXECUTION-LOG.md

---

## Phase Workflow Integration

The `/rg:*` commands drive the full cycle. Each command operates on a **phase artifact packet** stored at `.rg/<phase-name>/`.

### Directory Convention

```
.rg/                          ← gitignored (session-local working state)
  <phase-name>/
    CONTEXT.md                ← created by /rg:discuss
    PLAN.md                   ← created by /rg:plan
    EXECUTION-LOG.md          ← created and updated by /rg:execute
    VERIFICATION.md           ← created by /rg:verify
```

### Command Sequence

```
/rg:discuss <phase>   →  creates .rg/<phase>/CONTEXT.md
/rg:plan <phase>      →  reads CONTEXT.md, creates PLAN.md
/rg:execute <phase>   →  reads PLAN.md, writes code + EXECUTION-LOG.md
/rg:verify <phase>    →  reads all artifacts + code, creates VERIFICATION.md
```

Each command checks for its prerequisite artifact and refuses to run if it is missing.

### Agent Files

Commands embed their agent's rules via prompt:
- `/rg:plan` embeds `.claude/agents/planner.md`
- `/rg:execute` embeds `.claude/agents/executor.md`
- `/rg:verify` embeds `.claude/agents/verifier.md`

`/rg:discuss` has no agent file — it conducts the conversation directly.

