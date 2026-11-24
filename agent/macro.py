_LEFT_WINDOW_X = 0.335
_RIGHT_WINDOW_X = 0.658
_WIDTH = _RIGHT_WINDOW_X - _LEFT_WINDOW_X

GOLD_POS = 0.603, 0.55, 0.645, 0.58
DIAMOND_POS = 0.47, 0.55, 0.53, 0.58
MEDAL_POS = 0.53, 0.55, 0.58, 0.58
WAVE_POS = 0.46, 0.01, 0.526, 0.027
WAVE_POS2 = 0.45, 0.285, 0.55, 0.35
TIMER_POS = 0.40, 0.55, 0.46, 0.578
REBIRTH_POS = 0.357, 0.129, 0.641, 0.321
CONTINUE_POS = 0.569, 0.429, 0.631, 0.491

_pos = {
    "프리셋 변경 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.1, 0.49),
    "첫번째 펫 버튼": ("click", _LEFT_WINDOW_X + 0.1, 0.66),
    "두번째 펫 버튼": ("click", _LEFT_WINDOW_X + 0.14, 0.66),
    "세번째 펫 버튼": ("click", _LEFT_WINDOW_X + 0.18, 0.66),
    "네번째 펫 버튼": ("click", _LEFT_WINDOW_X + 0.22, 0.66),
    "다섯번째 펫 버튼": ("click", _LEFT_WINDOW_X + 0.26, 0.66),
    "여섯번째 펫 버튼": ("click", _LEFT_WINDOW_X + 0.30, 0.66),
    "일곱번째 펫 버튼": ("click", _LEFT_WINDOW_X + 0.1, 0.7),
    "병사 레벨업 감소 펫 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.04, 0.66),

    "첫번째 유물 버튼": ("click", _LEFT_WINDOW_X + 0.06, 0.4),
    "두번째 유물 버튼": ("click", _LEFT_WINDOW_X + 0.11, 0.4),
    "세번째 유물 버튼": ("click", _LEFT_WINDOW_X + 0.16, 0.4),
    "네번째 유물 버튼": ("click", _LEFT_WINDOW_X + 0.21, 0.4),
    "다섯번째 유물 버튼": ("click", _LEFT_WINDOW_X + 0.26, 0.4),

    "첫번째 영웅 버튼": ("click", _LEFT_WINDOW_X + 0.06, 0.18),
    "두번째 영웅 버튼": ("click", _LEFT_WINDOW_X + 0.11, 0.18),
    "세번째 영웅 버튼": ("click", _LEFT_WINDOW_X + 0.16, 0.18),
    "네번째 영웅 버튼": ("click", _LEFT_WINDOW_X + 0.21, 0.18),
    "다섯번째 영웅 버튼": ("click", _LEFT_WINDOW_X + 0.26, 0.18),
    "프리셋 변경 저장 버튼": ("click", _LEFT_WINDOW_X + 0.12, 0.85),
    "프리셋 변경 취소 버튼": ("click", _LEFT_WINDOW_X + 0.2, 0.85),
    
    "2배 환생 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.12, 0.47),
    "이어하기 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.05, 0.45),

    "길드 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.05, 0.15),
    "건물 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.01, 0.97),
    "놀이터 버튼": ("click", _LEFT_WINDOW_X + 0.15, 0.49),
    "양궁 시작 버튼": ("click", _LEFT_WINDOW_X + 0.16, 0.65),
    "양궁 닫기 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.01, 0.13),
    "길드 닫기 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.01, 0.2),

    "퀘스트 탭": ("click", _LEFT_WINDOW_X + 0.03, 0.97),
    "스와이프": ("swipe", _LEFT_WINDOW_X + 0.03, 0.85, _LEFT_WINDOW_X + 0.03, 0.7, 0.1, 3),
    "정스와이프": ("swipe", _LEFT_WINDOW_X + 0.03, 0.68, _LEFT_WINDOW_X + 0.03, 0.75, 0.1, 1),
    "29 퀘스트 오픈 및 강화 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.04, 0.82),
    "30 퀘스트 오픈 및 강화 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.04, 0.89),
    "29 퀘스트 레벨업 맥스 버튼": ("click", _LEFT_WINDOW_X + 0.1, 0.82),
    "30 퀘스트 레벨업 맥스 버튼": ("click", _LEFT_WINDOW_X + 0.1, 0.88),

    "성 탭": ("click", _LEFT_WINDOW_X + 0.14, 0.97),
    "성 자동 강화 버튼": ("click", _LEFT_WINDOW_X + 0.03, 0.62),
    "성채 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.09, 0.6),
    "비서 버튼": ("click", _LEFT_WINDOW_X + 0.28, 0.65),
    "비서 확인 버튼": ("click", 0.49, 0.35),
    "비서 완료 버튼": ("click", _LEFT_WINDOW_X + 0.15, 0.82),

    "영웅 탭": ("click", _LEFT_WINDOW_X + 0.09, 0.97),
    "영웅 프리셋 활성화 버튼": ("click", 0.52, 0.6),
    "첫번째 영웅 프리셋 버튼": ("click", _LEFT_WINDOW_X + 0.04, 0.65),
    "두번째 영웅 프리셋 버튼": ("click", _LEFT_WINDOW_X + 0.10, 0.65),
    "세번째 영웅 프리셋 버튼": ("click", _LEFT_WINDOW_X + 0.16, 0.65),
    "네번째 영웅 프리셋 버튼": ("click", _LEFT_WINDOW_X + 0.22, 0.65),
    "다섯번째 영웅 프리셋 버튼": ("click", _LEFT_WINDOW_X + 0.28, 0.65),
    "영웅 프리셋 확인 버튼": ("click", _LEFT_WINDOW_X + 0.12, 0.35),

    "영웅 자동 강화 버튼": ("click", _LEFT_WINDOW_X + 0.055, 0.6),
    "영웅 강화 탭": ("click", _LEFT_WINDOW_X + 0.15, 0.6),
    "영웅 전체 선택 버튼": ("click", _LEFT_WINDOW_X + 0.04, 0.44),
    "영웅 1000 강화 버튼": ("click", _LEFT_WINDOW_X + 0.07, 0.9),
    "영웅 100 강화 버튼": ("click", _LEFT_WINDOW_X + 0.13, 0.9),
    "영웅 10 강화 버튼": ("click", _LEFT_WINDOW_X + 0.20, 0.9),
    "영웅 1 강화 버튼": ("click", _LEFT_WINDOW_X + 0.26, 0.9),

    "마지막 영웅 클릭": ("click", _LEFT_WINDOW_X + 0.09, 0.91),
    "영웅 상세 버튼": ("click", _LEFT_WINDOW_X + 0.03, 0.3),
    "영웅 해제 버튼": ("click", _LEFT_WINDOW_X + 0.2, 0.97),
    "영웅 닫기 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.01, 0.15),

    "병영 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.09, 0.6),
    "인간 종족 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.18, 0.6),
    "엘프 종족 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.15, 0.6),
    "언데드 종족 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.12, 0.6),
    "오크 종족 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.1, 0.6),
    "나가 배치 스와이프": ("swipe", _LEFT_WINDOW_X + 0.03, 0.8, _LEFT_WINDOW_X + 0.03, 0.65, 0.5, 3),
    "나가 배치 역스와이프": ("swipe", _LEFT_WINDOW_X + 0.03, 0.68, _LEFT_WINDOW_X + 0.03, 0.73, 0.5, 2),
    "영웅 나가 배치 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.02, 0.73),

    "영입 및 구매 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.04, 0.6),
    "영입 새로고침 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.12, 0.6),
    "영입 새로고침 실패 시 버튼": ("click", _LEFT_WINDOW_X + _WIDTH - 0.12, 0.47),

    "중앙 성": ("click", 0.5, 0.26),
    "영웅 배치 확인 버튼": ("click", 0.47, 0.55),
    "왼쪽 영웅": ("click", 0.45, 0.25),
    "왼쪽 대각 위 영웅": ("click", 0.46, 0.2),
    "왼쪽 위 영웅": ("click", 0.49, 0.18),
    "왼쪽 대각 아래 영웅": ("click", 0.46, 0.3),
    "왼쪽 아래 영웅": ("click", 0.49, 0.32),

    "오른쪽 영웅": ("click", 0.55, 0.25),
    "오른쪽 대각 위 영웅": ("click", 0.54, 0.2),
    "오른쪽 위 영웅": ("click", 0.51, 0.18),
    "오른쪽 대각 아래 영웅": ("click", 0.54, 0.3),
    "오른쪽 아래 영웅": ("click", 0.51, 0.32),

    "왼쪽 대각 아래 영웅 to 중앙": ("swipe", 0.46, 0.3, 0.5, 0.26, 0.5, 1),
    "왼쪽 아래 영웅 to 중앙": ("swipe", 0.49, 0.32, 0.5, 0.26, 0.5, 1),
    "오른쪽 대각 아래 영웅 to 중앙": ("swipe", 0.54, 0.3, 0.5, 0.26, 0.5, 1),
    "오른쪽 아래 영웅 to 중앙": ("swipe", 0.51, 0.32, 0.5, 0.26, 0.5, 1),

    "오른쪽 대각 위 영웅 to 왼쪽": ("swipe", 0.54, 0.2, 0.47, 0.29, 0.5, 1),
    "오른쪽 위 영웅 to 왼쪽 대각 아래": ("swipe", 0.51, 0.18, 0.5, 0.35, 0.5, 1),
    "오른쪽 대각 위 영웅 to 오른쪽 아래": ("swipe", 0.54, 0.2, 0.52, 0.35, 0.5, 1),

    "왼쪽 대각 위 영웅 뒤집기": ("swipe", 0.46, 0.2, 0.46, 0.35, 0.5, 1),
    "오른쪽 대각 위 영웅 뒤집기": ("swipe", 0.54, 0.2, 0.54, 0.35, 0.5, 1),
    "오른쪽 위 영웅 뒤집기": ("swipe", 0.51, 0.18, 0.51, 0.38, 0.5, 1),
}

