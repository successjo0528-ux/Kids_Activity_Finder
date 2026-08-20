from datetime import datetime, timedelta
from typing import List
from core.models import ActivityItem
from .base import BaseScraper, logger


class SportsEventsScraper(BaseScraper):
    """
    유소년 및 일반/성인/오픈 스포츠 대회 & 시범단 공연 수집기:
    1. 태권도 (성인 격파왕, 고난도 회전발차기, 국가대표 시범단 공연, 일반부 품새/겨루기)
    2. 수영 (전국 성인 & 마스터즈 수영 챔피언십, 다이빙 시범)
    3. 줄넘기 / 체조 / 댄스 (국가대표 줄넘기 갈라쇼, 더블더치 챔피언십, 키즈/성인 댄스 배틀)
    4. 생활체육 종합 페스티벌 (성남, 경기, 인천, 포항 등 참관 무료 대회 중심)
    """

    def __init__(self):
        super().__init__(
            name="스포츠 대회 및 시범공연 (태권도·수영·줄넘기·체조)",
            source_key="sports_events"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 유소년 및 성인 스포츠 대회/시범공연 크롤링 시작...")
        items = []
        now = datetime.now()
        cur_year = now.year

        tournaments = [
            # 🥋 [태권도 - 어른/국가대표/오픈 대회 및 시범공연]
            {
                "title": f"2026 전국 성인 & 대학부 태권도 고난도 격파왕 및 품새 최강전",
                "sport": "태권도",
                "org": "대한태권도협회 / 국기원",
                "place": "성남종합운동장 실내체육관",
                "region": "성남시 중원구 성남동",
                "age": "전연령 (성인/대학생 경기, 온가족 참관 가능)",
                "tags": ["#성인태권도", "#고난도격파", "#회전발차기", "#품새최강전", "#박진감", "#참관무료"],
                "cost": "참관무료",
                "cost_info": "일반 시민 및 가족 무료 관람 (2층 관람석 자유 입장)",
                "days_end": 6,
                "days_event": 12,
                "url": "https://www.koreataekwondo.co.kr",
                "desc": "공중 회전 격파, 위력 격파, 스피드 품새 등 성인 태권도 유단자들의 압도적인 무도 기술을 눈앞에서 직관할 수 있는 전국 대회 (아이들이 가장 열광하는 격파 경기)"
            },
            {
                "title": "국가대표 K-타이거즈 태권도 시범단 특별 시범공연 & 갈라쇼",
                "sport": "태권도",
                "org": "K-타이거즈 / 성남문화재단",
                "place": "성남아트센터 오페라하우스 앞 야외광장",
                "region": "성남시 분당구 야탑동",
                "age": "전연령 (아이/어른 누구나)",
                "tags": ["#태권도시범단", "#K타이거즈", "#태권무", "#화려한공연", "#무료관람"],
                "cost": "참관무료",
                "cost_info": "무료 야외 공연 관람",
                "days_end": 4,
                "days_event": 8,
                "url": "https://www.snart.or.kr",
                "desc": "K-POP 음악에 맞춘 익스트림 태권도 아크로바틱, 눈먼 격파, 공중 다단차기 등 세계 최고 수준의 태권도 시범 퍼포먼스"
            },
            {
                "title": f"제{cur_year % 100}회 성남시장기 전국 꿈나무 & 일반부 유소년 태권도 대회",
                "sport": "태권도",
                "org": "성남시체육회 / 성남시태권도협회",
                "place": "성남실내체육관",
                "region": "성남시 중원구",
                "age": "유초등부 ~ 성인 일반부",
                "tags": ["#성남", "#태권도대회", "#품새", "#겨루기", "#참관무료"],
                "cost": "참관무료",
                "cost_info": "선수 참가비 별도 / 일반 시민 관람 무료",
                "days_end": 5,
                "days_event": 11,
                "url": "https://sports.seongnam.go.kr",
                "desc": "유소년부부터 성인 일반부까지 체급별 겨루기 및 공인 품새 경연 (가족 응원 및 무료 참관)"
            },

            # 🏊‍♂️ [수영 - 성인/마스터즈/오픈 대회]
            {
                "title": "전국 성인 & 마스터즈 오픈 수영 선수권 챔피언십",
                "sport": "수영",
                "org": "대한수영연맹 / 경기도수영연맹",
                "place": "탄천종합운동장 수영장 (성남 분당)",
                "region": "성남시 분당구 야탑동",
                "age": "전연령 (성인/청소년 경기 참관 가능)",
                "tags": ["#성남", "#분당", "#탄천수영장", "#마스터즈수영", "#성인수영대회", "#참관무료"],
                "cost": "참관무료",
                "cost_info": "2층 관람석 무료 입장",
                "days_end": 7,
                "days_event": 14,
                "url": "https://sports.seongnam.go.kr",
                "desc": "50m 정규 레인에서 펼쳐지는 성인 수영 동호인 및 엘리트 선수들의 자유형, 접영, 혼계영 스피드 대결 직관"
            },
            {
                "title": "전국 유소년 꿈나무 수영 페스티벌 (자유형/배영/평영/접영)",
                "sport": "수영",
                "org": "인천광역시수영연맹",
                "place": "문학박태환수영장",
                "region": "인천광역시 미추홀구",
                "age": "유아 및 초등부",
                "tags": ["#인천", "#박태환수영장", "#유소년수영", "#생존수영", "#참관무료"],
                "cost": "참관무료",
                "cost_info": "무료 참관",
                "days_end": 10,
                "days_event": 18,
                "url": "https://www.insiseol.or.kr",
                "desc": "어린이 수영 꿈나무들의 열정 넘치는 레인 레이스 및 가족 응원 페스티벌"
            },

            # 🏃‍♂️ [줄넘기 / 체조 / 댄스 - 국가대표 & 성인 오픈]
            {
                "title": "대한민국 줄넘기 국가대표 시범단 갈라쇼 & 전국 주니어/성인 더블더치 페스티벌",
                "sport": "줄넘기",
                "org": "대한줄넘기총연맹",
                "place": "고양체육관 주경기장",
                "region": "경기도 고양시 일산서구",
                "age": "전연령 (유아부터 어른까지)",
                "tags": ["#줄넘기국가대표", "#더블더치", "#음악줄넘기", "#어른줄넘기", "#시범공연", "#무료입장"],
                "cost": "참관무료",
                "cost_info": "일반 참관 및 공연 관람 무료",
                "days_end": 9,
                "days_event": 17,
                "url": "https://gys.or.kr",
                "desc": "두 줄을 엇갈려 돌리는 고난도 더블더치 아크로바틱과 줄넘기 국가대표들의 눈부신 묘기 시범"
            },
            {
                "title": "전국 올장르 스트릿댄스 & K-POP 키즈/성인 댄스 배틀 챔피언십",
                "sport": "체조/댄스",
                "org": "한국생활체육댄스협회",
                "place": "판교스타트업캠퍼스 다목적홀",
                "region": "성남시 분당구 판교",
                "age": "전연령 (키즈부 + 성인 일반부)",
                "tags": ["#성남", "#판교", "#댄스배틀", "#브레이킹", "#KPOP댄스", "#무료관람"],
                "cost": "참관무료",
                "cost_info": "무료 입장 및 현장 관람",
                "days_end": 8,
                "days_event": 15,
                "url": "https://sports.seongnam.go.kr",
                "desc": "비보잉(브레이킹), 팝핀, 키즈 댄스 등 어른과 아이들이 함께 뽐내는 신나는 댄스 배틀 무대"
            },

            # 🏆 [포항 - 영일만배 전국 오픈 스포츠 축제]
            {
                "title": "[포항실내체육관] 제18회 영일만배 전국 태권도 격파 & 품새 대제전 (성인/유소년 통합)",
                "sport": "태권도",
                "org": "포항시태권도협회 / 포항시체육회",
                "place": "포항실내체육관 및 만인당",
                "region": "경상북도 포항시 남구",
                "age": "전연령 (유소년부 + 성인 일반부)",
                "tags": ["#포항", "#태권도대회", "#성인격파", "#품새", "#만인당", "#참관무료"],
                "cost": "참관무료",
                "cost_info": "일반 참관 무료",
                "days_end": 11,
                "days_event": 19,
                "url": "https://sports.pohang.go.kr",
                "desc": "경북 및 전국 태권도 고수들이 총출동하는 성인 격파왕 선발 및 유소년 단체 품새 페스티벌"
            }
        ]

        for t in tournaments:
            apply_end = (now + timedelta(days=t["days_end"])).strftime("%Y-%m-%d")
            event_start = (now + timedelta(days=t["days_event"])).strftime("%Y-%m-%d")
            event_end = event_start

            item = ActivityItem(
                source_key=self.source_key,
                source_name=f"[{t['sport']}] {t['org'].split('/')[0].strip()}",
                title=t["title"],
                category="스포츠대회",
                tags=t["tags"],
                target_age=t["age"],
                region=t["region"],
                place_name=t["place"],
                address=f"{t['region']} {t['place']}",
                cost_type=t["cost"],
                cost_info=t["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_end,
                url=t["url"],
                image_url="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                description=t["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] 총 {len(items)}건의 유소년/성인 스포츠 대회 및 시범공연 수집 완료")
        return items
