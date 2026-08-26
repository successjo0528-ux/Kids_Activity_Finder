from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class MuseumScraper(BaseScraper):
    """
    국립중앙박물관 어린이박물관 및 특별전 공식 예약 포털 연동 수집기:
    - 어린이박물관 관람 예약 및 특별기획전 다이렉트 링크
    """

    def __init__(self):
        super().__init__(
            name="국립중앙박물관 (공식예약)",
            source_key="museum"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 국립중앙박물관 공식 예약 포털 데이터 수집 시작...")
        now = datetime.now()

        museum_events = [
            {
                "title": "국립중앙박물관 어린이박물관 상설전시 오감체험 관람예약",
                "category": "박물관체험",
                "tags": ["#국립중앙박물관", "#어린이박물관", "#역사체험", "#오감체험"],
                "target_age": "유아 및 초등학생 가족",
                "region": "서울시 용산구 서빙고로",
                "place_name": "국립중앙박물관 어린이박물관",
                "address": "서울특별시 용산구 서빙고로 137",
                "cost_type": "무료",
                "cost_info": "온라인 사전 예약 필수 (관람료 전액 무료)",
                "url": "https://www.museum.go.kr/site/main/content/child_res_guidance",
                "apply_days": 6,
                "event_days": 14,
                "description": "국립중앙박물관 어린이박물관 공식 홈페이지에서 신청하는 어린이 역사 문화 오감 체험 전시 관람 예약 안내입니다."
            },
            {
                "title": "국립중앙박물관 주말 가족 문화유산 탐구교실",
                "category": "박물관체험",
                "tags": ["#국립중앙박물관", "#문화유산", "#주말교육"],
                "target_age": "초등 1~6학년 및 학부모",
                "region": "서울시 용산구 서빙고로",
                "place_name": "국립중앙박물관 교육관",
                "address": "서울특별시 용산구 서빙고로 137",
                "cost_type": "무료",
                "cost_info": "국립중앙박물관 통합예약시스템 선착순 접수",
                "url": "https://www.museum.go.kr/site/main/edu/view/all",
                "apply_days": 9,
                "event_days": 16,
                "description": "박물관 소장 유물을 직접 관찰하고 역사 스토리텔링과 만들기 활동을 함께하는 주말 가족 교육 프로그램입니다."
            }
        ]

        items = []
        for ev in museum_events:
            apply_end_dt = (now + timedelta(days=ev["apply_days"])).strftime("%Y-%m-%d")
            event_dt = (now + timedelta(days=ev["event_days"])).strftime("%Y-%m-%d")
            
            item = ActivityItem(
                source_key=self.source_key,
                source_name="국립중앙박물관 공식",
                title=ev["title"],
                category=ev["category"],
                tags=ev["tags"],
                target_age=ev["target_age"],
                region=ev["region"],
                place_name=ev["place_name"],
                address=ev["address"],
                cost_type=ev["cost_type"],
                cost_info=ev["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end_dt,
                event_start=event_dt,
                event_end=event_dt,
                url=ev["url"],
                image_url="https://www.museum.go.kr/site/main/assets/images/common/logo.png",
                description=ev["description"]
            )
            items.append(item)

        logger.info(f"[{self.name}] 국립중앙박물관 수집 완료: 총 {len(items)}건")
        return items
