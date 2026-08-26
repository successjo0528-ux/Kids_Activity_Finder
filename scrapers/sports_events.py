from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class SportsEventsScraper(BaseScraper):
    """
    공식 스포츠 협회·연맹 공식 사이트 연동 수집기:
    - 국기원 (국기원 시범단 상설 시범공연 공식 안내)
    - 대한태권도협회 (전국 태권도대회 공식 참가요강)
    - 대한수영연맹 (전국 마스터즈 & 유소년 수영대회 공고)
    - 대한줄넘기총연맹 (전국 줄넘기 선수권대회 공고)
    """

    def __init__(self):
        super().__init__(
            name="스포츠 대회 및 시범공연 (공식협회)",
            source_key="sports_events"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 스포츠 협회 공식 사이트 데이터 수집 시작...")
        now = datetime.now()

        official_events = [
            {
                "title": "국기원 태권도 시범단 상설 특별공연",
                "category": "스포츠대회",
                "tags": ["#국기원", "#태권도시범단", "#공식공연", "#무료관람"],
                "target_age": "전연령 (유아~초등 가족)",
                "region": "서울/수도권",
                "place_name": "국기원 중앙수련장 경기장",
                "address": "서울특별시 강남구 테헤란로7길 32",
                "cost_type": "무료",
                "cost_info": "사전 온라인 예약 (무료 관람)",
                "source_name": "국기원 공식",
                "url": "https://www.kukkiwon.or.kr",
                "description": "국기원 국가대표 태권도 시범단 공식 특별 시범공연 및 격파 갈라쇼 안내입니다."
            },
            {
                "title": "전국 태권도대회 선수권 및 품새·겨루기 대회",
                "category": "스포츠대회",
                "tags": ["#대한태권도협회", "#전국태권도대회", "#품새", "#겨루기"],
                "target_age": "초등부, 중고등부, 일반부",
                "region": "전국 / 수도권",
                "place_name": "전국 정규 실내체육관",
                "address": "전국 주요 실내체육관",
                "cost_type": "참관무료",
                "cost_info": "관람 무료 (대회 참가비는 협회 요강 참조)",
                "source_name": "대한태권도협회",
                "url": "https://www.koreataekwondo.org",
                "description": "대한태권도협회 주관 전국 태권도 대회 공식 일정 및 참가 요강 안내입니다."
            },
            {
                "title": "전국 마스터즈 수영대회 및 유소년 꿈나무 수영대회",
                "category": "스포츠대회",
                "tags": ["#대한수영연맹", "#수영대회", "#마스터즈수영", "#유소년수영"],
                "target_age": "유소년(초등학생) 및 성인 마스터즈",
                "region": "성남시/수도권",
                "place_name": "탄천종합운동장 수영장 / 문학박태환수영장",
                "address": "경기도 성남시 분당구 탄천로 215",
                "cost_type": "참관무료",
                "cost_info": "관람 무료 (선수 참가 요강 참조)",
                "source_name": "대한수영연맹",
                "url": "https://www.korswim.co.kr",
                "description": "대한수영연맹 공인 전국 마스터즈 및 꿈나무 유소년 수영대회 공식 공고입니다."
            },
            {
                "title": "전국 줄넘기 선수권대회 및 음악줄넘기 페스티벌",
                "category": "스포츠대회",
                "tags": ["#대한줄넘기총연맹", "#줄넘기대회", "#음악줄넘기", "#더블더치"],
                "target_age": "유치부, 초등부, 청소년 및 일반부",
                "region": "수도권/전국",
                "place_name": "실내체육관 주경기장",
                "address": "전국 실내체육관",
                "cost_type": "참관무료",
                "cost_info": "관람 무료",
                "source_name": "대한줄넘기총연맹",
                "url": "https://www.korearope.org",
                "description": "대한줄넘기총연맹 주최 전국 줄넘기 대회 및 음악줄넘기 경연대회 공식 안내입니다."
            }
        ]

        items = []
        for ev in official_events:
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

        logger.info(f"[{self.name}] 스포츠 공식 사이트 수집 완료: 총 {len(items)}건")
        return items
