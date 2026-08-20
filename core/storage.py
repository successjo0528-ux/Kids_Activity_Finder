import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
from .models import ActivityItem


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
WEB_DIR = os.path.join(BASE_DIR, "web")
JSON_PATH = os.path.join(DATA_DIR, "activities.json")
WEB_JSON_PATH = os.path.join(WEB_DIR, "activities.json")


def ensure_dirs():
    """데이터 및 웹 디렉토리 존재 확인 및 생성"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(WEB_DIR, exist_ok=True)


def load_activities() -> List[ActivityItem]:
    """저장된 전체 활동 목록 불러오기"""
    ensure_dirs()
    if not os.path.exists(JSON_PATH):
        return []
    
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [ActivityItem(**item) for item in data]
    except Exception as e:
        print(f"데이터 로드 실패: {e}")
        return []


def save_activities(items: List[ActivityItem]) -> int:
    """새로운 활동 목록을 기존 데이터와 병합하여 data/ 및 web/ 폴더에 저장"""
    ensure_dirs()
    
    # 기존 데이터 로드
    existing_items = {item.id: item for item in load_activities()}
    
    # 새 데이터 병합 (최신 정보로 갱신)
    for item in items:
        existing_items[item.id] = item
    
    # 병합 목록 정렬
    merged_list = list(existing_items.values())
    
    # 딕셔너리로 직렬화
    serialized_data = [item.to_dict() for item in merged_list]
    
    # data/activities.json 저장
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(serialized_data, f, ensure_ascii=False, indent=2)
    
    # web/activities.json 동기화 복사 (GitHub Pages 및 웹앱용)
    with open(WEB_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(serialized_data, f, ensure_ascii=False, indent=2)
        
    print(f"총 {len(merged_list)}건의 활동 데이터 저장 완료 (신규/갱신: {len(items)}건)")
    return len(merged_list)
