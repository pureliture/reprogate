---
record_id: ADR-005
type: ADR
title: Isolated Meta Progress Reporting System
status: Accepted
date: 2026-03-19
deciders: pureliture, Gemini CLI
supersedes: N/A
---

# ADR-005: Isolated Meta Progress Reporting System

## 1. Context

프로젝트 진행률(Progress)을 시각화하고 추적할 방법이 필요합니다. 그러나 ReproGate의 `docs/` 디렉토리는 이미 `strategy / spec / design / records`라는 **제품 정의 레이어(Product Definition Layer)**로 사용되고 있으므로, 저장소 상태 파생물인 progress를 이 안에 섞는 것은 제품 문서의 순수성을 훼손합니다.

## 2. Decision

진척도(Progress)는 제품 본체가 아니라 **저장소 상태에서 파생되는 메타 보고 시스템**으로 간주하고, `meta/progress/` 디렉토리 아래에 완전히 격리하여 구현합니다.

- **격리 공간:** `meta/progress/`
- **산출물:** `progress.md`, `progress.json` (기계 생성됨, Source of truth 아님)
- **로직:** `build_progress_report.py`와 `progress-map.yaml`을 통해 Roadmap, Issue, PR 상태를 읽어 점수를 계산.
- **자동화:** `.github/workflows/update-progress-report.yml`을 통해 `generated_at` 이외의 실질적 변경이 있을 때만 자동 커밋.

## 3. Consequences

- `docs/` 레이어의 순수성이 유지됩니다.
- Progress reporting 시스템의 결합도가 낮아져, 추후 시스템을 제거하거나 변경하기 용이합니다.
- 메타 보고 시스템의 실패가 제품 정의(CI)의 실패로 번지지 않도록 분리 운영됩니다.

## Verification

- `meta/progress/progress.md` 산출물이 GitHub Issue/PR 상태 변화에 따라 정상적으로 반영됨을 확인합니다.
- `update-progress-report.yml` 워크플로우가 의미 있는 변경 시에만 커밋을 수행하는지 확인합니다.
