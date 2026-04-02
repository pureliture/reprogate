## ADDED Requirements

### Requirement: Stop hook captures session observations as structured template
Stop hook이 세션 종료 시 실행될 때, 시스템은 `instincts: []`인 구조화된 observation YAML template을 `.claude/session-data/`에 저장해야 한다(SHALL). LLM-assisted instinct 추출은 Stop hook이 아니라 `/rg:learn-eval` 실행 시점에 수행된다([ADR-016](../../../../../records/adr/ADR-016-stop-hook-observation-mechanism.md)).

#### Scenario: Normal session ends with observable patterns
- **WHEN** 개발자가 Claude Code 세션을 종료하고 Stop hook이 트리거되면
- **THEN** 시스템은 세션 내 반복 패턴을 감지하여 `observations` 배열이 포함된 instinct YAML을 생성하고 `~/.claude/homunculus/instincts/` 경로에 저장해야 한다

#### Scenario: Session ends with no notable patterns
- **WHEN** 세션이 짧거나 반복 패턴이 감지되지 않으면
- **THEN** 시스템은 `observations: []`인 instinct YAML을 생성하되, 파일은 동일하게 저장해야 한다

#### Scenario: Observation capture does not block session exit
- **WHEN** Stop hook의 observation 추출 중 오류가 발생하면
- **THEN** 시스템은 오류를 로깅하되 세션 종료를 차단해서는 안 된다(SHALL NOT)

### Requirement: Instinct YAML follows defined schema
생성된 instinct YAML은 정의된 스키마(`id`, `session_id`, `captured_at`, `observations`, `confidence`, `raw_summary`)를 따라야 한다(SHALL).

#### Scenario: Schema validation on write
- **WHEN** instinct YAML이 저장될 때
- **THEN** 필수 필드(`id`, `captured_at`, `observations`)가 모두 존재해야 하며, 누락 시 파일 저장을 건너뛰고 경고를 출력해야 한다

### Requirement: User is notified of pending instincts after session
세션 종료 후 미평가 instinct가 있으면 시스템은 그 수를 사용자에게 알려야 한다(SHALL).

#### Scenario: Pending instincts exist at session end
- **WHEN** Stop hook 완료 시 `~/.claude/homunculus/instincts/`에 미평가 파일이 1개 이상이면
- **THEN** 시스템은 "N개의 미평가 instinct가 있습니다. /learn-eval로 리뷰하세요." 형식의 메시지를 출력해야 한다
