import os
import sys
import socket
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Windows 콘솔 UTF-8 보정
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")


def get_local_ip():
    """스마트폰 접속을 위한 로컬 네트워크 IP 주소 안전하게 가져오기"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.3)
        # 로컬 네트워크 라우팅 IP 확인
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        # 브라우저 캐싱 방지 헤더 추가
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, format, *args):
        # 요청 로그 콘솔 출력
        print(f"[Web] {self.address_string()} - {args[0] if args else ''}")


def run_server(port: int = 8080):
    local_ip = get_local_ip()
    local_url = f"http://localhost:{port}"
    mobile_url = f"http://{local_ip}:{port}"

    print("=" * 65)
    print("🎈 Kids_Activity_Finder 웹 서버 가동 중")
    print("=" * 65)
    print(f"💻 [PC 브라우저 접속]     : {local_url}")
    print(f"📱 [스마트폰 와이파이 접속] : {mobile_url}")
    print("-" * 65)
    print(f"📂 웹 루트 경로: {WEB_DIR}")
    print("💡 서버를 종료하려면 이 창에서 Ctrl + C 를 누르세요.")
    print("=" * 65)
    sys.stdout.flush()

    # 기본 브라우저 자동 오픈
    try:
        webbrowser.open(local_url)
    except Exception:
        pass

    # ThreadingHTTPServer로 동시 다중 요청 처리
    httpd = ThreadingHTTPServer(("0.0.0.0", port), CustomHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[서버 종료] 웹 서버가 정상 종료되었습니다.")


if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
