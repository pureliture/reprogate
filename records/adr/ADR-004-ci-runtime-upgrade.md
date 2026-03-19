---
record_id: ADR-004
type: ADR
title: GitHub Actions 워크플로우 런타임 업그레이드 (Node 22+)
status: Accepted
date: 2026-03-19
deciders: pureliture, Gemini CLI
supersedes: N/A
---

# ADR-004: GitHub Actions 워크플로우 런타임 업그레이드 (Node 22+)

## 1. Context

GitHub Actions에서 Node.js 20 런타임에 대한 지원 중단 경고가 발생하기 시작했습니다. 안정적인 CI/CD 환경을 유지하고 최신 보안/성능 개선 사항을 반영하기 위해 워크플로우의 실행 환경을 업그레이드해야 합니다.

## 2. Decision

기존 `ubuntu-latest` (Node 20 기반 런타임 포함) 환경을 `ubuntu-24.04` (Node 22+ 지원)로 명시적으로 업그레이드하고, 핵심 액션들의 버전을 최신 패치로 고정합니다.

- Runner: `ubuntu-latest` -> `ubuntu-24.04`
- `actions/checkout`: `v4` -> `v4.2.1`
- `actions/setup-python`: `v5` -> `v5.2.0`

## 3. Consequences

- Node.js 20 관련 deprecation 경고가 제거됩니다.
- 최신 OS 환경에서 CI 스크립트가 실행되므로 더 안정적인 런타임을 보장받습니다.
- 향후 Node 22 기반 액션들로의 전환이 더 용이해집니다.

## Verification

로컬에서 `scripts/validate_product_definition.py`를 실행하여 정합성을 확인했습니다.
또한 GitHub PR 생성 후 `product-definition-ci` 액션이 성공적으로 완료되는지 확인합니다.