_delay = {
    "매우 짧은 딜레이": ("delay", 0.2),
    "짧은 딜레이": ("delay", 1),
    "긴 딜레이": ("delay", 5),
}

def _custom_delay(secondes):
    return ("delay", secondes)

_sequence = {
    "영입 시퀀스": [
        _pos["영웅 탭"],
        _pos["영입 및 구매 버튼"],
        _pos["영입 새로고침 버튼"],
        _pos["영입 및 구매 버튼"],
        _pos["영입 새로고침 실패 시 버튼"],
        _pos["영웅 탭"],

        _delay["짧은 딜레이"],
    ],
    "비서 시퀀스": [
        _pos["성 탭"],
        _pos["성채 버튼"],
        _pos["비서 버튼"],

        _pos["비서 확인 버튼"],

        _custom_delay(1), _pos["비서 완료 버튼"],
        _custom_delay(1), _pos["비서 완료 버튼"],
        _custom_delay(1), _pos["비서 완료 버튼"],
        _custom_delay(1), _pos["비서 완료 버튼"],
        _custom_delay(1), _pos["비서 완료 버튼"],
        _custom_delay(1), _pos["비서 완료 버튼"],
        _custom_delay(1), _pos["비서 완료 버튼"],
        _custom_delay(1), _pos["비서 완료 버튼"],
        _custom_delay(1), _pos["비서 완료 버튼"],
        _custom_delay(1), _pos["비서 완료 버튼"],

        _pos["성 탭"],
        _pos["성 탭"],

        _custom_delay(1),
    ],
    "양궁 시퀀스": [
        _pos["길드 버튼"],
        _pos["건물 버튼"],
        _pos["놀이터 버튼"],
        _pos["양궁 시작 버튼"],
    ],
    "양궁 닫기 시퀀스": [
        _pos["양궁 닫기 버튼"],
        _pos["길드 닫기 버튼"],
    ],
    "영웅 및 성 강화 시퀀스": [
        _pos["성 탭"],
        _pos["성 자동 강화 버튼"],
        _delay["짧은 딜레이"],
        _pos["성 자동 강화 버튼"],

        _pos["영웅 탭"],
        _pos["영웅 자동 강화 버튼"],
        _delay["짧은 딜레이"],
        _pos["영웅 자동 강화 버튼"],

        _delay["짧은 딜레이"],
    ],
    "등반 프리셋 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["두번째 유물 버튼"],
        _pos["두번째 펫 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],

        _delay["짧은 딜레이"],
    ],
    "퀘스트 확장 프리셋 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["네번째 펫 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],

        _delay["짧은 딜레이"],
    ],
    "퀘스트 오픈 프리셋 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["네번째 유물 버튼"],
        _pos["세번째 펫 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],

        _delay["짧은 딜레이"],
    ],
    "병사 최대 레벨 증가 프리셋 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["첫번째 펫 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],
        
        _delay["짧은 딜레이"],
    ],
    "병사 레벨 증가 프리셋 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["여섯번째 펫 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],
        
        _delay["짧은 딜레이"],
    ],
    "병사 레벨업 감소 프리셋 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["다섯번째 유물 버튼"],
        _pos["일곱번째 펫 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],
        
        _delay["짧은 딜레이"],
    ],
    "퀘스트 골드 잠금 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["첫번째 영웅 버튼"],
        _pos["두번째 유물 버튼"],
        _pos["두번째 펫 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],

        _custom_delay(0.5),

        _pos["퀘스트 탭"],

        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["두번째 영웅 버튼"],
        _pos["두번째 유물 버튼"],
        _pos["두번째 펫 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],

        _custom_delay(0.5),
    ],
    "등반 영웅 프리셋 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["두번째 영웅 버튼"],
        _pos["두번째 유물 버튼"],
        _pos["두번째 펫 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],

        _delay["짧은 딜레이"],
    ],
    "퀘스트 스와이프 시퀀스": [
        _pos["퀘스트 탭"],
        _pos["스와이프"],
        _delay["짧은 딜레이"],
        _pos["스와이프"],
        _delay["짧은 딜레이"],
        _pos["스와이프"],
        _delay["짧은 딜레이"],

        _delay["짧은 딜레이"],
    ],
    "29 퀘스트 오픈 및 레벨업 시퀀스": [
        _pos["퀘스트 탭"],
        _pos["29 퀘스트 오픈 및 강화 버튼"],
        _pos["29 퀘스트 오픈 및 강화 버튼"],
        _pos["29 퀘스트 오픈 및 강화 버튼"],
        _pos["29 퀘스트 레벨업 맥스 버튼"],

        _delay["짧은 딜레이"],
    ],
    "30 퀘스트 오픈 및 레벨업 시퀀스": [
        _pos["퀘스트 탭"],
        _pos["30 퀘스트 오픈 및 강화 버튼"],
        _pos["30 퀘스트 오픈 및 강화 버튼"],
        _pos["30 퀘스트 오픈 및 강화 버튼"],
        _pos["30 퀘스트 레벨업 맥스 버튼"],

        _delay["짧은 딜레이"],
    ],
    "8000 영웅 프리셋 변경 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["두번째 영웅 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],

        _pos["영웅 탭"],
        _pos["영웅 자동 강화 버튼"],
        _pos["영웅 자동 강화 버튼"],

        _delay["짧은 딜레이"],
    ],
    "9000 영웅 프리셋 변경 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["네번째 영웅 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],

        _pos["영웅 탭"],
        _pos["영웅 자동 강화 버튼"],
        _pos["영웅 자동 강화 버튼"],

        _custom_delay(1),
    ],
    "9700 영웅 프리셋 변경 시퀀스": [
        _pos["성 탭"],
        _pos["프리셋 변경 버튼"],
        _pos["다섯번째 영웅 버튼"],
        _pos["세번째 유물 버튼"],
        _pos["프리셋 변경 저장 버튼"],
        _pos["프리셋 변경 취소 버튼"],

        _custom_delay(1),
    ],
    "테스트 시퀀스": [
        _pos["성 탭"],

        _custom_delay(1),
    ]
}

