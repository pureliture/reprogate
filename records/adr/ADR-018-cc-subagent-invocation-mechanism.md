---
record_id: "ADR-018"
title: "Claude Code sub-agent invocation mechanism for specialist agents"
type: "adr"
status: "Accepted"
created_at: "2026-04-02"
tags: ["claude-code", "subagent", "task-tool", "specialist-agents", "invocation"]
---

# ADR-018: Claude Code sub-agent invocation mechanism for specialist agents

## Status
Accepted

## Context
`specialist-agents` change 설계 중 다음 Open Question이 제기되었다:

> "Claude Code `Task` tool 호출 시 에이전트 파일 경로를 어떻게 지정하는가? (`.claude/agents/<name>` vs 절대 경로)"

Claude Code의 sub-agent 호출 방법을 조사한 결과:

1. **`Task` tool** (`agent_type` 파라미터): `.github/agents/<name>.md` 또는 사용자 정의 에이전트 파일을 `agent_type` 값으로 참조. 프레임워크에 따라 다름.
2. **`.claude/agents/<name>.md`**: Claude Code가 프로젝트 레벨 에이전트를 자동 인식하는 공식 경로 (CC 1.x 이상).
3. **`subagent_type: "general-purpose"`**: 커스텀 에이전트 없이 범용 실행.

ReproGate가 사용하는 GSD 프레임워크(`gsd-executor`, `gsd-planner` 등)는 `.github/agents/` 경로를 사용한다.

## Decision

**`.claude/agents/<name>.md`를 공식 에이전트 정의 경로로 채택한다.** Phase 05 커맨드 파일(`.claude/commands/`)에서 이 에이전트들을 `Task` tool의 `agent_type` 파라미터 없이, 프롬프트 임베딩 방식으로 호출한다.

호출 패턴:
```markdown
<!-- In /rg:plan command -->
Use the planner agent defined in `.claude/agents/planner.md` to create PLAN.md from the provided CONTEXT.md.
Read `.claude/agents/planner.md` first to understand the agent's role and constraints.
```

또는 CC Task tool 지원 시:
```markdown
<use_mcp_tool>
  <server_name>agent</server_name>
  <tool_name>invoke</tool_name>
  <arguments>{"agent": "planner", "context_path": "..."}</arguments>
</use_mcp_tool>
```

## Consequences

- Phase 04: `.claude/agents/` 에 에이전트 정의 파일 생성 (ADR-017에 따라 tracked)
- Phase 05: 슬래시 커맨드가 에이전트 파일을 명시적으로 읽고 프롬프트에 임베딩하는 방식으로 호출
- **LLM 임베딩 방식 우선**: `agent_type` 파라미터 기반 네이티브 호출이 안정화되기 전까지 커맨드가 에이전트 파일을 직접 읽어 컨텍스트에 포함하는 방식이 호환성이 높다

## Rationale

`.claude/agents/` 경로는 Claude Code의 공식 권장 경로이다. 네이티브 `agent_type` 호출은 프레임워크 버전에 따라 지원 여부가 다를 수 있으므로, Phase 05 구현 시 프롬프트 임베딩 방식을 기본으로 하되 네이티브 호출이 안정화되면 마이그레이션한다. 이는 ReproGate "동작하는 최소 구현 우선" 원칙과 일치한다.
