---
packet_id: "WP-DPC-2026-03-003"
title: "ai-ops 프레임워크 추출 및 오픈소스화"
goal_ids: ["DPC-G1", "DPC-G4", "DPC-G5"]
status: "DONE"
work_type: "FRAMEWORK"
priority: "P0"
target_environment: "master"
start_process: "P0"
current_process: "S4"
next_process: "-"
owner: "SHARED"
created_at: "2026-03-10"
last_updated: "2026-03-11"
parent: "WP-DPC-2026-03-001"
track: "프레임워크 독립화"
---

# WP-DPC-2026-03-003: ai-ops 프레임워크 추출 및 오픈소스화

> Historical interpretation note: 이 문서는 ReproGate 이전 naming 단계의 framework extraction 기록이다. 현재는 **legacy surface를 정리하고 reusable framework surface를 남긴 historical migration packet**으로 해석한다.

## 1. Goal

ncube-regression-verify 프로젝트에서 ai-ops 프레임워크를 추출하여 **프로젝트 무관한 독립 GitHub public 레포지토리**로 전환한다.

## 2. Background

- ai-ops는 현재 ncube-regression-verify 프로젝트 내부에 존재
- 프레임워크 자산과 프로젝트 종속 자산이 혼재
- 다른 프로젝트에서도 ai-ops를 사용할 수 있도록 분리 필요
- 포팅 메커니즘을 통해 프로젝트가 ai-ops를 연결할 수 있어야 함

## 3. Requirements

### 3.1 추출 요구사항

1. ai-ops 레포지토리에는 **프로젝트와 무관한 프레임워크 내용만** push
2. ncube-regression-verify 프로젝트 관련 내용은 다른 디렉토리로 이관
3. 도구별 프로세스 강제화 코드(`.omc`, `.claude`, `.codex`)도 함께 push하되 프로젝트 무관 내용만

### 3.2 포팅 메커니즘 요구사항

1. 프로젝트에서 "ai-ops 프레임워크를 포팅해줘" 지시 시:
   - ai-ops 레포지토리 수정 없이
   - 프로젝트 내부의 `.claude`, `.codex`, `.omc`를 수정하여 연결
2. 포팅 시 ai-ops 레포에 프로젝트 관련 내용이 추가되면 안 됨
3. 타겟 프로젝트의 ai-ops 유관 내용(AGENTS.md 등)은 해당 프로젝트 내부에 존재

## 4. Scope

### 4.1 범위

- 현재 ai-ops 자산 식별 및 분류
- 프레임워크 vs 프로젝트 종속 경계 정의
- 디렉토리 구조 설계
- 포팅 메커니즘 설계
- 추출 및 분리 구현

### 4.2 비범위

- ai-ops 기능 확장
- 새로운 프로세스 추가
- 외부 통합 (MCP, Notion 등)

## Done Criteria

- [x] framework vs project boundary and portability requirements are documented
- [x] staged migration strategy and deletion-readiness criteria are documented
- [x] canonical record/script/historical handling policies are fixed
- [x] root canonical cutover is implemented
- [x] final deletion-readiness S1 review passes

## 5. Process Trail

| Phase | Process | Status | Date | Notes |
|-------|---------|--------|------|-------|
| 분석 | P0 | **DONE** | 2026-03-10 | 자산 분류, 공개 불가 콘텐츠 검사 완료 |
| 요구사항 | P1 | **DONE** | 2026-03-10 | 요구사항 구체화, 설정 기반 접근 확정 |
| 설계 | P2/ADR | PENDING | - | 디렉토리 구조, 포팅 메커니즘 설계 |
| 구현 | P3 | **DONE** | 2026-03-10 | C1~C7 완료 (스켈레톤, 문서, 스크립트, CLI, 스키마/템플릿, 설치 가이드) |
| 리뷰 | S1 | **DONE** | 2026-03-10 | deletion readiness hold, P3 재진입 결정 |
| 구현(보강) | P3 | **DONE** | 2026-03-10 | generate bootstrap completeness, template coverage, helper scripts 보강 |
| 리뷰(보강 후) | S1 | **DONE** | 2026-03-10 | framework bootstrap self-contained pass, source repo deletion readiness hold |
| 요구사항(전환전략) | P1 | **DONE** | 2026-03-10 | 단계적 이행 + 임시 compatibility bridge 전략 확정 |
| 구현(전환 1차) | P3 | **DONE** | 2026-03-10 | root bridge docs/scripts 추가 + active adapter read path 재배선 |
| 리뷰(전환 1차) | S1 | **DONE** | 2026-03-10 | root bridge/wrapper pass, record path legacy 유지 확인 |
| 구현(전환 2차) | P3 | **DONE** | 2026-03-10 | legacy dependency inventory + deletion readiness checklist 추가 |
| 리뷰(전환 2차) | S1 | **DONE** | 2026-03-10 | inventory/checklist 승인, 남은 canonical 결정은 P1로 이관 |
| 요구사항(정책 확정) | P1 | **DONE** | 2026-03-11 | canonical record/script path + historical retention/redirect 정책 확정 |
| 구현(전환 3차) | P3 | **DONE** | 2026-03-11 | root live control-board cutover + root script example 정렬 + legacy bridge/archive 적용 |
| 리뷰(전환 3차) | S1 | **DONE** | 2026-03-11 | root cutover는 승인, 그러나 deletion readiness는 아직 No-Go |
| 구현(전환 4차) | P3 | **DONE** | 2026-03-11 | root non-record SoT 승격 + root script implementation 흡수 + historical archive path 확정 |
| 리뷰(전환 4차 후속) | S1 | **DONE** | 2026-03-11 | live-path/ADR/workspace-policy 정합성 보정 후 root canonical 방향 승인, immediate legacy full deletion은 No-Go |
| 기록 | S4 | **DONE** | 2026-03-11 | S1 재리뷰 verdict와 다음 P1(legacy removal policy) 입력값 고정 |
| 요구사항(legacy removal policy) | P1 | **DONE** | 2026-03-11 | discussion/review/shim final disposition + next P3 removal scope + S1 review conditions fixed |
| 구현(legacy namespace sunset) | P3 | **DONE** | 2026-03-11 | legacy docs/scripts namespace 제거 + archive relocation + hook source root relocation |
| 리뷰(legacy namespace sunset) | S1 | **DONE** | 2026-03-11 | final deletion readiness PASS |
| 기록(최종 완료) | S4 | **DONE** | 2026-03-11 | PASS verdict, completion status, archive-only legacy policy 고정 |

## 6. P0 분석 결과

### 6.1 분석 대상

- `docs/ai-ops/`: AI 운영체계 문서 (44개 파일)
- `scripts/ai-ops/`: AI 운영체계 스크립트 (6개 파일)
- `.claude/`: Claude Code 설정
- `.omc/`: OMC 설정
- `.codex/`: Codex 설정
- `AGENTS.md`: Codex 어댑터

### 6.2 P0 산출물: 자산 분류 맵

#### 분류 기준

| 분류 | 설명 | 처리 방향 |
|------|------|----------|
| **Framework** | 프로젝트 무관, ai-ops 핵심 | 추출 대상 |
| **Project** | ncube-regression-verify 전용 | 이관 대상 |
| **Template** | 프레임워크 + 프로젝트 혼합 | 분리/템플릿화 |
| **Runtime** | 런타임 상태 | .gitignore |
| **Archive** | 보존용 | 선택적 포함 |

#### docs/ai-ops/ 분류

| 파일/디렉토리 | 분류 | 비고 |
|--------------|------|------|
| `constitution.md` | Framework | 불변 목표 |
| `operating-model.md` | Framework | 운영 모델 |
| `work-packet-spec.md` | Framework | WP 규격 |
| `goal-alignment-checklist.md` | Framework | G0 체크리스트 |
| `process-catalog/*` | Framework | P0-P4, S1-S4, G0 |
| `tool-hooks/*` | Framework | 도구별 훅 정의 |
| `commands/ai-ops.md` | Framework | ai-ops 명령 |
| `portability/*` | Framework | 포팅 경계 |
| `omc-config/*` | Framework | OMC 템플릿 |
| `ops-bootstrap-master-plan.md` | **Mixed** | 구조는 Framework, WP 참조는 Project |
| `work-packets/*` | Project | ncube WP 기록 |
| `adr/*` | Project | ncube ADR 기록 |
| `CHANGELOG.md` | Project | ncube 변경 이력 |
| `workspace-profiles/*` | Project | master/java8 |
| `future-direction-*.md` | Project | 논의 기록 |
| `README.md` | Template | 진입점 |
| `ai-collaboration-guide.md` | Archive | 설계 원본 |

#### scripts/ai-ops/ 분류

모두 **Framework** (6개):
- `check_ai_ops_compliance.py`
- `claude_pretooluse_guard.py`
- `install_git_hooks.sh`
- `launch_ai_ops_session.py`
- `set_process_context.py`
- `sync_omc_policy.sh`

#### .claude/ 분류

| 파일 | 분류 |
|------|------|
| `CLAUDE.md` | Template (OMC + ai-ops 분리 필요) |
| `commands/ai-ops.md` | Framework |
| `hooks/pretooluse-ai-ops-guard.py` | Framework |
| `settings.json` | Template |
| `settings.local.json` | Project |

#### .omc/ 분류

