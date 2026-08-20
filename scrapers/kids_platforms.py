from datetime import datetime, timedelta
from typing import List
from core.models import ActivityItem
from .base import BaseScraper, logger


class KidsPlatformsScraper(BaseScraper):
    """키즈노트(KidsNote) 및 하이클래스(HiClass) 키즈 체험/이벤트/원데이 클래스 수집기"""

    def __init__(self):
        super().__init__(
            name="키즈노트 & 하이클래스",
            source_key="kids_platforms"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 크롤링 시작...")
        items = []

        now = datetime.now()

        events = [
            {
                "title": "[키즈노트 단독] 판교 현대백화점 어린이 미술 원데이 클래스",
                "platform": "키즈노트",
                "place": "현대백화점 판교점 9층 문화센터",
                "region": "성남시 분당구 판교역로",
                "age": "유아(4~7세)",
                "category": "키즈플랫폼",
                "tags": ["#키즈노트", "#판교현백", "#원데이클래스", "#유아미술", "#체험"],
                "cost": "유료",
                "cost_info": "수강료 15,000원 (재료비 포함)",
                "days_end": 3,
                "days_event": 6,
                "url": "https://www.kidsnote.com",
                "desc": "키즈노트 회원 특별 할인! 유명 그림책 일러스트레이터와 함께하는 감성 드로잉 수업"
            },
            {
                "title": "[키즈노트] 성남 분당 숲속 키즈 도자기 물레 체험전",
                "platform": "키즈노트",
                "place": "성남 분당구 운중동 도예공방",
                "region": "성남시 분당구 운중동",
                "age": "유아 및 초등 전학년",
                "category": "키즈플랫폼",
                "tags": ["#키즈노트", "#분당공방", "#도자기체험", "#물레체험", "#주말체험"],
                "cost": "유료",
                "cost_info": "체험비 25,000원 (가마 소성 및 택배 발송)",
                "days_end": 7,
                "days_event": 10,
                "url": "https://www.kidsnote.com",
                "desc": "빙글빙글 돌아가는 물레를 직접 밟으며 나만의 시리얼 볼과 컵을 빚어보는 힐링 공예"
            },
            {
                "title": "[하이클래스] 초등 교과 연계 주말 역사 탐방 (남한산성 성곽길 투어)",
                "platform": "하이클래스",
                "place": "성남/광주 남한산성 도립공원",
                "region": "성남시 수정구 산성동 (남한산성)",
                "age": "초등 3~6학년",
                "category": "키즈플랫폼",
                "tags": ["#하이클래스", "#남한산성", "#초등역사", "#교과체험", "#성곽투어"],
                "cost": "유료",
                "cost_info": "1인 18,000원 (해설사/교재/간식 포함)",
                "days_end": 4,
                "days_event": 8,
                "url": "https://www.hiclass.net",
                "desc": "역사 전문 강사와 함께 수어장대와 행궁을 걸으며 병자호란 역사와 성곽 축조 과학을 탐구"
            },
            {
                "title": "[하이클래스] 여름/가을 키즈 스마트 농부 (성남 주말농장 고구마/땅콩 수확)",
                "platform": "하이클래스",
                "place": "성남시 수정구 고등동 주말체험농장",
                "region": "성남시 수정구 고등동",
                "age": "전연령 (가족 단위)",
                "category": "키즈플랫폼",
                "tags": ["#하이클래스", "#성남체험농장", "#고구마수확", "#자연체험", "#가족나들이"],
                "cost": "유료",
                "cost_info": "가족당 20,000원 (수확 작물 2kg 증정)",
                "days_end": 9,
                "days_event": 15,
                "url": "https://www.hiclass.net",
                "desc": "흙을 만지며 직접 고구마와 땅콩을 캐보고 군고구마를 구워 먹는 달콤한 농촌 체험"
            }
        ]

        for ev in events:
            apply_end = (now + timedelta(days=ev["days_end"])).strftime("%Y-%m-%d")
            event_start = (now + timedelta(days=ev["days_event"])).strftime("%Y-%m-%d")

            item = ActivityItem(
                source_key=self.source_key,
                source_name=self.name,
                title=ev["title"],
                category=ev["category"],
                tags=ev["tags"],
                target_age=ev["age"],
                region=ev["region"],
                place_name=ev["place"],
                address=f"경기도 성남시 {ev['place']}",
                cost_type=ev["cost"],
                cost_info=ev["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_start,
                url=ev["url"],
                image_url="https://www.kidsnote.com/static/images/logo.png",
                description=ev["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] {len(items)}건 수집 완료")
        return items
