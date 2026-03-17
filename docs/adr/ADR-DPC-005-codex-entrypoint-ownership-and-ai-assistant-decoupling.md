# ADR-DPC-005: Codex Entrypoint Ownership 및 JetBrains AI Assistant Decoupling

## Status

**Accepted** (2026-03-09)

## Context

`WP-DPC-2026-03-008`에서 Codex+OMX parity를 맞추기 위해 `$ai-ops` named entrypoint와
`.codex/jetbrains-ai-assistant-rules.md` 기반 보조 규칙을 함께 강화했다.

하지만 실제 운영에서 다음 문제가 드러났다.

1. JetBrains AI Assistant 일반 경로와 Codex+OMX 경로의 소유 경계가 흐려졌다.
2. hidden local rule-pack(`.codex/jetbrains-ai-assistant-rules.md`)이 canonical 정책 경로처럼 취급됐다.
3. `$ai-ops` skill이 active WP(`WP-DPC-2026-03-008`)를 직접 참조하면서 thin adapter 원칙과 토큰 효율을 해쳤다.
4. Codex SoT에는 사용자 프로세스 선택 전 Team 금지 규칙이 Claude 쪽만큼 직접적으로 드러나지 않았다.

또한 사용자는 JetBrains AI Assistant 일반 경로에서 더 이상 `$ai-ops`를 사용하지 않겠다고 명확히 했다.

## Decision

### 1. Entrypoint Ownership을 분리한다

- Claude Code: `/ai-ops`
- Codex+OMX: `$ai-ops`
- JetBrains AI Assistant 일반 경로: `$ai-ops`를 기본 진입점으로 사용하지 않고 `AGENTS.md` + SoT를 직접 따른다.

즉, `$ai-ops`는 **Codex+OMX 전용 named entrypoint**로 유지한다.

### 2. Hidden Local Rule-pack을 Canonical Enforcement Point로 두지 않는다

- `.codex/jetbrains-ai-assistant-rules.md`는 제거 대상으로 전환한다.
- Codex/JetBrains AI Assistant 정책의 canonical 소스는 root `docs/*`와 `AGENTS.md`다.
- 이 결정은 hidden local adapter를 canonical 정책 저장소로 두지 않는다는 `ADR-DPC-004`와 일관된다.

### 3. `$ai-ops` Skill은 Thin Adapter로 유지한다

- `$ai-ops` skill은 최소 SoT와 launch gate만 참조한다.
- active WP나 대형 WP 문서를 직접 참조하지 않는다.
- 작업 대상 WP는 `work-packets/index.md`와 현재 process context를 통해 해석한다.

### 4. Codex 경로에도 “선택 전 Team 금지”를 직접 명시한다

- 사용자 프로세스 선택 전에는 `omx team ...` 또는 동등한 Team 진입을 호출하지 않는다.
- Team 가능 프로세스에서도 사용자 선택과 `team_mode` 확정 전에는 Team 경로로 넘어가지 않는다.

## Consequences

### 긍정적

- Claude와 Codex 사이의 behavior parity가 더 명확해진다.
- `$ai-ops`의 기본 토큰 비용을 줄일 수 있다.
- JetBrains AI Assistant 일반 경로와 Codex+OMX 경로의 역할이 분리된다.
- hidden local file 변경에 정책이 종속되는 문제를 줄인다.

### 부정적

- JetBrains AI Assistant 경로에서 `AGENTS.md`의 유도력에 더 의존하게 된다.
- 기존 `.codex/*` 보조 자산과 문서의 동기화 정리가 필요하다.

### 완화 조치

- `AGENTS.md`, `commands/ai-ops.md`, `process-enforcement-matrix.md`에 같은 규칙을 직접 반영한다.
- `WP-DPC-2026-03-008` P3/S1에서 실제 동작과 문서 정합성을 다시 검증한다.

## Related

- [WP-DPC-2026-03-008](../work-packets/WP-DPC-2026-03-008-codex-omx-alignment.md)
- [ADR-DPC-003](./ADR-DPC-003-conditional-team-activation-and-optout.md)
- [ADR-DPC-004](./ADR-DPC-004-ai-tool-artifact-boundary.md)
- [ai-ops command](../commands/ai-ops.md)