| 파일 | 분류 |
|------|------|
| `AI-OPS-POLICY.md` | Framework |
| `ai-ops-process-context.json` | Runtime |
| `project-memory.json` | Runtime |
| `notepad.md` | Runtime |
| `sessions/`, `state/` | Runtime |

#### 루트 파일 분류

| 파일 | 분류 |
|------|------|
| `AGENTS.md` | Template (OMX + ai-ops 분리 필요) |
| `WORKSPACE-PROFILE.md` | Project |

### 6.3 추출 시 디렉토리 구조 (안)

```
ai-ops/                           # Framework Repository
├── docs/
│   ├── constitution.md
│   ├── operating-model.md
│   ├── work-packet-spec.md
│   ├── goal-alignment-checklist.md
│   ├── process-catalog/
│   ├── tool-hooks/
│   ├── commands/
│   ├── portability/
│   └── omc-config/
├── scripts/
│   ├── check_ai_ops_compliance.py
│   ├── claude_pretooluse_guard.py
│   ├── install_git_hooks.sh
│   ├── launch_ai_ops_session.py
│   ├── set_process_context.py
│   └── sync_omc_policy.sh
├── templates/                    # 포팅용 템플릿
│   ├── .claude/
│   ├── .codex/
│   ├── .omc/
│   ├── AGENTS.md.template
│   ├── WORKSPACE-PROFILE.md.template
│   └── project-ops/
├── port/                         # 포팅 스크립트
│   └── port_to_project.py
└── README.md
```

### 6.4 위험 포인트

1. **경로 의존성**: 스크립트가 `docs/ai-ops/`, `scripts/ai-ops/` 상대 경로에 의존
2. **어댑터 분리**: CLAUDE.md, AGENTS.md에서 OMC/OMX vs ai-ops 분리 필요
3. **WP/ADR 참조**: `ops-bootstrap-master-plan.md`에 ncube WP 직접 참조 포함
4. **포팅 메커니즘 미정의**: 프로젝트 연결 방식 설계 필요

### 6.5 공개 불가 콘텐츠 검사 결과

#### 검사 결과 요약

| 검사 항목 | 결과 |
|----------|------|
| API 키/비밀번호/토큰 | ✅ 없음 |
| 이메일 주소 | ✅ 없음 |
| 내부 IP/localhost | ✅ 없음 |
| 절대 경로 (/Users/) | ✅ 없음 |
| **프로젝트 특정 참조** | ⚠️ 18개 파일 |

#### 일반화 필요 파일 (Framework 분류)

| 파일 | 참조 내용 | 처리 방향 |
|------|----------|----------|
| `operating-model.md` | "ncube-regression-verify" | 플레이스홀더로 변경 |
| `commands/ai-ops.md` | `../ncube-regression-verify-java8` | 플레이스홀더로 변경 |
| `work-packet-spec.md` | `wafful4` 예시 | 예시 일반화 |
| `ops-bootstrap-master-plan.md` | `wafful4(java8)` | 일반화 또는 제거 |
| `tool-hooks/codex-jetbrains-ai-assistant-rules.md` | `wafful4` | 일반화 |
| `portability/ai-tool-artifact-boundary.md` | `wafful4` 예시 | 예시 일반화 |

#### 제외 권장 파일 (Archive)

- `ai-collaboration-guide.md` - 설계 원본, 프로젝트 특정 내용 다수 포함

### 6.6 P0 미확정 항목 (P1에서 해결)

1. ~~ai-ops ↔ 프로젝트 연결 방식~~ → **설정 기반 생성** 선택
2. ~~CLAUDE.md/AGENTS.md 생성 방식~~ → **Jinja2 템플릿** 선택
3. 프레임워크 버전 관리 → P3에서 결정
4. ~~런타임 상태 .gitignore 정책~~ → `.gitignore` 템플릿에 포함

## 7. P1: 요구사항 구체화 결과

### 7.1 사용자 결정 사항

| 결정 | 내용 |
|------|------|
| 백포팅 기능 | **제외** (프로젝트 전용, Framework에 포함 안 함) |
| 설정 방식 | **설정 파일 기반** (여러 사용자 공유/전파에 적합) |

### 7.2 설정 파일 구조 (ai-ops.config.yaml)

```yaml
version: "1.0"

project:
  name: "my-project"
  description: "프로젝트 설명"

workspaces:
  primary:
    name: "main"
    branch: "main"
    runtime: "Java 17"

processes:
  enabled: [P0, P1, P3, P4, S1, S2, S4]

tools:
  claude:
    enabled: true
    hook_enforcement: true
  codex:
    enabled: true

records:
  wp_path: "docs/ai-ops/work-packets"
  adr_path: "docs/ai-ops/adr"
  changelog_path: "docs/ai-ops/CHANGELOG.md"
```

### 7.3 요구사항 목록

#### Framework 레포지토리

| ID | 요구사항 | 우선순위 |
|----|---------|----------|
| FR-001 | 프로세스 정의 문서 (P0-P4, S1-S4, G0) | 필수 |
| FR-002 | 도구 훅 스크립트 (일반화) | 필수 |
| FR-003 | 설정 스키마 (`ai-ops.schema.json`) | 필수 |
| FR-004 | 템플릿 파일 (CLAUDE.md, AGENTS.md 등) | 필수 |
| FR-005 | CLI 스크립트 (`ai-ops init/generate/check`) | 필수 |
| FR-006 | 설치/설정 가이드 | 필수 |

#### 포팅 메커니즘

| ID | 요구사항 | 우선순위 |
|----|---------|----------|
| FR-010 | 포팅 시 ai-ops 레포 수정 없음 | 필수 |
| FR-011 | `ai-ops.config.yaml` 생성 | 필수 |
| FR-012 | 설정 기반 도구 파일 생성 | 필수 |
| FR-020 | 설정 파일 git 추적 (팀 공유) | 필수 |
| FR-021 | 런타임 상태 .gitignore | 필수 |

### 7.4 범위 / 비범위

**범위:**
- 프로세스 정의 (P0-P4, S1-S4, G0)
- 도구 훅 (일반화된 PreToolUse, Git hook)
- 설정 스키마 및 템플릿
- CLI 스크립트 (init, generate, check)
- WP/ADR 템플릿 구조

**비범위:**
- ❌ 백포팅 기능 (P4 백포팅 서브플로우)
- ❌ 물리 워크스페이스 분리 (master/java8)
- ❌ Java/Spring 버전별 가드
- ❌ ncube 프로젝트 WP/ADR 데이터
- ❌ OMC/OMX 자체 (별도 의존성)

### 7.5 디렉토리 구조 (확정)

```
ai-ops/
├── README.md
├── LICENSE
├── docs/
│   ├── constitution.md
│   ├── operating-model.md        # 일반화됨
│   ├── work-packet-spec.md
│   ├── process-catalog/
│   ├── tool-hooks/
│   └── commands/
├── scripts/
│   ├── cli.py                    # ai-ops CLI
│   ├── init.py
│   ├── generate.py
│   ├── check_compliance.py
│   └── hooks/
│       ├── claude_pretooluse_guard.py  # 일반화
│       └── git_pre_commit.sh
├── config/
│   └── ai-ops.schema.json
└── templates/
    ├── ai-ops.config.yaml.j2
    ├── claude/
    │   ├── CLAUDE.md.j2
    │   ├── commands/
    │   ├── hooks/
    │   └── settings.json.j2
    ├── codex/
    ├── AGENTS.md.j2
    └── project-ops/
```

### 7.6 완료 기준

| ID | 기준 | 검증 방법 |
|----|------|----------|
| DC-001 | ai-ops 레포에 프로젝트 특정 내용 없음 | grep 검사 |
| DC-002 | `ai-ops init` 작동 | 실행 테스트 |
| DC-003 | `ai-ops generate` 작동 | 실행 테스트 |
| DC-004 | 생성된 파일로 프로세스 실행 가능 | 파일럿 테스트 |

### 7.7 P3 전달 입력값

1. 디렉토리 구조 확정안
2. 설정 스키마 정의
3. CLI 인터페이스: `ai-ops init`, `ai-ops generate`, `ai-ops check`
4. 템플릿 목록 및 변수
5. 제거/일반화 대상 파일 목록

### 7.8 P3 착수 상태 (2026-03-10)

- `python3 scripts/ai-ops/set_process_context.py --process P3 --wp WP-DPC-2026-03-003 --team-mode single`로 Single fallback 확정
- 새 레포지토리 ``ai-ops` (this repository)` 진행 현황:
  - `C1` 완료: `README.md`, `LICENSE`, `.gitignore`, `docs/`, `scripts/`, `config/`, `templates/` 스켈레톤 생성
  - `C2` 완료: `constitution.md`, `operating-model.md`, `process-catalog/*` 일반화 문서 추가
  - `C3` 완료: `docs/commands/*`, `docs/tool-hooks/*` 일반화 문서 추가
  - `C4` 완료: `scripts/check_compliance.py`, `scripts/hooks/claude_pretooluse_guard.py`, `scripts/hooks/git_pre_commit.sh` 추가
  - `C5` 완료: `scripts/cli.py`, `scripts/init.py`, `scripts/generate.py`, `scripts/set_process_context.py` 구현
  - `C6` 완료: `config/ai-ops.schema.json`, `templates/*` 추가
  - `C7` 완료: `docs/installation.md`, `README.md` 보강
