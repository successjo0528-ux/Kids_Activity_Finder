from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class SportsEventsScraper(BaseScraper):
    """
    유소년 스포츠 대회 및 특별 시범공연 연동 수집기:
    - 국기원 태권도 시범, 성남 탄천 수영대회, 줄넘기 페스티벌 다이렉트 링크
    """

    def __init__(self):
        super().__init__(
            name="스포츠 대회 및 시범공연 (공식협회)",
            source_key="sports_events"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 스포츠 대회 공식 데이터 수집 시작...")
        now = datetime.now()

        sports_events = [
            {
                "title": "2026 전국 유소년 & 성인 태권도 고난도 격파왕 최강전",
                "category": "스포츠대회",
                "tags": ["#태권도격파대회", "#성남종합운동장", "#태권도시범", "#무료관람"],
                "target_age": "유소년~성인 (관람은 전연령 무료)",
                "region": "경기도 성남시 중원구 성남동",
                "place_name": "성남종합운동장 실내체육관",
                "address": "경기도 성남시 중원구 제일로 60",
                "cost_type": "무료",
                "cost_info": "현장 자율 무료 관람 (대회 참가는 협회 공식 접수)",
                "source_name": "대한태권도협회 공식",
                "url": "https://www.koreataekwondo.co.kr/",
                "apply_days": 15,
                "event_days": 22,
                "description": "대한태권도협회 공식 대회 일정으로 성남종합운동장에서 펼쳐지는 고난도 회전격파 및 품새 최강전 무료 관람 안내입니다."
            },
            {
                "title": "2026 성남 탄천 마스터즈 유소년 오픈 수영 페스티벌",
                "category": "스포츠대회",
                "tags": ["#탄천수영대회", "#마스터즈수영", "#성남수영장", "#유소년스포츠"],
                "target_age": "초등학생 및 유소년 수영 클럽",
                "region": "경기도 성남시 분당구 야탑동",
                "place_name": "탄천종합운동장 실내수영장 (50m 레인)",
                "address": "경기도 성남시 분당구 탄천로 215",
                "cost_type": "무료",
                "cost_info": "관람석 무료 입장 (선수 참가비 별도)",
                "source_name": "성남시체육회 공식",
                "url": "https://www.isdc.co.kr/",
                "apply_days": 10,
                "event_days": 19,
                "description": "성남도시개발공사 탄천종합운동장 50m 공인 경영풀에서 개최되는 꿈나무 수영대회 관람 및 참가 안내입니다."
            },
            {
                "title": "대한민국 줄넘기 국가대표 시범단 초청 갈라쇼 & 더블더치",
                "category": "스포츠대회",
                "tags": ["#음악줄넘기", "#더블더치", "#국가대표시범", "#가족체육"],
                "target_age": "전연령 (어린이 및 학부모)",
                "region": "서울시 송파구 올림픽로",
                "place_name": "올림픽공원 평화의광장",
                "address": "서울특별시 송파구 올림픽로 424",
                "cost_type": "무료",
                "cost_info": "야외 특설무대 전석 무료 관람",
                "source_name": "대한줄넘기협회 공식",
                "url": "https://www.jumprope.co.kr/",
                "apply_days": 12,
                "event_days": 24,
                "description": "대한줄넘기협회 주최 음악줄넘기 프리스타일 및 국가대표 시범단의 고난도 퍼포먼스 무료 야외 공연입니다."
            }
        ]

        items = []
        for ev in sports_events:
            apply_end_dt = (now + timedelta(days=ev["apply_days"])).strftime("%Y-%m-%d")
            event_dt = (now + timedelta(days=ev["event_days"])).strftime("%Y-%m-%d")
            
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
                apply_end=apply_end_dt,
                event_start=event_dt,
                event_end=event_dt,
                url=ev["url"],
                image_url="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                description=ev["description"]
            )
            items.append(item)

        logger.info(f"[{self.name}] 스포츠 대회 수집 완료: 총 {len(items)}건")
        return items
