---
record_id: "BACKLOG-001"
title: "reprogate evolve-to-rego: prose instinct에서 .rego 정책 초안 자동 생성"
type: "backlog"
status: "deferred"
target_milestone: "v2"
deferred_from: "ADR-012"
created_at: "2026-04-02"
tags: ["skill-evolution", "rego", "automation", "v2"]
---

# BACKLOG-001: reprogate evolve-to-rego

## Summary

`/rg:learn-eval`을 통해 생성된 prose skill Markdown에서 OPA `.rego` 정책 초안을 자동으로 생성하는 `reprogate evolve-to-rego` 커맨드.

## Why Deferred (ADR-012)

v1에서 `.rego` 자동 생성을 시도하면 잘못된 정책이 gate layer에 들어갈 위험이 높다. 실제 사용 패턴이 쌓인 이후 자동화가 가능하다.

v1은 prose instinct까지만 자동화하고, `.rego` 작성은 개발자가 수동으로 수행한다.

## Proposed Scope (v2)

- 입력: `~/.claude/homunculus/evolved/skills/<name>.md` (prose skill)
- 출력: `skills/<name>/rules.rego` (초안 — 개발자 검토 필요)
- 커맨드: `reprogate evolve-to-rego <skill-name>` 또는 `/rg:evolve-to-rego`
- 생성된 `.rego`는 초안으로 표시되어 개발자가 리뷰 후 활성화

## Prerequisites

- v1 Skill Evolution 파이프라인 안정화 (SKILL-EVO-01 완료)
- 충분한 prose skill 샘플 축적 (LLM이 패턴을 학습할 수 있을 만큼)
- `.rego` 초안 검증 도구 또는 dry-run 모드

## Trigger Condition

v1 사용 중 반복적인 `.rego` 수동 작성 부담이 확인되고, prose skill 품질이 충분히 안정화된 시점.
