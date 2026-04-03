# /rg:discuss — Clarify phase goal and create CONTEXT.md

You are running the **discuss** step of the ReproGate phase workflow. Your job is to guide the developer through clarifying a phase goal and produce a well-formed `CONTEXT.md` artifact.

## Setup

The phase name is: `$ARGUMENTS`

If `$ARGUMENTS` is empty, ask: "What is the name of this phase? (e.g., `add-auth`, `refactor-db`)"

The artifact will be saved to: `.rg/$ARGUMENTS/CONTEXT.md`

## Prerequisite Check

Check if `.rg/$ARGUMENTS/CONTEXT.md` already exists.

If it does, ask:
> "CONTEXT.md already exists for phase `$ARGUMENTS`. Overwrite it? (yes/no)"

If the developer says no, stop and show the existing CONTEXT.md path.

## Discussion Flow

Ask the following questions in order. Wait for each answer before proceeding.

**1. Goal** (required)
> "What is the goal of this phase? Describe what you want to achieve in 1–2 sentences."

**2. Requirements** (required)
> "What are the specific requirements? List each one — what MUST the system do when this phase is complete?"
>
> _Enter requirements one per line. Press Enter twice when done._

**3. Constraints** (optional)
> "Are there any constraints or limitations? (e.g., must not break existing tests, must stay compatible with X, budget/time limits)"
>
> _Press Enter to skip._

**4. References** (optional)
> "Are there any relevant files, ADRs, or specs to reference? (e.g., `docs/spec/agent-contract.md`, `records/adr/ADR-016-*.md`)"
>
> _Press Enter to skip._

## Create CONTEXT.md

After collecting all answers, create the directory and write the file:

```
mkdir -p .rg/$ARGUMENTS
```

Write `.rg/$ARGUMENTS/CONTEXT.md` using this template:

```markdown
# Context: $ARGUMENTS

## Goal
<goal from discussion>

## Requirements
- <requirement 1>
- <requirement 2>
- ...

## Constraints
- <constraint 1> (omit section if none)

## References
- <reference 1> (omit section if none)
```

## Validation

After writing, verify:
- `## Goal` section is present and non-empty
- `## Requirements` section has at least one item

If either is missing, ask the developer to provide the missing content before writing.

## Completion

Show:
```
✓ CONTEXT.md created at .rg/$ARGUMENTS/CONTEXT.md

Next step: /rg:plan $ARGUMENTS
```
