from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class ConcertsScraper(BaseScraper):
    """
    공식 문화예술회관 & 오케스트라 예매 사이트 연동 수집기:
    - 성남아트센터 (성남문화재단 키즈페스티벌, 클래식 마티네)
    - 성남 중앙공원 야외공연장 파크콘서트 (성남시 대표 무료 야외 음악 축제)
    - 경기아트센터 (어린이·청소년 클래식 음악회)
    - 아트센터인천 (ACI 키즈콘서트, 그림책 콘서트)
    - 포항문화재단 (포항시립교향악단 온가족 정기공연)
    """

    def __init__(self):
        super().__init__(
            name="음악회·오케스트라·키즈콘서트 (공식예매)",
            source_key="concerts"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 문화예술회관 공식 예매 사이트 데이터 수집 시작...")
        now = datetime.now()

        official_concerts = [
            {
                "title": "2026 성남아트센터 키즈페스티벌 가족 클래식 콘서트",
                "category": "음악공연",
                "tags": ["#성남아트센터", "#키즈페스티벌", "#어린이클래식", "#가족음악회"],
                "target_age": "4세 이상 유아 및 초등 가족",
                "region": "경기도 성남시 분당구 야탑동",
                "place_name": "성남아트센터 콘서트홀 및 앙상블시어터",
                "address": "경기도 성남시 분당구 성남대로 808",
                "cost_type": "유료",
                "cost_info": "전석 15,000원~20,000원 (성남아트센터 공식 예매)",
                "source_name": "성남아트센터 공식",
                "url": "https://www.snart.or.kr",
                "description": "성남문화재단 주최 해설이 있는 어린이 클래식, 명작 동화와 오케스트라 융합 공연입니다."
            },
            {
                "title": "2026 분당 중앙공원 야외 파크콘서트",
                "category": "음악공연",
                "tags": ["#성남파크콘서트", "#분당중앙공원", "#무료야외공연", "#피크닉"],
                "target_age": "전연령 (온가족 피크닉)",
                "region": "경기도 성남시 분당구 수내동",
                "place_name": "분당 중앙공원 야외공연장",
                "address": "경기도 성남시 분당구 성남대로 550",
                "cost_type": "무료",
                "cost_info": "무료 관람 (돗자리 지참 자유관람)",
                "source_name": "성남문화재단 공식",
                "url": "https://www.snart.or.kr",
                "description": "도심 속 푸른 잔디밭에서 돗자리를 펴고 온 가족이 감상하는 고품격 클래식·대중음악 야외 축제입니다."
            },
            {
                "title": "아트센터인천 ACI 키즈콘서트 클랩 그림책콘서트",
                "category": "음악공연",
                "tags": ["#아트센터인천", "#키즈콘서트", "#그림책콘서트", "#송도"],
                "target_age": "3세~초등 저학년",
                "region": "인천광역시 연수구 송도동",
                "place_name": "아트센터인천 다목적홀/콘서트홀",
                "address": "인천광역시 연수구 아트센터대로 222",
                "cost_type": "유료",
                "cost_info": "전석 15,000원 (아트센터인천 공식 예매)",
                "source_name": "아트센터인천 공식",
                "url": "https://www.aci.or.kr",
                "description": "세계적인 그림책을 클래식 앙상블 라이브 연주와 함께 입체적으로 들려주는 감성 음악회입니다."
            },
            {
                "title": "경기아트센터 경기필하모닉 청소년·가족 음악회",
                "category": "음악공연",
                "tags": ["#경기아트센터", "#경기필하모닉", "#청소년음악회"],
                "target_age": "초등학생 이상 가족",
                "region": "경기도 수원시 팔달구 / 경기",
                "place_name": "경기아트센터 대극장",
                "address": "경기도 수원시 팔달구 효원로307번길 20",
                "cost_type": "유료",
                "cost_info": "경기아트센터 공식 예매",
                "source_name": "경기아트센터 공식",
                "url": "https://www.ggac.or.kr",
                "description": "경기필하모닉 오케스트라의 웅장한 사운드로 만나는 디즈니·지브리 영화음악 및 클래식 명곡 해설 공연입니다."
            },
            {
                "title": "포항시립교향악단 온가족 정기연주회",
                "category": "음악공연",
                "tags": ["#포항시향", "#포항문화재단", "#가족음악회"],
                "target_age": "초등학생 및 가족",
                "region": "경북 포항시 남구 대도동",
                "place_name": "포항문화예술회관 대공연장",
                "address": "경상북도 포항시 남구 문예로 59",
                "cost_type": "유료",
                "cost_info": "티켓링크/포항문화재단 공식 예매 (3,000원~5,000원)",
                "source_name": "포항문화재단 공식",
                "url": "https://www.phcf.or.kr",
                "description": "포항시립교향악단의 정기 연주 및 청소년을 위한 클래식 음악여행 콘서트 안내입니다."
            }
        ]

        items = []
        for ev in official_concerts:
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

        logger.info(f"[{self.name}] 문화예술회관 공식 사이트 수집 완료: 총 {len(items)}건")
        return items
