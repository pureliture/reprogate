# ReproGate 시나리오 카탈로그

> 관련 문서: [product-boundary.md](product-boundary.md)
> 이 문서는 ReproGate의 제품 바운더리 결정(In/Out)이 실제 사용자 상황에서 어떻게 동작하는지 구체화하는 15개의 시나리오를 정의한다. 

---

## 🏗 그룹 A: Workflow-first 시나리오

### SC-001: 표준 워크플로 완주
#### 맥락
- **시작 모드**: workflow
- **전환 여부**: 없음
- **세션 길이**: 단발 ~ 장기
- **저장 선호**: built-in
- **강제 수준**: Soft / Hard
#### 사용자의 거부 포인트
- 없음 (가장 순응적인 경로)
#### ReproGate 최소 개입
- 선언된 워크플로 단계별 순차 진행 안내 및 추적
#### ReproGate 필수 책임
- 각 단계별 산출물이 표준 포맷에 맞게 기록되었는지 검증 (Gate)
#### 허용 가능한 우회
- 단계 내 자유로운 대화 진행
#### 절대 허용 불가한 계약 위반
- 최종 단계 종료 전에 필수 기록(Context, Decision, Verification) 누락
#### 최종 산출물
- 완료된 작업 기록 단위 + 통과된 Gate 검증 로그
#### 추출 가능한 Skill
- 없음 (이미 워크플로화 됨)
#### 적용 가능한 Rule
- `record-required`, `decision-documented`, `verification-present`

### SC-002: 워크플로 단계 임의 수정 (Deviation Awareness)
#### 맥락
- **시작 모드**: workflow
- **전환 여부**: 있음 (진행 중 단계 변경)
#### 사용자의 거부 포인트
- "지금 이 단계는 우리 상황에 안 맞으니 빼고 진행할래."
#### ReproGate 최소 개입
- 단계 생략/수정을 차단하지 않고, **Deviation 사실 자체를 기록**
#### ReproGate 필수 책임
- 단계를 생략했더라도 재현성 계약(의사결정과 검증 흔적)이 유지되는지 Rule 재평가
#### 절대 허용 불가한 계약 위반
- 검증(Verification) 단계를 생략했는데 다른 방식으로도 검증 흔적을 남기지 않음
#### 적용 가능한 Rule
- 워크플로 이탈 감지 Rule 및 표준 검증 Rule

### SC-003: 도중 하차 (Workflow Abandonment)
#### 맥락
- **전환 여부**: workflow → freeform
#### 사용자의 거부 포인트
- "너무 복잡하다. 일단 구조는 무시하고 자유롭게 코딩할래."
#### ReproGate 필수 책임
- 억지로 진행을 막지 않고 freeform trace로 전환. 
- 단, commit 시점 또는 check 시점에 재현성 결손(CI-5) 기준 차단.
#### 최종 산출물
- 진행하다 중단된 워크플로 메타데이터 + 나머지 freeform trace.
- (마지막에 Late Binding 시 정상 기록으로 승격 가능)

---

## 🛠 그룹 B: Skill-first 시나리오

### SC-004: 단발성 Skill 호출 (Single-shot)
#### 맥락
- **시작 모드**: skill
- **세션 길이**: 단발
#### 사용자의 거부 포인트
- "전체 작업 구조는 필요 없고, 딱 `generate-rfc` 스킬만 쓸래."
#### ReproGate 최소 개입
- Skill 실행 및 결과 반환
#### ReproGate 필수 책임
- 해당 Skill이 언제 누구에 의해 호출되었는지 이력(Trace)에 남기고, 대상 기록 파일과 연결 (CI-3).
#### 절대 허용 불가한 계약 위반
- Skill 호출 이력이 증발함.

### SC-005: 연속된 Skill 사용 (Skill Chaining)
#### 맥락
- **시작 모드**: skill
- **세션 길이**: 장기
#### 사용자의 거부 포인트
- "워크플로 선언은 싫지만, 스킬은 여러 개 연달아 쓸래."
#### ReproGate 필수 책임
- 명시적 워크플로 선언이 없어도, 호출된 Skill의 체인을 분석하여 암묵적 상태(Emergent Flow)를 시각화 (P-7 Flowboard).

### SC-006: Skill에서 워크플로로 전환
#### 맥락
- **전환 여부**: skill → workflow
#### 사용자의 거부 포인트
- 처음에 단발성 스킬로 시작했다가, 작업이 커짐을 인지하고 "이거 그냥 정식 이슈 워크플로로 전환해줘."
#### ReproGate 필수 책임
- 기존 Skill Trace를 유지한 채 워크플로 Context에 병합 (Late Binding).

---

## 💬 그룹 C: Freeform-first 시나리오