macros = {
    "양궁 시작": {"name": "양궁 시작", "data": [
        {"name": "양궁 시작", "sequence": _sequence["양궁 시퀀스"]}
    ]},
    "양궁 끝": {"name": "양궁 끝", "data": [
        {"name": "양궁 끝", "sequence": _sequence["양궁 닫기 시퀀스"]}
    ]},
    "영입": {"name": "영입", "data": [
        {"name": "영입", "sequence": _sequence["영입 시퀀스"]}
    ]},
    "비서": {"name": "비서", "data": [
        {"name": "비서", "sequence": _sequence["비서 시퀀스"]}
    ]},
    "등반 영웅 프리셋": {"name": "등반 영웅 프리셋", "data": [
        {"name": "등반 영웅 프리셋", "sequence": _sequence["등반 영웅 프리셋 시퀀스"]}
    ]},
    "영웅 및 성 강화": {"name": "영웅 및 성 강화", "data": [
        {"name": "영웅 및 성 강화", "sequence": _sequence["영웅 및 성 강화 시퀀스"]}
    ]},
    "퀘스트 29 레벨업": {"name": "퀘스트 29 레벨업", "data": [
        {"name": "퀘스트 확장 프리셋", "sequence": _sequence["퀘스트 확장 프리셋 시퀀스"]},
        {"name": "퀘스트 레벨업 딜레이", "sequence": [_custom_delay(10)]},
        {"name": "퀘스트 골드 잠금", "sequence": _sequence["퀘스트 골드 잠금 시퀀스"]},
    ]},
    "퀘스트 30 오픈": {"name": "퀘스트 30 오픈", "data": [
        {"name": "퀘스트 오픈 프리셋", "sequence": _sequence["퀘스트 오픈 프리셋 시퀀스"]},
        {"name": "딜레이", "sequence": [_custom_delay(5)]},
        {"name": "퀘스트 골드 잠금", "sequence": _sequence["퀘스트 골드 잠금 시퀀스"]},
    ]},
    "퀘스트 30 레벨업": {"name": "퀘스트 30 레벨업", "data": [
        {"name": "퀘스트 확장 프리셋", "sequence": _sequence["퀘스트 확장 프리셋 시퀀스"]},
        {"name": "딜레이", "sequence": [_custom_delay(10)]},
        {"name": "등반 프리셋", "sequence": _sequence["등반 프리셋 시퀀스"]},
    ]},
    "웨이브 8000": {"name": "8000 웨이브", "data": [
        {"name": "병사 레벨업 감소 프리셋", "sequence": _sequence["병사 레벨업 감소 프리셋 시퀀스"]},
        {"name": "8000 영웅 프리셋 변경", "sequence": _sequence["8000 영웅 프리셋 변경 시퀀스"]},
        {"name": "등반 프리셋", "sequence": _sequence["등반 프리셋 시퀀스"]},
    ]},
    "웨이브 9000": {"name": "9000 웨이브", "data": [
        {"name": "병사 레벨업 감소 프리셋", "sequence": _sequence["병사 레벨업 감소 프리셋 시퀀스"]},
        {"name": "9000 영웅 프리셋 변경", "sequence": _sequence["9000 영웅 프리셋 변경 시퀀스"]},
        {"name": "등반 프리셋", "sequence": _sequence["등반 프리셋 시퀀스"]},
        {"name": "병사 레벨 증가 프리셋", "sequence": _sequence["병사 레벨 증가 프리셋 시퀀스"]},
    ]},
    "웨이브 9700": {"name": "9700 웨이브", "data": [
        {"name": "9700 영웅 프리셋 변경", "sequence": _sequence["9700 영웅 프리셋 변경 시퀀스"]},
    ]},
    "테스트": {"name": "테스트", "data": [
        {"name": "테스트", "sequence": _sequence["테스트 시퀀스"]}
    ]}
}

