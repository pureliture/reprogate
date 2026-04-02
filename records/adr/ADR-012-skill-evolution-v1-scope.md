---
record_id: "ADR-012"
title: "Skill evolution v1 scope: prose instinct only, .rego manual"
type: "adr"
status: "Draft"
created_at: "2026-04-02"
tags: ["skills", "evolution", "opa", "rego", "scope"]
---

# ADR-012: Skill evolution v1 scope: prose instinct only, .rego manual

## Status
Draft

## Context
ECC의 skill evolution 파이프라인은 4단계로 구성된다: session observation → instinct YAML → `/evolve` 클러스터링 → `/learn-eval` 품질 게이트. 이 파이프라인의 출력은 `~/.claude/homunculus/evolved/skills/*.md` — **산문형(prose) skill**이다.

ReproGate의 gate layer는 OPA `.rego` 파일을 요구한다. 현재 evolved instinct에서 `.rego` 정책으로 자동 변환하는 경로가 없다(HARNESS-ARCHITECTURE.md Q4, ECC-CORE.md).

## Decision

**v1 범위**: skill evolution 파이프라인은 prose instinct까지만 자동화한다.

- `Stop` hook → session observation → instinct YAML 초안 (자동)
- `/learn-eval` 품질 게이트 통과 시 prose skill 저장 (반자동)
- `.rego` 정책은 개발자가 **수동으로 작성**한다 — evolved instinct를 참고 자료로 활용

**v2 갭 (defer)**: `reprogate evolve-to-rego` 커맨드를 통해 prose instinct에서 `.rego` 초안을 자동 생성하는 기능은 v2에서 다룬다.

**근거**: v1에서 `.rego` 자동 생성을 시도하면 잘못된 정책이 gate에 들어갈 위험이 높다. 수동 작성은 번거롭지만 정책의 정확성을 보장한다. 실제 사용 패턴이 쌓인 이후 자동화가 가능하다.

## Consequences
- Positive: gate layer의 정책 품질이 보장된다.
- Positive: v1 구현 범위가 명확히 제한된다.
- Neutral: 새 skill 추가 시 개발자가 `.rego` 직접 작성해야 함 — 기존 Phase 1 방식과 동일.
- Negative: evolved instinct → gate 반영까지 수동 단계가 존재해 자동화 루프가 완전히 닫히지 않는다.

## Verification
- [x] `/learn-eval` 커맨드 구현 시 prose skill 저장 위치가 명시됨 — `.claude/commands/learn-eval.md` Step 5: `~/.claude/homunculus/evolved/skills/<name>.md`.
- [x] `SKILL-EVO-01` 요구사항에 "prose instinct까지" 범위가 문서화됨 — `session_stop.py` docstring 및 `specs/session-observation-capture/spec.md` 참조.
- [x] v2 backlog에 `reprogate evolve-to-rego` 항목이 등록됨 — `records/backlog/BACKLOG-001-evolve-to-rego.md`.
