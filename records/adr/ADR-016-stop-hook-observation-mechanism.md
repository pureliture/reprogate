---
record_id: "ADR-016"
title: "Stop hook observation mechanism: template-only at capture, LLM-assisted at review"
type: "adr"
status: "Accepted"
created_at: "2026-04-02"
tags: ["hooks", "skill-evolution", "llm", "stop-hook", "observation", "learn-eval"]
---

# ADR-016: Stop hook observation mechanism: template-only at capture, LLM-assisted at review

## Status
Accepted

## Context
`skill-evolution-pipeline` change 설계 중 다음 Open Question이 제기되었다:

> "Stop hook에서 LLM call이 Claude Code API를 직접 호출할 수 있는가, 아니면 별도 subprocess가 필요한가?"

`session_stop.py` 구현을 확인한 결과, 현재 Stop hook은 LLM을 호출하지 않고 `instincts: []`인 빈 observation YAML template을 생성한다. 즉, LLM 분석 없이 구조만 초기화한다.

두 가지 아키텍처 선택지를 검토했다:

**Option A (현재 구현)**: Stop hook → raw template YAML 생성 (LLM 없음) → `/learn-eval` 실행 시 LLM이 session 데이터를 분석하여 instincts 추출

**Option B**: Stop hook에서 직접 LLM subprocess를 호출하여 instinct YAML 초안을 즉시 생성

## Decision

**Option A를 공식 채택한다.** Stop hook은 LLM을 호출하지 않으며, 구조화된 observation template만 생성한다. LLM-assisted instinct 추출은 개발자가 명시적으로 `/rg:learn-eval`을 실행하는 시점에 수행된다.

- Stop hook: `session_id`, `captured_at`, `profile`, `tool_calls_count`, `instincts: []` 포함 YAML 저장
- `/rg:learn-eval`: session summary + observation YAML을 읽어 LLM이 `instincts` 배열을 채운 후 품질 게이트 진행

## Consequences

- Positive: Stop hook이 외부 프로세스나 네트워크 없이 즉시 실행된다 — 세션 종료 지연 없음.
- Positive: LLM 호출 실패가 세션 종료를 차단하지 않는다.
- Positive: 개발자가 언제 리뷰할지 시점을 선택할 수 있다.
- Neutral: instinct 추출이 세션 직후 자동으로 이루어지지 않는다 — `/rg:learn-eval`을 실행해야 함.
- Negative: 시간이 지나면 세션 컨텍스트가 희미해질 수 있다. Mitigation: Stop hook이 미리뷰 observation 수 알림 출력.

## Verification
- [x] `session_stop.py`가 `instincts: []`인 template YAML을 생성함 (구현 확인됨).
- [ ] `/rg:learn-eval` 커맨드가 observation YAML을 읽어 LLM으로 instincts를 채우는 플로우를 구현함.
- [ ] `skill-evolution-pipeline` proposal의 Open Question이 이 ADR 참조로 해소됨.
