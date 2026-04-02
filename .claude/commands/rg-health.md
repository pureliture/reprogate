# /rg:health — Check ReproGate harness component health

You are running the **health** check for the ReproGate delivery harness.

This command is **read-only**: it inspects file existence and structure. It does NOT modify any files, run tests, or execute code.

⚠️ Note: This check is file-existence based. Presence of a file does not guarantee its behavior is correct — use `/rg:verify` for behavioral verification of a specific phase.

## Setup

If `$ARGUMENTS` is non-empty, treat it as an optional phase name to also check `.rg/$ARGUMENTS/` artifact status (if the directory exists). Otherwise skip the phase-specific section.

## Checks to Perform

Run all checks below and collect results. Show the full dashboard at the end.

### 1. Git Hooks

Check these files exist and are executable:

| File | Expected |
|------|----------|
| `.githooks/pre-commit` | exists + executable |

```bash
test -x .githooks/pre-commit && echo "ok" || echo "missing or not executable"
```

### 2. Skills (Gate Rules)

Check these directories and key files exist:

| Path | Expected |
|------|----------|
| `skills/record-required/rules.rego` | exists |
| `skills/decision-documented/rules.rego` | exists |
| `skills/scope-defined/rules.rego` | exists |
| `skills/verification-present/rules.rego` | exists |

### 3. Specialist Agents

Check these files exist:

| File | Expected |
|------|----------|
| `.claude/agents/planner.md` | exists |
| `.claude/agents/executor.md` | exists |
| `.claude/agents/verifier.md` | exists |

### 4. Phase Workflow Commands

Check these files exist:

| File | Expected |
|------|----------|
| `.claude/commands/rg-discuss.md` | exists |
| `.claude/commands/rg-plan.md` | exists |
| `.claude/commands/rg-execute.md` | exists |
| `.claude/commands/rg-verify.md` | exists |
| `.claude/commands/rg-summary.md` | exists |
| `.claude/commands/rg-health.md` | exists |

### 5. Spec Documents

Check these spec files exist:

| File | Expected |
|------|----------|
| `docs/spec/agent-contract.md` | exists |
| `docs/spec/phase-summary-schema.md` | exists |

### 6. Summary Records

Count existing summaries:
```bash
ls records/summaries/*.md 2>/dev/null | grep -v .gitkeep | wc -l
```

Report: "N phase summaries on record"

### 7. Phase-Specific Check (Optional)

Only if `$ARGUMENTS` was provided and `.rg/$ARGUMENTS/` exists:

| Artifact | Path |
|----------|------|
| CONTEXT.md | `.rg/$ARGUMENTS/CONTEXT.md` |
| PLAN.md | `.rg/$ARGUMENTS/PLAN.md` |
| EXECUTION-LOG.md | `.rg/$ARGUMENTS/EXECUTION-LOG.md` |
| VERIFICATION.md | `.rg/$ARGUMENTS/VERIFICATION.md` |

Show which exist (✅) and which are missing (⬜).

## Dashboard Output

Present results in this format:

```
## ReproGate Harness Health

### Git Hooks
✅ .githooks/pre-commit — executable

### Skills
✅ record-required
✅ decision-documented
✅ scope-defined
✅ verification-present

### Specialist Agents
✅ planner.md
✅ executor.md
✅ verifier.md

### Phase Workflow Commands
✅ rg-discuss.md
✅ rg-plan.md
✅ rg-execute.md
✅ rg-verify.md
✅ rg-summary.md
✅ rg-health.md

### Spec Documents
✅ docs/spec/agent-contract.md
✅ docs/spec/phase-summary-schema.md

### Summary Records
📄 N phase summaries on record
   → records/summaries/

---
Overall: N/M components healthy
```

Use ✅ for present/ok, ❌ for missing/broken, ⬜ for optional/not started.

If any required component is ❌:
```
⚠️ Issues found:
- <component>: <what's wrong and suggested fix>
```

If all required components are ✅:
```
✅ All harness components healthy.
```