- 생성 커밋:
- `15a7422` `feat(ai-ops): WP-010 P3 기본 레포지토리 구조 생성`
- `8628810` `docs(ai-ops): WP-010 P3 프로세스 카탈로그 추가`
- `7f7e1be` `docs(ai-ops): WP-010 P3 도구 훅 및 명령 문서 추가`
- `fa9a1ec` `feat(ai-ops): WP-010 P3 핵심 스크립트 추가`
- `32103e6` `feat(ai-ops): WP-010 P3 CLI 스크립트 구현`
- `6d90120` `feat(ai-ops): WP-010 P3 설정 스키마 및 템플릿 추가`
- `49a4ece` `docs(ai-ops): WP-010 P3 설치 가이드 완성`
- `e5629f7` `docs(ai-ops): WP-010 P3 추출 구현 완료 기록` (source repo 기록 동기화)
- 다음 권장 프로세스: `S1` (추출 결과 리뷰)

### 7.9 S1 리뷰 결과 (2026-03-10)

#### 리뷰 범위

- 새 프레임워크 레포 ``ai-ops` (this repository)`
- 사용자 후속 계획: **최종적으로 source repo (`ncube-regression-verify`)에서 `ai-ops` 디렉토리를 삭제 가능한가**

#### 확인한 강점

- 새 레포 working tree clean
- 커밋 체인(C1~C7) 분리 완료
- `python3 scripts/check_compliance.py --mode working_tree` 통과
- `python3 scripts/cli.py check --mode none` 통과
- `init -> generate -> check` 흐름 검증 완료
- `set_process_context.py` 동작 확인
- `docs/scripts/config/templates`에서 프로젝트 특화 문자열(`ncube`, `wafful4`, 절대경로 등) 미검출

#### 핵심 리뷰 발견사항

1. **생성 산출물 불완전**
   - `generate` 결과는 현재 `AGENTS.md`, `.claude/CLAUDE.md`만 생성함
   - 그러나 생성된 문서는 `docs/constitution.md`, `docs/process-catalog/README.md`, `scripts/set_process_context.py` 등을 전제로 함
   - 즉, 타겟 프로젝트에 실제로 필요한 framework docs/scripts를 함께 공급하지 못함
2. **템플릿 coverage 부족**
   - `templates/codex/`, `templates/project-ops/`는 아직 `.gitkeep` בלבד
   - 삭제 계획 관점에서 target bootstrap story가 아직 완성되지 않음
3. **삭제 readiness 미충족**
   - 현재 상태로 source repo의 `docs/ai-ops`를 제거하면, 새 framework만으로 기존 운영 경로를 대체하기 어렵다

#### S1 판정

- **승인 보류 / P3 재진입 필요**
- 이유: 추출 레포 자체는 동작하지만, **source repo에서 `ai-ops` 디렉토리를 제거할 정도의 포팅/부트스트랩 완결성**은 아직 부족함
- 다음 권장 프로세스: `P3`
  - target project에 framework docs/scripts/bootstrap assets를 어떻게 공급할지 구현
  - codex / project-ops template coverage 확장
  - 삭제 전 migration path 검증

### 7.10 P3 보강 구현 결과 (2026-03-10)

#### 실행 경로

- current repo context 기록:
  - `python3 scripts/ai-ops/set_process_context.py --process P3 --wp WP-DPC-2026-03-003 --team-mode auto`
  - `python3 scripts/ai-ops/set_process_context.py --process P3 --wp WP-DPC-2026-03-003 --team-mode single`
- external framework repo: ``ai-ops` (this repository)`

#### 구현 내용

1. **bootstrap-complete generate**
   - `scripts/generate.py`가 `AGENTS.md`, `.claude/CLAUDE.md`만 생성하던 상태에서 벗어나
     target project에 `docs/`, `scripts/`, `config/`, `templates/`, `ai-ops.config.yaml`을 함께 bootstrap하도록 확장
   - 동시에 `WORKSPACE-PROFILE.md`, `.codex/README.md`, `.claude/commands/ai-ops.md`, `.claude/settings.json`,
     `.claude/hooks/pretooluse-ai-ops-guard.py`, configured record scaffold를 생성
2. **누락 framework assets 보강**
   - `docs/goal-alignment-checklist.md`
   - `docs/work-packet-spec.md`
   - `docs/portability/ai-tool-artifact-boundary.md`
   - `docs/omc-config/README.md`
   - `docs/omc-config/AI-OPS-POLICY.template.md`
3. **template coverage 확장**
   - `templates/codex/README.md.j2`
   - `templates/project-ops/CHANGELOG.md.j2`
   - `templates/project-ops/work-packets/index.md.j2`
   - `templates/project-ops/adr/README.md.j2`
   - `templates/WORKSPACE-PROFILE.md.j2`
   - `templates/claude/commands/ai-ops.md.j2`
   - `templates/claude/settings.json.j2`
   - `templates/claude/hooks/pretooluse-ai-ops-guard.py.j2`
4. **helper script 보강**
   - `scripts/launch_ai_ops_session.py`
   - `scripts/install_git_hooks.sh`
   - `scripts/sync_omc_policy.sh`
   - omission rationale: `.githooks/*`는 committed framework asset로 두지 않고 `install_git_hooks.sh`가 local bootstrap 시 생성하도록 유지
5. **verification hardening**
   - `scripts/check_compliance.py`가 `ai-ops.config.yaml`의 `wp_path / adr_path / changelog_path`를 읽어 custom record path 정합성도 점검

#### 검증 결과

- external repo 정적 검증:
  - `python3 scripts/check_compliance.py --mode working_tree` → pass
  - `python3 scripts/cli.py check --mode working_tree` → pass
  - `python3 -m py_compile scripts/check_compliance.py scripts/generate.py scripts/init.py scripts/cli.py scripts/set_process_context.py scripts/launch_ai_ops_session.py scripts/hooks/claude_pretooluse_guard.py` → pass
- generated target smoke:
  - temp output에서 `python3 scripts/cli.py init ...` / `python3 scripts/cli.py generate ...` → pass
  - generated tree에 missing docs / helper scripts / codex+claude+project scaffold 존재 확인
  - generated target에서 `./scripts/install_git_hooks.sh`, `./scripts/sync_omc_policy.sh`,
    `python3 scripts/set_process_context.py --process P3 --wp WP-DEMO --team-mode single`,
    `python3 scripts/launch_ai_ops_session.py --launcher omx --dry-run -- --model gpt-5` → pass

#### 후속 권장 프로세스

- `S1`
  - source repo의 `docs/ai-ops` 삭제 readiness 재점검
  - generated target만으로 bootstrap / hook / helper / launch path가 self-consistent한지 확인

### 7.11 S1 재리뷰 결과 (2026-03-10)

#### 리뷰 범위

- external framework repo ``ai-ops` (this repository)`
- generated target bootstrap 결과
- current source repo `ncube-regression-verify-ai-ops`에서의 legacy path 의존성

#### 확인한 점

1. **framework bootstrap completeness는 유의미하게 개선됨**
   - temp target에서 `init -> generate` 후 `docs/`, `scripts/`, `config/`, `templates/`, adapter files, project record scaffold가 함께 생성됨
   - generated target 내부에서 `install_git_hooks.sh`, `sync_omc_policy.sh`, `set_process_context.py`, `launch_ai_ops_session.py --dry-run`까지 실행 가능함
2. **external repo 단독 bootstrap story는 이제 self-consistent함**
   - generated adapter가 참조하는 핵심 framework docs / helper scripts가 target으로 함께 공급됨
   - `templates/codex`, `templates/project-ops`, `templates/claude/{commands,hooks,settings}` placeholder 상태가 해소됨

#### 남은 핵심 갭

1. **source repo의 active path contract는 아직 legacy namespace에 고정**
   - `AGENTS.md`, `.claude/CLAUDE.md`, `.codex/README.md`, `.claude/commands/ai-ops.md` 등이 여전히 `docs/ai-ops/*`, `scripts/ai-ops/*`를 직접 참조
   - `scripts/ai-ops/install_git_hooks.sh`, `scripts/ai-ops/sync_omc_policy.sh`, guard/compliance 경로도 legacy layout을 전제로 함
2. **새 framework generate 결과는 root-oriented portable layout**
   - generated target은 `docs/constitution.md`, `docs/process-catalog/*`, `scripts/set_process_context.py` 같은 root layout을 제공
   - 즉 현재 source repo의 `docs/ai-ops/*`, `scripts/ai-ops/*` contract와 1:1 호환되지 않음
3. **따라서 source repo의 `docs/ai-ops` 삭제 readiness는 아직 미충족**
   - 지금 바로 `docs/ai-ops`를 제거하면 current adapter / hook / workspace reference가 깨짐
   - 삭제 전에는 source repo migration path 또는 compatibility layer 중 하나가 필요함

#### S1 판정

- **조건부 승인 / deletion readiness 보류**
- 승인 범위:
  - external `ai-ops` framework repo의 bootstrap completeness 보강 자체는 통과
- 보류 범위:
  - current source repo에서 `docs/ai-ops`를 제거해도 되는지 여부는 아직 보류

#### 다음 권장 프로세스

- `P1`
  - source repo migration strategy를 명시적으로 정한다
  - 선택지 예시:
    1. current source repo를 portable root layout(`docs/*`, `scripts/*`) 기준으로 재배선
    2. external framework에 legacy compatibility output(`docs/ai-ops/*`, `scripts/ai-ops/*`)을 추가
  - 위 선택 없이 바로 삭제/이관 구현에 들어가면 범위 오판 위험이 있음

