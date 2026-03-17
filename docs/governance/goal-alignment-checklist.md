# Goal Alignment Checklist

Use this checklist during `G0` or when a task shifts scope mid-session.

## 1. Goal Fit

- [ ] Does the requested work still align with `docs/strategy/final-definition.md`?
- [ ] Which top-level goal or delivery outcome does this task support?
- [ ] Does the active work packet still match the requested work?
- [ ] Is this work inside the agreed scope, or has it drifted?
- [ ] Are prerequisite packets, docs, or decisions already recorded?
- [ ] Is an explicit next process already suggested by the current packet?

## 2. Artifact Readiness

- [ ] Does the active work packet or equivalent task record exist?
- [ ] Are the required work records clear for this task type?
- [ ] Are the required framework docs available in the target repository?
- [ ] Are the required scripts or hooks available where the adapters reference them?
- [ ] Are the project record paths (`wp_path`, `adr_path`, `changelog_path`) known?

## 3. Execution Safety

- [ ] Has the user selected the process to run?
- [ ] If the process is team-capable, has `team_mode` been resolved to `team` or `single`?
- [ ] Is runtime state being treated only as support, not as the sole evidence source?
- [ ] Are the expected verification steps clear before implementation starts?

## Suggested Output Format

```markdown
## G0 Goal Alignment Result

- Goal fit: <summary>
- Canonical definition check: <aligned | drift>
- Active packet: <packet id / status / current_process>
- Scope drift: <none | details>
- Required artifacts: <ready | missing items>
- Execution gate: <ready | blocked>
```
