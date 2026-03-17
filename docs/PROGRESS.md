# dpc 구현 진척 현황

> Last Updated: 2026-03-17
> Overall Progress: ~40%

## 1. CLI Commands

| 항목 | 진척 | 파일 | 비고 |
|------|------|------|------|
| `dpc init` | 80% | `scripts/init.py` | .dpc/ 생성 동작 |
| `dpc generate` | 80% | `scripts/generate.py` | 템플릿 기반 생성 |
| `dpc check` | 20% | `scripts/check_compliance.py` | Gate 엔진 미연동 |

## 2. Core Engines

| 항목 | 진척 | 파일 | 비고 |
|------|------|------|------|
| gate-engine (OPA) | 0% | - | **미구현** - `opa eval` 호출 필요 |
| template-engine | 80% | `scripts/generate.py` | Jinja2 기반 |
| context-engine | 40% | `scripts/set_process_context.py` | 프로세스 컨텍스트 |

## 3. Presets

| 항목 | 진척 | 파일 | 비고 |
|------|------|------|------|
| minimal/ | 0% | - | **미구현** |
| tdd/ | 0% | - | **미구현** |
| google-practices/ | 0% | - | 미구현 |
| adr-driven/ | 0% | - | 미구현 |

## 4. Adapters

| 항목 | 진척 | 파일 | 비고 |
|------|------|------|------|
| claude/ | 80% | `templates/claude/` | hooks, settings 템플릿 |
| codex/ | 20% | `templates/codex/` | README만 |
| prompts/ | 0% | - | 미구현 (Cursor, Kiro 등) |

## 5. Guides

| 항목 | 진척 | 비고 |
|------|------|------|
| methodology-setup.md | 0% | 미구현 |
| preset-selection.md | 0% | 미구현 |
| rules-writing.md | 0% | 미구현 |

## 6. Design/Docs

| 항목 | 진척 | 비고 |
|------|------|------|
| architecture.md | 100% | 완료 |
| presets-spec.md | 100% | 완료 |
| ADR-007 (OPA/Rego) | 100% | 완료 |

---

## Next Actions (우선순위)

1. **[P0] Gate 엔진 구현** - `opa eval` 호출 Python 래퍼
2. **[P0] 기본 프리셋** - `minimal`, `tdd` rules.rego 작성
3. **[P1] dpc check 연동** - Gate 엔진 + CLI 통합
4. **[P2] prompts/ 어댑터** - 비Claude 도구 지원
5. **[P2] Guides** - LLM 도우미 문서

---

## Change Log

### 2026-03-17
- 초기 진척 현황 문서 생성
- 설계 완료: architecture.md, presets-spec.md, ADR-007
- 마이그레이션 완료: WP-002~007 DONE
