## ADDED Requirements

### Requirement: /rg:discuss creates CONTEXT.md from developer conversation
시스템은 개발자와의 대화를 통해 phase 목표, 요구사항, 제약을 수집하고 `.rg/<phase-name>/CONTEXT.md`를 생성해야 한다(SHALL).

#### Scenario: Developer runs /rg:discuss for a new phase
- **GIVEN** 개발자가 `/rg:discuss my-feature`를 실행하면
- **THEN** 커맨드는 phase 목표, 요구사항, 제약, 참조 문서를 질문하고
- **THEN** `.rg/my-feature/CONTEXT.md`를 `docs/spec/agent-contract.md`의 CONTEXT.md 스키마에 따라 생성해야 한다

### Requirement: /rg:discuss validates CONTEXT.md completeness
생성된 CONTEXT.md는 `Goal`과 `Requirements` 섹션을 필수로 포함해야 한다(SHALL).

#### Scenario: CONTEXT.md missing required fields
- **WHEN** discuss 완료 후 CONTEXT.md에 Goal 또는 Requirements가 없으면
- **THEN** 커맨드는 누락된 섹션을 개발자에게 알리고 재입력을 요청해야 한다

### Requirement: /rg:discuss is idempotent for existing CONTEXT.md
이미 CONTEXT.md가 존재하면 커맨드는 덮어쓰기 전 확인을 요청해야 한다(SHALL).

#### Scenario: Developer re-runs /rg:discuss for existing phase
- **WHEN** `.rg/my-feature/CONTEXT.md`가 이미 존재할 때 `/rg:discuss my-feature`를 실행하면
- **THEN** "CONTEXT.md already exists. Overwrite?" 확인 프롬프트를 표시해야 한다
