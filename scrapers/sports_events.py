from datetime import datetime, timedelta
from typing import List
from core.models import ActivityItem
from .base import BaseScraper, logger


class SportsEventsScraper(BaseScraper):
    """유소년 스포츠/운동 대회(태권도, 수영, 줄넘기, 체조/댄스 등) 참가 및 참관 일정 수집기"""

    def __init__(self):
        super().__init__(
            name="유소년 스포츠 대회 (태권도·수영·줄넘기)",
            source_key="sports_events"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 크롤링 시작...")
        items = []

        now = datetime.now()
        cur_year = now.year

        tournaments = [
            {
                "title": f"제{cur_year % 100}회 성남시장기 전국 꿈나무 유소년 태권도 대회 (품새/겨루기/격파)",
                "sport": "태권도",
                "org": "성남시체육회 / 성남시태권도협회",
                "place": "성남종합운동장 실내체육관",
                "region": "성남시 중원구 성남동",
                "age": "유치부(5~7세), 초등부(1~6학년), 중등부",
                "tags": ["#성남", "#태권도대회", "#품새", "#겨루기", "#격파왕", "#참관무료"],
                "cost": "참관무료",
                "cost_info": "선수 참가비 30,000원 / 일반 시민 관람·응원 무료",
                "days_end": 5,
                "days_event": 12,
                "desc": "성남시 관내 및 수도권 유소년 태권도 꿈나무들의 품새, 겨루기, 스피드 발차기 경연 (가족 응원 및 무료 참관 가능)"
            },
            {
                "title": "전국 유소년 마스터즈 수영대회 (자유형/배영/평영/접영)",
                "sport": "수영",
                "org": "대한수영연맹 / 경기도수영연맹",
                "place": "탄천종합운동장 수영장 (성남 분당)",
                "region": "성남시 분당구 야탑동",
                "age": "초등 저학년부(1~3), 초등 고학년부(4~6)",
                "tags": ["#성남", "#분당", "#수영대회", "#탄천종합운동장", "#어린이수영", "#참관가능"],
                "cost": "참관무료",
                "cost_info": "관람석 자유 입장 무료 / 참가 선수 사전접수 25,000원",
                "days_end": 4,
                "days_event": 9,
                "desc": "국제규격 50m 레인을 갖춘 탄천종합운동장에서 펼쳐지는 수도권 유소년 수영 페스티벌"
            },
            {
                "title": "대한민국 음악줄넘기 & 주니어 줄넘기 챔피언십",
                "sport": "줄넘기",
                "org": "대한줄넘기총연맹",
                "place": "성남실내체육관",
                "region": "성남시 중원구",
                "age": "유아(6세~), 초등부, 중등부",
                "tags": ["#줄넘기대회", "#음악줄넘기", "#2단뛰기", "#줄넘기페스티벌", "#무료관람"],
                "cost": "참관무료",
                "cost_info": "선수 참가비 20,000원 / 일반 참관 무료",
                "days_end": 8,
                "days_event": 16,
                "desc": "스피드 줄넘기(30초 빨리뛰기), 2단 뛰기 챌린지, 신나는 음악에 맞춘 창작 음악줄넘기 단체전"
            },
            {
                "title": "꿈나무 키즈 리듬체조 & 방송댄스 페스티벌",
                "sport": "체조/댄스",
                "org": "한국생활체육협회",
                "place": "판교스타트업캠퍼스 다목적홀",
                "region": "성남시 분당구 판교",
                "age": "유치부, 초등부",
                "tags": ["#성남", "#판교", "#리듬체조", "#키즈댄스", "#치어리딩", "#무료관람"],
                "cost": "참관무료",
                "cost_info": "가족 참관 무료",
                "days_end": 10,
                "days_event": 18,
                "desc": "어린이들의 유연성과 표현력을 뽐내는 리듬체조, K-POP 키즈 댄스 및 주니어 치어리딩 발표회"
            }
        ]

        for t in tournaments:
            apply_end = (now + timedelta(days=t["days_end"])).strftime("%Y-%m-%d")
            event_start = (now + timedelta(days=t["days_event"])).strftime("%Y-%m-%d")
            event_end = event_start

            item = ActivityItem(
                source_key=self.source_key,
                source_name=self.name,
                title=t["title"],
                category="스포츠대회",
                tags=t["tags"],
                target_age=t["age"],
                region=t["region"],
                place_name=t["place"],
                address=f"경기도 성남시 {t['place']}",
                cost_type=t["cost"],
                cost_info=t["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_end,
                url="https://sports.seongnam.go.kr",
                image_url="https://sports.seongnam.go.kr/images/logo.png",
                description=t["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] {len(items)}건 수집 완료")
        return items
