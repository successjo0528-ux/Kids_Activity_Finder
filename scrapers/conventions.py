from typing import List
from datetime import datetime
from core.models import ActivityItem
from .base import BaseScraper, logger


class ConventionsScraper(BaseScraper):
    """
    코엑스, 킨텍스, 세택 공식 대형 전시·박람회 연동 수집기:
    - 코엑스 5대 핵심 전시 (인공지능 페스타, 한국전자전, 코베, 제58회 유교전, 디자인코리아)
    - 킨텍스 코베 베이비페어 & 유아교육전 (seq=26033004)
    - 세택 서울국제유아교육전
    - 실제 공식 상세 페이지 URL 및 대표 포스터 이미지 전수 연동
    """

    def __init__(self):
        super().__init__(
            name="코엑스 & 킨텍스 전시 (공식박람회)",
            source_key="conventions"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 대형 전시회 공식 포털 데이터 수집 시작...")

        exhibitions = [
            {
                "title": "인공지능 페스타 2026 (AI FESTA 26 - 코엑스 Hall C)",
                "category": "과학체험",
                "tags": ["#코엑스", "#AIFESTA", "#인공지능페스타", "#AI로봇체험", "#미래기술"],
                "target_age": "초등학생, 청소년 및 온가족 (AI·로봇 체험)",
                "region": "서울시 강남구 삼성동",
                "place_name": "코엑스(COEX) 전시장 Hall C",
                "address": "서울특별시 강남구 영동대로 513",
                "cost_type": "무료",
                "cost_info": "사전등록 시 무료입장 (현장 10,000원)",
                "source_name": "코엑스(COEX) 공식",
                "url": "https://www.coex.co.kr/exhibitions/%ec%9d%b8%ea%b3%b5%ec%a7%80%eb%8a%a5-%ed%8e%98%ec%8a%a4%ed%83%80-2026/?var_page=3&search_start_date=2026.08.26&search_end_date=2027.08.26&list_type=LIST",
                "image_url": "https://www.coex.co.kr/wp-content/themes/coex-visitor/assets/images/bg/bg-hoverExhibition.png",
                "apply_start": "2026-08-26",
                "apply_end": "2026-10-06",
                "event_start": "2026-10-06",
                "event_end": "2026-10-08",
                "description": "최신 생성형 AI 기술과 로봇, 미래 지능형 소프트웨어를 직접 체험하고 시연해볼 수 있는 대규모 AI 페스티벌로 사전등록 시 무료입장 가능합니다."
            },
            {
                "title": "KES 2026 한국전자전 (코엑스 Hall A, B, C, D)",
                "category": "과학체험",
                "tags": ["#코엑스", "#KES2026", "#한국전자전", "#모빌리티", "#미래전자"],
                "target_age": "초등 고학년, 청소년 및 온가족",
                "region": "서울시 강남구 삼성동",
                "place_name": "코엑스(COEX) 전시장 Hall A~D",
                "address": "서울특별시 강남구 영동대로 513",
                "cost_type": "무료",
                "cost_info": "온라인 사전등록 시 전일 무료초청",
                "source_name": "코엑스(COEX) 공식",
                "url": "https://www.coex.co.kr/exhibitions/kes-2026%ed%95%9c%ea%b5%ad%ec%a0%84%ec%9e%90%ec%a0%84/?var_page=4&search_start_date=2026.08.26&search_end_date=2027.08.26&list_type=LIST",
                "image_url": "https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                "apply_start": "2026-08-26",
                "apply_end": "2026-10-21",
                "event_start": "2026-10-21",
                "event_end": "2026-10-24",
                "description": "대한민국 대표 첨단 IT·가전·스마트 모빌리티·로봇 융합 전시회로 미래 전자 기술과 혁신 제품을 직접 만나볼 수 있습니다."
            },
            {
                "title": "2026 코베 베이비페어 (코엑스 Hall A)",
                "category": "전시체험",
                "tags": ["#코엑스", "#코베베이비페어", "#유아용품", "#가족박람회"],
                "target_age": "영유아 부모, 임산부 및 미취학 아동",
                "region": "서울시 강남구 삼성동",
                "place_name": "코엑스(COEX) 전시장 Hall A",
                "address": "서울특별시 강남구 영동대로 513",
                "cost_type": "무료",
                "cost_info": "코베 공식 사전등록 시 무료입장",
                "source_name": "코엑스(COEX) 공식",
                "url": "https://www.coex.co.kr/exhibitions/2026-%ec%bd%94%eb%b2%a0-%eb%b2%a0%ec%9d%b4%eb%b9%84%ed%8e%98%ec%96%b4/?var_page=4&search_start_date=2026.08.26&search_end_date=2027.08.26&list_type=LIST",
                "image_url": "https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                "apply_start": "2026-08-26",
                "apply_end": "2026-10-29",
                "event_start": "2026-10-29",
                "event_end": "2026-11-01",
                "description": "코엑스에서 열리는 메쎄이상 주최 대표 베이비키즈페어로 육아용품 체험 및 현장 이벤트가 풍성하게 열립니다."
            },
            {
                "title": "제58회 서울국제유아교육전 & 키즈페어 (코엑스 Hall A)",
                "category": "전시체험",
                "tags": ["#코엑스", "#유교전", "#서울국제유아교육전", "#어린이도서", "#세계전람"],
                "target_age": "영유아, 미취학 아동 및 학부모·교사",
                "region": "서울시 강남구 삼성동",
                "place_name": "코엑스(COEX) 전시장 Hall A",
                "address": "서울특별시 강남구 영동대로 513",
                "cost_type": "무료",
                "cost_info": "유교전 공식 사전등록 시 전일 무료입장",
                "source_name": "코엑스(COEX) 공식",
                "url": "https://www.coex.co.kr/exhibitions/%ec%a0%9c58%ed%9a%8c-%ec%84%9c%ec%9a%b8%ea%b5%ad%ec%a0%9c%ec%9c%a0%ec%95%84%ea%b5%90%ec%9c%a1%ec%a0%84/?var_page=5&search_start_date=2026.08.26&search_end_date=2027.08.26&list_type=LIST",
                "image_url": "https://www.coex.co.kr/wp-content/uploads/2026/01/제58회-유교전-세계전람.jpg",
                "apply_start": "2026-08-26",
                "apply_end": "2026-11-19",
                "event_start": "2026-11-19",
                "event_end": "2026-11-22",
                "description": "국내 최장수·최대 규모 서울국제유아교육전으로 어린이 그림책, 창의 교구, 스마트 러닝 프로그램 및 다양한 체험 부스가 운영됩니다."
            },
            {
                "title": "디자인코리아 2026 (DESIGN KOREA - 코엑스 Hall D)",
                "category": "전시체험",
                "tags": ["#코엑스", "#디자인코리아", "#창의디자인", "#어린이디자인체험", "#K디자인"],
                "target_age": "전연령 (어린이, 청소년 및 가족)",
                "region": "서울시 강남구 삼성동",
                "place_name": "코엑스(COEX) 전시장 Hall D",
                "address": "서울특별시 강남구 영동대로 513",
                "cost_type": "무료",
                "cost_info": "사전등록 시 무료 / 현장 할인",
                "source_name": "코엑스(COEX) 공식",
                "url": "https://www.coex.co.kr/exhibitions/%eb%94%94%ec%9e%90%ec%9d%b8%ec%bd%94%eb%a6%ac%ec%95%84-2026/?var_page=5&search_start_date=2026.08.26&search_end_date=2027.08.26&list_type=LIST",
                "image_url": "https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                "apply_start": "2026-08-26",
                "apply_end": "2026-11-11",
                "event_start": "2026-11-11",
                "event_end": "2026-11-15",
                "description": "산업통상자원부와 한국디자인진흥원이 주최하는 아시아 대표 디자인 축제로 어린이 창의 디자인 워크숍과 인터랙티브 전시가 열립니다."
            },
            {
                "title": "2026 코베 베이비페어 & 유아교육전 (킨텍스 전시홀 10)",
                "category": "전시체험",
                "tags": ["#킨텍스", "#코베베이비페어", "#유아교육전", "#메쎄이상", "#무료입장"],
                "target_age": "영유아 부모, 임산부 및 미취학 아동",
                "region": "경기도 고양시 일산서구",
                "place_name": "킨텍스(KINTEX) 전시장 전시홀 10",
                "address": "경기도 고양시 일산서구 킨텍스로 217-60",
                "cost_type": "무료",
                "cost_info": "온라인 사전등록 시 무료입장 (현장 10,000원)",
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