### SC-007: 종료 전 일괄 승격 (Late Binding)
#### 맥락
- **시작 모드**: freeform
- **세션 길이**: 단발~장기
#### 사용자의 거부 포인트
- "작업할 땐 아무 간섭도 하지 마. 다 짜고 나서 구조화할래."
#### ReproGate 최소 개입
- 대화 및 프롬프트의 Raw Trace만 조용히 유지 (P-1).
#### ReproGate 필수 책임
- 세션 종료 또는 사용자 요청 시, Raw Trace에서 의사결정/검증 흔적을 추출해 정식 기록 단위로 승격시켜야 함 (CI-2).
#### 최종 산출물
- 깔끔하게 구조화된 작업 기록 파일 + 원본 Raw Trace 링크.

### SC-008: 대화 중 뜬금없는 Skill 호출
#### 맥락
- **전환 여부**: freeform → skill → freeform
#### 사용자의 거부 포인트
- 자유롭게 코딩하다가 "이 코드는 `review-security` 스킬로 검사만 한 번 해줘."
#### ReproGate 필수 책임
- 대화 문맥 끊김 없이 Skill을 실행하고, 해당 평가 결과를 현재 Freeform Trace 내에 삽입.

### SC-009: 철저히 구조를 거부하는 누적 세션
#### 맥락
- **세션 길이**: 누적 (다수 세션)
- **강제 수준**: Soft
#### 사용자의 거부 포인트
- "Skill도, 승격도 다 싫다. 며칠째 그냥 자유 대화만 할 거다."
#### ReproGate 필수 책임
- 구조화를 시도하진 않되, 주기적으로 "현재까지의 맥락이 사라질 위험"을 경고.
- 결국 PR/Commit 시점에는 재현성 결손(기록 부재)으로 차단 (CI-5).
#### 적용 가능한 Rule
- `record-required` (차단 발생)

### SC-010: Freeform에서 새로운 Skill 추출
#### 맥락
- **시작 모드**: freeform
#### 사용자의 거부 포인트
- 구조화된 틀을 안 썼지만 꽤 좋은 반복 패턴대로 대화함.
#### ReproGate 필수 책임
- 대화 종료 시, "이 작업 패턴을 새로운 Skill(예: `custom-debug-flow`)로 추출할까요?" 제안.
#### 추출 가능한 Skill
- 유저 고유의 프롬프트 전개 패턴.

---

## 💾 그룹 D: 저장 방식 커스터마이징 시나리오

### SC-011: Notion을 동기화 Source-of-Truth로 사용
#### 맥락
- **시작 모드**: external
- **저장 선호**: external
#### 사용자의 거부 포인트
- "기록은 좋지만, Markdown 파일 말고 우리 팀 Notion에 쌓을래."
#### ReproGate 필수 책임
- Notion 문서를 기반으로 메타데이터(identity, decision, verification)를 파싱하여 Rule 평가 (CI-4).
- ReproGate는 Notion의 저장 포맷을 통제하지 않음.

### SC-012: 순수 Git 커밋 메시지 기반 검증
#### 맥락
- **저장 선호**: external (Git)
- **강제 수준**: Hard (Pre-commit)
#### 사용자의 거부 포인트
- "파일을 새로 만드는 건 번거롭다. Commit Message를 상세히 썼으니 이걸로 통과시켜."
#### ReproGate 필수 책임
- Commit Message 파싱 Adapter를 통해 의사결정과 검증 흔적이 존재하는지 확인.
- Record Identity를 "Commit 단위"로 인정할 수 있도록 추상화.

### SC-013: Hybrid Storage (Issue Tracker + Local)
#### 맥락
- **저장 선호**: 혼합
#### 사용자의 거부 포인트
- "작업 목표(Context)는 Jira에 있고, 코드 검증 결과(Verification)는 로컬 `.md` 파일에 남길래."
#### ReproGate 필수 책임
- Canonical Metadata Layer를 통해 두 출처의 정보를 병합하여 Gate를 평가.
- Source-of-Truth 정책 결정을 강제하지 않음.

### SC-014: External CI Pipeline에서 Gate 단독 실행
#### 맥락
- **전환 여부**: 로컬에서 저장소(GitHub)로 업로드 후
- **강제 수준**: CI 연동
#### 사용자의 거부 포인트
- "로컬에서는 에러 뱉어서 무시하고 `git push --no-verify`로 강제 푸시했어."
#### ReproGate 필수 책임
- 로컬 생태계 없이도, 저장소에 푸시된 파일(Record)만으로 `reprogate check`가 독립 평가를 수행하여 CI 파이프라인에서 차단.
- (Rule 평가는 실행 환경과 무관해야 함)

### SC-015: 외부 도구를 프록시로 활용
#### 맥락
- **시작 모드**: external
#### 사용자의 거부 포인트
- "ReproGate CLI 안 쓸래. 내 IDE의 별도 AI 플러그인(Cursor 등)과 결합할래."
#### ReproGate 필수 책임
- Adapter를 통해 외부 도구의 실행 로그를 ReproGate Trace 형식으로 수신.
- Rule/Gate 평가는 외부 도구에 흡수되지 않고 철저히 ReproGate Core가 담당.
