# Rule / Gate Spec

Status: Draft

## Purpose

ReproGate의 Rule 평가와 Gate 집행이 무엇을 입력으로 받고,
어떤 상태와 강도로 판정되는지 정의한다.

## Inputs to Close
- docs/strategy/product-boundary.md
- docs/strategy/scenarios.md
- docs/spec/record-contract.md

## Decisions To Close
- advisory / soft / hard gate 의미
- missing / partial / ready / conflicted 상태 모델
- built-in evaluator와 external policy backend의 역할 분리
- built-in workflow 사용 여부가 아니라 reproducibility defect를 평가한다는 원칙의 입력 모델

## Out of Scope
- 특정 policy engine 구현 선택
- CI provider별 integration 상세
