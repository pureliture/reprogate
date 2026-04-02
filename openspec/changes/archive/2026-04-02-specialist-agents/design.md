## Context

Phase 03 완료로 ECC 코어(hook lifecycle, skill evolution)가 갖춰졌다. GSD 플로우의 핵심인 `plan → execute → verify` 사이클을 실행하려면 각 단계를 전담하는 전문 에이전트가 필요하다. 현재 이 에이전트들이 없어 `/rg:*` 커맨드(Phase 05)를 구현할 수 없다.

Claude Code는 sub-agent 호출 (`Task tool` 또는 `!` 커맨드)을 지원한다. Specialist agents는 이 메커니즘을 통해 orchestrator(Phase Workflow 커맨드)에게 위임받아 실행된다.

제약:
- `.claude/agents/` 경로는 현재 gitignored — 에이전트 정의는 로컬 전용 (`.claude/` gitignore 정책)
- `docs/spec/agent-contract.md`는 tracked — 공식 계약 문서는 레포에 커밋
- 에이전트는 **stateless input/output contract**를 따라야 함 — 세션 상태에 의존하면 안 됨
- 각 에이전트는 단일 책임 원칙을 따름: planner는 계획만, executor는 실행만, verifier는 검증만

## Goals / Non-Goals

**Goals:**
- planner, executor, verifier 에이전트의 역할과 artifact contract 정의
- 세 에이전트 간 핸드오프 프로토콜 명세
- `docs/spec/agent-contract.md`에 공식 스키마 문서화
- `.claude/agents/` 에이전트 파일 생성 (로컬 전용)

**Non-Goals:**
- `/rg:plan`, `/rg:execute`, `/rg:verify` 슬래시 커맨드 구현 (Phase 05)
- 에이전트 자동 오케스트레이션 / 파이프라인 자동화 (Phase 05)
- MCP 기반 외부 에이전트 통합 (v2)

## Decisions

### Decision 1: 에이전트 정의 형식 — Claude Code `.md` agent definition

**선택**: `.claude/agents/<name>.md` 파일로 에이전트를 정의. Claude Code의 native sub-agent 메커니즘 활용.

**대안 검토**:
- *Python subprocess*: 범용적이나 CC sub-agent 장점(컨텍스트 공유, tool access)을 잃음
- *별도 YAML 스키마*: 커스텀 파서 필요, CC native 지원 없음

**근거**: Claude Code가 `.claude/agents/` 파일을 natively 인식하므로 추가 런타임 없이 orchestrator가 `Task` tool로 호출 가능.

### Decision 2: Artifact Contract — 파일 기반 핸드오프

```
CONTEXT.md  →  [planner]  →  PLAN.md
PLAN.md     →  [executor] →  code changes + EXECUTION-LOG.md
EXECUTION-LOG.md + code →  [verifier] →  VERIFICATION.md
```

각 에이전트는 지정된 파일을 읽고 출력 파일을 생성한다. 세션 상태나 메모리에 의존하지 않는다.

**근거**: 파일 기반 계약은 ReproGate의 "record-first" 원칙과 일치하고, 에이전트 교체나 재실행이 가능하다.

### Decision 3: 에이전트 단일 책임

- **Planner**: CONTEXT.md + requirements → PLAN.md (태스크 분해만, 구현 없음)
- **Executor**: PLAN.md → 코드 변경 + EXECUTION-LOG.md (계획 재작성 없음)
- **Verifier**: 구현 결과물 → VERIFICATION.md (코드 수정 없음)

**근거**: 책임 분리가 없으면 각 에이전트가 이전 단계의 결정을 역행할 수 있다.

## Risks / Trade-offs

- **[Risk] .claude/ gitignored 해결됨** → ADR-017: `.claude/agents/` 예외 처리로 에이전트 파일을 레포에 추적. `.claude/commands/`는 계속 gitignored.
- **[Risk] Planner 품질 편차** → LLM이 만드는 PLAN.md의 태스크 granularity가 일관적이지 않을 수 있음. Mitigation: PLAN.md 스키마를 명세하여 verifier가 계획 품질도 평가.
- **[Trade-off] Executor의 deviation 처리** → 구현 중 계획과 다른 방향이 필요한 경우 executor가 멈춰야 하나 계속해야 하나? 결정: deviation을 EXECUTION-LOG.md에 기록하고 계속 진행 (ReproGate의 "deviation is allowed but must be recorded" 원칙, vision.md).

## Migration Plan

1. `docs/spec/agent-contract.md` 생성 (artifact contract 공식 문서)
2. `.claude/agents/planner.md`, `executor.md`, `verifier.md` 생성 (로컬 전용)
3. Phase 05 작업 시 이 에이전트 파일을 `/rg:plan`, `/rg:execute`, `/rg:verify` 커맨드에서 참조

## Open Questions

모든 Open Questions 해결됨:
- **`.claude/agents/` gitignore 정책** → ADR-017: 에이전트 파일은 레포에 tracked (`.gitignore` 예외 처리)
- **CC sub-agent 호출 메커니즘** → ADR-018: `.claude/agents/<name>.md` 경로 + 프롬프트 임베딩 방식 우선
