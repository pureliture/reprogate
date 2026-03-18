# Skill / Workflow Object Model

Status: Draft

## Purpose

ReproGate에서 Skill과 Workflow를 어떤 객체 단위로 식별하고,
버전/복제/승격/override 관계를 어떻게 다룰지 정의한다.

## Inputs to Close
- docs/strategy/product-boundary.md
- docs/strategy/scenarios.md
- docs/spec/record-contract.md

## Decisions To Close
- Atomic Skill과 Workflow의 구분 기준
- clone / fork / override / alias / namespace 모델
- local / proposed / team-approved 상태 모델
- built-in / custom / project-local / org-level precedence

## Out of Scope
- 특정 UI 편집기 구현
- skill extraction 알고리즘 상세
