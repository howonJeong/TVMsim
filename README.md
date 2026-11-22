# TVMsim
 
고속철도 신호 시스템(TVM430 · 연동장치 · CTC)을 단순화해 구현한 Python 시뮬레이터
 
*A simplified Python simulator of high-speed railway signalling: TVM430 cab signalling, interlocking, and CTC.*
 
---
 
## 동기 · Motivation
 
2026년 11월, 경부고속선 동대구–경주 구간에서 열차 한 대가 고장 나면서 12시간 가까이 지연 여파가 있었음. 이 일을 계기로 고속철도가 열차 간격을 어떻게 유지하는지, 분기에서 충돌을 어떻게 막는지, 이상 상황을 누가 어떻게 처리하는지 궁금해짐.
  
> In November 2026, a single train failure between Dongdaegu and Gyeongju on the Gyeongbu High-Speed Line caused knock-on delays lasting nearly 12 hours. It made me curious how high-speed lines keep trains apart, how junctions prevent collisions, and who handles abnormal situations and how.
>
> This project aims to understand that system by building it, and to get comfortable with Python and its ecosystem along the way.
 
---

## 목표 · Goals

예전에 비슷한 프로젝트를 AI에 전부 맡기는 바이브 코딩으로 시도한 적이 있음.
설명할 수 없었고, 결국 좌절했으므로, 이 프로젝트를 시작했다.

- **이해하며 만들기**: 모든 코드를 직접 작성하고, 왜 그렇게 짰는지 설명할 수 있을 것
- **Python 실력**: PS 위주의 C++ 경험에서 벗어나, Python과 그 생태계에 익숙해질 것
- **규모 있는 프로젝트 경험**: 모듈 분리, 클래스 설계, 버전 관리, 테스트 등
  한 파일짜리 풀이에서는 얻기 어려운 경험을 쌓을 것

> I once tried a similar project through pure "vibe coding", leaving everything to AI.
> The code grew, but I couldn't explain what I was building, and I ended up frustrated.
> This project started from the decision to do it differently.
>
> - **Build with understanding**: write every line myself and be able to explain why
> - **Python proficiency**: move beyond competitive-programming C++ and get fluent in Python and its ecosystem
> - **Real project experience**: module structure, class design, version control, and testing,
>   which single-file problem solving doesn't teach

---

 ## AI 활용 · Use of AI

이 프로젝트는 AI (Claude Opus 5.5)를 멘토처럼 활용하며 진행했다.
> 지침: PS 같은 코딩 문제나 스스로 사고가 필요한 문제를 풀다가 궁금증이 생겨 질문하면,
> 모든 정답을 알려줄 수 없다고 말하고 도와달라고 한 부분에 대해서만 도와줄 것.

This project was built with AI (Claude Opus 5.5) used as a mentor.
> Rule: When I ask about a coding problem or anything that requires my own thinking,
> do not give the full answer; help only with the specific part I ask about.*

- **도메인 학습**: TVM430, 연동장치, CTC, KTCS-2 등 철도 신호 개념 설명
- **설계 논의**: 자료구조, 클래스 구조, 모듈 분리 방향에 대한 피드백
- **코드 리뷰**: 작성한 코드의 버그와 개선점을 힌트 위주로 지적받음
- **문서·데이터 초안**: README 초안, 예시 배선 YAML

코드는 정답을 받지 않고 직접 작성하는 것을 원칙으로 했다.

>
> - **Domain learning**: explanations of railway signalling concepts (TVM430, interlocking, CTC, KTCS-2)
> - **Design discussion**: feedback on data structures, class design, and module layout
> - **Code review**: bugs and improvements pointed out mainly as hints
> - **Drafts**: README draft and the example track layout YAML
>
> As a rule, the code itself was written by me rather than copied from AI answers.

---

## 모델링 대상 · What It Models
 
