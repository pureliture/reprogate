# Storage Adapter Spec

Status: Draft

## Purpose

ReproGate가 built-in 저장 방식 외에도 external storage를 허용하면서,
canonical metadata layer를 통해 동일한 Rule/Gate 평가를 가능하게 하는 구조를 정의한다.

## Inputs to Close
- docs/strategy/product-boundary.md
- docs/strategy/scenarios.md
- docs/spec/record-contract.md
- docs/spec/rule-gate-spec.md

## Decisions To Close
- canonical metadata layer의 책임
- source-of-truth 충돌 처리 원칙
- read-only / import / sync integration 모드
- 진행 중 저장 어댑터 변경 제한 원칙

## Out of Scope
- 특정 SaaS(Notion/Jira/Confluence)별 상세 adapter 구현
- sync scheduler 구현 상세
