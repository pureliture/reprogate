## ADDED Requirements

### Requirement: /rg:verify invokes verifier agent via prompt embedding
시스템은 `/rg:verify <phase-name>` 실행 시 `.claude/agents/verifier.md`를 읽어 컨텍스트에 임베딩하고, verifier agent 역할로 CONTEXT.md + PLAN.md + EXECUTION-LOG.md + 코드를 검토하여 VERIFICATION.md를 생성해야 한다(SHALL).

#### Scenario: Developer runs /rg:verify
- **GIVEN** `.rg/my-feature/EXECUTION-LOG.md`가 존재할 때
- **WHEN** 개발자가 `/rg:verify my-feature`를 실행하면
- **THEN** verifier agent 규칙에 따라 모든 요구사항을 검토하고
- **THEN** `.rg/my-feature/VERIFICATION.md`를 PASS 또는 FAIL 판정과 함께 생성해야 한다

### Requirement: /rg:verify fails if EXECUTION-LOG.md is missing
EXECUTION-LOG.md가 없으면 `/rg:verify`는 실행을 중단하고 `/rg:execute`를 먼저 실행하도록 안내해야 한다(SHALL).

#### Scenario: Missing EXECUTION-LOG.md
- **WHEN** `.rg/my-feature/EXECUTION-LOG.md`가 없을 때 `/rg:verify my-feature`를 실행하면
- **THEN** "EXECUTION-LOG.md not found. Run /rg:execute my-feature first." 메시지를 표시해야 한다

### Requirement: /rg:verify no-code-modification guardrail is enforced
verifier agent의 "코드 수정 금지" guardrail이 커맨드에서 명시적으로 강조되어야 한다(SHALL).

#### Scenario: Verifier stays in audit mode
- **WHEN** verifier가 실행되면
- **THEN** 어떤 코드 파일도 수정하거나 생성하지 않아야 한다

### Requirement: /rg:verify summarizes result to developer
검증 완료 후 PASS/FAIL 결과와 미충족 요구사항 목록을 개발자에게 요약해서 표시해야 한다(SHALL).

#### Scenario: Verification complete
- **WHEN** VERIFICATION.md 생성이 완료되면
- **THEN** 결과 요약(PASS/FAIL, blockers 수)을 콘솔에 출력해야 한다
