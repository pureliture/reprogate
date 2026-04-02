## Why

ReproGate v1.0의 Skill Evolution 파이프라인이 아직 구현되지 않았다. Hook Lifecycle(Phase 02)이 완료되어 session observation을 캡처할 수 있는 기반이 생겼지만, 그 observation을 instinct YAML로 정제하고 prose skill로 승격시키는 자동화 경로가 없다. 현재 개발자는 세션에서 발생한 패턴을 수동으로 skill화해야 하며, 이는 ADR-009에서 약속한 "작업 패턴의 자산화"가 실현되지 않은 상태다.

## What Changes

- `Stop` hook에서 session observation을 캡처하여 `~/.claude/homunculus/instincts/` 에 YAML 초안으로 저장하는 로직 추가
- `/learn-eval` 슬래시 커맨드 구현: instinct YAML의 품질 게이트 평가 및 prose skill 저장
- `instinct-observation` 스키마 정의: session에서 추출된 패턴을 구조화된 YAML로 표현
- `prose-skill` 저장 경로 및 명명 규칙 확립 (`~/.claude/homunculus/evolved/skills/*.md`)
- ADR-012 범위 준수: prose instinct까지만 자동화, `.rego` 정책은 수동 작성 유지

## Capabilities

### New Capabilities

- `session-observation-capture`: Stop hook 트리거 시 structured observation template YAML을 자동 생성하는 능력 (LLM 없음, ADR-016)
- `instinct-quality-gate`: `/learn-eval` 커맨드로 instinct YAML의 완성도·중복·강제성을 LLM과 함께 평가하고, 통과 시 표준화된 prose skill Markdown으로 저장·조회하는 능력

### Modified Capabilities

<!-- 기존 spec-level 요구사항 변경 없음 -->

## Impact

- `scripts/reprogate_hook_stop.py` (또는 신규 파일): Stop hook observation 캡처 로직
- `.claude/commands/learn-eval.md`: 신규 슬래시 커맨드 정의
- `~/.claude/homunculus/instincts/` 디렉토리 구조 (user-level, Git 외부)
- `~/.claude/homunculus/evolved/skills/` 디렉토리 구조 (user-level, Git 외부)
- `ADR-012` 검증 항목: SKILL-EVO-01 요구사항 문서화, v2 backlog 등록