### 7.12 P1 단계적 이행 전략 확정 (2026-03-10)

#### 목표

- 최종적으로는 source repo가 `docs/*`, `scripts/*` 중심의 portable root layout을 기준으로 동작하도록 전환한다.
- 단, 전환 중에는 기존 `docs/ai-ops/*`, `scripts/ai-ops/*` 계약을 한 번에 제거하지 않고 임시 compatibility bridge를 유지한다.

#### 검토한 선택지

1. **일괄 hard-cut 전환**
   - source repo의 모든 참조를 한 번에 portable root layout으로 교체
   - 장점: 가장 깔끔함
   - 단점: 현재 adapter / hook / workspace 경로 파손 위험이 큼
2. **legacy compatibility output 장기 유지**
   - external framework가 `docs/ai-ops/*`, `scripts/ai-ops/*`까지 계속 생성
   - 장점: source repo 수정이 적음
   - 단점: legacy 구조를 장기 유지하게 되어 deletion goal과 상충
3. **단계적 이행 + 임시 compatibility bridge** ← **선택**
   - source repo는 portable root layout을 목표 구조로 채택
   - 단기적으로는 legacy path를 유지/브리지하면서 참조를 점진적으로 재배선
   - 장점: 최종 목표와 안전한 전환을 동시에 만족

#### 확정 결정

- **선택안: 단계적 이행 + 임시 compatibility bridge**
- 이유:
  - 목표가 단순 포팅 성공이 아니라 **source repo에서 기존 ai-ops 디렉터리를 삭제할 수 있는 상태**이기 때문
  - 동시에 current source repo의 active adapter / hook / workspace reference를 즉시 끊으면 회귀 위험이 높기 때문

#### 범위

1. source repo의 active 참조 경로를 분류한다.
   - `AGENTS.md`
   - `.claude/CLAUDE.md`
   - `.codex/README.md`
   - `.claude/commands/ai-ops.md`
   - `scripts/ai-ops/*`
   - `docs/ai-ops/*` 직접 참조 문서
2. portable root layout 기준의 canonical target을 정의한다.
   - `docs/*`
   - `scripts/*`
   - `config/*`
   - generated adapter files
3. legacy path별 bridge 방식과 제거 순서를 결정한다.

#### 비범위

- 이번 P1에서 실제 source repo 재배선 구현 완료
- 이번 P1에서 `docs/ai-ops` 즉시 삭제
- 이번 P1에서 compatibility layer의 최종 제거

#### P3 전달 입력값

다음 P3는 아래 순서로 수행한다.

1. **legacy dependency inventory 작성**
   - current source repo에서 `docs/ai-ops/*`, `scripts/ai-ops/*` 직접 참조 지점 전수 식별
2. **bridge 설계 및 구현**
   - 가장 위험한 active path부터 root layout 또는 bridge로 전환
   - 필요 시 thin wrapper / redirect / compatibility docs 도입
3. **adapter 재배선**
   - `AGENTS.md`, `.claude/CLAUDE.md`, `.codex/README.md`, `.claude/commands/ai-ops.md` 순으로 재정렬
4. **삭제 readiness 재검증**
   - `docs/ai-ops`를 제거하지는 않더라도, 제거 직전 상태까지 도달했는지 점검

#### 완료 기준

- 왜 hard-cut이 아니라 staged migration이어야 하는지 근거가 명시됨
- 다음 P3가 구현할 대상 path set과 우선순위가 정의됨
- deletion readiness를 판정하기 위한 bridge / canonical target 개념이 문서화됨

### 7.13 P3 단계적 이행 1차 구현 (2026-03-10)

#### 실행 경로

- context 기록:
  - `python3 scripts/set_process_context.py --process P3 --wp WP-DPC-2026-03-003 --team-mode auto`
  - `python3 scripts/set_process_context.py --process P3 --wp WP-DPC-2026-03-003 --team-mode single`

#### 구현 내용

1. **root bridge docs 추가**
   - `docs/constitution.md`
   - `docs/ops-bootstrap-master-plan.md`
   - `docs/work-packets/index.md`
   - `docs/commands/ai-ops.md`
   - `docs/tool-hooks/process-enforcement-matrix.md`
   - `docs/process-catalog/{README,process-selection-guide,minimum-logical-role-set,P0-P4-core-processes,S1-S4-support-processes}.md`
   - 목적: active adapter가 root path를 읽더라도 현재 canonical legacy source(`docs/ai-ops/*`)로 안전하게 연결되도록 함
2. **root bridge scripts 추가**
   - `scripts/set_process_context.py`
   - `scripts/check_compliance.py`
   - `scripts/launch_ai_ops_session.py`
   - `scripts/install_git_hooks.sh`
   - `scripts/sync_omc_policy.sh`
   - 목적: active adapter가 root script path를 사용해도 기존 `scripts/ai-ops/*` 실행 경로를 그대로 래핑
3. **active adapter read path 재배선**
   - `AGENTS.md`
   - `.claude/CLAUDE.md`
   - `.codex/README.md`
   - `.claude/commands/ai-ops.md`
   - `.agents/skills/ai-ops/SKILL.md`
   - 변경 원칙:
     - first-read / session-entry / helper script path는 root bridge 기준으로 전환
     - current record path(`docs/ai-ops/work-packets`, `docs/ai-ops/adr`)는 이번 라운드에서 유지

#### 구현 판단

- 이번 라운드는 **canonical storage 이동**이 아니라 **entry/read path 안정화**에 집중했다.
- 즉,
  - 읽는 경로는 `docs/*`, `scripts/*`로 옮기고
  - 실제 authoritative source와 기록 저장은 아직 `docs/ai-ops/*`, `scripts/ai-ops/*`를 유지한다.
- 이렇게 해야 staged migration의 risk를 낮추면서 다음 라운드에서 record/canonical 이동 여부를 검증할 수 있다.

#### 검증 결과

- active adapter 5종 점검:
  - `AGENTS.md`, `.claude/CLAUDE.md`, `.codex/README.md`, `.claude/commands/ai-ops.md`, `.agents/skills/ai-ops/SKILL.md`
  - 위 파일들에서 legacy 직접 참조는 의도적으로 남겨둔 record path를 제외하고 root bridge 기준으로 정리
- root bridge 파일 존재 확인:
  - `docs/*`, `scripts/*` bridge/wrapper 생성 확인

#### 후속 권장 프로세스

- `S1`
  - root bridge + active adapter 재배선이 staged migration 1차로 적절한지 검토
  - 다음 라운드에서 canonical record path 자체를 이동할지, record path는 legacy로 유지할지 판정

### 7.14 S1 리뷰 결과 - 단계적 이행 1차 (2026-03-10)

#### 리뷰 범위

- root bridge docs / wrapper scripts
- active adapter read path 재배선 결과
- current source repo에서 남아 있는 legacy 직접 참조

#### 검증 결과

- `python3 scripts/set_process_context.py --process S1 --wp WP-DPC-2026-03-003 --team-mode single` → pass
- `python3 scripts/check_compliance.py --mode none` → pass
- `python3 scripts/launch_ai_ops_session.py --dry-run --launcher omx -- --model gpt-5` → pass
- active adapter 직접 참조 점검:
  - `AGENTS.md`
  - `.claude/CLAUDE.md`
  - `.codex/README.md`
  - `.claude/commands/ai-ops.md`
  - `.agents/skills/ai-ops/SKILL.md`
  - 위 파일들에서 legacy 직접 참조는 의도적으로 남겨둔 record path 안내를 제외하고 root bridge 기준으로 정리됨

#### 리뷰 판단

- **Approve**
- 이유:
  1. entry/read path는 staged migration의 목적대로 root bridge 기준으로 안정화됨
  2. wrapper script를 통해 실제 실행 경로도 유지됨
  3. current canonical record path(`docs/ai-ops/work-packets`, `docs/ai-ops/adr`)는 아직 유지되어 기록 체계 충돌을 만들지 않음

#### 남은 보강 포인트

1. record path를 언제 root layout으로 이동할지 여부는 아직 미결
2. bridge 파일이 얇은 redirect 문서인 만큼, 최종 제거 시점과 canonical switch 규칙을 별도 라운드에서 정리해야 함

#### 다음 권장 프로세스

- `P3`
  - staged migration 2차 구현
  - 범위 후보:
    1. record/canonical path 이동 설계 및 일부 구현
    2. bridge removal 조건 문서화
    3. source repo에서 `docs/ai-ops` 삭제 readiness 체크리스트 구체화

### 7.15 P3 단계적 이행 2차 구현 (2026-03-10)

#### 구현 내용

1. **legacy dependency inventory 추가**
   - `docs/ai-ops/portability/legacy-dependency-inventory.md`
   - 남아 있는 legacy 의존성을 아래 범주로 분리:
     - active adapter에서 의도적으로 남긴 record path
     - canonical legacy source (`docs/ai-ops/*`, `scripts/ai-ops/*`)
     - internal framework docs / policy / hook 문서의 self-reference
     - historical WP/ADR/archive 문서
2. **deletion readiness checklist 추가**
   - `docs/ai-ops/portability/staged-migration-deletion-readiness-checklist.md`
   - 삭제 판단을 위한 기준을 명시:
     - entry/read path root bridge 전환 완료 여부
     - wrapper/script 동작 여부
     - record path cutover 여부
     - historical docs treatment
     - final remove 조건

