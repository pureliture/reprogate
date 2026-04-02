## Context

Phase 05 완료로 `/rg:*` 워크플로우가 CONTEXT.md → PLAN.md → EXECUTION-LOG.md → VERIFICATION.md를 생성한다. 이 artifact들은 `.rg/`에 gitignored 상태로 저장된다.

Phase 06은 이 artifact들의 "후처리"를 담당한다:
1. `/rg:summary`: phase 완료 후 결과물을 레포에 기록 가능한 형태로 변환
2. `/rg:health`: 하네스 전체 상태를 현재 시점에서 점검

제약:
- `.rg/` artifact는 gitignored — summary가 `records/summaries/`로 "승격"되어야 영속됨
- `/rg:health`는 레포 파일을 읽는 것만 해야 함 (부작용 없이)
- 두 커맨드 파일은 ADR-017 정책에 따라 tracked (`.claude/commands/.gitignore` 예외 추가)
- `records/summaries/`는 레포에 커밋 — Phase 06 이후의 팀 공유와 Phase 05의 `.rg/` gitignore 정책과의 연속성

## Goals / Non-Goals

**Goals:**
- `/rg:summary` — phase artifact packet을 `records/summaries/` tracked summary로 변환
- `/rg:health` — 하네스 컴포넌트 상태 점검 커맨드 (읽기 전용)
- `records/summaries/` 스키마 및 컨벤션 정의
- 두 커맨드의 `.claude/commands/.gitignore` 예외 처리

**Non-Goals:**
- 자동 summary 생성 (phase 완료 시 자동 실행) — v2
- Terminal HUD / 실시간 상태 표시 — v2 (roadmap에 명시)
- 원격 summary 공유 / MCP export — v2

## Decisions

### Decision 1: Phase summary — `records/summaries/<YYYY-MM-DD>-<phase>.md` (tracked)

`.rg/` artifact는 세션 내 작업 상태이고, `records/summaries/`는 완료된 작업의 영속 기록이다.

```
records/
  summaries/
    2026-04-02-my-feature.md
    2026-04-15-add-auth.md
```

**근거**: `records/` 하위에 두면 기존 gatekeeper skill이 인식하고 records 규칙이 적용된다. 날짜 prefix로 연대순 정렬이 가능하다. 팀 공유 시 `git log records/summaries/`로 phase 이력 추적 가능.

**Tracked 여부**: tracked (gitignore 아님). phase summary는 작업 결과의 공식 기록이다.

### Decision 2: `/rg:summary` — VERIFICATION.md가 필수 전제조건

summary는 VERIFICATION.md (PASS/FAIL 판정)가 있어야 작성 가능하다. VERIFICATION.md가 없으면 커맨드가 중단하고 `/rg:verify`를 실행하도록 안내한다.

**근거**: 검증되지 않은 phase의 summary를 기록에 남기는 것은 ReproGate의 "verifiable work" 원칙에 위배된다.

### Decision 3: `/rg:health` — 레포 파일 기반 정적 분석

`/rg:health`는 다음을 확인한다:
- Hook 파일 존재 여부 (`scripts/hooks/*.py`)
- Skills 수 (`skills/` 디렉토리)
- 최근 gate failures (`records/gate-failures/` 파일 수)
- 최근 observations (`~/.claude/homunculus/instincts/` 파일 수 — 존재하면)
- ADR 수 / 최근 ADR
- 커맨드 파일 존재 여부 (4개 `/rg:*` + 2개 Phase 06)

**근거**: 별도 상태 추적 없이 레포 구조만으로 하네스 상태를 파악한다. 이는 "파일이 기록이다" 원칙과 일치한다.

### Decision 4: Phase summary 스키마

```markdown
# Phase Summary: <phase-name>

**Date:** YYYY-MM-DD
**Result:** PASS ✅ | FAIL ❌

## Goal
<from CONTEXT.md>

## Outcome
<what was actually achieved — from VERIFICATION.md>

## Key Decisions
<notable decisions made during execution — from EXECUTION-LOG.md deviations>

## Deviations
<summary of deviations — from EXECUTION-LOG.md>

## Next Steps
<what follows — optional>
```

## Risks / Trade-offs

- **[Trade-off] records/summaries/ tracked** → phase마다 commit이 추가됨. 노이즈가 될 수 있으나, 이는 "기록 가능한 것은 기록한다" 원칙의 의도된 결과다.
- **[Risk] /rg:health false confidence** → 파일 존재만 확인하므로 파일이 있어도 broken일 수 있음. Mitigation: health 리포트에 "파일 존재 확인 (동작 보장 아님)" 명시.

## Open Questions

모든 결정 완료.
