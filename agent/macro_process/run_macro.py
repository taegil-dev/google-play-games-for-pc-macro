import copy
from pathlib import Path
import sys
from typing import Any
import datetime

import env_data.env_data as env
import image_match.image_match as im
import macro_click.macro_click as mc
import macro_process.arrow_target_macro as atm


BASE_DIR = getattr(sys, "frozen", False) and Path(sys.executable).resolve().parent or Path(__file__).resolve().parent.parent

image_matcher = im.ImageMatcher()
templates_dir = BASE_DIR / "templates"

image_matcher.load_template("rebirth", templates_dir / "rebirth.jpg")
image_matcher.load_template("continue", templates_dir / "continue.jpg")
image_matcher.load_template("continue_end", templates_dir / "continue_end.jpg")
image_matcher.load_template("arrow_target", templates_dir / "arrow_target.jpg")


def rebirth(thread_var):
    # 환생 버튼
    mc.click(thread_var.macro_stop, 0.538, 0.47, show_marker=False)
    thread_var.macro_stop.wait(5)

    # 영웅 탭
    mc.click(thread_var.macro_stop, 0.344, 0.97, show_marker=False)
    thread_var.macro_stop.wait(1)


def continue_game(thread_var):
    # 이어하기 버튼
    mc.click(thread_var.macro_stop, 0.608, 0.45, show_marker=False)
    thread_var.macro_stop.wait(0.2)

    # 중앙 성
    for _ in range(18):
        mc.click(thread_var.macro_stop, 0.5, 0.26, show_marker=False)


def rebirth_sequence(thread_var, pos):
    # 이어하기 체크
    _continue = im.check_continue(image_matcher, pos["CONTINUE_POS"])

    # 매크로 결과에 넣을 웨이브 탐지 단, 환생창이 있을 경우 중앙 웨이브 탐지를 하지 못하므로 비교는 하지 않는다
    wave = im.check_floor(pos["WAVE_POS"], pos["WAVE_POS2"], compare=False)

    print(f'{datetime.datetime.now().strftime("%H:%M")} - ⚠️ 현재 웨이브: {wave}, 환생 감지; {_continue and "🔁 이어하기" or "❇️ 환생"}')

    thread_var.macro_stop.wait(1)
    if _continue:
        continue_game(thread_var)
        return False, wave
    
    rebirth(thread_var)
    return True, wave

def ignore_condition(
        sequence_name: str,
        ignore: dict[str, Any], 
        pos: dict[str, tuple[float, float, float, float]]
    ) -> bool:
    if not ignore:
        return False
    
    if ignore['condition'] == 'wave':
        floor = im.check_floor(pos['WAVE_POS'], pos['WAVE_POS2'])
        if floor is None:
            return False
        
        if(ignore['type'] == 'lower' and floor < ignore['goal']):
            print(f'{datetime.datetime.now().strftime("%H:%M")} - ❌ {sequence_name} 무시; 현재 웨이브 {floor} < 목표 웨이브 {ignore["goal"]}')
            return True
        
        elif (ignore['type'] == 'higher' and floor > ignore['goal']):
            print(f'{datetime.datetime.now().strftime("%H:%M")} - ❌ {sequence_name} 무시; 현재 웨이브 {floor} > 목표 웨이브 {ignore["goal"]}')
            return True
        
    elif ignore['condition'] == 'gold':
        gold_info = im.check_gold(pos['GOLD_POS'])
        if not gold_info:
            return False
        
        gold_str = f"{gold_info['value']}{gold_info['unit']}"
        result = im.compare_gold(gold_str, ignore['goal'])
        if(ignore['type'] == 'lower'):
            if not result:
                print(f'{datetime.datetime.now().strftime("%H:%M")} - ❌ {sequence_name} 무시; 현재 골드 {gold_str} < 목표 골드 {ignore["goal"]}')
                return True
        
        elif (ignore['type'] == 'higher'):
            if result:
                print(f'{datetime.datetime.now().strftime("%H:%M")} - ❌ {sequence_name} 무시; 현재 골드 {gold_str} > 목표 골드 {ignore["goal"]}')
                return True
        
    return False

