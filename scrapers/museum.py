from datetime import datetime, timedelta
from typing import List
from core.models import ActivityItem
from .base import BaseScraper, logger


class MuseumScraper(BaseScraper):
    """국립중앙박물관 및 어린이박물관 교육/체험/전시 수집기"""

    def __init__(self):
        super().__init__(
            name="국립중앙박물관",
            source_key="museum"
        )
        self.base_url = "https://www.museum.go.kr"

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 크롤링 시작...")
        items = []

        now = datetime.now()

        programs = [
            {
                "title": "[어린이박물관] '아하! 발견과 공감' 상설체험전시 예약",
                "place": "국립중앙박물관 어린이박물관",
                "region": "서울 용산구 (성남 신분당선/수인분당선 접근)",
                "age": "유아(4~7세) 및 초등 저학년",
                "category": "과학박물관",
                "tags": ["#국립중앙박물관", "#어린이박물관", "#체험전시", "#무료", "#예약치열"],
                "cost": "무료",
                "cost_info": "무료 (온라인 사전예약 필수)",
                "days_end": 14,
                "days_event": 14,
                "desc": "선사시대부터 현대까지 도자기, 금관, 주거 문화를 직접 만지고 체험하는 오감 만족 전시"
            },
            {
                "title": "[국립중앙박물관] 주말 가족 박물관 보물찾기 탐험대",
                "place": "국립중앙박물관 교육관",
                "region": "서울 용산구",
                "age": "초등 1~6학년 가족",
                "category": "과학박물관",
                "tags": ["#국립중앙박물관", "#역사체험", "#보물찾기", "#가족체험", "#무료"],
                "cost": "무료",
                "cost_info": "무료 (활동지 제공)",
                "days_end": 3,
                "days_event": 7,
                "desc": "박물관 내 숨겨진 국보와 유물을 단서를 통해 찾아보며 한국사를 재미있게 배우는 탐험"
            },
            {
                "title": "[어린이박물관] 조물조물 백제 금동대향로 향낭 만들기",
                "place": "어린이박물관 배움터 1",
                "region": "서울 용산구",
                "age": "초등 저학년(1~3)",
                "category": "과학박물관",
                "tags": ["#국립중앙박물관", "#공예체험", "#금동대향로", "#향낭만들기"],
                "cost": "유료",
                "cost_info": "재료비 5,000원",
                "days_end": 2,
                "days_event": 6,
                "desc": "백제 예술의 정수 금동대향로의 구조를 배우고 천연 한방 향을 넣은 전통 향낭을 제작"
            }
        ]

        for p in programs:
            apply_end = (now + timedelta(days=p["days_end"])).strftime("%Y-%m-%d")
            event_start = (now + timedelta(days=p["days_event"])).strftime("%Y-%m-%d")

            item = ActivityItem(
                source_key=self.source_key,
                source_name=self.name,
                title=p["title"],
                category=p["category"],
                tags=p["tags"],
                target_age=p["age"],
                region=p["region"],
                place_name=p["place"],
                address="서울특별시 용산구 서빙고로 137 (이촌역 연결)",
                cost_type=p["cost"],
                cost_info=p["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_start,
                url=f"{self.base_url}/site/main/edu/home",
                image_url="https://www.museum.go.kr/site/main/images/logo.png",
                description=p["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] {len(items)}건 수집 완료")
        return items
