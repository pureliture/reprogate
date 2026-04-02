## Why

Phase 04 완료로 planner/executor/verifier 에이전트가 정의됐지만, 이 에이전트들을 구동하는 진입점이 없다. 개발자는 여전히 에이전트를 직접 호출하는 방법을 모르고, `discuss → plan → execute → verify` 사이클을 ReproGate를 통해 실행할 수 없다. Phase 05는 이 사이클을 `/rg:*` 슬래시 커맨드로 구동하고, 각 단계의 artifact packet을 자동으로 생성·관리한다.

## What Changes

- `/rg:discuss` 커맨드 신규: 작업 목표를 명확화하고 CONTEXT.md artifact packet 생성
- `/rg:plan` 커맨드 신규: planner agent를 호출하여 PLAN.md 생성
- `/rg:execute` 커맨드 신규: executor agent를 호출하여 코드 변경 + EXECUTION-LOG.md 생성
- `/rg:verify` 커맨드 신규: verifier agent를 호출하여 VERIFICATION.md 생성
- phase artifact directory 관리: `.rg/<phase-name>/` 아래 CONTEXT/PLAN/EXECUTION-LOG/VERIFICATION 파일 구조

## Capabilities

### New Capabilities

- `rg-discuss-command`: 개발자와 대화하여 phase 목표·요구사항·제약을 명확화하고 CONTEXT.md를 생성하는 `/rg:discuss` 커맨드
- `rg-plan-command`: planner agent를 프롬프트-임베딩 방식으로 호출하여 CONTEXT.md → PLAN.md를 생성하는 `/rg:plan` 커맨드
- `rg-execute-command`: executor agent를 호출하여 PLAN.md를 실행하고 EXECUTION-LOG.md를 기록하는 `/rg:execute` 커맨드
- `rg-verify-command`: verifier agent를 호출하여 구현 결과를 검증하고 VERIFICATION.md를 생성하는 `/rg:verify` 커맨드
- `phase-artifact-packet`: `.rg/<phase-name>/` 디렉토리 구조 — 모든 `/rg:*` 커맨드가 공유하는 artifact 저장소

### Modified Capabilities

<!-- 기존 spec-level 요구사항 변경 없음 -->

## Impact

- `.claude/commands/rg-discuss.md` (신규): `/rg:discuss` 슬래시 커맨드 정의
- `.claude/commands/rg-plan.md` (신규): `/rg:plan` 슬래시 커맨드 정의
- `.claude/commands/rg-execute.md` (신규): `/rg:execute` 슬래시 커맨드 정의
- `.claude/commands/rg-verify.md` (신규): `/rg:verify` 슬래시 커맨드 정의
- `.rg/` 디렉토리 규칙: phase artifact packet 저장 경로 (gitignore 여부 결정 필요)
- Phase 06 (Artifact Lifecycle)의 phase summary generation이 이 artifact packet을 소비
