## Why

Phase 05 완료로 `discuss → plan → execute → verify` 전체 사이클이 실행 가능해졌다. 그러나 사이클 완료 후 결과물을 공유하거나 하네스 전체 상태를 파악하는 방법이 없다. 개발자는 `.rg/<phase>/VERIFICATION.md`를 수동으로 읽어야 하고, 여러 phase를 거친 후 어떤 작업이 완료됐는지 전체 그림이 없다. Phase 06은 phase 요약 생성(sharing을 위한)과 하네스 헬스 체크(운영 인식을 위한)를 추가하여 v1.0 delivery harness를 완성한다.

## What Changes

- `/rg:summary` 커맨드 신규: 완료된 phase의 VERIFICATION.md + EXECUTION-LOG.md를 읽어 사람이 읽기 좋은 phase summary를 생성하고 `records/summaries/`에 저장
- `/rg:health` 커맨드 신규: 레포의 하네스 상태(활성 hooks, skills 수, 최근 gate failures, 마지막 observations)를 점검하여 대시보드 형태로 출력
- phase summary 스키마 정의: `records/summaries/<date>-<phase>.md` 표준 구조

## Capabilities

### New Capabilities

- `rg-summary-command`: 완료된 phase의 artifact packet을 소비하여 shareable phase summary를 `records/summaries/`에 생성하는 `/rg:summary` 커맨드
- `rg-health-command`: 하네스 컴포넌트(hooks, skills, gate failures, observations)의 상태를 점검하고 요약 리포트를 출력하는 `/rg:health` 커맨드
- `phase-summary-schema`: `records/summaries/<YYYY-MM-DD>-<phase>.md` 표준 구조 정의 — goal, outcome, key decisions, deviations, next steps

### Modified Capabilities

<!-- 기존 spec-level 요구사항 변경 없음 -->

## Impact

- `.claude/commands/rg-summary.md` (신규): `/rg:summary` 슬래시 커맨드 (tracked per ADR-017)
- `.claude/commands/rg-health.md` (신규): `/rg:health` 슬래시 커맨드 (tracked per ADR-017)
- `records/summaries/` 디렉토리 신규: phase summary 저장 경로 (gitignored or tracked — 결정 필요)
- `.claude/commands/.gitignore` 업데이트: rg-summary.md, rg-health.md 예외 추가
- `docs/spec/agent-contract.md` 소비: `/rg:summary`가 phase artifact를 canonical source로 활용
