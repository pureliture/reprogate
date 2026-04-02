## Context

Phase 04에서 planner/executor/verifier 에이전트가 정의됐고, `docs/spec/agent-contract.md`에 CONTEXT→PLAN→EXECUTION-LOG→VERIFICATION 핸드오프 스키마가 확립됐다. `.claude/agents/` 파일들은 이제 레포에 tracked된다 (ADR-017).

Phase 05는 이 에이전트들을 실제로 구동하는 진입점을 만든다. 개발자는 `/rg:discuss`, `/rg:plan`, `/rg:execute`, `/rg:verify`를 통해 GSD 플로우를 ReproGate 위에서 실행할 수 있다.

제약:
- `.claude/commands/` 경로는 현재 gitignored — 커맨드 파일은 로컬 전용 (ADR-017: `agents/`만 예외 처리됨)
- 에이전트 호출은 프롬프트-임베딩 방식 (ADR-018)
- `.rg/` artifact packet 디렉토리의 tracked 여부를 결정해야 함
- Phase 06을 위해 artifact packet 구조가 일관성 있어야 함

## Goals / Non-Goals

**Goals:**
- 4개 `/rg:*` 커맨드 정의 (discuss, plan, execute, verify)
- phase artifact packet 디렉토리 구조 및 컨벤션 정의
- 각 커맨드가 spec/agent-contract.md의 schema를 따르는 것 보장
- 커맨드가 에이전트 파일을 읽어 컨텍스트에 임베딩하는 패턴 확립

**Non-Goals:**
- 커맨드 자동 체이닝 (discuss → plan → execute → verify 자동 파이프라인) — Phase 06 또는 v2
- CI/CD 통합 — v2
- 멀티 팀원 협업 — v2

## Decisions

### Decision 1: Phase artifact directory — `.rg/<phase-name>/`

```
.rg/
  <phase-name>/
    CONTEXT.md
    PLAN.md
    EXECUTION-LOG.md
    VERIFICATION.md
```

**근거**: `.planning/` 경로는 GSD가 사용 중이므로 충돌 방지. `.rg/`는 ReproGate 전용 prefix로 명확하다. 각 phase는 독립적인 하위 디렉토리를 갖는다.

**Tracked 여부**: `.rg/` 디렉토리는 gitignored. artifact packet은 세션 내 작업 상태이며, 완료 후 summary가 `records/`에 보관된다 (Phase 06). 중간 작업 상태를 레포에 커밋하면 노이즈가 많아진다.

### Decision 2: 에이전트 호출 방식 — 프롬프트 임베딩

각 커맨드 파일이 해당 에이전트 파일을 명시적으로 읽고 그 내용을 컨텍스트에 포함시킨다.

```markdown
<!-- In /rg:plan -->
Read `.claude/agents/planner.md` to understand the planner agent's role and constraints.
Then act as the planner agent: read CONTEXT.md at `.rg/$ARGUMENTS/CONTEXT.md` and produce PLAN.md.
```

**근거**: ADR-018 결정. 네이티브 `agent_type` 호출보다 버전 호환성이 높다.

### Decision 3: `/rg:discuss` 는 에이전트 없이 커맨드 자체가 진행

planner/executor/verifier와 달리, `discuss`는 개발자와의 대화를 통해 CONTEXT.md를 작성하는 단계다. 별도 에이전트가 필요하지 않다 — 커맨드 파일이 직접 질문하고 CONTEXT.md를 생성한다.

**근거**: discuss는 요구사항 수집 단계이므로 LLM이 직접 응답하는 것이 자연스럽다. 에이전트 파일로 분리하면 오히려 과도한 추상화다.

### Decision 4: `$ARGUMENTS` — phase 이름 파라미터

모든 `/rg:*` 커맨드는 `$ARGUMENTS`로 phase 이름을 받는다.

```
/rg:plan my-feature
→ reads .rg/my-feature/CONTEXT.md
→ writes .rg/my-feature/PLAN.md
```

이름이 없으면 커맨드가 현재 활성 phase를 감지하거나 목록을 보여준다.

## Risks / Trade-offs

- **[Risk] .claude/commands/ gitignored 해결됨** → ADR-017 개정: `/rg:*` 커맨드 파일은 레포에 tracked. `learn-eval.md` 등 개인 커맨드는 계속 gitignored.
- **[Risk] .rg/ conflict with GSD .planning/** → GSD 상태와 ReproGate artifact가 다른 디렉토리에 있어 혼란 가능. Mitigation: README에 경로 컨벤션 명시.
- **[Trade-off] 커맨드 자동 체이닝 없음** → 개발자가 4개 커맨드를 순서대로 수동 실행해야 함. 명확성 > 자동화, Phase 05에서는 수동 흐름이 더 안전하다.

## Open Questions

모든 결정 완료. ADR-017, ADR-018에서 주요 설계 제약 확립됨.