#### 구현 이유

- 현재는 “삭제 readiness가 아직 부족하다”는 판단은 있었지만,
  **무엇이 남았는지 / 무엇이 충족되면 삭제 가능한지**가 충분히 구조화되어 있지 않았다.
- 이번 라운드는 다음 구현/리뷰에서 불필요한 재해석을 줄이기 위해
  남은 legacy dependency와 삭제 판정 기준을 문서화하는 데 집중했다.

#### 산출물

- `docs/ai-ops/portability/legacy-dependency-inventory.md`
- `docs/ai-ops/portability/staged-migration-deletion-readiness-checklist.md`

#### 후속 권장 프로세스

- `S1`
  - inventory/checklist가 staged migration 2차 입력값으로 충분한지 검토
  - 다음 라운드에서 record/canonical path cutover를 실제 구현할지 판정

### 7.16 S1 리뷰 결과 - 단계적 이행 2차 (2026-03-10)

#### 리뷰 범위

- `docs/ai-ops/portability/legacy-dependency-inventory.md`
- `docs/ai-ops/portability/staged-migration-deletion-readiness-checklist.md`
- 해당 산출물을 반영한 WP/index/changelog 동기화 상태

#### 리뷰 판단

- **Approve**

#### 승인 이유

1. 남아 있는 legacy 의존성이 “active adapter / wrapper / internal self-reference / historical material”로 구조화되었다.
2. deletion readiness를 단순 감각이 아니라 체크리스트 기준으로 판정할 수 있게 되었다.
3. 현재 시점의 verdict가 **No-Go**인 이유가 명확해졌고, 다음에 무엇을 결정해야 하는지도 좁혀졌다.

#### 아직 남은 핵심 미결정

다음 항목은 구현보다 먼저 결정이 필요한 성격이다.

1. canonical record path 정책
   - `docs/ai-ops/work-packets`, `docs/ai-ops/adr`, `docs/ai-ops/CHANGELOG.md`를 유지할지
   - 아니면 root layout으로 이동할지
2. canonical script path 정책
   - `scripts/ai-ops/*`를 유지할지
   - 아니면 `scripts/*`로 승격할지
3. historical material 처리 정책
   - archive 동결
   - redirect
   - 일부 이관

#### 결론

- 이번 P3의 inventory/checklist 산출물은 **충분히 유효하고 승인 가능**하다.
- 다만 다음 단계는 곧바로 구현보다는, 위 미결정을 정리하는 **P1 재진입**이 더 적절하다.

#### 다음 권장 프로세스

- `P1`
  - canonical record/script path 정책 확정
  - historical material retention/redirect 정책 확정
  - 이후 구현 라운드의 cutover 범위를 좁혀서 P3로 전달

### 7.17 P1 canonical policy refinement (2026-03-11)

#### 목표

- staged migration의 마지막 미결정이던 record path / script path / historical handling 정책을 고정한다.
- 다음 P3가 구현 범위를 해석하지 않고 바로 cutover 설계/구현에 들어갈 수 있게 한다.

#### 이번 라운드에서 다시 확인한 사실

1. external framework repo의 현재 bootstrap completeness 변경은 아직 uncommitted 상태다.
   - 따라서 이번 라운드는 external repo 구조를 다시 바꾸지 않고, **current source repo가 채택할 canonical target**만 확정한다.
2. extracted framework의 기본 generated layout은 이미 root-oriented portable 구조다.
   - default records: `docs/work-packets`, `docs/adr`, `docs/CHANGELOG.md`
   - stable entry scripts: `scripts/*`
3. current source repo는 entry/read path만 root bridge로 올렸고, canonical storage는 아직 legacy에 남아 있다.
   - 즉 deletion readiness를 끝내려면 “무엇이 최종 canonical인가”를 더 미루면 안 된다.

#### 확정 결정 1: canonical record path 정책

- **최종 canonical AI Ops record path는 root layout으로 고정한다.**
  - `docs/work-packets/`
  - `docs/adr/`
  - `docs/CHANGELOG.md`
- 이유:
  1. extracted framework의 default config / generated target과 일치한다.
  2. 이미 active adapter의 first-read path는 `docs/*` bridge 기준으로 정리되어 있다.
  3. `docs/ai-ops/*`를 장기 canonical로 유지하면 deletion goal과 충돌한다.
- 경계:
  - 제품/프로젝트 전용 기록은 계속 `docs/project-ops/*`에 남긴다.
  - root `docs/work-packets`, `docs/adr`, `docs/CHANGELOG.md`는 **AI Ops live control board**로 사용한다.
- migration rule:
  - cutover 전까지는 기존 `docs/ai-ops/work-packets`, `docs/ai-ops/adr`, `docs/ai-ops/CHANGELOG.md`가 임시 authoritative 상태를 유지할 수 있다.
  - cutover 후에는 위 legacy 경로를 **redirect/freeze only**로 취급하고, 새 live record는 root canonical path에만 기록한다.

#### 확정 결정 2: canonical script path 정책

- **최종 stable operator-facing script path는 root `scripts/*`로 고정한다.**
  - `scripts/set_process_context.py`
  - `scripts/check_compliance.py`
  - `scripts/launch_ai_ops_session.py`
  - `scripts/install_git_hooks.sh`
  - `scripts/sync_omc_policy.sh`
- 이유:
  1. current source repo에 이미 같은 이름의 root wrapper가 존재한다.
  2. extracted framework도 stable command surface를 root `scripts/*` 기준으로 생성한다.
  3. 사용자/어댑터/문서가 계속 `scripts/ai-ops/*`를 보게 두면 bridge 제거 조건이 끝없이 뒤로 밀린다.
- migration rule:
  - `scripts/ai-ops/*`는 다음 P3 동안 **temporary compatibility implementation layer**로만 유지한다.
  - 문서, hook, guard, githook, adapter에서의 user-facing command 예시는 root `scripts/*` 기준으로 전환한다.
  - `claude_pretooluse_guard.py` 같은 tool-specific supporting asset 정리는 P3 cutover 범위에서 다루되, public/stable command policy 자체는 root `scripts/*`로 본다.

#### 확정 결정 3: historical material retention / redirect 정책

- 원칙은 **retention first, live path cutover second, historical text freeze third**로 둔다.
- 세부 규칙:
  1. **live control-board artifacts**
     - active index / open WP / active ADR navigation / integrated changelog는 root canonical path로 이동한다.
  2. **closed historical WP/ADR records**
     - 삭제하지 않는다.
     - cutover 시점에 active control board 밖의 retained archive 영역으로 보존하거나, legacy 위치를 frozen archive로 남긴 뒤 redirect/stub만 두는 방식으로 처리한다.
  3. **discussion / future-direction / archive 성격 문서**
     - 이번 P1 범위에서 내용 수정 없이 historical material로 간주한다.
     - 오래된 경로 문자열은 대량 rewrite하지 않고 frozen history로 허용한다.
  4. **redirect rule**
     - 운영자가 먼저 찾는 entry path(legacy index/README/command-level entry)는 thin redirect 또는 bridge 안내를 제공한다.
     - 반면 historical 본문 내부의 과거 경로 표기는 “당시 기록”으로 간주해 rewrite를 강제하지 않는다.
- 이유:
  - history 보존 없이 legacy tree를 지우면 traceability를 잃고,
  - 모든 과거 문서를 일괄 rewrite하면 범위가 커지고 기록 정직성이 떨어진다.

#### 이번 P1이 이전 기록에 대해 갖는 의미

- 이 WP의 앞부분에 남아 있는 legacy example/path는 **당시 결정과 상태를 보존하는 historical record**다.
- 2026-03-11 기준으로는 아래 정책이 supersede 한다.
  - canonical live records → root `docs/*`
  - canonical stable commands → root `scripts/*`
  - legacy `docs/ai-ops/*`, `scripts/ai-ops/*` → migration 중 compatibility/archive surface

#### 다음 P3 전달 입력값

1. AI Ops live records를 root canonical path로 cutover한다.
2. compliance / guard / hook / command 문서의 user-facing script examples를 root `scripts/*`로 정렬한다.
3. legacy `docs/ai-ops/*`는 live path와 historical/archive path로 분리한다.
4. redirect/bridge/stub와 removal condition을 함께 문서화한다.
5. 마지막으로 deletion readiness checklist를 새 canonical 기준으로 다시 평가한다.

#### 완료 기준

- canonical record path가 root `docs/*`로 고정되었다.
- canonical stable command path가 root `scripts/*`로 고정되었다.
- historical material에 대해 “삭제하지 않음 / live path와 분리 / frozen text 허용” 정책이 명시되었다.
- 다음 P3의 cutover 구현 범위가 해석 여지 없이 좁혀졌다.

### 7.18 P3 root canonical cutover implementation (2026-03-11)

#### 구현 목표

- P1에서 확정한 root canonical policy를 실제 repository layout에 반영한다.
- active live control-board와 user-facing stable command surface를 root namespace로 이동한다.
- legacy namespace는 live canonical이 아니라 compatibility/archive surface로 재정의한다.

#### 구현 내용

