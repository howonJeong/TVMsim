# TVMsim
 
고속철도 신호 시스템(TVM430 · 연동장치 · CTC)을 단순화해 구현한 Python 시뮬레이터
 
*A simplified Python simulator of high-speed railway signalling: TVM430 cab signalling, interlocking, and CTC.*
 
---
 
## 동기 · Motivation
 
2026년 11월, 경부고속선 동대구–경주 구간에서 열차 한 대가 고장 나면서 12시간 가까이 지연 여파가 있었음. 이 일을 계기로 고속철도가 열차 간격을 어떻게 유지하는지, 분기에서 충돌을 어떻게 막는지, 이상 상황을 누가 어떻게 처리하는지 궁금해짐.
 
이 프로젝트의 목표는 구조를 직접 만들어 보며 이해하는 것과, Python 언어와 생태계에 익숙해지는 것임.
 
> In November 2026, a single train failure between Dongdaegu and Gyeongju on the Gyeongbu High-Speed Line caused knock-on delays lasting nearly 12 hours. It made me curious how high-speed lines keep trains apart, how junctions prevent collisions, and who handles abnormal situations and how.
>
> This project aims to understand that system by building it, and to get comfortable with Python and its ecosystem along the way.
 
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
 
- [x]21Nov26 **1. 선로 모델 · Track Model** — YAML 배선 로딩, `Block` dataclass, 콘솔 출력
  <br>*Load layout from YAML, `Block` dataclass, console output*
- [x]22Nov26 **2. 점유 검지 · Occupancy Detection** — 열차 위치에 따른 점유 자동 갱신 (블록 두 개에 걸친 열차 포함)
  <br>*Automatic occupancy from train position, including trains spanning two blocks*
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