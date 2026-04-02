## ADDED Requirements

### Requirement: Phase artifact directory follows standard layout
모든 `/rg:*` 커맨드는 `.rg/<phase-name>/` 디렉토리 아래 표준 파일 구조를 사용해야 한다(SHALL).

```
.rg/
  <phase-name>/
    CONTEXT.md        ← /rg:discuss 생성
    PLAN.md           ← /rg:plan 생성
    EXECUTION-LOG.md  ← /rg:execute 생성 및 업데이트
    VERIFICATION.md   ← /rg:verify 생성
```

#### Scenario: All commands use the same phase directory
- **GIVEN** phase 이름이 `my-feature`일 때
- **THEN** 모든 `/rg:*` 커맨드는 `.rg/my-feature/` 경로를 공유해야 한다

### Requirement: .rg/ directory is gitignored
`.rg/` 디렉토리는 `.gitignore`에 추가되어야 한다(SHALL). phase artifact packet은 세션 내 작업 상태이며 레포에 커밋하지 않는다.

#### Scenario: Phase artifacts not tracked
- **WHEN** `.rg/` 디렉토리가 생성되면
- **THEN** `git status`에서 ignored로 표시되어야 한다

### Requirement: Phase artifact packet schema matches agent-contract
CONTEXT.md, PLAN.md, EXECUTION-LOG.md, VERIFICATION.md 각각의 내용은 `docs/spec/agent-contract.md`에 정의된 스키마를 따라야 한다(SHALL).

#### Scenario: Agent reads artifact with correct schema
- **WHEN** executor agent가 PLAN.md를 읽으면
- **THEN** `## Tasks`, `## Expected Outputs` 섹션이 존재해야 한다

### Requirement: Commands handle missing phase name gracefully
phase 이름 없이 커맨드를 실행하면, 현재 `.rg/` 아래의 phase 목록을 보여주거나 이름 입력을 안내해야 한다(SHALL).

#### Scenario: /rg:plan without phase name
- **WHEN** 개발자가 `/rg:plan` (이름 없이)을 실행하면
- **THEN** `.rg/` 아래 존재하는 phase 목록 또는 "Usage: /rg:plan <phase-name>" 안내를 표시해야 한다
