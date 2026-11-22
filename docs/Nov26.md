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

22일
    22일
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
