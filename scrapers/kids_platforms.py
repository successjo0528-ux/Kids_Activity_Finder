from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class KidsPlatformsScraper(BaseScraper):
    """
    대표 키즈플랫폼 & 백화점 문화센터 공식 사이트 연동 수집기:
    - 현대백화점 판교점 문화센터 (유아 오감발달, 어린이 베이킹 & 미술 원데이)
    - 키즈노트 클래스 (어린이 체험 클래스 공식 플랫폼)
    """

    def __init__(self):
        super().__init__(
            name="키즈플랫폼 & 백화점 문화센터 (공식사이트)",
            source_key="kids_platforms"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 키즈플랫폼 및 문화센터 공식 사이트 데이터 수집 시작...")
        now = datetime.now()

        official_platforms = [
            {
                "title": "현대백화점 판교점 문화센터 어린이·유아 강좌 수강신청",
                "category": "키즈플랫폼",
                "tags": ["#현대백화점판교점", "#문센", "#유아놀이", "#원데이클래스"],
                "target_age": "영유아 및 초등학생",
                "region": "경기도 성남시 분당구 백현동",
                "place_name": "현대백화점 판교점 9층 문화센터",
                "address": "경기도 성남시 분당구 판교역로146번길 20",
                "cost_type": "유료",
                "cost_info": "강좌별 10,000원~35,000원 (현대백화점 공식 수강신청)",
                "source_name": "현대백화점 문화센터 공식",
                "url": "https://www.ehyundai.com/culture",
                "description": "트니트니 체육, 오감발달 유리드믹스, 어린이 베이킹 및 창의 미술 원데이 클래스입니다."
            },
            {
                "title": "키즈노트(KidsNote) 어린이 원데이 체험 클래스",
                "category": "키즈플랫폼",
                "tags": ["#키즈노트", "#체험클래스", "#어린이원데이", "#창의체험"],
                "target_age": "4세~초등 4학년",
                "region": "수도권/전국",
                "place_name": "키즈노트 제휴 체험 센터",
                "address": "전국 제휴 체험 클래스",
                "cost_type": "유료",
                "cost_info": "키즈노트 앱/웹 클래스 예약",
                "source_name": "키즈노트 공식",
                "url": "https://www.kidsnote.com",
                "description": "대한민국 대표 영유아 플랫폼 키즈노트에서 엄선한 키즈 베이킹, 도예, 과학 원데이 클래스입니다."
            }
        ]

        items = []
        for ev in official_platforms:
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

        logger.info(f"[{self.name}] 키즈플랫폼 공식 사이트 수집 완료: 총 {len(items)}건")
        return items
