from __future__ import annotations
import ctypes
import importlib
import json
import logging
import os
import msvcrt
import signal
import subprocess
import sys
import threading
import time
from types import SimpleNamespace
from typing import Any
from Lib.pathlib import Path
import datetime
import httpx
from supabase import create_client

import env_data.env_data as env
import macro_click.macro_click as mc
from window_capture.screen_uploader import start_screen_thread
import image_match.image_match as im
from macro_process import run_macro as rm, restart_game as rg
from updater import check_update as cu
from macro_editor.ef2 import pos as p


BASE_DIR = getattr(sys, "frozen", False) and Path(sys.executable).resolve().parent or Path(__file__).resolve().parent

shutdown = threading.Event()
macro_stop = threading.Event()
macro_thread: threading.Thread | None = None
macro_lock = threading.Lock()
state = 'idle'
last_error = ''


restart = threading.Event()

thread_var = SimpleNamespace(
    shutdown=shutdown,
    macro_stop=macro_stop,
    restart=restart,
)

supabase = create_client(
    env.SUPABASE_URL,
    env.SUPABASE_ANON_KEY
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def load_macros():
    path = BASE_DIR / "macro.py"

    if not path.is_file():
        raise FileNotFoundError(f"매크로 파일을 찾을 수 없습니다: {path}")

    spec = importlib.util.spec_from_file_location(
        "external_macros",
        path
    )

    if spec is None or spec.loader is None:
        raise RuntimeError("매크로 파일을 로드할 수 없습니다.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return {
        "macros": module.macros,
        "multi_macros": module.multi_macros,
        "region": p.region
    }


def get_access_token():
    session = supabase.auth.get_session()

    if session is None:
        auth = supabase.auth.sign_in_with_password({
            "email": env.SUPABASE_EMAIL,
            "password": env.SUPABASE_PASSWORD
        })
        session = auth.session

    if session is None:
        raise RuntimeError("Supabase 인증 실패")

    return session.access_token


def post_repeat_command(kind: str, macro: dict[str, Any]):
    access_token = get_access_token()
    server_headers = {'Authorization': f'Bearer {access_token}'}
    with httpx.Client(base_url=env.CLIENT_URL+'/', headers=server_headers, timeout=10) as client:
        try:
            ack = client.post('api/dashboard/commands', 
                    json={"type": kind, "payload": {"name": macro["name"], "repeat": True}})
            ack.raise_for_status()
        except Exception as e:
            print(f'Error occurred while sending repeat command: {e}')


def post_command_result(command_id: str, msg: str):
    client_headers = {'Authorization': f'Bearer {env.DEVICE_TOKEN}', 'X-Device-ID': env.DEVICE}
    with httpx.Client(base_url=env.CLIENT_URL+'/api/agent', headers=client_headers, timeout=10) as client:
        try:
            result = {'status': 'done', 'error': msg}
            ack = client.post(f'commands/{command_id}/ack', json=result)
            ack.raise_for_status()
        except Exception as e:
            print(f'Error occurred while sending ack: {e}')


def run_command(
        command_id: str | None,
        macro: list[dict[str, Any]], 
        kind: str,
        is_repeat: bool, 
        region: dict[str, tuple[float, float, float, float]]
    ):
    global state, last_error
    try:
        while not shutdown.is_set() and not macro_stop.is_set():
            is_rebirth = False
            wave = 0

            print(f'{datetime.datetime.now().strftime("%H:%M")} - ✅ 매크로 {macro["name"]} 실행{is_repeat and " (반복)" or ""}')

            # 매크로 실행; 실행 결과로 환생 또는 종료 시 현재 웨이브랑 환생 여부를 반환
            wave, is_rebirth = rm.run_macro(thread_var, macro["data"], region)

            print(f'{datetime.datetime.now().strftime("%H:%M")} - ✅ 매크로 종료{is_rebirth and "; 환생 성공" or ""}')

            msg = ""
            if is_rebirth:
                diamond = im.check_diamond(region["DIAMOND_POS"])
                medal, medal_unit = im.check_medal(region["MEDAL_POS"])

                msg = f"❇️ 환생 결과 : Wave {wave} 🎖️{medal}{medal_unit} 💎{diamond}"
                print(f'{datetime.datetime.now().strftime("%H:%M")} - {msg}')

            # 매크로 실행 결과를 클라이언트로 전송
            if command_id:
                post_command_result(command_id, msg)
            elif not command_id and is_repeat:
                continue

            break

    except Exception as e:
        last_error = str(e)
        print(f'{datetime.datetime.now().strftime("%H:%M")} - ❌ 매크로 실패: {last_error}; 매크로 종료')
        macro_stop.set()

    finally:
        state = 'idle'

    # 반복 매크로의 경우 다시 실행
    if command_id and is_repeat and not shutdown.is_set() and not macro_stop.is_set():
        post_repeat_command(kind, macro)


def stop_macro():
    global state

    macro_stop.set()
    with macro_lock:
        thread = macro_thread

    if thread and thread.is_alive():
        thread.join(timeout=2)

    state = 'idle'


def execute(command: dict[str, Any], command_id: str):
    global macro_thread, state, last_error

    kind = command['type'].upper()
    p = command.get('payload') or {}
    if kind == 'STOP':
        stop_macro()
        
        print(f'{datetime.datetime.now().strftime("%H:%M")} - ⛔ 매크로 중지')

    elif kind == 'CLICK':
        stop_macro()

        print(f'{datetime.datetime.now().strftime("%H:%M")} - CLICK command executed')

        mc.click(macro_stop, float(p['x']), float(p['y']))

    elif kind == 'SWIPE':
        stop_macro()

        print(f'{datetime.datetime.now().strftime("%H:%M")} - SWIPE command executed')

        mc.swipe(
            shutdown,
            macro_stop,
            float(p['start_x']), 
            float(p['start_y']), 
            float(p['end_x']), 
            float(p['end_y'])
        )

    elif kind == 'RUN_MACRO' or kind == 'RUN_MULTI_MACRO':
        stop_macro()
        macro_name = p.get('name')
        is_repeat = p.get('repeat')

        if not macro_name:
            raise ValueError('Missing macro name')
        
        data = load_macros()

        if kind == 'RUN_MACRO':
            macro = data["macros"][macro_name]

        elif kind == 'RUN_MULTI_MACRO':
            macro = data["multi_macros"][macro_name]

        if not macro:
            raise ValueError(f'Unknown macro: {macro_name}')
        
        macro_stop.clear()
        last_error = ''
        state = 'running'
        t = threading.Thread(target=run_command, args=(command_id, macro, kind, is_repeat, data["region"]), daemon=True)

        with macro_lock:
            macro_thread = t

        t.start()
    else:
        raise ValueError(f'Unsupported command: {kind}')

def connect_server():
    global screen_stop

    last_beat = 0.

    screen_stop, screen_thread, screen_watching = start_screen_thread(shutdown)

    headers = {'Authorization': f'Bearer {env.DEVICE_TOKEN}', 'X-Device-ID': env.DEVICE}
    with httpx.Client(base_url=env.CLIENT_URL+'/api/agent', headers=headers, timeout=10) as client:
        while not shutdown.is_set():
            try:
                # 주기적인 연결
                if time.monotonic() - last_beat >= env.HEARTBEAT:
                    r = client.post('heartbeat', json={'status': state, 'last_error': last_error})
                    if r.status_code == 404:
                        continue

                    data = r.json()

                    # 웹페이지를 보고 있을 때만 화면 공유
                    if data.get("screen_watching"):
                        screen_watching.set()
                    else:
                        screen_watching.clear()

                    r.raise_for_status()
                    last_beat = time.monotonic()

                # 명령 받기
                r = client.get('commands/next')

                r.raise_for_status()

                # 명령 실행
                cmd = r.json().get('command')
                if cmd:
                    command_id = str(cmd['id'])
                    try:
                        execute(cmd, command_id)

                        # 명령 결과를 매크로 중지일 땐 done, 그 외엔 claimed로 처리; 매크로는 실행이 종료되면 done으로 처리됨
                        result = {'status': cmd["type"].upper() == "STOP" and 'done' or 'claimed', 'error': ''}
                    except Exception as e:
                        print(f'{datetime.datetime.now().strftime("%H:%M")} - Command {command_id} failed: {e}')
                        result = {'status': 'failed', 'error': str(e)[:500]}

                    # Backend must deduplicate commands and atomically claim them.
                    ack = client.post(f'commands/{command_id}/ack', json=result)
                    ack.raise_for_status()

            except httpx.HTTPStatusError as e:
                print(f'{datetime.datetime.now().strftime("%H:%M")} - {e.request.url}; Backend returned {e.response.text}')

            except (httpx.HTTPError, KeyError) as e:
                print(f'{datetime.datetime.now().strftime("%H:%M")} - Connection/protocol error: {e}')

            except ValueError as e:
                print(f'{datetime.datetime.now().strftime("%H:%M")} - ValueError: {e}')

            shutdown.wait(env.POLL)

    screen_stop.set()
    screen_thread.join(timeout=2)
    stop_macro()


def select_menu(multi_macro_names: list[str], macro_names: list[str]):
    selected = ""

    while True:
        print(f'\n\r{datetime.datetime.now().strftime("%H:%M")} - 🔗 실행할 매크로를 선택해주세요: ', end="", flush=True)

        try:
            selected = input().strip()
        except EOFError as e:
            print("\n❌ 입력이 취소되었습니다. agent를 종료합니다.")
            sys.exit(0)

        if selected in multi_macro_names:
            return "multi_macros", selected
        elif selected in macro_names:
            return "macros", selected
        else:
            print(f'\n\r{datetime.datetime.now().strftime("%H:%M")} - ❌ 매크로를 찾을 수 없습니다: {selected}')
            print(f'🔗 사용 가능한 매크로 목록: {", ".join(multi_macro_names + macro_names)}')


def execute_on_local():
    global macro_thread, state, last_error

    data = load_macros()
    multi_macro_names = [name for name, _ in data['multi_macros'].items()]
    macro_names = [name for name, _ in data['macros'].items()]

    while not shutdown.is_set():
        if state == "idle":
            kind, macro_name = select_menu(multi_macro_names, macro_names)
            macro = data[kind][macro_name]

            try:
                is_repeat = input(f"{datetime.datetime.now().strftime("%H:%M")} - 🔁 반복 실행 여부(y/n): ").strip().lower() == "y"
            except EOFError as e:
                print("\n❌ 입력이 취소되었습니다. agent를 종료합니다.")
                sys.exit(0)

            print(f'{datetime.datetime.now().strftime("%H:%M")} - ⚠️ 현재 매크로를 종료하려면 "q"를 누르세요.\n')

            macro_stop.clear()
            last_error = ''
            state = 'running'
            t = threading.Thread(target=run_command, args=(None, macro, kind, is_repeat, data["region"]), daemon=True)

            with macro_lock:
                macro_thread = t

            t.start()

        shutdown.wait(2)

        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key.lower() == 'q':
                print(f'\n\r{datetime.datetime.now().strftime("%H:%M")} - ⛔ 매크로 중지')
                stop_macro()

    stop_macro()


def main():
    if not env.CLIENT_URL.startswith('https://') and not env.CLIENT_URL.startswith('http://localhost'):
        raise SystemExit('API_BASE_URL must use HTTPS (except localhost)')

    try:
        connect = input("\n🔗 서버와 연결하시겠습니까?(y/n): ").strip().lower() == "y"
    except EOFError as e:
        print("\n❌ 입력이 취소되었습니다. agent를 종료합니다.")
        sys.exit(0)

    print(f'\n{datetime.datetime.now().strftime("%H:%M")} - ✅ 에이전트 정상 실행중 id: {env.DEVICE}')

    # 서버 연결해서 실행
    if connect:
        connect_server()
    # 로컬로 실행
    else:
        execute_on_local()


def apply_restart():
    try:
        res = input("\n🔁 자동 재실행 기능을 사용하시겠습니까?(y/n): ").strip().lower() == "y"
    except EOFError as e:
        print("\n❌ 입력이 취소되었습니다. agent를 종료합니다.")
        sys.exit(0)
    
    if not res:
        return
    
    print("\n바탕화면에 있는 바로가기 파일을 찾고 있습니다...\n")

    # 바탕화면 경로 가져오기; 윈도우 환경에 따라 절대적인 경로가 다르기 때문에 컴퓨터에 저장되어 있는 바탕화면 경로를 가져오는 방법을 사용
    buffer = ctypes.create_unicode_buffer(260)
    ctypes.windll.shell32.SHGetFolderPathW(
        None,
        0x0010,  # CSIDL_DESKTOPDIRECTORY
        None,
        0,
        buffer
    )

    desktop = Path(buffer.value)

    # 파일이름은 항상 동일(구글 플레이 for PC 기준)
    target_path = desktop / "오늘도 환생 2  방치형 디펜스 RPG.lnk"
    if target_path.exists():
        print(f"✅ 파일을 정상적으로 찾았습니다: {target_path}")
    else:
        print(f"❌ 파일을 찾을 수 없습니다. 파일을 추가하고 다시 시도해주세요.")
        sys.exit(1)

    try:
        restart_time = input("⏱️ 자동 재실행 시간 설정(기본 3600초)(숫지만 입력): ")
    except EOFError as e:
        print("\n❌ 입력이 취소되었습니다. agent를 종료합니다.")
        sys.exit(0)

    try:
        restart_time = int(restart_time)
    except ValueError:
        restart_time = 3600

    rg.set_restart(shutdown, restart, target_path, restart_time)


def apply_update():
    update_info = cu.check_update()
    print(f"🚀 agent.exe v{cu.get_current_version()} 실행 중...")
    if not update_info[0]:
        return

    print(f"\n🎉 새로운 버전이 있습니다: v{update_info[1]['version']} 🎉")
    try:
        is_update = input("업데이트 하시겠습니까? (y/n): ").strip().lower() == "y"
    except EOFError as e:
        print("\n❌ 입력이 취소되었습니다. agent를 종료합니다.")
        sys.exit(0)
    
    if not is_update:
        return

    updater = os.path.join(BASE_DIR, "updater.exe")
    subprocess.Popen(
        [
            updater,
            str(os.getpid()),
            json.dumps(update_info[1]),
            sys.executable
        ], cwd=BASE_DIR, creationflags=subprocess.CREATE_NEW_CONSOLE)

    sys.exit(0)


if __name__ == '__main__':
    def handle_signal(_signum, _frame):
        shutdown.set()
        macro_stop.set()
        rg.stop_restart()

    # 시그널 등록
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # 업데이트 확인
    apply_update()
    # 재시작 설정
    apply_restart()
        
    main()