def run_sequence(thread_var, sequences, image_region):
    is_rebirth = False
    for sequence in sequences:
        if thread_var.shutdown.is_set() or thread_var.macro_stop.is_set():
            break

        # 재실행 감지 용 반복문
        while True:
            restart = False
            for pos in sequence.get("sequence", []):
                # 시퀀스 딜레이
                thread_var.macro_stop.wait(env.SEQUENCE_DELAY)

                if thread_var.shutdown.is_set() or thread_var.macro_stop.is_set():
                    break

                # 게임 재실행
                if thread_var.restart.is_set():
                    print(f'{datetime.datetime.now().strftime("%H:%M")} - ⛔ 매크로 일시중지; 게임 재실행 중')
                    # 매크로를 잠시 멈춤
                    while thread_var.restart.is_set():
                        continue

                    print(f'{datetime.datetime.now().strftime("%H:%M")} - 🚥 매크로 재시작')
                    # 재실행 시 시퀀스 처음부터 다시 시작
                    restart = True
                    break

                # 환생 체크
                result = im.check_rebirth(image_matcher, image_region["REBIRTH_POS"])
                if result:
                    check = rebirth_sequence(thread_var, image_region)
                    # 이어하기
                    if not check[0]:
                        continue
                    # 환생
                    is_rebirth = True
                    break


                if pos[0] == "click":
                    mc.click(
                        thread_var.macro_stop,
                        pos[1], 
                        pos[2],
                        show_marker=False
                    )
                elif pos[0] == "swipe":
                    mc.swipe(
                        thread_var.shutdown,
                        thread_var.macro_stop,
                        pos[1], 
                        pos[2], 
                        pos[3], 
                        pos[4], 
                        pos[5], 
                        pos[6],
                        show_marker=False
                    )
                elif pos[0] == "delay":
                    thread_var.macro_stop.wait(pos[1])

            # 중간에 멈출 시 다시 시작
            if restart:
                continue
            # 재실행이 아닐 시 while문 탈출
            break

    return is_rebirth


