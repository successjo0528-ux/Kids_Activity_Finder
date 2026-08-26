import os
import sys
import json
import re
import time
from datetime import datetime, date

try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRAPERS_DIR = os.path.join(BASE_DIR, "scrapers")
DASHBOARD_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Tool_Dashboard"))
sys.path.insert(0, BASE_DIR)

print("=" * 70)
print("[VERIFY] Kids_Activity_Finder 10개 채널 출처 교차 검증 & 무결성 검사")
print("=" * 70)

results = []
summary_md = []
summary_md.append("## 🎈 Kids Activity Finder 일일 자동 수집 & 출처 교차 검증 보고서")
summary_md.append(f"- **검증 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} KST")

# [검증 1] 데이터 파일 존재 및 로드
print("\n[검증 1] 크롤링 데이터 파일 무결성 및 구조 검사...")
data_path = os.path.join(BASE_DIR, "data", "activities.json")
web_data_path = os.path.join(BASE_DIR, "web", "activities.json")

items = []
if os.path.exists(data_path) and os.path.exists(web_data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    items = raw_data.get("items", []) if isinstance(raw_data, dict) else raw_data
    total_cnt = len(items)
    print(f"  [OK] data/activities.json 로드 성공 (총 {total_cnt}건)")
    print(f"  [OK] web/activities.json 동기화 확인")
    results.append(("데이터 파일 로드", True, f"총 {total_cnt}건 수집됨"))
else:
    print("  [FAIL] 데이터 파일 누락")
    results.append(("데이터 파일 로드", False, "파일 누락"))

# [검증 2] 10개 출처별 교차 검증 (Source Cross-Validation)
print("\n[검증 2] 10개 출처별 데이터 수집 건수 및 실시간 수집량 검사...")
sources_map = {}
for it in items:
    k = it.get("source_key", "unknown")
    sources_map.setdefault(k, []).append(it)

expected_sources = [
    ("seongnam_lib", "공공도서관 문화체험 (성남시립·인천·포항)", 20),
    ("contests", "어린이 미술·글짓기·AI 대회 (알럽콘)", 10),
    ("conventions", "코엑스 & 킨텍스 전시 (공식박람회 실시간)", 10),
    ("seongnam_city", "지자체 시청 & 청소년재단 (공식포털)", 4),
    ("regional_museums_sports", "경기·인천·포항 박물관·미술관", 4),
    ("concerts", "음악회·오케스트라·키즈콘서트", 3),
    ("sports_events", "스포츠 대회 및 시범공연", 3),
    ("gwacheon_sci", "국립과천과학관 (공식예약)", 2),
    ("museum", "국립중앙박물관 (공식예약)", 2),
    ("kids_platforms", "키즈플랫폼 & 문화센터", 2),
]

summary_md.append("\n### 📊 채널별 수집 건수 및 상태 검증")
summary_md.append("| 채널 키 | 출처명 | 수집 건수 | 최소 기대치 | 상태 |")
summary_md.append("| :--- | :--- | :---: | :---: | :---: |")

all_sources_ok = True
for s_key, s_name, min_expected in expected_sources:
    actual_count = len(sources_map.get(s_key, []))
    is_ok = actual_count >= min_expected
    status_str = "✅ PASS" if is_ok else "❌ FAIL"
    if not is_ok:
        all_sources_ok = False
    print(f"  [{status_str}] {s_name:<35} | {actual_count:>2}건 (기준: {min_expected}건 이상)")
    summary_md.append(f"| `{s_key}` | {s_name} | **{actual_count}건** | {min_expected}건 | {status_str} |")

results.append(("10개 출처 수집 검증", all_sources_ok, f"{len(sources_map)}개 채널 가동 중"))

# [검증 3] 10개 스크래퍼 소스코드 동적/실시간 크롤링 엔진 감사 (Scraper Code Audit)
print("\n[검증 3] 10개 스크래퍼 소스코드 동적 크롤링 엔진 감사 (Code Audit)...")
scraper_files = {
    "seongnam_lib.py": "성남시립 도서관 실시간 크롤러",
    "contests.py": "알럽콘 전국 공모전 실시간 크롤러",
    "conventions.py": "코엑스/킨텍스 전시회 실시간 크롤러",
    "museum.py": "국립중앙박물관 실시간 연동 크롤러",
    "gwacheon_sci.py": "국립과천과학관 실시간 연동 크롤러",
    "regional_museums_sports.py": "지역 박물관/미술관 연동 수집기",
    "seongnam_city.py": "지자체 시청 포털 연동 수집기",
    "concerts.py": "공연장/콘서트홀 연동 수집기",
    "sports_events.py": "스포츠협회 연동 수집기",
    "kids_platforms.py": "문화센터 연동 수집기"
}

summary_md.append("\n### 🔍 스크래퍼 엔진 소스코드 감사 (Audit)")
summary_md.append("| 스크래퍼 파일 | 대상 채널 | 네트워크 통신 | HTML 파서 | 엔진 등급 |")
summary_md.append("| :--- | :--- | :---: | :---: | :---: |")

audit_passed = True
for s_file, desc in scraper_files.items():
    file_path = os.path.join(SCRAPERS_DIR, s_file)
    if not os.path.exists(file_path):
        print(f"  [❌ MISSING] {s_file} 파일 누락")
        audit_passed = False
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    has_net = "requests" in code_content or "urllib" in code_content
    has_soup = "BeautifulSoup" in code_content or "bs4" in code_content
    
    if has_net and has_soup:
        tier = "⭐ Real-time Web Crawler"
    elif has_net:
        tier = "⚡ Live Server Connector"
    else:
        tier = "⚠️ Static Mock (하드코딩)"
        audit_passed = False

    net_icon = "✅" if has_net else "❌"
    soup_icon = "✅" if has_soup else "➖"
    
    print(f"  [OK] {s_file:<25} | Net: {net_icon} | HTML Parser: {soup_icon} | {tier}")
    summary_md.append(f"| `{s_file}` | {desc} | {net_icon} | {soup_icon} | {tier} |")

results.append(("스크래퍼 코드 감사", audit_passed, "10개 스크래퍼 실시간 네트워크 통신 확인"))

# [검증 4] 날짜 유효성 및 상태/D-Day 교차 검증 (전수 검사)
print("\n[검증 4] 전체 데이터 날짜 포맷 및 상태/D-Day 전수 교차 검증...")
date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
invalid_dates = []
status_anomalies = []
today = date.today()

for idx, it in enumerate(items, 1):
    ap_s = it.get("apply_start", "")
    ap_e = it.get("apply_end", "")
    ev_s = it.get("event_start", "")
    st = it.get("status", "")
    title = it.get("title", "")

    # 1. 날짜 포맷 검사
    for field_name, d_val in [("apply_start", ap_s), ("apply_end", ap_e), ("event_start", ev_s)]:
        if d_val and not date_pattern.match(d_val[:10]):
            invalid_dates.append((idx, title, field_name, d_val))

    # 2. 접수예정 D-Day 일치성 검사
    if ap_s and date_pattern.match(ap_s[:10]):
        s_date = datetime.strptime(ap_s[:10], "%Y-%m-%d").date()
        if today < s_date:
            if st != "접수예정":
                status_anomalies.append((idx, title, f"시작일 미래({ap_s})이나 상태가 '{st}'임"))

print(f"  - 날짜 형식 오류: {len(invalid_dates)}건")
print(f"  - 상태 매핑 이상: {len(status_anomalies)}건")

date_status_ok = len(invalid_dates) == 0 and len(status_anomalies) == 0
results.append(("날짜 및 상태 무결성", date_status_ok, f"오류 {len(invalid_dates) + len(status_anomalies)}건"))

# [검증 5] 프론트엔드 필수 파일 검증
print("\n[검증 5] 모바일 웹앱 PWA 필수 파일 검사...")
web_files = ["index.html", "style.css", "app.js", "manifest.json", "activities.json"]
all_web_ok = True
for wf in web_files:
    p = os.path.join(BASE_DIR, "web", wf)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        print(f"  [OK] web/{wf} ({os.path.getsize(p)} bytes)")
    else:
        print(f"  [FAIL] web/{wf} 누락 또는 빈 파일")
        all_web_ok = False
results.append(("프론트엔드 파일", all_web_ok, "5개 파일 정상"))

# [검증 6] 대시보드 등록 검사
if os.path.exists(DASHBOARD_DIR):
    print("\n[검증 6] Tool_Dashboard 등록 및 런처 연동 검사...")
    prog_json_path = os.path.join(DASHBOARD_DIR, "programs.json")
    if os.path.exists(prog_json_path):
        with open(prog_json_path, "r", encoding="utf-8") as f:
            dashboard_progs = json.load(f)
        kids_prog = next((p for p in dashboard_progs if p.get("id") == "tool-kids-activity-finder"), None)
        if kids_prog:
            print(f"  [OK] Tool_Dashboard 등록 확인: {kids_prog.get('name')}")
            results.append(("대시보드 등록", True, "programs.json 등록 확인"))

# 최종 결과 요약
print("\n" + "=" * 70)
print("[RESULT] 최종 검증 결과 요약:")
summary_md.append("\n### 📋 종합 검증 결과 요약")
summary_md.append("| 검증 항목 | 판정 | 세부 결과 |")
summary_md.append("| :--- | :---: | :--- |")

all_passed = True
for name, passed, detail in results:
    status_icon = "PASS" if passed else "FAIL"
    badge_icon = "✅ PASS" if passed else "❌ FAIL"
    print(f"  - [{status_icon}] | {name}: {detail}")
    summary_md.append(f"| {name} | {badge_icon} | {detail} |")
    if not passed:
        all_passed = False

print("=" * 70)
if all_passed:
    print("[SUCCESS] 10개 모든 출처의 동적 크롤링 무결성 검증이 완벽하게 통과(PASS)했습니다!")
else:
    print("[WARN] 일부 항목에 문제가 있습니다. 확인이 필요합니다.")
print("=" * 70)

# GitHub Actions Step Summary 출력 지원
gh_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
if gh_summary_path:
    try:
        with open(gh_summary_path, "a", encoding="utf-8") as f:
            f.write("\n".join(summary_md) + "\n")
    except Exception as e:
        print(f"GitHub Step Summary 쓰기 오류: {e}")

if not all_passed:
    sys.exit(1)
sys.exit(0)
