## ADDED Requirements

### Requirement: Phase summary follows standard schema
`records/summaries/` 아래 생성되는 모든 phase summary는 표준 스키마를 따라야 한다(SHALL).

```markdown
# Phase Summary: <phase-name>

**Date:** YYYY-MM-DD
**Result:** PASS ✅ | FAIL ❌

## Goal
<from CONTEXT.md ## Goal>

## Outcome
<from VERIFICATION.md ## Summary>

## Key Decisions
<notable decisions from EXECUTION-LOG.md ## Deviations, if any>

## Deviations
<count and summary — N deviations, all acceptable | concerns noted>

## Next Steps
<optional — what should follow this phase>
```

#### Scenario: Summary conforms to schema
- **WHEN** `/rg:summary` 가 summary를 생성하면
- **THEN** `## Goal`, `## Outcome`, `**Result:**`, `**Date:**` 필드가 반드시 존재해야 한다

### Requirement: Phase summary filename follows date-name convention
summary 파일명은 `<YYYY-MM-DD>-<phase-name>.md` 형식이어야 한다(SHALL).

#### Scenario: Summary file naming
- **WHEN** `my-feature` phase의 summary가 2026-04-02에 생성되면
- **THEN** 파일 경로는 `records/summaries/2026-04-02-my-feature.md`이어야 한다

### Requirement: records/summaries/ directory is tracked
`records/summaries/` 디렉토리와 그 안의 파일들은 gitignored가 아닌 tracked 상태여야 한다(SHALL).

#### Scenario: Summary is committed
- **WHEN** `records/summaries/` 아래 파일이 생성되면
- **THEN** `git status`에서 `??` (untracked) 또는 `M` (modified)로 표시되어야 한다 (ignored가 아님)
