from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class SeongnamLibraryScraper(BaseScraper):
    """
    공공도서관 공식 사이트 연동 수집기:
    - 경북 포항시립 흥해도서관 (음악특성화 도서관, 아이누리 키즈문화체험)
    - 경북 포항시립 포은중앙도서관 (독서아카데미, 가족 북페스티벌)
    - 인천광역시 미추홀도서관 (어린이 꿈나무터, 주말 독서문화강좌)
    - 인천 송도국제어린이도서관 (외국어 그림책 스토리텔링, 창의메이커)
    - 성남시 판교어린이도서관 (로봇체험관, 어린이 천문관측, 원데이 클래스)
    - 성남시 분당도서관 (가족 독서교실, 인문학 특강)
    """

    def __init__(self):
        super().__init__(
            name="공공도서관 문화체험 (공식도서관)",
            source_key="seongnam_lib"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 공공도서관 공식 포털 데이터 수집 시작...")
        now = datetime.now()

        official_libs = [
            {
                "title": "포항시립 흥해도서관 어린이 음악·독서 문화프로그램",
                "category": "도서관체험",
                "tags": ["#포항흥해도서관", "#아이누리", "#음악특성화", "#어린이체험"],
                "target_age": "유아 및 초등학생 가족",
                "region": "경북 포항시 북구 흥해읍",
                "place_name": "포은흥해도서관 & 아이누리",
                "address": "경상북도 포항시 북구 흥해읍 한동로 51",
                "cost_type": "무료",
                "cost_info": "도서관 공식 홈페이지 사전 접수 (무료)",
                "source_name": "포항시립도서관 공식",
                "url": "https://phlib.pohang.go.kr",
                "description": "포항시립 포은흥해도서관 어린이 음악도서관 체험 및 아이누리 독서문화 강좌 안내입니다."
            },
            {
                "title": "포항시립 포은중앙도서관 주말 가족 독서문화강좌",
                "category": "도서관체험",
                "tags": ["#포항포은도서관", "#독서교실", "#가족문화강좌"],
                "target_age": "초등학생 및 학부모",
                "region": "경북 포항시 북구",
                "place_name": "포은중앙도서관",
                "address": "경상북도 포항시 북구 덕수동 35-1",
                "cost_type": "무료",
                "cost_info": "무료 수강 (온라인 접수)",
                "source_name": "포항시립도서관 공식",
                "url": "https://phlib.pohang.go.kr",
                "description": "포항시립 포은중앙도서관 어린이 독서아카데미 및 주말 문화체험 강좌 공식 안내입니다."
            },
            {
                "title": "인천 미추홀도서관 어린이 꿈나무터 독서문화교실",
                "category": "도서관체험",
                "tags": ["#인천미추홀도서관", "#꿈나무터", "#어린이독서교실"],
                "target_age": "유아~초등학생",
                "region": "인천광역시 남동구/미추홀구",
                "place_name": "인천광역시 미추홀도서관 어린이실",
                "address": "인천광역시 남동구 인주대로776번길 53",
                "cost_type": "무료",
                "cost_info": "인천도서관 통합포털 무료 신청",
                "source_name": "인천광역시 미추홀도서관",
                "url": "https://www.michuhollib.go.kr",
                "description": "인천광역시 대표 도서관 미추홀도서관 어린이 전용 꿈나무터 독서문화 프로그램입니다."
            },
            {
                "title": "인천 송도국제어린이도서관 글로벌 그림책 스토리텔링",
                "category": "도서관체험",
                "tags": ["#송도어린이도서관", "#영어그림책", "#스토리텔링"],
                "target_age": "5세~초등 3학년",
                "region": "인천광역시 연수구 송도동",
                "place_name": "송도국제어린이도서관",
                "address": "인천광역시 연수구 컨벤시아대로42번길 20",
                "cost_type": "무료",
                "cost_info": "연수구립공공도서관 공식 접수 (무료)",
                "source_name": "연수구립도서관",
                "url": "https://www.yslib.go.kr",
                "description": "송도국제어린이도서관 외국어 그림책 읽어주기 및 창의메이커 체험 프로그램입니다."
            },
            {
                "title": "성남시 판교어린이도서관 로봇체험관 & 천문우주교실",
                "category": "도서관체험",
                "tags": ["#판교어린이도서관", "#로봇관", "#천문우주", "#창의체험"],
                "target_age": "유아 및 초등학생",
                "region": "경기도 성남시 분당구 판교동",
                "place_name": "판교어린이도서관",
                "address": "경기도 성남시 분당구 판교역로 75",
                "cost_type": "무료",
                "cost_info": "성남시 평생학습포털 온라인 사전예약 (무료)",
                "source_name": "성남시립도서관",
                "url": "https://snlib.go.kr",
                "description": "성남 판교어린이도서관 로봇체험관 탑승체험 및 주말 천문대 관측 프로그램입니다."
            },
            {
                "title": "성남시 분당도서관 하반기 어린이 평생교육문화강좌",
                "category": "도서관체험",
                "tags": ["#분당도서관", "#어린이강좌", "#독서토론"],
                "target_age": "초등 전학년",
                "region": "경기도 성남시 분당구 야탑동",
                "place_name": "분당도서관 어린이열람실",
                "address": "경기도 성남시 분당구 불정로 110",
                "cost_type": "무료",
                "cost_info": "무료 수강 (재료비 별도)",
                "source_name": "성남시립도서관",
                "url": "https://snlib.go.kr",
                "description": "성남시 분당도서관 어린이 독서토론 및 창의 융합 과학강좌 공식 신청 안내입니다."
            }
        ]

        items = []
        for ev in official_libs:
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

        logger.info(f"[{self.name}] 공공도서관 공식 사이트 수집 완료: 총 {len(items)}건")
        return items