multi_macros = {
    "자동 환생": {"name": "자동 환생", "data": {
        "rebirth": [
            {"name": "환생"},
        ],

        "time": [
            {"name": "등반 프리셋 변경", 
             "goal": "00:00",
             "sequence": macros["등반 영웅 프리셋"]["data"],
             "ignore": {"condition": "wave", "type": "higher", "goal": 9000}},

            {"name": "영입", 
             "goal": "00:00",
             "sequence": macros["영입"]["data"]},

            {"name": "영웅 및 성 강화", 
             "goal": "00:35",
             "sequence": macros["영웅 및 성 강화"]["data"],
             "ignore": {"condition": "gold", "type": "higher", "goal": "50ao"}},

            {"name": "비서", 
             "goal": "01:00",
             "sequence": macros["비서"]["data"]},

            {"name": "영입", 
             "goal": "15:00",
             "sequence": macros["영입"]["data"]},

            {"name": "영입", 
             "goal": "30:00",
             "sequence": macros["영입"]["data"]},
        ],

        "gold": [
            {"name": "퀘스트 29 레벨업", 
            "goal": "3ao",
            "sequence": macros["퀘스트 29 레벨업"]["data"],
            "ignore": {"condition": "gold", "type": "higher", "goal": "1ap"}},

            {"name": "영웅 및 성 강화", 
             "goal": "1an",
             "sequence": macros["영웅 및 성 강화"]["data"],
             "ignore": {"condition": "wave", "type": "higher", "goal": 8000}},

            {"name": "퀘스트 30 오픈", 
             "goal": "130ao",
             "sequence": macros["퀘스트 30 오픈"]["data"],
             "ignore": {"condition": "gold", "type": "higher", "goal": "1ap"}},

            {"name": "영웅 및 성 강화", 
             "goal": "1au",
             "sequence": macros["영웅 및 성 강화"]["data"],
             "ignore": {"condition": "wave", "type": "higher", "goal": 8500}},

            {"name": "퀘스트 30 레벨업",
             "goal": "300au",
             "sequence": macros["퀘스트 30 레벨업"]["data"],
             "ignore": {"condition": "wave", "type": "higher", "goal": 9000}},
        ],

        "wave": [
            {"name": "웨이브 9000",
             "goal": 9200,
             "sequence": macros["웨이브 9000"]["data"],
             "ignore": {"condition": "wave", "type": "higher", "goal": 9700}},

            {"name": "웨이브 9700",
             "goal": 9705,
             "sequence": macros["웨이브 9700"]["data"]},
        ],
    }},
    "양궁": {"name": "양궁", "data": {
        "empty": [
            {"name": "양궁 시작", "sequence": macros["양궁 시작"]["data"]},

            {"name": "양궁",
             "condition": "custom",
             "goal": 0,
             "sequence": ""},

            {"name": "양궁 끝", "sequence": macros["양궁 끝"]["data"]},
        ]
    }},
    "테스트": {"name": "테스트", "data": {
        "gold": [
            {"name": "테스트", "goal": "1an", "sequence": macros["테스트"]["data"]},
        ]
    }}
}