import os
import sys
import json
import urllib.request
import time

try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = r"G:\My Program\Kids_Activity_Finder"
DASHBOARD_DIR = r"G:\My Program\Tool_Dashboard"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, DASHBOARD_DIR)

print("=" * 65)
print("[VERIFY] Kids_Activity_Finder 전체 시스템 최종 실동작 종합 검증")
print("=" * 65)

results = []

# [1] 데이터 파일 무결성 검증
print("\n[검증 1] 크롤링 데이터 파일 무결성 검사...")
data_path = os.path.join(BASE_DIR, "data", "activities.json")
web_data_path = os.path.join(BASE_DIR, "web", "activities.json")

if os.path.exists(data_path) and os.path.exists(web_data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"  [OK] data/activities.json 로드 성공 (총 {len(data)}건)")
    print(f"  [OK] 카테고리 분포: {set(item.get('category') for item in data)}")
    results.append(("데이터 무결성", True, f"{len(data)}건 저장됨"))
else:
    print("  [FAIL] 데이터 파일 누락")
    results.append(("데이터 무결성", False, "파일 누락"))

# [2] 프론트엔드 필수 파일 검증
print("\n[검증 2] 모바일 웹앱 PWA 필수 파일 검사...")
web_files = ["index.html", "style.css", "app.js", "manifest.json", "activities.json"]
all_web_ok = True
for wf in web_files:
    p = os.path.join(BASE_DIR, "web", wf)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        print(f"  [OK] web/{wf} 존재 확인 ({os.path.getsize(p)} bytes)")
    else:
        print(f"  [FAIL] web/{wf} 누락 또는 빈 파일")
        all_web_ok = False
results.append(("프론트엔드 파일", all_web_ok, "5개 파일 정상"))

# [3] 웹 서버 HTTP 200 응답 검증
print("\n[검증 3] 로컬 웹 서버 HTTP 200 응답 검사...")
from launcher import is_server_running, start_server_background
if not is_server_running(8080):
    start_server_background(8080)
    time.sleep(1)

try:
    with urllib.request.urlopen("http://localhost:8080/index.html", timeout=2) as res:
        code_html = res.status
    with urllib.request.urlopen("http://localhost:8080/activities.json", timeout=2) as res:
        code_json = res.status
    
    if code_html == 200 and code_json == 200:
        print("  [OK] http://localhost:8080/index.html -> HTTP 200 OK")
        print("  [OK] http://localhost:8080/activities.json -> HTTP 200 OK")
        results.append(("웹 서버 응답", True, "HTTP 200 OK"))
    else:
        print(f"  [FAIL] 비정상 응답: HTML={code_html}, JSON={code_json}")
        results.append(("웹 서버 응답", False, f"HTML={code_html}, JSON={code_json}"))
except Exception as e:
    print(f"  [FAIL] 서버 연결 실패: {e}")
    results.append(("웹 서버 응답", False, str(e)))

# [4] 대시보드 programs.json 등록 및 런처 연동 검증
print("\n[검증 4] Tool_Dashboard 등록 및 런처 연동 검사...")
prog_json_path = os.path.join(DASHBOARD_DIR, "programs.json")
with open(prog_json_path, "r", encoding="utf-8") as f:
    dashboard_progs = json.load(f)

kids_prog = next((p for p in dashboard_progs if p.get("id") == "tool-kids-activity-finder"), None)
if kids_prog:
    target = kids_prog.get("target_path", "")
    target_exists = os.path.exists(target)
    print(f"  [OK] Tool_Dashboard 등록 확인 (이름: {kids_prog.get('name')})")
    print(f"  [OK] 실행 타겟 경로: {target} (존재 여부: {target_exists})")
    results.append(("대시보드 등록", target_exists, "programs.json 등록 정상"))
else:
    print("  [FAIL] Tool_Dashboard에 tool-kids-activity-finder 미등록")
    results.append(("대시보드 등록", False, "미등록"))

print("\n" + "=" * 65)
print("[RESULT] 최종 검증 결과 요약:")
all_passed = True
for name, passed, detail in results:
    status_icon = "PASS" if passed else "FAIL"
    print(f"  - [{status_icon}] | {name}: {detail}")
    if not passed:
        all_passed = False

print("=" * 65)
if all_passed:
    print("[SUCCESS] 모든 항목이 완벽하게 통과(PASS)했습니다! 실동작 검증 완료.")
else:
    print("[WARN] 일부 항목에 문제가 있습니다. 확인이 필요합니다.")
print("=" * 65)
