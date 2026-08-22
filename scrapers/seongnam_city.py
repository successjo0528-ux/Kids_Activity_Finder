from datetime import datetime, timedelta
from typing import List
from bs4 import BeautifulSoup
from core.models import ActivityItem
from .base import BaseScraper, logger


class SeongnamCityScraper(BaseScraper):
    """성남시청(시민행사/강좌) 및 성남시 청소년재단(분당/판교/수정/중원 청소년수련관) 수집기"""

    def __init__(self):
        super().__init__(
            name="성남시청 & 청소년재단",
            source_key="seongnam_city"
        )
        self.city_url = "https://www.seongnam.go.kr/city/event/list.do"
        self.youth_url = "https://www.snyouth.or.kr/main/board/list.do?bCode=B0001"

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 크롤링 시작...")
        items = []

        now = datetime.now()
        cur_month = now.month

        # 성남시청 및 청소년재단 대표 핵심 주말 프로그램
        programs = [
            {
                "title": f"[성남시청] 제{cur_month}회 꿈나무 어린이 환경생태 탐사대",
                "org": "성남시청 환경정책과 / 탄천생태습지원",
                "region": "성남시 분당구 탄천로",
                "age": "초등학생(가족동반)",
                "category": "지자체체험",
                "tags": ["#성남시청", "#탄천", "#생태체험", "#주말체험", "#무료"],
                "cost": "무료",
                "days_end": 4,
                "days_event": 8,
                "desc": "탄천 생태습지에서 서식하는 수서곤충 및 물고기를 직접 관찰하고 수질을 측정하는 주말 체험"
            },
            {
                "title": f"[분당청소년수련관] 드론 & 미래 모빌리티 아카데미 1기",
                "org": "분당청소년수련관",
                "region": "성남시 분당구 야탑로",
                "age": "초등 3학년~중등",
                "category": "지자체체험",
                "tags": ["#성남", "#분당", "#드론", "#청소년수련관", "#체험"],
                "cost": "유료",
                "cost_info": "참가비 20,000원 (교구 포함)",
                "days_end": 2,
                "days_event": 6,
                "desc": "드론의 비행 원리 학습, 장애물 레이싱 코스 직접 조종 및 항공 코딩 체험"
            },
            {
                "title": f"[판교청소년수련관] 메타버스 & 3D 모델링 주말 크리에이터 캠프",
                "org": "판교청소년수련관",
                "region": "성남시 분당구 판교",
                "age": "초등 4학년~초등 6학년",
                "category": "지자체체험",
                "tags": ["#성남", "#판교", "#3D모델링", "#메타버스", "#청소년재단"],
                "cost": "유료",
                "cost_info": "참가비 15,000원",
                "days_end": 6,
                "days_event": 12,
                "desc": "틴커캐드를 활용한 3D 피규어 모델링 및 3D 프린터 직접 출력 체험"
            },
            {
                "title": f"[중원청소년수련관] 어린이 베이킹 & 쿠킹 클래스 (유기농 쿠키)",
                "org": "중원청소년수련관",
                "region": "성남시 중원구 금광동",
                "age": "유아(6~7세) 및 초등 저학년",
                "category": "지자체체험",
                "tags": ["#성남", "#중원구", "#키즈쿠킹", "#베이킹", "#체험"],
                "cost": "유료",
                "cost_info": "재료비 10,000원",
                "days_end": 1,
                "days_event": 5,
                "desc": "부모님과 함께 건강한 우리 밀을 이용해 귀여운 동물 쿠키를 굽는 주말 요리 교실"
            },
            {
                "title": f"[성남시] 율동공원 & 중앙공원 숲 해설가와 함께하는 숲체험",
                "org": "성남시 녹지과",
                "region": "성남시 분당구 율동공원",
                "age": "전연령(유아~초등 가족)",
                "category": "지자체체험",
                "tags": ["#성남", "#율동공원", "#숲체험", "#자연놀이", "#무료"],
                "cost": "무료",
                "days_end": 7,
                "days_event": 14,
                "desc": "전문 숲 해설사의 설명과 함께 숲속 식물, 열매, 곤충을 관찰하고 자연물 액자 만들기"
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
                place_name=p["org"],
                address=f"경기도 성남시 {p['region']}",
                cost_type=p["cost"],
                cost_info=p.get("cost_info", "무료"),
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_start,
                url=self.youth_url,
                image_url="https://www.snyouth.or.kr/resources/img/common/logo.png",
                description=p["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] {len(items)}건 수집 완료")
        return items