1. **root live records cutover**
   - root canonical 경로를 실제 live record로 채움:
     - `docs/CHANGELOG.md`
     - `docs/work-packets/index.md`
     - `docs/work-packets/WP-DPC-2026-03-001-ai-ops-bootstrap.md`
     - `docs/work-packets/WP-DPC-2026-03-002-codex-omx-alignment.md`
     - `docs/work-packets/WP-DPC-2026-03-003-framework-extraction.md`
     - `docs/adr/ADR-DPC-001..005`
   - active board는 root 경로를 기준으로 읽고 갱신하도록 정렬했다.
2. **legacy live-path bridge 전환**
   - 기존 active legacy path를 thin bridge/stub로 전환:
     - `docs/ai-ops/CHANGELOG.md`
     - `docs/ai-ops/work-packets/index.md`
     - active legacy WP 3건
     - `docs/ai-ops/adr/ADR-DPC-001..005`
   - closed historical packets는 당분간 `docs/ai-ops/work-packets/`에 retained archive로 남긴다.
3. **user-facing stable command path 정렬**
   - command / hook / policy / README 계열 문서의 operator-facing examples를 root `scripts/*` 기준으로 변경:
     - `scripts/set_process_context.py`
     - `scripts/check_compliance.py`
     - `scripts/launch_ai_ops_session.py`
     - `scripts/install_git_hooks.sh`
     - `scripts/sync_omc_policy.sh`
4. **hook / guard / githook 경로 정렬**
   - `.githooks/pre-commit`, `.githooks/pre-push`를 root compliance wrapper 기준으로 전환
   - `scripts/ai-ops/install_git_hooks.sh`가 root wrapper executable을 설치 대상으로 삼도록 조정
   - `scripts/ai-ops/claude_pretooluse_guard.py`와 `.claude/hooks/pretooluse-ai-ops-guard.py`가 root stable command path를 허용/안내하도록 정렬
5. **deletion-readiness documentation refresh**
   - `legacy-dependency-inventory.md`
   - `staged-migration-deletion-readiness-checklist.md`
   - 위 문서를 root canonical cutover 이후 상태로 갱신해 남은 blocker를 다시 좁힌다.

#### 구현 판단

- 이번 라운드는 `docs/ai-ops/*` 전체 삭제가 아니라,
  **live canonical을 root로 승격하고 legacy를 bridge/archive로 낮추는 단계**다.
- 따라서 deletion readiness 최종 판정은 아직 S1 리뷰에 남겨두되,
  다음 리뷰가 “무엇이 아직 blocker인가”만 보면 되도록 cutover ground를 먼저 만든다.

#### 검증 결과

- `python3 scripts/check_compliance.py --mode none --wp-file docs/work-packets/WP-DPC-2026-03-003-framework-extraction.md` → pass
- `python3 -m py_compile scripts/ai-ops/check_ai_ops_compliance.py scripts/ai-ops/claude_pretooluse_guard.py .claude/hooks/pretooluse-ai-ops-guard.py` → pass
- `python3 scripts/set_process_context.py --process P3 --wp WP-DPC-2026-03-003 --team-mode single` → pass
- `python3 scripts/launch_ai_ops_session.py --dry-run --launcher omx -- --model gpt-5` → pass

#### 후속 권장 프로세스

- `S1`
  - root canonical cutover가 실제로 self-consistent한지 검토
  - legacy namespace가 archive/bridge로 충분한지 검토
  - 최종 deletion readiness verdict를 재판정

### 7.19 S1 review result - root canonical cutover (2026-03-11)

#### 리뷰 범위

- root live records:
  - `docs/work-packets/*`
  - `docs/adr/*`
  - `docs/CHANGELOG.md`
- legacy bridge/archive files:
  - `docs/ai-ops/work-packets/*`
  - `docs/ai-ops/adr/*`
  - `docs/ai-ops/CHANGELOG.md`
- root stable command path + remaining implementation layer:
  - `scripts/*`
  - `scripts/ai-ops/*`

#### 확인한 점

1. **live control-board cutover 자체는 유효하다**
   - active index / WP / ADR / changelog의 live path가 root namespace로 승격되었다.
   - active adapter와 user-facing command examples도 root `scripts/*` 기준으로 정렬되었다.
2. **legacy bridge files는 충분히 얇다**
   - reviewed legacy WP/ADR/changelog/index는 live record가 아니라 canonical root path를 가리키는 bridge/stub 역할로 축소되었다.
3. **tooling path도 root stable command 기준으로 일관화되었다**
   - compliance, context, launch, githook examples는 root wrapper를 기준으로 동작한다.

#### 남은 핵심 blocker

1. **`docs/ai-ops/` 전체 삭제 readiness는 아직 미충족이다**
   - `docs/constitution.md`, `docs/ops-bootstrap-master-plan.md`, `docs/commands/ai-ops.md`,
     `docs/process-catalog/*`, `docs/tool-hooks/*`는 아직 root bridge일 뿐이고,
     authoritative content는 계속 `docs/ai-ops/*`에 남아 있다.
   - 즉 record cutover만으로는 `docs/ai-ops/` 전체 삭제 목표를 충족하지 못한다.
2. **`scripts/ai-ops/*`는 아직 implementation layer로 남아 있다**
   - stable command surface는 root `scripts/*`로 옮겼지만, 실제 구현은 여전히 legacy namespace에 의존한다.
3. **historical retained material의 최종 archive disposition이 아직 안 끝났다**
   - closed WP/discussion 문서를 현 위치에 둘지, dedicated archive로 재배치할지 후속 구현이 필요하다.

#### S1 판정

- **Approve (P3 cutover scope) / No-Go (deletion readiness)**
- 의미:
  - 이번 P3 구현 범위인 root live control-board cutover와 root stable command 정렬은 승인한다.
  - 하지만 source repo에서 `docs/ai-ops/`를 삭제해도 되는 상태는 아직 아니다.

#### 다음 권장 프로세스

- `P3`
  - root bridge 문서(`docs/constitution.md`, `docs/ops-bootstrap-master-plan.md`, `docs/commands/*`, `docs/process-catalog/*`, `docs/tool-hooks/*`)의 canonical 승격 또는 archive 분리를 결정/구현
  - `scripts/ai-ops/*` implementation layer 축소 또는 제거 전략 구현
  - historical retained material의 최종 archive 위치 확정
  - 그 후 deletion readiness를 다시 S1에서 재판정

### 7.20 P3 root SoT promotion / implementation collapse / archive disposition (2026-03-11)

#### 구현 범위

1. **non-record AI Ops SoT root 승격**
   - root canonical로 승격:
     - `docs/constitution.md`
     - `docs/ops-bootstrap-master-plan.md`
     - `docs/operating-model.md`
     - `docs/work-packet-spec.md`
     - `docs/goal-alignment-checklist.md`
     - `docs/commands/*`
     - `docs/process-catalog/*`
     - `docs/tool-hooks/*`
     - `docs/portability/ai-tool-artifact-boundary.md`
     - `docs/omc-config/*`
     - `docs/workspace-profiles/*`
   - 대응 legacy `docs/ai-ops/*`는 canonical content를 비우고 thin bridge/stub로 축소

2. **`scripts/ai-ops/*` implementation layer 축소**
   - root `scripts/*`가 실제 구현을 직접 소유하도록 전환:
     - `scripts/check_compliance.py`
     - `scripts/set_process_context.py`
     - `scripts/launch_ai_ops_session.py`
     - `scripts/install_git_hooks.sh`
     - `scripts/sync_omc_policy.sh`
   - legacy `scripts/ai-ops/*`의 위 5개 파일은 root로 forward하는 compatibility shim으로 축소
   - `scripts/ai-ops/claude_pretooluse_guard.py`는 tool-specific supporting asset로 계속 유지

3. **historical archive disposition 확정**
   - closed historical WP canonical archive:
     - `docs/archive/ai-ops/work-packets/WP-DPC-2026-03-002..007,009`
   - historical design source archive:
     - `docs/archive/ai-ops/ai-collaboration-guide.md`
   - legacy `docs/ai-ops/work-packets/WP-DPC-2026-03-002..007,009`는 archive redirect stub로 축소
   - `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md`,
     `docs/ai-ops/future-direction-discussion-2026-03-09.md`는 이번 라운드 사용자 제약에 따라 frozen in-place exception으로 명시

4. **control-board / deletion-readiness 문서 동기화**
   - `docs/work-packets/index.md`
   - `docs/CHANGELOG.md`
   - `docs/ai-ops/portability/legacy-dependency-inventory.md`
   - `docs/ai-ops/portability/staged-migration-deletion-readiness-checklist.md`

#### 구현 판단

- 이번 P3는 root live record cutover 이후 남아 있던 **non-record SoT / implementation ownership / archive path**
  세 축을 root/bridge/archive로 다시 정리하는 라운드다.
- 따라서 삭제 readiness의 핵심 blocker였던
  `root bridge only`, `legacy implementation ownership`, `historical archive 미정`은 모두 구현 측면에서는 해소되었다.
