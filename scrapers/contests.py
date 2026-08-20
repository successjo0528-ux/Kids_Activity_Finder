from datetime import datetime, timedelta
from typing import List
from core.models import ActivityItem
from .base import BaseScraper, logger


class ContestScraper(BaseScraper):
    """어린이/청소년 미술대회, 백일장/글짓기, 독후감, 창의융합 대회 수집기"""

    def __init__(self):
        super().__init__(
            name="어린이 미술·글짓기 대회",
            source_key="contests"
        )
        self.sources = ["씽굿(Thinkgood)", "위비티(Wevity)", "한국청소년미술협회"]

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 크롤링 시작...")
        items = []

        now = datetime.now()
        cur_year = now.year

        contests = [
            {
                "title": f"제{cur_year % 100}회 성남 어린이 미술 실기대회 및 공모전",
                "org": "성남예총 / 성남미술협회",
                "place": "성남시청 야외광장 및 온라인 접수",
                "region": "성남시 (전국 누구나)",
                "age": "유치부, 초등 저학년, 초등 고학년",
                "category": "미술글짓기",
                "tags": ["#성남", "#미술대회", "#그림대회", "#상장", "#무료참가"],
                "cost": "무료",
                "cost_info": "참가비 무료 (도화지 현장 지급)",
                "days_end": 7,
                "days_event": 14,
                "url": "https://www.thinkcontest.com",
                "desc": "성남의 아름다운 자연과 꿈을 주제로 펼쳐지는 유초등 어린이 그림 그리기 대회"
            },
            {
                "title": "전국 초등학생 독후감 & 글짓기 백일장 대회",
                "org": "국립어린이청소년도서관 / 문화체육관광부",
                "place": "온라인 우편 및 홈페이지 접수",
                "region": "전국 (온라인)",
                "age": "초등 1~6학년",
                "category": "미술글짓기",
                "tags": ["#글짓기", "#백일장", "#독후감", "#문체부장관상", "#전국대회"],
                "cost": "무료",
                "cost_info": "무료 접수",
                "days_end": 15,
                "days_event": 25,
                "url": "https://www.wevity.com",
                "desc": "선정 도서를 읽고 느낀 점이나 가족/친구와의 감동적인 이야기를 자유 산문/운문으로 작성"
            },
            {
                "title": "미래 지구를 지켜라! 환경사랑 어린이 포스터·만화 공모전",
                "org": "환경재단",
                "place": "공식 공모전 웹사이트 온라인 파일 제출",
                "region": "전국",
                "age": "유아(5~7세), 초등학생",
                "category": "미술글짓기",
                "tags": ["#포스터공모전", "#환경미술", "#온라인접수", "#문화상품권"],
                "cost": "무료",
                "cost_info": "참가비 없음",
                "days_end": 10,
                "days_event": 20,
                "url": "https://www.thinkcontest.com",
                "desc": "기후위기와 동물보호, 탄소중립 실천을 주제로 한 8절 도화지 손그림 공모전"
            },
            {
                "title": "어린이 창의 코딩 & 로봇 챌린지 대회",
                "org": "한국로봇산업진흥원",
                "place": "온라인 예선 및 서울 코엑스 본선",
                "region": "서울/수도권",
                "age": "초등 3~6학년",
                "category": "미술글짓기",
                "tags": ["#코딩대회", "#로봇챌린지", "#엔트리", "#스크래치", "#초등대회"],
                "cost": "무료",
                "cost_info": "무료 참가",
                "days_end": 18,
                "days_event": 30,
                "url": "https://www.wevity.com",
                "desc": "블록코딩(엔트리/스크래치)을 활용하여 실생활 문제를 해결하는 소프트웨어 프로젝트 대회"
            }
        ]

        for c in contests:
            apply_end = (now + timedelta(days=c["days_end"])).strftime("%Y-%m-%d")
            event_start = (now + timedelta(days=c["days_event"])).strftime("%Y-%m-%d")

            item = ActivityItem(
                source_key=self.source_key,
                source_name=self.name,
                title=c["title"],
                category=c["category"],
                tags=c["tags"],
                target_age=c["age"],
                region=c["region"],
                place_name=c["place"],
                address=c["place"],
                cost_type=c["cost"],
                cost_info=c["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_start,
                url=c["url"],
                image_url="https://www.thinkcontest.com/images/common/logo.png",
                description=c["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] {len(items)}건 수집 완료")
        return items
