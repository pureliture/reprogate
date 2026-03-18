# Record Contract Spec

Status: Draft

## Purpose

`docs/strategy/`에서 정의된 ReproGate의 핵심 계약 중
Record Identity, Decision Trace, Verification Trace, Policy Input 생성의 최소 불변 계약을 정의한다.

## Inputs to Close
- docs/strategy/final-definition.md
- docs/strategy/product-boundary.md
- docs/strategy/scenarios.md

## Decisions To Close
- 최소 필수 메타데이터 필드
- Decision / Verification / Provenance의 필수/선택 구분
- Policy Input Ready 판정 기초
- late binding / catch-up 시 provenance 요구 수준

## Out of Scope
- 저장소별 adapter 구현 세부
- UI 편집 경험
- 팀 승인 프로세스
