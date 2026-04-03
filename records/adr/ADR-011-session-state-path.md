---
record_id: "ADR-011"
title: "Session state storage path: project-local over global"
type: "adr"
status: "Draft"
created_at: "2026-04-02"
tags: ["hooks", "session", "state", "ecc", "storage"]
---

# ADR-011: Session state storage path: project-local over global

## Status
Draft

## Context
ECC(Everything-Claude-Code)는 세션 상태를 전역 경로(`~/.claude/session-data/`)에 저장한다. ReproGate는 피벗 이후 artifact-resident 모델(모든 작업 산출물이 프로젝트 로컬 Git 레포에 존재)을 채택했다(ADR-009).

ECC-CORE.md 리서치에서 이 경로 결정이 오픈 이슈로 플래그되었다: "ECC global `~/.claude/` vs project-local `.claude/` — ReproGate's artifact model suggests project-local."

## Decision

세션 상태를 **프로젝트 로컬** `.claude/session-data/` 경로에 저장한다.

- **SessionStart hook**: `.claude/session-data/current-session.json` 초기화
- **Stop hook**: `.claude/session-data/` 에 세션 요약 저장
- **PreCompact hook**: `.claude/session-data/pre-compact-state.json` 저장

`.claude/session-data/`는 `.gitignore`에 추가한다 (세션 런타임 데이터는 커밋 대상 아님). 단, 세션에서 추출된 instinct/skill 초안이 `skills/` 로 프로모션되면 그 시점부터 Git에 추적된다.

전역 ECC 세션 상태와 혼용하지 않는다.

## Consequences
- Positive: ReproGate의 artifact-resident 원칙과 일치 — 프로젝트별 맥락이 프로젝트에 귀속된다.
- Positive: 여러 ReproGate 프로젝트를 병행할 때 세션 상태가 섞이지 않는다.
- Neutral: ECC 전역 세션 데이터와 별도로 관리되므로 ECC의 크로스-레포 세션 기능은 사용할 수 없다.
- Negative: 레포마다 `.claude/` 디렉토리가 생기므로 gitignore 관리 필요.

## Verification
- [ ] `.claude/session-data/` 가 `.gitignore`에 등록됨.
- [ ] SessionStart/Stop/PreCompact hook이 해당 경로에 읽기/쓰기함.
- [ ] `reprogate init` 이 `.claude/session-data/` 디렉토리를 생성함.
