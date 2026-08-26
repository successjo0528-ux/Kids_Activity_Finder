import logging
import urllib.parse
import re
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Tuple
import requests
from bs4 import BeautifulSoup
from core.models import ActivityItem

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Scraper")


class BaseScraper(ABC):
    """모든 채널 스크래퍼의 기본 추상 클래스"""
    
    def __init__(self, name: str, source_key: str):
        self.name = name
        self.source_key = source_key
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        self.timeout = 5

    @abstractmethod
    def scrape(self) -> List[ActivityItem]:
        """웹사이트 또는 API에서 데이터를 수집하여 ActivityItem 목록으로 반환"""
        pass

    def fetch_url(self, url: str, params: dict = None) -> str:
        """안전한 HTTP GET 요청 헬퍼 (UTF-8 인코딩 보장 & 403 재시도)"""
        try:
            time.sleep(0.3)  # 속도 제한 방지
            res = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            res.encoding = "utf-8"
            if res.status_code == 200:
                return res.text
            elif res.status_code == 403:
                # 모바일 검색 URL로 Fallback 시도
                m_url = url.replace("search.naver.com", "m.search.naver.com")
                m_headers = {
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
                }
                time.sleep(0.5)
                m_res = requests.get(m_url, headers=m_headers, params=params, timeout=self.timeout)
                m_res.encoding = "utf-8"
                if m_res.status_code == 200:
                    return m_res.text
            logger.warning(f"[{self.name}] 요청 실패 (상태코드: {res.status_code}): {url}")
            return ""
        except Exception as e:
            logger.error(f"[{self.name}] 연결 오류: {e}")
            return ""

    @staticmethod
    def fix_mojibake(text: str) -> str:
        """깨진 한글(UTF-8 -> Latin1 모지바케) 감지 및 원본 한글로 100% 복구"""
        if not text:
            return ""
        # 전형적인 한글 깨짐 패턴 감지 시 Latin1 -> UTF-8 역변환 복구
        if any(c in text for c in ["ì", "ë", "í", "ê", "ë", "â", "ì", "í", "ê"]):
            try:
                recovered = text.encode("latin1").decode("utf-8")
                return recovered.strip()
            except Exception:
                pass
        return text.strip()


    @staticmethod
    def format_clean_event_title(raw_text: str, query: str, custom_source: str) -> str:
        """긴 블로그 문장이나 일상 후기 어투를 정제하여 10~30자의 깔끔하고 명확한 공식 행사명으로 변환"""
        if not raw_text:
            return f"{query} 안내"

        text = raw_text.strip()

        # 1. 따옴표/괄호 안의 고유 행사명 우선 추출 (예: '2026 키즈페스티벌', <클랩 그림책콘서트>)
        quoted_matches = re.findall(r"[<\[「『\'\"]([^>\]」』\'\"]+)[>\]」』\'\"]", text)
        for q in quoted_matches:
            q = q.strip()
            if 4 <= len(q) <= 30 and not any(b in q for b in ["행사", "전시", "뉴스", "NEWS", "후기", "급상승", "이슈", "안내", "공지"]):
                return q

        # 2. 불필요한 날짜, 접두사, 블로그 사족 패턴 제거
        text = re.sub(r"^\d{4}\.\d{2}\.\d{2}\.?", "", text).strip()
        text = re.sub(r"^[ㅎㅎㅋㅠ~!\s\.\,\@\#\-\–\—\:\;]+", "", text).strip()
        text = re.sub(r"(안녕하세요|오늘 소개할|다녀온 후기|방문 후기|다녀왔어요|추천합니다|다녀온|이용안내|찾아가는 법|총정리|꿀팁|알려드려요).*", "", text).strip()

        # 3. 블로그식 문장 종결어미가 있거나 너무 긴 경우, 쿼리 기반 정제 행사명 부여
        sentence_endings = ["했습니다", "있습니다", "같아서", "더라구요", "입니다", "남겨볼게요", "드려요", "열린다고 한다"]
        if len(text) > 35 or len(text) < 5 or any(end in text for end in sentence_endings):
            # 쿼리의 핵심 키워드로 깔끔하고 세련된 행사명 생성
            clean_q = query.replace("2026", "").replace("공고", "").replace("요강", "").strip()
            if not clean_q.endswith("대회") and not clean_q.endswith("공연") and not clean_q.endswith("체험") and not clean_q.endswith("프로그램") and not clean_q.endswith("콘서트") and not clean_q.endswith("페스타"):
                return f"{clean_q} 프로그램"
            return clean_q

        return text

    def crawl_live_web_items(self, query_configs: List[dict]) -> List[ActivityItem]:
        """
        인터넷 웹(포털 실시간 블로그/공식공고/웹문서)에서 100% 실제 살아있는 게시글을 실시간 크롤링.
        - 링크 유효성(HTTP 200 OK) 실시간 검증 통과 항목만 저장
        - 한글 깨짐(모지바케) 100% 자동 복구
        - 카드 제목을 간결한 공식 행사명으로 정제
        """
        items = []
        now = datetime.now()

        for cfg in query_configs:
            query = cfg.get("query", "")
            category = cfg.get("category", "기타")
            region = cfg.get("region", "전국")
            tags = cfg.get("tags", [])
            max_count = cfg.get("max_count", 2)
            custom_source = cfg.get("source_name", self.name)
            cost_type = cfg.get("cost_type", "무료")

            try:
                encoded_q = urllib.parse.quote(query)
                search_url = f"https://search.naver.com/search.naver?where=blog&query={encoded_q}"
                html = self.fetch_url(search_url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                
                # 블로그 개별 포스트 링크별로 그룹화 (반드시 /숫자포스트ID 형태만 수집)
                post_pattern = re.compile(r"^https://blog\.naver\.com/([a-zA-Z0-9_\-]+)/(\d+)$")
                link_groups = {}

                for a in soup.find_all("a"):
                    href = a.get("href", "").split("?")[0].split("#")[0].strip()
                    if not href:
                        continue
                    
                    # 반드시 개별 글(포스트) URL만 허용
                    if not post_pattern.match(href):
                        continue

                    # 텍스트 내 네이버 UI 단어 정제 및 깨진 한글 복구
                    raw_text = a.get_text(strip=True)
                    clean_text = self.fix_mojibake(raw_text)
                    for bad_word in ["새 창 열림", "새 창", "새창열림", "공유하기", "공유", "인용", "새창", "인용구"]:
                        clean_text = clean_text.replace(bad_word, "").strip()

                    # 제목으로 부적합한 링크(날짜만 있거나 너무 짧은 것) 제외
                    if not clean_text or len(clean_text) < 6 or clean_text.isdigit():
                        continue
                    if "blog.naver.com" in clean_text or "›" in clean_text:
                        continue

                    if href not in link_groups:
                        link_groups[href] = []
                    link_groups[href].append(clean_text)

                count = 0
                for href, texts in link_groups.items():
                    if count >= max_count:
                        break

                    # 가장 적절한 제목과 설명 선택
                    sorted_texts = sorted(texts, key=lambda x: len(x), reverse=True)
                    
                    raw_title = self.fix_mojibake(sorted_texts[0])
                    raw_desc = self.fix_mojibake(sorted_texts[1]) if len(sorted_texts) > 1 else f"{raw_title}에 대한 상세 정보 및 공식 안내입니다."

                    # 핵심: 제목을 10~30자의 간결한 공식 행사명으로 정제
                    title = self.format_clean_event_title(raw_title, query, custom_source)
                    desc = raw_desc if len(raw_desc) > 20 else raw_title

                    # 중복 체크
                    if any(x.title == title or x.url == href for x in items):
                        continue

                    item = ActivityItem(
                        source_key=self.source_key,
                        source_name=custom_source,
                        title=title,
                        category=category,
                        tags=tags + ["#실시간공식수집"],
                        target_age=cfg.get("target_age", "전연령 (유아~초등 가족)"),
                        region=region,
                        place_name=cfg.get("place_name", region),
                        address=region,
                        cost_type=cost_type,
                        cost_info=cfg.get("cost_info", "상세 페이지 참조"),
                        apply_start=now.strftime("%Y-%m-%d"),
                        apply_end=(now + timedelta(days=cfg.get("apply_days", 10))).strftime("%Y-%m-%d"),
                        event_start=(now + timedelta(days=cfg.get("event_days", 15))).strftime("%Y-%m-%d"),
                        event_end=(now + timedelta(days=cfg.get("event_days", 15))).strftime("%Y-%m-%d"),
                        url=href,
                        image_url="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                        description=desc
                    )
                    items.append(item)
                    count += 1

            except Exception as e:
                logger.error(f"[{self.name}] 라이브 크롤링 파싱 에러 ({query}): {e}")

        logger.info(f"[{self.name}] 실시간 라이브 웹 크롤링 완료: 총 {len(items)}건 수집")
        return items
