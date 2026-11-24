21일
    1. 배운거
    pip freeze > requirements.txt로 패키지 프리즈
    Yaml 로딩 / 딕셔너리로 옮기기
    dataclass 활용법

    2. 한거
    선로 데이터 yaml에서 읽어온 후 dataclass로 변환
    모든 블럭 콘솔에 출력
    점유된 블록 출력

    3. 내일 
    열차 배차 시 노선 상 점유 갱신 - next 필드 추가하기

23일
    1. 배운거
    __str__ 정의 → print(obj), str(obj)에서 자동 호출
    __str__은 반드시 str 반환 (list 반환 시 TypeError)
    함수는 print 대신 문자열 반환 → 로그·테스트에 유리
    일반 클래스: __init__에서 self.x로 만든 변수는 인스턴스별, 클래스 본문 변수는 공유
    문자열은 불변 → join은 새 문자열 반환, 문자열 하나를 넘기면 글자 단위로 쪼개짐
        리스트에 모은 뒤 마지막에 join 한 번, 여러 줄은 '\n'.join
    순환 import 주의 → main이 track, train을 각각 import하는 단방향 구조

    2. 한거
    YAML에 next 추가, prev는 로딩 후 코드로 생성 (id 문자열로 연결)
    LinkedTrack 클래스 (일반 클래스)
        블록 dict 보관, connect_track으로 prev 채우기
        prev 없는 블록을 head 리스트로 (시작점 여러 개 대비)
        head부터 next 따라가며 시작점별 한 줄씩 출력
    simcore 패키지로 분리 (track.py, train.py), main.py는 조립만, 추후 simulation.py로 또 이사 예정
    Train 클래스: id, 선두 블록 id, 블록 시작점~선두 거리(head_offset), 길이
        점유 블록 목록은 저장하지 않고 계산
    점유 계산 함수: 선두에서 prev 따라가며 남은 길이 차감
        꼬리가 블록 경계에 딱 걸치면 이전 블록 미점유 (> 0)
        선로 시작점 밖으로 나가면 중단

    3. 내일
    점유 겹침(충돌) 검사
    TVM 속도코드 계산 시작
    (나중에) 
    YAML 검증: 없는 id 참조, 순환, head_offset > 블록 길이
    최소 차량 대수 맞춰서 2대인 지금은 괜찮은데 나중 위해 점유 함수가 열차 점유 블록 리스트를 일괄적으로 받는 솔루션 필요

24일
    1. 배운거
    분기기 개념
        분기기는 점이 아니라 길이가 있는 선로 구간, 자기 궤도회로를 가짐
        분기기 구간이 점유되면 전환 금지 (열차 밑에서 전환 = 탈선)
        역 밖에도 분기 있음: 건넘선(반대 선로 운행용), 노선 접속점, 차량기지 입출고선
    설계 원칙
        선로(Block)와 장치(Switch) 분리: 분기기 블록은 일반 Block, Switch는 방향·잠금 상태만
        같은 정보는 한 곳에만 기록, 반대쪽 참조는 로딩 시 코드로 채움 (next→prev, switch.block→block.switch_id)
        정위 = 블록의 next, 둘이 같은지 로딩 시 검증
        "다음 블록 구하기"는 반드시 메서드 하나를 거치게 (next 직접 읽으면 반위 무시 버그)
    Enum
        값으로 멤버 찾기: SwitchDir("REVERSE")
        bool보다 의미가 드러나고, 상태 추가(전환 중 등)가 쉬움
    is vs ==
        is: 같은 객체인지 (None, Enum 멤버에 사용)
        ==: 값이 같은지 (문자열·숫자·리스트는 반드시 ==)
    __post_init__: dataclass __init__ 직후 자동 호출, 타입 변환·검증용
        dict[키]는 None이 아니라 KeyError, 존재 확인은 in
        print("error") 대신 raise ValueError(무엇이 잘못됐는지)
    메서드 이름 앞 _ 는 클래스 내부용 관례, 같은 클래스 메서드는 self.method()로 호출
    Python 주석은 # (// 는 정수 나눗셈)

    2. 한거
    (23일 새벽) README 정리: 한/영 병기, 목표 섹션, AI 활용·사용 지침 섹션
    배선 YAML에 역 구내 추가
        W1T, W2T(분기기 블록), B14 1번선, B15 2번선, B16 유치선
        switches 섹션: W1, W2 (block, normal_next, reverse_next, direction)
    SwitchDir Enum, Switch dataclass (+ __post_init__ 문자열→Enum 변환)
    Block에 switch_id 필드 (YAML에는 안 적음)
    LinkedTrack
        switches 로딩, _validate_switches (블록 존재, 정위=next 검증)
        검증 후 블록에 switch_id 채우기
        connect_track: 반위 쪽 블록 prev도 채움 → head는 B1 하나
        next_block 메서드, __str__이 사용하도록 변경
    W1·W2 반위 출력 확인
    발견한 문제
        반위일 때 B14가 출력에서 사라짐 (점유돼 있어도 안 보임)
        분기기를 아무 때나 바꿀 수 있음 → B14 열차 있는데 W1 반위 가능 = 연동 필요

    3. 내일
    출력 형식 업그레이드 (전체 배선도)
        재귀(DFS)로 정위·반위 양쪽 출력, 줄 리스트 반환
        들여쓰기 폭 맞추기, =N=/=R= 표시, 선택 진로 굵은 선
    연동도표 YAML 설계
        signals 섹션 (신호 위치)
        routes: 시작 신호, 도착점, 필요한 분기기 방향, 경유 블록 (적을지 계산할지 결정)
    Interlocking 클래스 시작
    미뤄 둔 것: 점유 함수가 열차 리스트 받기, 점유 겹침 검사, 오늘 작업 커밋