## ADDED Requirements

### Requirement: /rg:execute invokes executor agent via prompt embedding
시스템은 `/rg:execute <phase-name>` 실행 시 `.claude/agents/executor.md`를 읽어 컨텍스트에 임베딩하고, executor agent 역할로 `.rg/<phase-name>/PLAN.md`를 실행하여 코드 변경과 EXECUTION-LOG.md를 생성해야 한다(SHALL).

#### Scenario: Developer runs /rg:execute
- **GIVEN** `.rg/my-feature/PLAN.md`가 존재할 때
- **WHEN** 개발자가 `/rg:execute my-feature`를 실행하면
- **THEN** executor agent 규칙에 따라 PLAN.md의 태스크를 순서대로 실행해야 한다
- **THEN** `.rg/my-feature/EXECUTION-LOG.md`를 생성하고 각 태스크 완료 시 업데이트해야 한다

### Requirement: /rg:execute fails if PLAN.md is missing
PLAN.md가 없으면 `/rg:execute`는 실행을 중단하고 `/rg:plan`을 먼저 실행하도록 안내해야 한다(SHALL).

#### Scenario: Missing PLAN.md
- **WHEN** `.rg/my-feature/PLAN.md`가 없을 때 `/rg:execute my-feature`를 실행하면
- **THEN** "PLAN.md not found. Run /rg:plan my-feature first." 메시지를 표시해야 한다

### Requirement: /rg:execute deviation recording is enforced
executor agent의 "deviation은 반드시 EXECUTION-LOG.md에 기록" 규칙이 커맨드에서 명시적으로 강조되어야 한다(SHALL).

#### Scenario: Deviation occurs during execution
- **WHEN** executor가 PLAN.md와 다른 방식으로 구현하면
- **THEN** EXECUTION-LOG.md의 Deviations 테이블에 기록해야 한다
