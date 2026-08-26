import json
import os
import shutil
from datetime import datetime, timezone, timedelta, date
from typing import List, Dict, Any
from .models import ActivityItem

# KST (Korea Standard Time, UTC+9)
KST = timezone(timedelta(hours=9))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
WEB_DIR = os.path.join(BASE_DIR, "web")
JSON_PATH = os.path.join(DATA_DIR, "activities.json")
WEB_JSON_PATH = os.path.join(WEB_DIR, "activities.json")
ROOT_JSON_PATH = os.path.join(BASE_DIR, "activities.json")


def ensure_dirs():
    """데이터 및 웹 디렉토리 존재 확인 및 생성"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(WEB_DIR, exist_ok=True)


def load_activities() -> List[ActivityItem]:
    """저장된 전체 활동 목록 불러오기 (배열 또는 메타데이터 래핑 객체 호환)"""
    ensure_dirs()
    if not os.path.exists(JSON_PATH):
        return []
    
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
            items_data = raw.get("items", []) if isinstance(raw, dict) else raw
            return [ActivityItem(**item) for item in items_data]
    except Exception as e:
        print(f"데이터 로드 실패: {e}")
        return []


def save_activities(items: List[ActivityItem]) -> int:
    """
    활동 목록을 data/, web/ 및 루트 경로에 KST 메타데이터와 함께 3중 자동 동기화 저장:
    - [자동 정제] 마감/종료되었거나 일정이 지난 활동 자동 제외 필터링 적용
    - [중복 제거] 동일 URL 기반 중복 제거
    """
    ensure_dirs()
    today_str = datetime.now(KST).strftime("%Y-%m-%d")
    
    # 1. 마감/종료 및 과거 일정 데이터 자동 제외
    active_items = []
    for item in items:
        # 상태가 마감/종료이거나 D-Day가 마감/종료인 경우 제외
        if item.status in ["마감", "종료"] or item.d_day in ["마감", "종료"]:
            continue
        
        # 접수 마감일 또는 행사일이 이미 오늘보다 과거인 경우 제외
        end_ref = item.apply_end if item.apply_end else (item.event_end if item.event_end else item.event_start)
        if end_ref and len(end_ref) >= 10 and end_ref[:10] < today_str:
            continue
            
        active_items.append(item)
    
    # 2. 중복 제거 (URL 기준)
    unique_items = {}
    for item in active_items:
        if item.url not in unique_items:
            unique_items[item.url] = item
    
    merged_list = list(unique_items.values())
    
    # 3. 딕셔너리로 직렬화
    serialized_items = [item.to_dict() for item in merged_list]
    
    now_kst = datetime.now(KST)
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][now_kst.weekday()]
    date_str = f"{now_kst.year}년 {now_kst.month:02d}월 {now_kst.day:02d}일 ({weekday_kr})"
    
    payload = {
        "metadata": {
            "title": "Kids Activity Finder",
            "updated_at": now_kst.strftime("%Y-%m-%d %H:%M:%S"),
            "date_str": date_str,
            "total_count": len(merged_list)
        },
        "items": serialized_items
    }
    
    # 1. data/activities.json 저장
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    
    # 2. web/activities.json 저장
    with open(WEB_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # 3. 루트 activities.json 저장 (루트 접속 호환)
    with open(ROOT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        
    print(f"총 {len(merged_list)}건의 유효 활동 데이터 저장 완료 (마감 제외 완료, 갱신 시각: {payload['metadata']['updated_at']} KST)")
    return len(merged_list)
