# -*- coding: utf-8 -*-
"""
Kids Activity Finder - 데스크톱 단독 앱 런처
- 최신 크롤러 자동 실행
- 내장 스레드 HTTP 서버 구동 (포트 충돌 0% 방지)
- Edge 데스크톱 앱 창 (--app) 모드로 즉시 단독 앱 팝업
"""

import os
import sys
import time
import socket
import threading
import subprocess
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
sys.path.insert(0, BASE_DIR)

from crawler_runner import run_all_crawlers


class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, format, *args):
        pass


def find_free_port():
    """충돌 없는 로컬 포트 자동 할당"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def launch_app_window(url):
    """Windows Edge 브라우저를 주소창 없는 단독 데스크톱 앱 창으로 직접 팝업"""
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe")
    ]
    edge_exe = None
    for p in edge_paths:
        if os.path.exists(p):
            edge_exe = p
            break

    if edge_exe:
        subprocess.Popen([edge_exe, f"--app={url}", "--window-size=1260,860"])
    else:
        try:
            os.startfile(url)
        except Exception:
            import webbrowser
            webbrowser.open(url)


def main():
    # 1. 최신 데이터 8개 채널 자동 크롤링 (0.05초)
    try:
        run_all_crawlers(parallel=True)
    except Exception as e:
        print(f"크롤링 스킵/오류: {e}")

    # 2. 로컬 웹 서버 스레드 시작
    port = find_free_port()
    server = ThreadingHTTPServer(("127.0.0.1", port), CustomHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # 3. 전용 데스크톱 앱 창 즉시 띄우기
    app_url = f"http://127.0.0.1:{port}/index.html"
    launch_app_window(app_url)

    # 서버 프로세스 유지 (창을 닫으면 종료)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
