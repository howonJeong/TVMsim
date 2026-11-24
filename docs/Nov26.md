# 개발 노트

## 11/21

### 배운 것
- `pip freeze > requirements.txt`로 패키지 목록 기록
- YAML 로딩 → dict로 변환
- dataclass 기본 사용법

### 한 것
- 선로 YAML을 읽어 `Block` dataclass로 변환
- 블록 전체 콘솔 출력, 점유 블록 표시

### 다음
- 열차 배치 시 점유 갱신, `next` 필드 추가

---

## 11/23

### 배운 것
- `__str__`: `print()`, `str()`에서 자동 호출. 반드시 `str` 반환
- 함수는 `print`보다 문자열 반환이 낫다 (로그·테스트)
- `__init__`의 `self.x`는 인스턴스별, 클래스 본문 변수는 공유
- 문자열은 불변. `join`은 새 문자열 반환 → 리스트에 모은 뒤 한 번만 `join`
- 순환 import 주의: `main`이 `track`, `train`을 각각 import하는 단방향 구조로

### 한 것
- YAML에 `next` 추가, `prev`는 로딩 후 코드로 생성
- `LinkedTrack` 클래스: 블록 보관, `prev` 연결, `head`(시작점)부터 순서대로 출력
- `simcore` 패키지로 분리 (`track.py`, `train.py`). 나중에 `simulation.py`로 옮길 예정
- `Train`: id, 선두 블록, 블록 시작점~선두 거리, 길이. 점유 목록은 저장하지 않고 계산
- 점유 계산: 선두에서 `prev`를 따라가며 길이 차감
  - 꼬리가 블록 경계에 딱 걸치면 이전 블록은 미점유
  - 선로 시작점을 넘으면 중단

### 다음
- 점유 겹침(충돌) 검사
- TVM 속도코드 계산
- 나중에: YAML 검증 (없는 id, 순환, `head_offset` 범위), 점유 함수가 여러 열차를 한 번에 받도록

---

## 11/24

### 배운 것
- **분기기**: 점이 아니라 길이가 있는 선로 구간. 점유 중이면 전환 금지 (탈선 방지)
- 역 밖에도 분기가 있다: 건넘선, 노선 접속점, 차량기지 입출고선
- **설계 원칙**
  - 선로(`Block`)와 장치(`Switch`) 분리
  - 같은 정보는 한 곳에만 적고, 반대쪽 참조는 로딩 때 코드로 채운다
  - 정위 = 블록의 `next`. 일치 여부는 로딩 때 검증
  - 다음 블록은 반드시 `next_block()`을 거쳐서 구한다
- `Enum`: `SwitchDir("REVERSE")`처럼 값으로 멤버 찾기. bool보다 의미가 분명함
- `is`는 같은 객체 (`None`, Enum), `==`는 같은 값 (문자열·숫자는 항상 `==`)
- `__post_init__`: dataclass 생성 직후 호출. 타입 변환·검증용
  - YAML은 `REVERSE`를 문자열로 읽고, dataclass는 변환해 주지 않음
- 에러 처리: `dict[키]`는 KeyError → 존재 확인은 `in`. `print` 대신 `raise ValueError`
- 메서드 앞 `_`는 내부용 관례. 주석은 `#` (`//`는 정수 나눗셈)

### 한 것
- (11/23 새벽) README 정리: 한/영 병기, 목표, AI 활용 섹션
- YAML에 역 구내 추가: 분기기 블록 `W1T`·`W2T`, 1번선 `B14`, 2번선 `B15`, 유치선 `B16`, `switches` 섹션
- `SwitchDir` Enum, `Switch` dataclass, `Block.switch_id`
- `LinkedTrack`: 분기기 로딩·검증, `switch_id` 채우기, 반위 쪽 `prev` 연결, `next_block()`
- 반위 출력 확인
- 발견한 문제
  - 반위일 때 `B14`가 출력에서 사라짐
  - 분기기를 아무 때나 바꿀 수 있음 → 연동 필요

### 다음
- 전체 배선도 출력: 재귀로 양쪽 분기 출력, 들여쓰기 정렬, `N`/`R` 표시
- 연동도표 YAML: `signals`, `routes` (시작 신호, 도착점, 분기기 방향, 경유 블록)
- `Interlocking` 클래스 시작
- 미뤄 둔 것: 여러 열차 점유 처리, 점유 겹침 검사, 커밋