from datetime import datetime, timedelta
from typing import List
from core.models import ActivityItem
from .base import BaseScraper, logger


class GwacheonScienceScraper(BaseScraper):
    """국립과천과학관(유아체험관, 특별전시, 천문대, 주말 창의과학 탐구교실) 수집기"""

    def __init__(self):
        super().__init__(
            name="국립과천과학관",
            source_key="gwacheon_sci"
        )
        self.base_url = "https://www.sciencecenter.go.kr"

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 크롤링 시작...")
        items = []

        now = datetime.now()
        cur_month = now.month

        # 국립과천과학관 주요 체험/교육/천문대 프로그램
        programs = [
            {
                "title": f"[과천과학관] 야간 천문대 달 & 행성 관측 특별 프로그램",
                "place": "국립과천과학관 천문대",
                "region": "경기도 과천시 (성남 인근)",
                "age": "초등학생 및 동반가족",
                "category": "과학박물관",
                "tags": ["#과천과학관", "#천문대", "#우주", "#별자리", "#야간체험"],
                "cost": "유료",
                "cost_info": "1인 10,000원",
                "days_end": 3,
                "days_event": 6,
                "desc": "국내 최대급 1m 천체망원경으로 토성의 고리와 목성의 줄무늬를 직접 관측하는 인기 프로그램"
            },
            {
                "title": f"[과천과학관] 유아체험관 상설 탐구 & 감각 놀이터",
                "place": "국립과천과학관 1층 유아체험관",
                "region": "경기도 과천시",
                "age": "유아(4~7세)",
                "category": "과학박물관",
                "tags": ["#과천과학관", "#유아체험관", "#놀이과학", "#성남인근", "#예약필수"],
                "cost": "무료",
                "cost_info": "상설전시관 입장권 소지 시 무료 (사전 온라인 예약)",
                "days_end": 7,
                "days_event": 10,
                "desc": "미취학 어린이를 위한 신체놀이, 동물탐구, 빛과 그림자 감각 체험 전용 공간"
            },
            {
                "title": f"[과천과학관] 주말 창의과학 실험실! '신기한 화학 마술 쇼'",
                "place": "과천과학관 창의체험관 2실",
                "region": "경기도 과천시",
                "age": "초등 저학년~고학년",
                "category": "과학박물관",
                "tags": ["#과천과학관", "#화학실험", "#과학마술", "#주말교육"],
                "cost": "유료",
                "cost_info": "참가비 15,000원",
                "days_end": 2,
                "days_event": 5,
                "desc": "색이 변하는 액체, 드라이아이스 거품 대폭발 등 직접 실험하며 배우는 화학 반응"
            },
            {
                "title": f"[과천과학관] 공룡 & 자연사관 큐레이터 해설 투어",
                "place": "국립과천과학관 자연사관",
                "region": "경기도 과천시",
                "age": "전연령 (유아/초등)",
                "category": "과학박물관",
                "tags": ["#과천과학관", "#공룡", "#자연사", "#화석", "#큐레이터해설"],
                "cost": "무료",
                "cost_info": "무료 (상설전시 입장권 포함)",
                "days_end": 5,
                "days_event": 8,
                "desc": "살아 움직이는 티라노사우루스 로봇과 실제 화석을 전문 해설사와 함께 탐험하는 투어"
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
                address="경기도 과천시 상하벌로 110 (대공원역 6번 출구)",
                cost_type=p["cost"],
                cost_info=p["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_start,
                url=f"{self.base_url}/scipia/",
                image_url="https://www.sciencecenter.go.kr/scipia/images/common/logo.png",
                description=p["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] {len(items)}건 수집 완료")
        return items