| 계층 · Layer | 실제 시스템 · Real System | 이 프로젝트에서의 역할 · Role in This Project |
| --- | --- | --- |
| 선로 · Track | 폐색 구간, 분기기, 신호 · Block sections, switches, signals | 블록·분기기·신호를 노드로 하는 방향 그래프 · Directed graph of blocks, switches, and signals |
| 점유 검지 · Occupancy | 궤도회로 · Track circuits | 열차 위치로 블록 점유 상태 갱신 · Updates block occupancy from train positions |
| 연동장치 · Interlocking | 전자연동장치 · Electronic interlocking | 진로 설정 조건 검사, 쇄정·해정, 겹치는 진로 배제 · Route checks, locking/release, conflicting-route exclusion |
| 열차 방호 · Train Protection | TVM430 차내신호 · TVM430 cab signalling | 가장 가까운 정지점까지의 블록 수로 속도코드 계산 · Speed codes from block count to the nearest stop point |
| 열차 · Train | 차상 장치 + 기관사 · Onboard unit + driver | 가감속, 코드 추종, 과속 시 자동 제동 · Acceleration, code following, overspeed braking |
| 관제 · Control | CTC, 자동진로설정 · CTC, automatic route setting | 운행계획 기반 진로 요청, 수동 진로 변경 · Timetable-based route requests, manual overrides |
 
---

## 로드맵 · Roadmap
 
- [x] **1. 선로 모델 · Track Model** — YAML 배선 로딩, `Block` dataclass, 콘솔 출력 
  <br>*Load layout from YAML, `Block` dataclass, console output* - 21Nov26 finished
- [x] **2. 점유 검지 · Occupancy Detection** — 열차 위치에 따른 점유 자동 갱신 (블록 두 개에 걸친 열차 포함)
  <br>*Automatic occupancy from train position, including trains spanning two blocks* - 22Nov26 finished
- [ ] **3. 연동 로직 · Interlocking** — 진로 정의, 설정 조건, 쇄정·해정, 겹치는 진로 배제
  <br>*Route definitions, setting conditions, locking/release, conflict exclusion*
- [ ] **4. TVM 코드 계산 · TVM Speed Codes** — 정지점에서 거꾸로 따라가며 블록별 속도코드 부여
  <br>*Assign per-block speed codes by tracing back from stop points*
- [ ] **5. 열차 동역학 · Train Dynamics** — 가감속, 코드 추종, 과속 시 자동 제동
  <br>*Acceleration/braking, code following, automatic overspeed braking*
- [ ] **6. 시뮬레이션 루프 · Simulation Loop** — 위치 → 점유 → 코드 → 열차 제어 순서의 고정 틱 갱신
  <br>*Fixed-tick update: position → occupancy → codes → train control*
- [ ] **7. CTC 계층 · CTC Layer** — 운행계획 기반 자동진로설정, 수동 진로 요청
  <br>*Timetable-based automatic route setting, manual route requests*
- [ ] **8. 시각화 · Visualization** — pygame 렌더러
  <br>*pygame renderer*
- [ ] **9. 이상 상황 · Abnormal Scenarios** — 고장 열차, 진로 취소와 접근쇄정, 반대 선로 운행
  <br>*Failed trains, route cancellation with approach locking, wrong-line running*
---
 
## 프로젝트 구조 · Project Structure
 
```
TVMsim/
├── main.py           # 실행 진입점 · Entry point
├── simcore/          # 시뮬레이션 패키지 · Simulation package (track, interlocking, tvm, ctc, render)
├── data/             # 배선 YAML · Track layout YAML
├── tests/            # pytest
├── docs/             # 설계 노트 · Design notes
└── requirements.txt
```
 
---
 
## 기술 스택 · Tech Stack
 
- **Python 3.10+**
- **PyYAML** — 배선 데이터 · Track layout data
- **pytest** — 연동 규칙 테스트 (예정) · Interlocking rule tests (planned)
- **pygame** — 시각화 (예정) · Visualization (planned)
- **ruff** — 포맷팅, 린트 · Formatting and linting
---
 
## 참고 · Disclaimer
 
이 프로젝트는 학습용 시뮬레이터이다.
 
- 블록 길이를 일정하게 두고, 속도코드 단계는 단순화되었다.
- 실제 연동장치와 ATP는 SIL4 등급으로, 다중화 하드웨어와 형식 검증, 독립 안전 평가를 거친다. 이 프로젝트는 그런 안전 공학의 요구사항은 다루지 않는다 (못한다).
- 블록 단위 동작이 직관적인 TVM 방식을 먼저 구현하였다.
> This is a learning-oriented simulator.
>
> - Block lengths are kept uniform and speed-code steps are simplified.
> - Real interlockings and ATP systems are SIL4-rated, built on redundant hardware, formal verification, and independent safety assessment. This project does not (and cannot) address those safety-engineering requirements.
> - TVM was implemented first because its block-based behaviour is intuitive.

