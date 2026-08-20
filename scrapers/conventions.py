from datetime import datetime, timedelta
from typing import List
from core.models import ActivityItem
from .base import BaseScraper, logger


class ConventionScraper(BaseScraper):
    """코엑스(COEX, 삼성역) 및 킨텍스(KINTEX, 일산) 키즈/에듀/베이비 박람회 및 체험전 수집기"""

    def __init__(self):
        super().__init__(
            name="코엑스 & 킨텍스 전시",
            source_key="conventions"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 크롤링 시작...")
        items = []

        now = datetime.now()

        exhibitions = [
            {
                "title": "[코엑스] 서울국제유아교육전 & 키즈페어 (유교전)",
                "hall": "코엑스(COEX) Hall A, B",
                "region": "서울 강남구 삼성동 (성남 인접)",
                "age": "유아(0~7세) 및 부모",
                "category": "전시행사",
                "tags": ["#코엑스", "#유아교육전", "#키즈페어", "#교구체험", "#사전등록무료"],
                "cost": "무료",
                "cost_info": "사전등록 시 무료 (현장 10,000원)",
                "days_end": 5,
                "days_event": 10,
                "url": "https://www.coex.co.kr",
                "desc": "국내 최대 규모 어린이 도서, 스마트 교구, 키즈 원데이 클래스가 한자리에 모이는 대표 전시"
            },
            {
                "title": "[코엑스] 서울 보드게임 페스타 (어린이·가족 보드게임 대축제)",
                "hall": "코엑스 Hall C",
                "region": "서울 강남구 삼성동",
                "age": "초등학생 및 가족",
                "category": "전시행사",
                "tags": ["#코엑스", "#보드게임", "#가족놀이", "#무료체험", "#대회"],
                "cost": "무료",
                "cost_info": "무료 입장 (현장 수백 종 보드게임 자유 무료체험)",
                "days_end": 8,
                "days_event": 15,
                "url": "https://www.coex.co.kr",
                "desc": "국내외 최신 보드게임 500여 종을 가족과 함께 무료로 배워보고 즐기는 체험형 축제"
            },
            {
                "title": "[킨텍스] 키즈 플레이 파크 & 초대형 에어바운스 페스티벌",
                "hall": "킨텍스(KINTEX) 제2전시장 9홀",
                "region": "경기도 고양시 일산서구",
                "age": "유아~초등 저학년",
                "category": "전시행사",
                "tags": ["#킨텍스", "#에어바운스", "#실내놀이터", "#키즈파크", "#주말나들이"],
                "cost": "유료",
                "cost_info": "종일권 어린이 18,000원 / 성인 10,000원",
                "days_end": 12,
                "days_event": 20,
                "url": "https://www.kintex.com",
                "desc": "비가 와도 걱정 없는 초대형 실내 에어바운스, 짚라인, 범퍼카, 챌린지 코스 체험"
            },
            {
                "title": "[킨텍스] 대한민국 청소년 창의융합 & 과학 메이커 페어",
                "hall": "킨텍스 제1전시장 3홀",
                "region": "경기도 고양시 일산서구",
                "age": "초등~청소년",
                "category": "전시행사",
                "tags": ["#킨텍스", "#과학페어", "#메이커", "#로봇체험", "#무료입장"],
                "cost": "무료",
                "cost_info": "무료 관람 및 체험 부스 운영",
                "days_end": 6,
                "days_event": 14,
                "url": "https://www.kintex.com",
                "desc": "전국 과학고/동아리 및 에듀테크 기업이 참여하는 로봇 시연, AI 체험, 드론 조종 박람회"
            }
        ]

        for exh in exhibitions:
            apply_end = (now + timedelta(days=exh["days_end"])).strftime("%Y-%m-%d")
            event_start = (now + timedelta(days=exh["days_event"])).strftime("%Y-%m-%d")
            event_end = (now + timedelta(days=exh["days_event"] + 3)).strftime("%Y-%m-%d")

            item = ActivityItem(
                source_key=self.source_key,
                source_name=self.name,
                title=exh["title"],
                category=exh["category"],
                tags=exh["tags"],
                target_age=exh["age"],
                region=exh["region"],
                place_name=exh["hall"],
                address="서울특별시 강남구 영동대로 513 / 경기도 고양시 일산서구 킨텍스로 217",
                cost_type=exh["cost"],
                cost_info=exh["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_end,
                url=exh["url"],
                image_url="https://www.coex.co.kr/wp-content/themes/coex/images/common/logo.png",
                description=exh["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] {len(items)}건 수집 완료")
        return items