def run_macro(thread_var, macro, region):
    # 서로 다른 조건들을 가진 시퀀스들을 전부 실행; 단, 먼저 조건이 충족된 시퀀스만 실행, 순자적 실행
    condition_wave = copy.deepcopy(macro.get("wave", None))
    condition_gold = copy.deepcopy(macro.get("gold", None))
    condition_time = copy.deepcopy(macro.get("time", None))
    condition_custom = copy.deepcopy(macro.get("custom", None))
    condition_empty = copy.deepcopy(macro.get("empty", None))
    condition_rebirth = copy.deepcopy(macro.get("rebirth", None))

    # 전부 포함이 안된다면 일반 매크로
    is_normal_macro = not any([condition_wave, condition_gold, condition_time, condition_custom, condition_empty, condition_rebirth])

    wave = 0
    is_rebirth = False
    while not thread_var.shutdown.is_set() and not thread_var.macro_stop.is_set():
        # 매크로 전부 실행 완료
        if not any([condition_wave, condition_gold, condition_time, condition_custom, condition_empty, condition_rebirth]):
            break

        # 매크로 딜레이
        thread_var.macro_stop.wait(env.MACRO_DELAY)
        
        # 게임 재실행
        if thread_var.restart.is_set():
            print(f'{datetime.datetime.now().strftime("%H:%M")} - ⛔ 매크로 일시중지; 게임 재실행 중')
            while thread_var.restart.is_set():
                continue

            print(f'{datetime.datetime.now().strftime("%H:%M")} - 🚥 매크로 재시작')
            continue

        # 시퀀스 돌리다가 환생한 상태
        if is_rebirth:
            return wave, is_rebirth

        # 환생 체크
        result = im.check_rebirth(image_matcher, region["REBIRTH_POS"])
        if result:
            is_rebirth, wave = rebirth_sequence(thread_var, region)
            # 이어하기
            if not is_rebirth:
                continue

        # 단일 매크로는 조건 매크로가 없으므로 바로 실행
        if is_normal_macro:
            is_rebirth = run_sequence(thread_var, macro, region)
            break

        # 웨이브 조건 체크
        if condition_wave:
            goal = condition_wave[0].get("goal", 0)
            name = condition_wave[0].get("name", "Unnamed Sequence")
            ignore = condition_wave[0].get("ignore", None)

            # 웨이브를 확인하는 절차; 상단 웨이브는 뿔피리, 엘비에 따라 숫자가 이상하게 생길 수 있으므로 중앙 웨이브랑 비교하여 한번 걸러냄
            floor = im.check_floor(region["WAVE_POS"], region["WAVE_POS2"])
            if floor:
                if floor >= goal:
                    # 실행한 시퀀스 제거
                    sequence = condition_wave.pop(0)
                    if not ignore_condition(name, ignore, region):
                        print(f'{datetime.datetime.now().strftime("%H:%M")} - 🔔 현재 웨이브 {floor} : 목표 웨이브 {goal}')
                        print(f'{datetime.datetime.now().strftime("%H:%M")} - ▶️ 시퀀스 {name} 실행')
                        is_rebirth = run_sequence(thread_var, sequence['sequence'], region)

        # 골드 조건 체크
        if condition_gold:
            goal = condition_gold[0].get("goal", "1a")
            name = condition_gold[0].get("name", "Unnamed Sequence")
            ignore = condition_gold[0].get("ignore", None)

            # 여러번 확인
            check = False
            for _ in range(2):
                # 골드는 숫자와 단위로 감지
                gold = im.check_gold(region["GOLD_POS"])
                if gold:
                    gold_str = f"{gold['value']}{gold['unit']}"

                    # 골드 비교는 문자열로 비교 "100az"
                    if im.compare_gold(gold_str, goal):
                        check = True
                    else:
                        check = False
                        break

                thread_var.macro_stop.wait(0.5)

            if check:
                # 실행한 시퀀스 제거
                sequence = condition_gold.pop(0)
                if not ignore_condition(name, ignore, region):
                    print(f'{datetime.datetime.now().strftime("%H:%M")} - 🔔 현재 골드 {gold_str} : 목표 골드 {goal}')
                    print(f'{datetime.datetime.now().strftime("%H:%M")} - ▶️ 시퀀스 {sequence["name"]} 실행')
                    is_rebirth = run_sequence(thread_var, sequence['sequence'], region)

        # 시간 조건 체크
        if condition_time:
            goal = condition_time[0].get("goal", "00:00")
            name = condition_time[0].get("name", "Unnamed Sequence")
            ignore = condition_time[0].get("ignore", None)

            # (초, 분, 시)의 정수 튜플 반환
            current_time = im.check_time(region["TIMER_POS"])

            # 튜플과 문자열로 비교 00:00:00
            if im.compare_time(current_time, goal):
                # 실행한 시퀀스 제거
                sequence = condition_time.pop(0)
                if not ignore_condition(name, ignore, region):
                    print(f'{datetime.datetime.now().strftime("%H:%M")} - 🔔 현재 시간 {current_time[2] < 10 and "0" or ""}{current_time[2]}:{current_time[1] < 10 and "0" or ""}{current_time[1]}:{current_time[0] < 10 and "0" or ""}{current_time[0]} : 목표 시간 {goal}')
                    print(f'{datetime.datetime.now().strftime("%H:%M")} - ▶️ 시퀀스 {sequence["name"]} 실행')
                    is_rebirth = run_sequence(thread_var, sequence['sequence'], region)

        # 특수 목적용 매크로
        if condition_custom:
            # 실행할 함수를 넣어둠
            data = {
                "양궁": { "func": atm.auto_shoot_fast, "args": [image_matcher, thread_var.macro_stop] }
            }
            
            print(f'{datetime.datetime.now().strftime("%H:%M")} - ▶️ 시퀀스 {sequence["name"]} 실행')

            # 시퀀스 이름으로 함수를 찾아서 실행
            if sequence['name'] in data:
                # 이름(args...)
                data[sequence['name']]["func"](*data[sequence['name']]["args"])
                break

        # 조건이 없는 시퀀스 실행
        if condition_empty:
            name = condition_empty[0].get("name", "Unnamed Sequence")
            ignore = condition_empty[0].get("ignore", None)

            # 실행한 시퀀스 제거
            sequence = condition_empty.pop(0)
            if not ignore_condition(name, ignore, region):
                print(f'{datetime.datetime.now().strftime("%H:%M")} - ▶️ 시퀀스 {sequence["name"]} 실행')
                is_rebirth = run_sequence(thread_var, sequence['sequence'], region)

    return wave, is_rebirth