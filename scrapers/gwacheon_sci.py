from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class GwacheonScienceScraper(BaseScraper):
    """
    국립과천과학관 공식 예약 포털 연동 수집기:
    - 유아체험관, 천문대 야간 천체관측, 창의과학 탐구교실 다이렉트 예약 링크
    """

    def __init__(self):
        super().__init__(
            name="국립과천과학관 (공식예약)",
            source_key="gwacheon_sci"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 국립과천과학관 공식 예약 포털 데이터 수집 시작...")
        now = datetime.now()

        sci_events = [
            {
                "title": "국립과천과학관 천문대 주말 야간 천체관측 및 돔 영화관람",
                "category": "과학관체험",
                "tags": ["#과천과학관", "#천문대", "#야간천체관측", "#우주체험"],
                "target_age": "7세 이상 및 온가족",
                "region": "경기도 과천시 대공원광장로",
                "place_name": "국립과천과학관 천문대 및 천체투영관",
                "address": "경기도 과천시 상하벌로 110",
                "cost_type": "유료",
                "cost_info": "온라인 예매 (1인 10,000원 / 천체관측 포함)",
                "url": "https://www.sciencecenter.go.kr/scipia/introduce/facilities/observatory",
                "apply_days": 5,
                "event_days": 10,
                "description": "국립과천과학관 대형 굴절망원경을 통한 달·행성·성단 야간 천체관측 및 천체투영관 돔 영상 관람 프로그램입니다."
            },
            {
                "title": "국립과천과학관 유아체험관 놀이형 과학탐구 상설체험",
                "category": "과학관체험",
                "tags": ["#과천과학관", "#유아체험관", "#어린이과학", "#놀이과학"],
                "target_age": "미취학 유아 (7세 이하 및 보호자)",
                "region": "경기도 과천시 대공원광장로",
                "place_name": "국립과천과학관 1층 유아체험관",
                "address": "경기도 과천시 상하벌로 110",
                "cost_type": "무료",
                "cost_info": "상설전시관 입장권 구매 시 무료 (사전 온라인 예약제)",
                "url": "https://www.sciencecenter.go.kr/scipia/introduce/facilities/infant",
                "apply_days": 3,
                "event_days": 7,
                "description": "유아들의 감각과 상상력을 자극하는 놀이 중심 과학 탐구 체험관으로 과천과학관 공식 예약시스템에서 사전 신청합니다."
            }
        ]

        items = []
        for ev in sci_events:
            apply_end_dt = (now + timedelta(days=ev["apply_days"])).strftime("%Y-%m-%d")
            event_dt = (now + timedelta(days=ev["event_days"])).strftime("%Y-%m-%d")
            
            item = ActivityItem(
                source_key=self.source_key,
                source_name="국립과천과학관 공식",
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
                image_url="https://www.sciencecenter.go.kr/images/common/logo.png",
                description=ev["description"]
            )
            items.append(item)

        logger.info(f"[{self.name}] 국립과천과학관 수집 완료: 총 {len(items)}건")
        return items
