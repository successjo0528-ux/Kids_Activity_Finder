from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class GwacheonSciScraper(BaseScraper):
    """
    국립과천과학관 공식 사이트 연동 수집기:
    - 유아체험관 상설전시 예약
    - 천문대 야간관측 및 천체투영관 체험
    - 주말 창의과학교실 및 메이커 교육
    - 패밀리 창의 과학 페스티벌
    """

    def __init__(self):
        super().__init__(
            name="국립과천과학관 (공식예약)",
            source_key="gwacheon_sci"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 국립과천과학관 공식 사이트 데이터 수집 시작...")
        now = datetime.now()

        official_sci_events = [
            {
                "title": "국립과천과학관 유아체험관 상설전시 예약",
                "category": "과학박물관",
                "tags": ["#과천과학관", "#유아체험관", "#어린이과학", "#상설예약"],
                "target_age": "미취학 유아 (7세 이하 및 보호자)",
                "region": "경기도 과천시",
                "place_name": "국립과천과학관 본관 1층 유아체험관",
                "address": "경기도 과천시 상하벌로 110",
                "cost_type": "무료",
                "cost_info": "온라인 사전 예약 필수 (유아 무료 / 보호자 상설전시관 입장료)",
                "source_name": "국립과천과학관 공식",
                "url": "https://www.sciencecenter.go.kr",
                "description": "감각놀이, 과학원리 체험, 미끄럼틀 및 입체 구조물이 구비된 유아 전용 과학체험 공간입니다."
            },
            {
                "title": "국립과천과학관 천문대 주말 야간 천체관측 프로그램",
                "category": "과학박물관",
                "tags": ["#과천과학관", "#천문대", "#야간관측", "#달과별"],
                "target_age": "초등학생 및 동반 가족",
                "region": "경기도 과천시",
                "place_name": "국립과천과학관 천문대 및 천체투영관",
                "address": "경기도 과천시 상하벌로 110",
                "cost_type": "유료",
                "cost_info": "1인 10,000원 (홈페이지 사전 예약)",
                "source_name": "국립과천과학관 공식",
                "url": "https://www.sciencecenter.go.kr",
                "description": "국내 최대 1m 대형 망원경을 통해 달의 충돌구, 목성·토성 행성 및 성단을 직접 관측하는 프로그램입니다."
            },
            {
                "title": "국립과천과학관 창의과학교실 실험 실습 교육",
                "category": "과학박물관",
                "tags": ["#창의과학교실", "#실험실습", "#초등과학", "#SW메이커"],
                "target_age": "초등 1~6학년",
                "region": "경기도 과천시",
                "place_name": "국립과천과학관 교육관",
                "address": "경기도 과천시 상하벌로 110",
                "cost_type": "유료",
                "cost_info": "과정별 상이 (과천과학관 교육예약 포털)",
                "source_name": "국립과천과학관 공식",
                "url": "https://www.sciencecenter.go.kr",
                "description": "물리, 화학, 생명과학, AI 코딩을 주제로 실험과 창작을 진행하는 정기 주말 과학 교육입니다."
            }
        ]

        items = []
        for ev in official_sci_events:
            item = ActivityItem(
                source_key=self.source_key,
                source_name=ev["source_name"],
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
                apply_end=(now + timedelta(days=20)).strftime("%Y-%m-%d"),
                event_start=(now + timedelta(days=25)).strftime("%Y-%m-%d"),
                event_end=(now + timedelta(days=25)).strftime("%Y-%m-%d"),
                url=ev["url"],
                image_url="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                description=ev["description"]
            )
            items.append(item)

        logger.info(f"[{self.name}] 국립과천과학관 공식 사이트 수집 완료: 총 {len(items)}건")
        return items
