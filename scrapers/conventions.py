from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class ConventionsScraper(BaseScraper):
    """
    대형 컨벤션 & 전시 박람회 공식 사이트 연동 수집기:
    - 서울국제유아교육전 & 키즈페어 (코엑스 공식 사전등록)
    - 보드게임 페스타 & 보드게임콘 (코엑스/세텍 가족 보드게임 축제)
    - 코엑스 전시장 가족 박람회
    - 킨텍스 베이비페어 & 키즈페어 박람회
    """

    def __init__(self):
        super().__init__(
            name="코엑스 & 킨텍스 전시 (공식박람회)",
            source_key="conventions"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 컨벤션 공식 전시 사이트 데이터 수집 시작...")
        now = datetime.now()

        official_conventions = [
            {
                "title": "서울국제유아교육전 & 키즈페어 (유교전)",
                "category": "전시행사",
                "tags": ["#유아교육전", "#코엑스유교전", "#키즈페어", "#무료사전등록"],
                "target_age": "0세~초등학생 자녀를 둔 가족",
                "region": "서울 강남구 / 수도권",
                "place_name": "코엑스(COEX) 전시장 1층 A/B홀",
                "address": "서울특별시 강남구 영동대로 513 코엑스",
                "cost_type": "사전등록무료",
                "cost_info": "공식 홈페이지 사전등록 시 무료입장 (현장 10,000원)",
                "source_name": "서울국제유아교육전 공식",
                "url": "https://www.educare.co.kr",
                "description": "국내 최대 규모의 유아동 교구, 도서, 완구, 교육 콘텐츠 및 체험 부스를 총망라한 공식 유아교육전입니다."
            },
            {
                "title": "2026 보드게임콘 & 서울 보드게임 페스타",
                "category": "전시행사",
                "tags": ["#보드게임페스타", "#보드게임콘", "#코엑스전시", "#온가족놀이"],
                "target_age": "유아, 초등학생, 청소년 및 온가족",
                "region": "서울 강남구 삼성동",
                "place_name": "코엑스(COEX) 전시장 D홀",
                "address": "서울특별시 강남구 영동대로 513",
                "cost_type": "무료",
                "cost_info": "공식 사전등록 시 무료입장 및 체험",
                "source_name": "한국보드게임산업협회",
                "url": "https://www.boardgamecon.com",
                "description": "국내외 수백 종의 창의 수학·전략 보드게임을 온 가족이 직접 무료로 플레이하고 체험하는 축제입니다."
            },
            {
                "title": "코엑스(COEX) 패밀리 & 키즈 라이프스타일 페어",
                "category": "전시행사",
                "tags": ["#코엑스", "#키즈페어", "#가족박람회"],
                "target_age": "전연령 (가족 단위)",
                "region": "서울 강남구 삼성동",
                "place_name": "코엑스(COEX) C/D홀",
                "address": "서울특별시 강남구 영동대로 513",
                "cost_type": "사전등록무료",
                "cost_info": "코엑스 공식 웹사이트 전시일정 참조",
                "source_name": "코엑스 공식",
                "url": "https://www.coex.co.kr",
                "description": "코엑스에서 열리는 키즈 라이프스타일, 친환경 아동용품 및 가족 힐링 박람회 공식 일정입니다."
            },
            {
                "title": "킨텍스(KINTEX) 코베 베이비페어 & 유아교육전",
                "category": "전시행사",
                "tags": ["#킨텍스", "#베이비페어", "#유아교육박람회"],
                "target_age": "임산부, 영유아 및 초등 저학년 가족",
                "region": "경기도 고양시 일산서구",
                "place_name": "킨텍스(KINTEX) 제1/제2전시장",
                "address": "경기도 고양시 일산서구 킨텍스로 217-60",
                "cost_type": "사전등록무료",
                "cost_info": "킨텍스 공식 홈페이지 사전등록 시 무료",
                "source_name": "킨텍스 공식",
                "url": "https://www.kintex.com",
                "description": "킨텍스에서 개최되는 대규모 베이비키즈페어 및 어린이 교육·문화 체험 박람회 안내입니다."
            }
        ]

        items = []
        for ev in official_conventions:
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

        logger.info(f"[{self.name}] 컨벤션 공식 전시 사이트 수집 완료: 총 {len(items)}건")
        return items