- 다만 hidden/local adapter surface(`.claude/*`, `.omc/*`, project skill metadata`)는 이번 라운드의 수정 대상이 아니므로,
  final deletion readiness verdict는 S1에서 다시 재판정하도록 남긴다.

#### 검증 결과

- `python3 scripts/check_compliance.py --mode none` → pass
- `python3 scripts/check_compliance.py --mode none --wp-file docs/work-packets/WP-DPC-2026-03-003-framework-extraction.md` → pass
- `python3 -m py_compile scripts/check_compliance.py scripts/set_process_context.py scripts/launch_ai_ops_session.py scripts/ai-ops/check_ai_ops_compliance.py scripts/ai-ops/set_process_context.py scripts/ai-ops/launch_ai_ops_session.py scripts/ai-ops/claude_pretooluse_guard.py` → pass
- `python3 scripts/launch_ai_ops_session.py --dry-run --launcher omx -- --model gpt-5` → pass
- `python3 scripts/ai-ops/launch_ai_ops_session.py --dry-run --launcher omx -- --model gpt-5` → pass

#### 다음 권장 프로세스

- `S1`
  - root canonical SoT 승격 범위가 self-consistent한지 검토
  - legacy bridge/shim/doc archive 예외가 충분히 얇고 안전한지 판정
  - source repo deletion readiness의 최종 pass/no-go를 다시 결정

### 7.21 S1 re-review result - post-P3 consistency fixes (2026-03-11)

#### 리뷰 범위

- live-path consistency fixes:
  - `docs/CHANGELOG.md`
  - `docs/work-packets/WP-DPC-2026-03-003-framework-extraction.md` references
  - `WORKSPACE-PROFILE.md`
  - `docs/omc-config/AI-OPS-POLICY.template.md` / `.omc/AI-OPS-POLICY.md`
  - `docs/adr/ADR-DPC-003-conditional-team-activation-and-optout.md`
  - `docs/adr/ADR-DPC-005-codex-entrypoint-ownership-and-ai-assistant-decoupling.md`
- root / legacy / archive split after the latest P3 fixes
- remaining compatibility / discussion-exception surfaces

#### 확인한 점

1. **root canonical 방향은 현재 self-consistent하다**
   - active operator-facing docs와 examples가 root `docs/*`, `scripts/*` 기준으로 정렬되었다.
   - targeted live-path link check가 통과했다.
2. **남은 legacy surface는 현재 의도된 잔존물이다**
   - `docs/ai-ops/*`는 bridge/stub, migration-review docs, frozen discussion exceptions 용도로 남아 있다.
   - `scripts/ai-ops/*`는 five command shim + `claude_pretooluse_guard.py` supporting asset 예외로 한정된다.
3. **따라서 구조 방향 승인과 물리 삭제 승인 여부를 분리해야 한다**
   - root canonical 아키텍처는 승인 가능하다.
   - 반면 legacy namespace의 즉시 물리 삭제는 아직 성급하다.

#### S1 판정

- **Approve (root canonical direction) / No-Go (immediate full legacy deletion)**

#### 다음 권장 프로세스

- `P1`
  - 남아 있는 `docs/ai-ops/*` bridge/review/discussion surface의 최종 제거 정책 확정
  - `scripts/ai-ops/*` shim 제거 시점과 `claude_pretooluse_guard.py` 처리 정책 확정
  - 최종 legacy removal criteria를 deletion-readiness checklist에 반영

### 7.22 S4 record - S1 re-review verdict fixed (2026-03-11)

#### 기록 내용

- 이번 라운드의 공식 판단을 다음과 같이 고정한다.
  1. **더 큰 목표는 portable framework를 위한 root canonical layout(`docs/*`, `scripts/*`) 정착이다.**
  2. 현재 source repo는 그 방향으로 정렬되었고, 이 구조 방향은 승인되었다.
  3. 그러나 `docs/ai-ops/*`와 `scripts/ai-ops/*`의 잔존 호환층은 아직 정책적으로 남겨둔 surface이므로, 즉시 삭제 대상으로 간주하지 않는다.

#### 남은 리스크 / TODO

- `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md`, `docs/ai-ops/future-direction-discussion-2026-03-09.md`의 최종 처리 정책 미확정
- `docs/ai-ops/portability/*` migration-review docs의 최종 거처 미확정
- `scripts/ai-ops/check_ai_ops_compliance.py`, `set_process_context.py`, `launch_ai_ops_session.py`, `install_git_hooks.sh`, `sync_omc_policy.sh` shim 제거 시점 미확정
- `scripts/ai-ops/claude_pretooluse_guard.py`를 supporting asset로 계속 둘지, 다른 위치로 승격/분리할지 미확정

#### 후속 권장 프로세스

- `P1` (final legacy removal policy refinement)

### 7.23 P1 final legacy removal policy (2026-03-11)

#### 목표

이번 P1의 목적은 “즉시 전면 삭제”가 아니라, **next P3에서 무엇을 제거/이동/보존할지와 그 이후 S1이 무엇을 판정해야 하는지**를 최종 고정하는 것이다.

#### 핵심 결정

1. **legacy namespace는 더 이상 장기 유지 surface가 아니다**
   - `docs/ai-ops/*`, `scripts/ai-ops/*`는 모두 next P3 이후에는 삭제 또는 archive/move 대상이다.
   - permanent live exception은 두지 않는다.
2. **discussion helper와 discussion record는 분리 처리한다**
   - `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md`는 helper 성격이므로 archive가 아니라 삭제한다.
   - `docs/ai-ops/future-direction-discussion-2026-03-09.md`는 historical discussion record이므로 archive로 이동한다.
3. **migration-review docs는 root canonical portability 문서가 아니다**
   - `legacy-dependency-inventory.md`, `staged-migration-deletion-readiness-checklist.md`는 source-repo transition review material이다.
   - 따라서 최종 거처는 `docs/portability/*`가 아니라 `docs/archive/ai-ops/migration-review/`다.
4. **five shim scripts는 next P3에서 제거한다**
   - `check_ai_ops_compliance.py`
   - `set_process_context.py`
   - `launch_ai_ops_session.py`
   - `install_git_hooks.sh`
   - `sync_omc_policy.sh`
   - 위 5개는 redirect-only shim이므로 archive 가치가 없고, historical trace는 WP/CHANGELOG에 남기면 충분하다.
5. **hook source는 삭제가 아니라 relocation 대상이다**
   - live file 기준으로는 `scripts/ai-ops/claude_pretooluse_guard.py`만 남아 있으므로, 이를 root-owned tool path(`scripts/hooks/*`)로 이동한다.
   - 이렇게 해야 `scripts/ai-ops/` 전체 제거가 가능하다.
6. **`claude_prompthouse_qa.py`는 현재 repo 기준 미존재 항목이다**
   - 2026-03-11 기준 current tree와 git history에서 확인되지 않았다.
   - 따라서 현재 blocker는 아니며, 나중에 Claude 전용 QA helper가 필요해도 `scripts/ai-ops/*` 아래로 두지 않는다.

#### 분류표 (제거 / 유지 / archive 이동)

| 대상 | 분류 | 최종 처리 |
|---|---|---|
| `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md` | 제거 대상 | next P3에서 삭제 |
| `docs/ai-ops/future-direction-discussion-2026-03-09.md` | archive 이동 대상 | `docs/archive/ai-ops/discussions/`로 이동 후 동결 |
| `docs/ai-ops/portability/legacy-dependency-inventory.md` | archive 이동 대상 | next P3 + S1 verdict 후 `docs/archive/ai-ops/migration-review/`로 이동 |
| `docs/ai-ops/portability/staged-migration-deletion-readiness-checklist.md` | archive 이동 대상 | next P3 + S1 verdict 후 `docs/archive/ai-ops/migration-review/`로 이동 |
| `docs/ai-ops/*` thin bridge/stub files | 제거 대상 | next P3에서 제거 |
| `scripts/ai-ops/check_ai_ops_compliance.py` | 제거 대상 | next P3에서 삭제 |
| `scripts/ai-ops/set_process_context.py` | 제거 대상 | next P3에서 삭제 |
| `scripts/ai-ops/launch_ai_ops_session.py` | 제거 대상 | next P3에서 삭제 |
| `scripts/ai-ops/install_git_hooks.sh` | 제거 대상 | next P3에서 삭제 |
| `scripts/ai-ops/sync_omc_policy.sh` | 제거 대상 | next P3에서 삭제 |
| `scripts/ai-ops/claude_pretooluse_guard.py` | 유지 아님 / 이동 대상 | root-owned `scripts/hooks/*`로 relocation 후 legacy copy 삭제 |
| `scripts/ai-ops/claude_prompthouse_qa.py` (if introduced later) | legacy 유지 금지 | root-owned or non-legacy experimental namespace only |

#### 다음 P3에서 실제 제거할 범위

1. `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md` 삭제
2. `docs/ai-ops/future-direction-discussion-2026-03-09.md` archive 이동
3. `docs/ai-ops/*` remaining bridge/stub surface 제거
4. `scripts/ai-ops/*` five shim scripts 삭제
5. `scripts/ai-ops/claude_pretooluse_guard.py` root-owned path로 이동 후 legacy copy 삭제
6. migration-review docs는 archive path로 이동하되, next S1 verdict가 PASS/NO-GO를 명시하도록 기록 구조 정리

#### 최종 legacy removal criteria

다음 조건을 모두 만족할 때만 “legacy removal complete”로 판정한다.

1. live/operator-facing AI Ops 경로가 모두 root `docs/*`, `scripts/*`만 사용한다.
2. `docs/ai-ops/*`에 live bridge/review/discussion surface가 남아 있지 않다.
3. `scripts/ai-ops/*`에 live shim/hook source가 남아 있지 않다.
4. frozen historical context는 `docs/archive/ai-ops/*`에 보존된다.
5. 삭제된 helper/shim의 history는 WP/CHANGELOG/archive material만으로 충분히 복원 가능하다.
6. next S1 review가 PASS verdict를 명시한다.

#### S1 리뷰용 조건

- live docs/adapters/scripts에서 legacy operational reference가 사라졌는지 확인
- `docs/archive/ai-ops/discussions/` 및 `docs/archive/ai-ops/migration-review/`에 필요한 history가 보존됐는지 확인
- `scripts/install_git_hooks.sh`와 관련 docs가 relocated hook source를 기준으로 동작하는지 확인
- five shim 삭제가 실제 운영 경로를 깨지 않는지 확인
- 최종 verdict를 PASS/NO-GO로 문서화

#### 다음 권장 프로세스

- `P3`
  - 위 정책을 실제 file move/delete/rewire로 구현
  - 구현 직후 `S1`에서 deletion readiness PASS/NO-GO를 최종 판정

### 7.24 P3 implementation - legacy namespace sunset (2026-03-11)

#### 구현 내용

1. **discussion / migration-review material archive 이동**
   - `docs/ai-ops/future-direction-discussion-2026-03-09.md`
     → `docs/archive/ai-ops/discussions/future-direction-discussion-2026-03-09.md`
   - `docs/ai-ops/portability/legacy-dependency-inventory.md`
     → `docs/archive/ai-ops/migration-review/legacy-dependency-inventory.md`
   - `docs/ai-ops/portability/staged-migration-deletion-readiness-checklist.md`
     → `docs/archive/ai-ops/migration-review/staged-migration-deletion-readiness-checklist.md`
2. **legacy helper / bridge namespace 삭제**
   - `docs/ai-ops/*` 전체 제거
   - `scripts/ai-ops/*` 전체 제거
3. **Claude hook source relocation**
   - `scripts/ai-ops/claude_pretooluse_guard.py`
     → `scripts/hooks/claude_pretooluse_guard.py`
   - `scripts/install_git_hooks.sh`를 새 root-owned hook source 기준으로 재배선
   - 관련 live docs를 새 path 기준으로 동기화

#### 분류 결과 반영

- 제거:
  - `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md`
  - `docs/ai-ops/work-packets/WP-DPC-2026-03-003-CONTINUE-P3-PROMPT.md`
  - remaining legacy bridge/stub docs
  - five redirect-only legacy shim scripts
- archive 이동:
  - future-direction discussion record
  - migration-review inventory/checklist
- root relocation:
  - Claude PreToolUse hook source

#### 구현 후 상태

1. live canonical AI Ops surface는 `docs/*`, `scripts/*`, `docs/archive/ai-ops/*`로 정리되었다.
2. `docs/ai-ops/*`, `scripts/ai-ops/*`에 대한 live 운영 의존은 제거됐다.
3. 남은 판단은 **S1에서 deletion readiness를 PASS로 볼 수 있는지**에 대한 최종 리뷰다.

#### 검증 결과

- `bash scripts/install_git_hooks.sh` → pass
- `python3 scripts/check_compliance.py --mode none` → pass
- `python3 scripts/check_compliance.py --mode none --wp-file docs/work-packets/WP-DPC-2026-03-003-framework-extraction.md` → pass
- `python3 -m py_compile scripts/check_compliance.py scripts/set_process_context.py scripts/launch_ai_ops_session.py scripts/hooks/claude_pretooluse_guard.py` → pass
- `python3 scripts/launch_ai_ops_session.py --dry-run --launcher omx -- --model gpt-5` → pass
- `rg -n "docs/ai-ops/|scripts/ai-ops/" .claude .codex .agents AGENTS.md docs scripts -g '!docs/archive/**' -g '!docs/CHANGELOG.md' -g '!docs/work-packets/**' -g '!**/.omx/**'`
  → live operational ref 0건, historical/policy mention만 잔존

#### 다음 권장 프로세스

- `S1`
  - legacy namespace sunset round의 deletion readiness PASS/NO-GO 최종 판정

### 7.25 S1 final review result - deletion readiness pass (2026-03-11)

#### 리뷰 범위

- `7693250` P3 legacy namespace sunset commit
- legacy tracked path removal 여부
- archive relocation completeness
- hook relocation + install/sync 정합성
- live operational surface의 non-legacy independence

#### 확인한 점

1. **legacy tracked path가 제거되었다**
   - `git ls-files 'docs/ai-ops/**' 'scripts/ai-ops/**'` 결과가 비어 있다.
2. **discussion / migration-review history가 archive로 보존되었다**
   - `docs/archive/ai-ops/discussions/future-direction-discussion-2026-03-09.md`
   - `docs/archive/ai-ops/migration-review/legacy-dependency-inventory.md`
   - `docs/archive/ai-ops/migration-review/staged-migration-deletion-readiness-checklist.md`
3. **Claude PreToolUse hook source relocation이 정상 동작한다**
   - `scripts/hooks/claude_pretooluse_guard.py` 존재
   - `.claude/hooks/pretooluse-ai-ops-guard.py`와 sync 일치 확인
   - `bash scripts/install_git_hooks.sh` pass
4. **live 운영 surface는 legacy namespace에 의존하지 않는다**
   - live ref scan 결과 operational dependency는 0건
   - 남은 문자열은 정책/역사 설명용 언급뿐이다.
5. **필수 검증이 모두 통과했다**
   - compliance check pass
   - py/AST validation pass
   - launch dry-run pass

#### S1 판정

- **PASS** — final deletion readiness approved

#### 후속 권장 프로세스

- `S4`
  - PASS verdict와 WP 종료 상태를 공식 기록으로 고정

### 7.26 S4 final record - WP completion fixed (2026-03-11)

#### 기록 내용

이번 라운드에서 다음을 공식 완료 상태로 고정한다.

1. root canonical AI Ops surface는 `docs/*`, `scripts/*`로 정착되었다.
2. legacy `docs/ai-ops/*`, `scripts/ai-ops/*`는 source repo live namespace에서 제거되었다.
3. 필요한 historical trace는 `docs/archive/ai-ops/*`에만 남긴다.
4. `WP-DPC-2026-03-003`의 final deletion readiness는 **PASS**다.
5. single-agent S4 기록은 reviewer/verifier evidence를 같은 세션에서 순차 수행한 검증 결과를 근거로 남긴다.

#### 최종 상태

- `status: DONE`
- `current_process: S4`
- `next_process: -`

## 8. Deliverables

- [x] P0: 자산 분류 맵
- [x] P0: 프레임워크 vs 프로젝트 종속 경계 문서
- [x] P0: 공개 불가 콘텐츠 검사
- [x] P1: 추출/포팅 요구사항 명세
- [x] P1: 설정 기반 접근 방식 확정
- [x] P1: 디렉토리 구조 확정
- [x] P3/C1: 기본 레포지토리 구조 생성
- [x] P3/C2: constitution / operating-model / process-catalog 일반화
- [x] P3/C3: commands / tool-hooks 일반화
- [x] P3/C4: 핵심 스크립트 일반화
- [x] P3/C5: CLI 스크립트 구현
- [x] P3/C6: 설정 스키마 및 템플릿 추가
- [x] P3/C7: 설치/포팅 가이드 완성
- [x] P3: 추출 구현
- [x] P3: CLI 스크립트 구현
- [x] P3: 템플릿 구현
- [x] P3: 포팅 가이드
- [x] P3 follow-up: target bootstrap completeness 보강
- [x] P3 follow-up: missing framework docs / helper scripts 보강
- [x] P3 follow-up: codex / project-ops / claude command-hook template coverage 확장
- [x] P3 follow-up: temp target bootstrap smoke + helper script 검증
- [x] P1 follow-up: canonical record path 정책 확정 (`docs/work-packets`, `docs/adr`, `docs/CHANGELOG.md`)
- [x] P1 follow-up: canonical stable command path 정책 확정 (`scripts/*`)
- [x] P1 follow-up: historical retention / redirect 정책 확정
- [x] P3 follow-up: legacy namespace sunset implementation
- [x] P3 follow-up: discussion / migration-review archive relocation
- [x] P3 follow-up: legacy bridge/shim physical removal
- [x] P3 follow-up: Claude PreToolUse hook source root relocation
- [x] P3 follow-up: root live control-board path cutover
- [x] P3 follow-up: root stable command examples 정렬
- [x] P3 follow-up: legacy active-path bridge/archive stub 적용
- [x] P3 follow-up: root non-record AI Ops SoT promotion
- [x] P3 follow-up: root stable command implementation ownership 이동
- [x] P3 follow-up: closed historical archive path finalization
- [x] S1 follow-up: P3 cutover review completed
- [x] S1 follow-up: post-P3 consistency re-review completed
- [ ] S1 follow-up: final deletion readiness verdict pass
- [ ] P1 follow-up: final legacy removal policy fixed

## 9. Risks

1. ~~프레임워크/프로젝트 경계가 모호~~ → P0에서 분류 완료
2. hidden/local adapter surface가 여전히 일부 legacy path를 품고 있을 수 있음 → S1에서 별도 판정 필요
3. 템플릿 엔진 학습 곡선 (Jinja2)

## 10. References

- [future-direction-discussion-2026-03-09.md](../ai-ops/future-direction-discussion-2026-03-09.md)
- [AI Tool Artifact Boundary](../portability/ai-tool-artifact-boundary.md)
- [constitution.md](../governance/constitution.md)
