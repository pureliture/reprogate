---
record_id: "RFC-003"
title: "ReproGate 제품 바운더리 정의"
type: "rfc"
status: "Draft"
created_at: "2026-03-18"
tags: ["product-boundary", "strategy", "stage-1.5"]
---

# RFC-003: ReproGate 제품 바운더리 정의

## Status
Draft

## Summary
Stage 2 (Distribution) 진입 전에, ReproGate의 제품 바운더리를 **정적 기능 목록이 아닌 사용자 시나리오 축** 기반으로 재정의한다. 핵심은 "어떤 기능이 있느냐"가 아니라 "사용자가 구조를 어떤 강도로 받아들이고, 중간에 어떻게 전환하는가"를 기준으로 바운더리를 설계하는 것이다.

## Motivation
현재 product-spec과 architecture 문서는 **기능 중심** 기술에 가깝다. 하지만 ReproGate처럼 방법론 컴파일러를 표방하는 제품은, 사용자가 워크플로를 일부만 수정하거나 스킬만 단발로 쓰거나 처음엔 구조를 거부하다가 나중에 도입하는 등 **행위 전환**이 핵심 시나리오다. 이를 반영하지 않으면 Stage 2에서 "누구를 위해 무엇을 배포하는가"가 흐려진다.

## Design / Proposal

산출물: [product-boundary.md](file:///Users/pureliture/IdeaProjects/ai-ops/docs/strategy/product-boundary.md)

## Verification
- [x] product-boundary.md가 5개 시나리오 축을 포함
- [x] 3층 바운더리 모델(Core / Flexible / Integration)이 정의됨
- [x] 최소 불변 계약 5개가 명시됨
- [x] 필수 요구사항(R1~R7)이 기존 문서와 정합성 확인됨
- [x] 시나리오 카탈로그 템플릿 포함
- [x] roadmap.md에 바운더리 정의 단계 반영
- [x] vision.md에 바운더리 원칙(P-1~P-7) 반영
- [x] 시나리오 카탈로그 초기 시나리오 작성
