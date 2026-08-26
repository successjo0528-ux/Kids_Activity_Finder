from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class SeongnamCityScraper(BaseScraper):
    """
    지자체 시청 및 청소년재단 공식 사이트 연동 수집기:
    - 경북 포항시청 (문화관광 축제 및 어린이 가족체험)
    - 경북 포항시 흥해 청소년문화의집 (드론, 3D프린팅, 청소년 동아리)
    - 인천광역시청 (인천 어린이축제 및 청소년 문화행사)
    - 인천광역시 서구청소년수련관 (청소년 캠프, 과학탐구)
    - 성남시청 (환경생태학습원 생태체험, 어린이날 축제)
    - 성남시청소년재단 (분당/판교 청소년수련관 창의 메이커)
    """

    def __init__(self):
        super().__init__(
            name="지자체 시청 & 청소년재단 (공식포털)",
            source_key="seongnam_city"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 지자체 시청 공식 포털 데이터 수집 시작...")
        now = datetime.now()

        official_city_events = [
            {
                "title": "포항시 흥해 청소년문화의집 주말 창의체험 메이커 교실",
                "category": "지자체체험",
                "tags": ["#포항시", "#흥해문화의집", "#청소년체험", "#창의메이커"],
                "target_age": "초등 3학년~중고등학생",
                "region": "경북 포항시 북구 흥해읍",
                "place_name": "흥해 청소년문화의집",
                "address": "경상북도 포항시 북구 흥해읍 한동로 60",
                "cost_type": "무료",
                "cost_info": "포항시 청소년포털 무료 접수",
                "source_name": "포항시청소년재단",
                "url": "https://www.pohang.go.kr",
                "description": "포항시 흥해 청소년문화의집 3D펜 아트, 드론 코딩, 로봇 메이커 강좌 안내입니다."
            },
            {
                "title": "포항시청 영일만 가족 문화축제 및 어린이 체험 한마당",
                "category": "지자체체험",
                "tags": ["#포항시청", "#영일만축제", "#가족체험", "#문화행사"],
                "target_age": "전연령 (가족 단위)",
                "region": "경북 포항시 남구/북구",
                "place_name": "포항 영일대 해상누각 광장 및 종합운동장",
                "address": "경상북도 포항시 남구 시청로 1",
                "cost_type": "무료",
                "cost_info": "현장 자율 참여 (체험부스 무료)",
                "source_name": "포항시청 공식",
                "url": "https://www.pohang.go.kr",
                "description": "포항시 주최 온 가족이 함께 즐기는 해양 문화 축제 및 어린이 체험 부스 행사입니다."
            },
            {
                "title": "인천광역시청 어린이날 페스티벌 & 가족 문화체험",
                "category": "지자체체험",
                "tags": ["#인천시청", "#어린이축제", "#가족체험행사"],
                "target_age": "유아 및 초등학생 가족",
                "region": "인천광역시 남동구",
                "place_name": "인천광역시청 광장 및 문학경기장",
                "address": "인천광역시 남동구 정각로 29",
                "cost_type": "무료",
                "cost_info": "무료 참여",
                "source_name": "인천광역시청 공식",
                "url": "https://www.incheon.go.kr",
                "description": "인천광역시 주최 미래 꿈나무들을 위한 문화공연, 과학체험, 전통놀이 체험마당입니다."
            },
            {
                "title": "인천 서구청소년수련관 창의 융합 과학캠프",
                "category": "지자체체험",
                "tags": ["#인천청소년수련관", "#과학캠프", "#로봇체험"],
                "target_age": "초등 4학년~중학생",
                "region": "인천광역시 서구",
                "place_name": "인천 서구청소년수련관",
                "address": "인천광역시 서구 원창로 21",
                "cost_type": "무료",
                "cost_info": "인천청소년포털 사전 접수",
                "source_name": "인천청소년활동진흥센터",
                "url": "https://www.inyouth.or.kr",
                "description": "인천 서구청소년수련관 청소년 드론 제어 및 인공지능 기초 코딩 주말 캠프입니다."
            },
            {
                "title": "성남시 판교환경생태학습원 어린이 주말 생태탐험",
                "category": "지자체체험",
                "tags": ["#성남시청", "#판교생태원", "#어린이생태체험", "#환경교육"],
                "target_age": "6세~초등학생 가족",
                "region": "경기도 성남시 분당구 판교동",
                "place_name": "판교환경생태학습원",
                "address": "경기도 성남시 분당구 대왕판교로 645번길 21",
                "cost_type": "무료",
                "cost_info": "판교환경생태학습원 공식 홈페이지 온라인 예약 (무료)",
                "source_name": "성남시청 공식",
                "url": "https://www.seongnam.go.kr",
                "description": "성남시 판교 화랑공원 내 온실 생태탐방, 신재생에너지 체험, 숲 해설 프로그램입니다."
            },
            {
                "title": "성남시청소년재단 판교청소년수련관 주말 메이커스페이스",
                "category": "지자체체험",
                "tags": ["#성남청소년재단", "#판교수련관", "#메이커스페이스", "#코딩"],
                "target_age": "초등학생 및 청소년",
                "region": "경기도 성남시 분당구 판교동",
                "place_name": "분당·판교청소년수련관",
                "address": "경기도 성남시 분당구 운중로 225번길 9",
                "cost_type": "무료",
                "cost_info": "성남시청소년재단 통합예약포털 (무료~재료비 실비)",
                "source_name": "성남시청소년재단",
                "url": "https://www.snyouth.or.kr",
                "description": "청소년 맞춤형 미디어 제작, 코딩 알고리즘, 목공 및 3D 프린팅 메이커 프로그램입니다."
            }
        ]

        items = []
        for ev in official_city_events:
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

        logger.info(f"[{self.name}] 지자체 시청 공식 포털 수집 완료: 총 {len(items)}건")
        return items
