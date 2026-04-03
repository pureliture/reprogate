---
record_id: "ADR-010"
title: "notesmd-cli adoption as document navigation layer"
type: "adr"
status: "Draft"
created_at: "2026-04-02"
tags: ["tooling", "docs", "navigation", "external-dependency"]
---

# ADR-010: notesmd-cli adoption as document navigation layer

## Status
Draft

## Context
리서치 과정에서 `notesmd-cli`가 코드베이스 및 레퍼런스 어디에도 존재하지 않아 불명확한 참조로 플래그되었다(HARNESS-ARCHITECTURE.md Q5). `reprogate` CLI가 현재 레코드 생성·검증을 담당하고 있으며, 문서 탐색과 시각화는 별도 도구가 없는 상태다.

`notesmd-cli`(https://github.com/Yakitrak/notesmd-cli)는 Obsidian-compatible 로컬 마크다운 vault를 터미널에서 탐색·검색·열람할 수 있는 Go 기반 CLI다. Obsidian 실행 없이 headless 환경에서 동작한다.

## Decision

`notesmd-cli`를 **외부 선택적 의존성**으로 채택한다. 역할은 다음과 같이 제한된다:

- `docs/`와 `records/` 디렉토리의 마크다운 문서 탐색·검색·열람
- 터미널 기반 문서 시각화 (보조 도구)

레코드 생성·검증·게이트 평가는 기존과 동일하게 `reprogate` CLI가 담당한다. `notesmd-cli`는 **읽기 전용** 탐색 도구로만 사용되며, 하네스 핵심 흐름(hook, gate, phase flow)에 개입하지 않는다.

설치는 필수가 아니며, 미설치 시 하네스 기능에 영향 없음. `reprogate.yaml`의 `optional_tools` 섹션에 등록한다.

## Consequences
- Positive: `docs/`·`records/` 탐색이 터미널에서 가능해져 문서 기반 작업 흐름이 매끄러워진다.
- Positive: Obsidian 미설치 환경에서도 동작한다.
- Neutral: 외부 의존성 추가이지만 선택적이므로 하네스 배포 요구사항에 영향 없음.
- Negative: Go 도구이므로 설치 방식이 기존 Python/Node 스택과 상이하다.

## Verification
- [ ] `reprogate.yaml`의 `optional_tools` 섹션에 `notesmd-cli` 등록.
- [ ] README 또는 설치 가이드에 선택적 도구로 문서화.
- [ ] `notesmd-cli` 미설치 환경에서 하네스 핵심 기능 동작 확인.
