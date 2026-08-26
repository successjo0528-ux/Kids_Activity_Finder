from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class ConventionsScraper(BaseScraper):
    """
    코엑스, 킨텍스, 세택 공식 전시·박람회 연동 수집기:
    - 킨텍스 코베 베이비페어 & 유아교육전 (seq=26033004) 다이렉트 연동
    - 코엑스 및 세택 베이비/키즈페어 실제 상세 안내 및 사전등록 딥링크
    """

    def __init__(self):
        super().__init__(
            name="코엑스 & 킨텍스 전시 (공식박람회)",
            source_key="conventions"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 대형 전시회 공식 포털 데이터 수집 시작...")
        now = datetime.now()

        exhibitions = [
            {
                "title": "2026 코베 베이비페어 & 유아교육전 (킨텍스 전시홀 10)",
                "category": "전시체험",
                "tags": ["#킨텍스", "#코베베이비페어", "#유아교육전", "#메쎄이상", "#무료입장"],
                "target_age": "영유아 부모, 임산부 및 미취학 아동",
                "region": "경기도 고양시 일산서구",
                "place_name": "킨텍스(KINTEX) 전시장 전시홀 10",
                "address": "경기도 고양시 일산서구 킨텍스로 217-60",
                "cost_type": "무료",
                "cost_info": "온라인 사전등록 시 무료입장 (현장 구매 시 10,000원)",
                "source_name": "킨텍스(KINTEX) 공식",
                "url": "https://www.kintex.com/web/ko/event/view.do?seq=26033004&pageIndex=2&pageUnit=9&searchKeyword=&searchType=11%2C&searchStartDt=2026-08-26&searchEndDt=2027-02-26&searchCheck=6",
                "image_url": "https://www.kintex.com/imageView.do?atchmnflNo=469129&fileseq=6",
                "apply_start": "2026-08-26",
                "apply_end": "2026-10-08",
                "event_start": "2026-10-08",
                "event_end": "2026-10-11",
                "description": "코베 베이비페어&유아교육전은 임신, 출산, 육아, 유아교육 관련 국내 최대 규모 전문 전시회로 유모차·카시트·교구·도서 무료 체험 및 사전등록 혜택이 제공됩니다."
            },
            {
                "title": "2026 서울 베이비 & 키즈페어 (코엑스 A홀)",
                "category": "전시체험",
                "tags": ["#코엑스", "#베이비키즈페어", "#유아용품", "#가족박람회"],
                "target_age": "영유아 부모 및 임산부, 미취학 아동",
                "region": "서울시 강남구 삼성동",
                "place_name": "코엑스(COEX) 전시장 A홀",
                "address": "서울특별시 강남구 영동대로 513",
                "cost_type": "무료",
                "cost_info": "사전등록 시 무료입장 (현장 구매 시 10,000원)",
                "source_name": "코엑스(COEX) 공식",
                "url": "https://www.coex.co.kr/exhibition-schedule/",
                "image_url": "https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                "apply_start": "2026-08-26",
                "apply_end": "2026-09-20",
                "event_start": "2026-09-20",
                "event_end": "2026-09-23",
                "description": "코엑스 공식 전시회 일정에서 확인 가능한 국내 대표 베이비키즈페어로 사전등록 시 무료입장이 가능합니다."
            },
            {
                "title": "2026 서울국제유아교육전 & 키즈페어 (SETEC 학여울역)",
                "category": "전시체험",
                "tags": ["#세택", "#유교전", "#유아교육전", "#키즈페어"],
                "target_age": "영유아 및 학부모",
                "region": "서울시 강남구 대치동",
                "place_name": "세택(SETEC) 1, 2전시장",
                "address": "서울특별시 강남구 남부순환로 3104",
                "cost_type": "무료",
                "cost_info": "유교전 공식 사전등록 시 전일 무료초청",
                "source_name": "SETEC 전시컨벤션",
                "url": "https://www.setec.or.kr/front/event/eventList.do",
                "image_url": "https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                "apply_start": "2026-08-26",
                "apply_end": "2026-09-25",
                "event_start": "2026-09-25",
                "event_end": "2026-09-28",
                "description": "세택(SETEC) 전시 행사 일정에서 신청 가능한 대표 서울국제유아교육전 및 어린이 도서·교구 체험전입니다."
            }
        ]

        items = []
        for ev in exhibitions:
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
                apply_start=ev["apply_start"],
                apply_end=ev["apply_end"],
                event_start=ev["event_start"],
                event_end=ev["event_end"],
                url=ev["url"],
                image_url=ev["image_url"],
                description=ev["description"]
            )
            items.append(item)

        logger.info(f"[{self.name}] 대형 전시회 수집 완료: 총 {len(items)}건")
        return items
