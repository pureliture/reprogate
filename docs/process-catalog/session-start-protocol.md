# Session Start Protocol

> Status: Active
> Purpose: required startup routine for AI-assisted sessions

## Purpose

Define the minimum startup sequence that restores context, prevents goal drift, and identifies the correct packet or work item before execution begins.

## Required Reading Order

1. `docs/constitution.md`
2. `docs/operating-model.md`
3. `docs/process-catalog/README.md`
4. the active project plan, control board, or work-packet index provided by the adapter
5. the active work packet or task specification, when one exists

## Mandatory G0 Check

Before doing implementation work, perform a goal-alignment check.

### Goal Check

| # | Check |
|---|---|
| 1 | Which North Star goal does this work support? |
| 2 | What is the current phase or program position? |
| 3 | Is the active task drifting from its higher-level goal? |
| 4 | Are there missing tracks, packets, or prerequisites? |
| 5 | Is unplanned work being performed implicitly? |

### Active Task Check

| # | Check |
|---|---|
| 6 | Does the active work packet or task record exist? |
| 7 | What are its current `status` and `current_process`? |
| 8 | Is execution about to begin without a durable tracking artifact? |

## Output Template

```markdown
## G0 Goal Alignment Result

### Goal Check
| Item | Result |
|---|---|
| 1. North Star | [goal id or "needs confirmation"] |
| 2. Phase / position | [current phase or plan location] |
| 3. Goal drift | ✅ none / ⚠️ suspected |
| 4. Missing prerequisites | ✅ none / ⚠️ list |
| 5. Unplanned work | ✅ none / ⚠️ description |

### Active Task Check
| Item | Result |
|---|---|
| 6. Tracking artifact exists | ✅ yes / ❌ no |
| 7. Current status | status: [x], current_process: [y] |
| 8. Safe to proceed | ✅ yes / ❌ no |

**G0 Result**: [clear / needs confirmation / stop]
```

## Decision After G0

| Result | Next Action |
|---|---|
| Clear | move to process selection |
| Needs confirmation | ask for clarification |
| Stop | do not begin execution |

## Related Documents

- [Goal Alignment](./G0-goal-alignment.md)
- [Process Selection Guide](./process-selection-guide.md)
