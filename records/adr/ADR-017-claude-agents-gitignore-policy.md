---
record_id: "ADR-017"
title: "Claude agents gitignore policy: track agent definitions in repository"
type: "adr"
status: "Accepted"
created_at: "2026-04-02"
tags: ["gitignore", "agents", "claude-code", "specialist-agents", "delivery-harness"]
---

# ADR-017: Claude agents gitignore policy: track agent definitions in repository

## Status
Accepted

## Context
`specialist-agents` change 설계 중 다음 리스크가 확인되었다:

> "`.claude/agents/` 경로는 현재 gitignored — 에이전트 정의는 로컬 전용."

현재 `.gitignore`에는 `.claude/` 전체가 포함되어 있다. Phase 03 `learn-eval.md` 커맨드는 개인 로컬 전용 도구이므로 gitignore가 적절했다. 그러나 Phase 04의 `planner.md`, `executor.md`, `verifier.md`는 상황이 다르다:

- Phase 05 (Phase Workflow)의 `/rg:plan`, `/rg:execute`, `/rg:verify` 커맨드가 이 파일들에 의존한다
- 에이전트 파일이 로컬 전용이면 팀 전파가 불가능하다
- ReproGate harness의 핵심 전달물(specialist agents)이 레포에 없으면 "artifact-driven" 원칙이 무너진다

두 가지 옵션을 검토했다:

**Option A**: `.claude/agents/` 예외 처리 (`.gitignore`에서 `!.claude/agents/` 추가)

**Option B**: `.claude/agents/` 유지 gitignore, 에이전트를 다른 tracked 경로에 배치 (e.g., `agents/` 또는 `docs/agents/`)

## Decision

**Option A를 채택한다.** `.gitignore`에서 `.claude/agents/` 경로를 예외 처리하여 에이전트 정의 파일을 레포에 추적한다.

```gitignore
.claude/
!.claude/agents/
!.claude/agents/**
```

`learn-eval.md`와 같은 개인 커맨드(`commands/`)는 계속 gitignored 상태로 유지한다.

## Consequences

- `.claude/agents/planner.md`, `executor.md`, `verifier.md` — 레포에 커밋됨, 팀 전파 가능
- `.claude/commands/learn-eval.md` — 계속 gitignored (개인 학습 도구)
- `.claude/settings.json`, 기타 `.claude/` 파일 — 계속 gitignored

## Rationale

ReproGate의 핵심 원칙은 "기록 가능한 것은 기록해야 한다"이다. specialist agents는 delivery pipeline의 필수 컴포넌트이므로 레포에 추적해야 한다. 반면 `/rg:learn-eval` 커맨드는 개발자 개인의 성장 도구이며, 팀마다 다를 수 있으므로 로컬 전용이 적합하다.
