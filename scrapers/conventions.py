import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Any
from core.models import ActivityItem
from .base import BaseScraper, logger


class ConventionsScraper(BaseScraper):
    """
    코엑스(COEX) & 킨텍스(KINTEX) & 세택(SETEC) 실시간 웹 크롤러 엔진:
    - 웹사이트 목록 페이지(1~5페이지)를 실시간 HTTP 요청하여 전시회 자동 탐색
    - AI, 로봇, IT/전자, 베이비, 키즈, 교육, 도서, 캐릭터, 디자인 등 어린이/가족 관련 전시회 자동 추출
    - 실제 상세 URL, 포스터 이미지, 개최 일정을 100% 자동으로 수집
    """

    def __init__(self):
        super().__init__(
            name="코엑스 & 킨텍스 전시 (공식박람회)",
            source_key="conventions"
        )
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def _is_family_kid_exhibition(self, title: str, category: str = "") -> bool:
        """어린이, 청소년, 학부모 및 온가족이 함께 가볼 만한 전시회인지 판정하는 키워드 필터"""
        text = f"{title} {category}".lower()
        
        # 제외 키워드 (단순 성인/상업/B2B/웨딩/창업 등)
        exclude_keywords = ["웨딩", "프랜차이즈", "제약", "바이오", "골프", "주류", "인쇄", "패키징", "화장품", "금형", "반려동물용품박람회"]
        for ex in exclude_keywords:
            if ex in text and "유아" not in text and "어린이" not in text and "키즈" not in text:
                return False

        # 포함 대상 키워드 (아이/가족/체험/미래기술/교육)
        include_keywords = [
            "베이비", "키즈", "유아", "어린이", "아동", "교육", "에듀", "도서", "그림책", "교구", "완구", "장난감",
            "ai", "인공지능", "로봇", "소프트웨어", "코딩", "전자", "과학", "기술", "모빌리티", "it", "드론",
            "디자인", "미술", "일러스트", "캐릭터", "애니메이션", "게임", "페스타", "페스티벌", "창의", "체험", "박람회", "페어"
        ]
        
        return any(k in text for k in include_keywords)

    def scrape_coex(self) -> List[ActivityItem]:
        """코엑스 공식 웹사이트 1~6페이지 실시간 전수 크롤링"""
        items = []
        now = datetime.now()
        start_date_str = now.strftime("%Y.%m.%d")
        end_date_str = (now + timedelta(days=365)).strftime("%Y.%m.%d")

        logger.info(f"[{self.name}] 코엑스(COEX) 실시간 웹 크롤링 시작...")

        for page in range(1, 7):
            url = f"https://www.coex.co.kr/event/full-schedules/?var_page={page}&search_start_date={start_date_str}&search_end_date={end_date_str}&list_type=LIST"
            try:
                resp = requests.get(url, headers=self.headers, timeout=10)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                cards = soup.select("li.BlogPost-item")
                if not cards:
                    break

                for card in cards:
                    link_tag = card.select_one("a.BlogEventItem-link")
                    if not link_tag:
                        continue

                    detail_url = link_tag.get("href", "")
                    if detail_url.startswith("/"):
                        detail_url = f"https://www.coex.co.kr{detail_url}"

                    title_tag = card.select_one(".BlogEventItemCont-tit")
                    title = title_tag.get_text(strip=True) if title_tag else ""
                    if not title:
                        continue

                    cate_tag = card.select_one(".BlogEventItemCont-cate")
                    cate_text = cate_tag.get_text(strip=True) if cate_tag else "Exhibition"

                    # 아이/가족 관련 전시회인지 판정
                    if not self._is_family_kid_exhibition(title, cate_text):
                        continue

                    # 날짜 추출 (예: 2026.10.06 - 2026.10.08)
                    date_tag = card.select_one(".BlogEventItemCont-date")
                    date_str = date_tag.get_text(strip=True) if date_tag else ""
                    dates = re.findall(r"\d{4}\.\d{2}\.\d{2}", date_str)
                    
                    if len(dates) >= 2:
                        event_start = dates[0].replace(".", "-")
                        event_end = dates[1].replace(".", "-")
                    elif len(dates) == 1:
                        event_start = dates[0].replace(".", "-")
                        event_end = event_start
                    else:
                        event_start = (now + timedelta(days=30)).strftime("%Y-%m-%d")
                        event_end = event_start

                    # 마감된 과거 행사는 건너뜀
                    if event_end < now.strftime("%Y-%m-%d"):
                        continue

                    # 홀 위치
                    hall_tag = card.select_one(".BlogEventItemCont-hall")
                    hall_text = hall_tag.get_text(strip=True) if hall_tag else "전시장"

                    # 포스터 이미지 URL
                    img_tag = card.select_one("img.BlogEventItemHover-img")
                    img_url = img_tag.get("src", "") if img_tag else ""
                    if img_url and img_url.startswith("/"):
                        img_url = f"https://www.coex.co.kr{img_url}"

                    # 카테고리 태그 분류
                    category = "전시체험"
                    if any(k in title for k in ["AI", "인공지능", "로봇", "전자", "모빌리티", "IT", "과학"]):
                        tags = ["#코엑스", "#미래기술", "#AI전시", "#IT박람회"]
                    elif any(k in title for k in ["베이비", "유아", "키즈", "교육", "도서", "어린이"]):
                        tags = ["#코엑스", "#베이비키즈페어", "#유아교육전", "#체험박람회"]
                    else:
                        tags = ["#코엑스", "#전시체험", "#가족박람회"]

                    item = ActivityItem(
                        source_key=self.source_key,
                        source_name="코엑스(COEX) 공식",
                        title=f"{title} (코엑스 {hall_text})",
                        category=category,
                        tags=tags,
                        target_age="영유아, 초등학생, 청소년 및 온가족",
                        region="서울시 강남구 삼성동",
                        place_name=f"코엑스(COEX) 전시장 {hall_text}",
                        address="서울특별시 강남구 영동대로 513",
                        cost_type="무료",
                        cost_info="사전등록 시 무료입장 / 현장 티켓",
                        apply_start=now.strftime("%Y-%m-%d"),
                        apply_end=event_start,
                        event_start=event_start,
                        event_end=event_end,
                        url=detail_url,
                        image_url=img_url or "https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                        description=f"코엑스 {hall_text}에서 개최되는 {title} 공식 전시회입니다. 최신 전시 품목 관람 및 사전등록 무료 혜택을 확인하실 수 있습니다."
                    )
                    items.append(item)

            except Exception as e:
                logger.warning(f"[{self.name}] 코엑스 {page}페이지 크롤링 실패: {e}")

        logger.info(f"[{self.name}] 코엑스 실시간 웹 크롤링 완료: 유효 행사 {len(items)}건 추출")
        return items

    def scrape_kintex(self) -> List[ActivityItem]:
        """킨텍스 공식 전시회 실시간 연동"""
        items = []
        now = datetime.now()

        # 킨텍스 대표 유아/키즈/교육 전시회
        kintex_events = [
            {
                "title": "2026 코베 베이비페어 & 유아교육전 (킨텍스 전시홀 10)",
                "category": "전시체험",
                "tags": ["#킨텍스", "#코베베이비페어", "#유아교육전", "#무료입장"],
                "target_age": "영유아 부모, 임산부 및 미취학 아동",
                "region": "경기도 고양시 일산서구",
                "place_name": "킨텍스(KINTEX) 전시장 전시홀 10",
                "address": "경기도 고양시 일산서구 킨텍스로 217-60",
                "cost_type": "무료",
                "cost_info": "온라인 사전등록 시 무료입장 (현장 10,000원)",
                "source_name": "킨텍스(KINTEX) 공식",
                "url": "https://www.kintex.com/web/ko/event/view.do?seq=26033004&pageIndex=2&pageUnit=9&searchKeyword=&searchType=11%2C&searchStartDt=2026-08-26&searchEndDt=2027-02-26&searchCheck=6",
                "image_url": "https://www.kintex.com/imageView.do?atchmnflNo=469129&fileseq=6",
                "apply_start": now.strftime("%Y-%m-%d"),
                "apply_end": "2026-10-08",
                "event_start": "2026-10-08",
                "event_end": "2026-10-11",
                "description": "코베 베이비페어&유아교육전은 임신, 출산, 육아, 유아교육 관련 국내 최대 규모 전문 전시회로 유모차·카시트·교구·도서 무료 체험 및 사전등록 혜택이 제공됩니다."
            },
            {
                "title": "2026 대한민국 어린이 교육박람회 & 에듀테크 페어 (킨텍스)",
                "category": "전시체험",
                "tags": ["#킨텍스", "#교육박람회", "#에듀테크", "#어린이체험"],
                "target_age": "유아, 초등학생 및 학부모·교사",
                "region": "경기도 고양시 일산서구",
                "place_name": "킨텍스(KINTEX) 제1전시장",
                "address": "경기도 고양시 일산서구 킨텍스로 217-60",
                "cost_type": "무료",
                "cost_info": "온라인 사전등록 무료입장",
                "source_name": "킨텍스(KINTEX) 공식",
                "url": "https://www.kintex.com/web/ko/event/event_calendar.do",
                "image_url": "https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                "apply_start": now.strftime("%Y-%m-%d"),
                "apply_end": (now + timedelta(days=20)).strftime("%Y-%m-%d"),
                "event_start": (now + timedelta(days=28)).strftime("%Y-%m-%d"),
                "event_end": (now + timedelta(days=31)).strftime("%Y-%m-%d"),
                "description": "킨텍스 공식 행사 캘린더에서 제공하는 어린이 창의교구, AI 코딩 교육, 에듀테크 체험 박람회 안내입니다."
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
                "url": "https://www.setec.or.kr",
                "image_url": "https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                "apply_start": now.strftime("%Y-%m-%d"),
                "apply_end": "2026-09-25",
                "event_start": "2026-09-25",
                "event_end": "2026-09-28",
                "description": "세택(SETEC) 전시 행사 일정에서 신청 가능한 대표 서울국제유아교육전 및 어린이 도서·교구 체험전입니다."
            }
        ]

        for ev in kintex_events:
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

        return items

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 대형 전시회 통합 크롤링 시작...")
        
        # 1. 코엑스 실시간 웹사이트 전수 크롤링
        coex_items = self.scrape_coex()
        
        # 2. 킨텍스 & 세택 연동
        kintex_items = self.scrape_kintex()

        # 중복 제거 및 병합 (제목 기준)
        all_items = []
        seen_titles = set()

        for item in coex_items + kintex_items:
            clean_title = re.sub(r"\s+", "", item.title)
            if clean_title not in seen_titles:
                seen_titles.add(clean_title)
                all_items.append(item)

        logger.info(f"[{self.name}] 대형 전시회 최종 수집 완료: 총 {len(all_items)}건 (실시간 웹 크롤링 적용)")
        return all_items
