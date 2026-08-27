import re
import urllib.parse
from typing import List
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from core.models import ActivityItem
from .base import BaseScraper, logger


class ContestsScraper(BaseScraper):
    """
    국내 최대 공모전 3중 통합 크롤러 엔진:
    1. 알럽콘 (ilovecontest.com): 전국 유소년 미술대회, 글짓기·백일장, AI·코딩 대회
    2. 위비티 (wevity.com): 국내 1위 공모전 허브 (어린이·초등·청소년 공모전 전수 수집)
    3. 실시간 대기업 공모전 뉴스 RSS: 현대차·삼성·구몬·금융사 등 대기업 비정기 어린이 공모전 실시간 포착
    """

    def __init__(self):
        super().__init__(
            name="어린이 미술·글짓기·AI 대회 (알럽콘·위비티·기업공모전)",
            source_key="contests"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 3중 공모전 엔진(알럽콘 + 위비티 + 대기업 뉴스 RSS) 실시간 통합 크롤링 시작...")
        items = []
        now = datetime.now()

        # ----------------------------------------------------
        # 1. 알럽콘 (ilovecontest.com) 크롤링
        # ----------------------------------------------------
        ilove_urls = [
            ("https://ilovecontest.com/bbs/board.php?bo_table=contest", "알럽콘 공모전"),
            ("https://ilovecontest.com/bbs/board.php?bo_table=contest_schedule_day", "알럽콘 백일장/대회"),
        ]

        for target_url, source_label in ilove_urls:
            try:
                html = self.fetch_url(target_url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                
                for a in soup.find_all("a"):
                    href = a.get("href", "")
                    if "wr_id=" not in href or "comment" in href:
                        continue
                    
                    raw_text = a.get_text(strip=True)
                    if not raw_text or len(raw_text) < 5:
                        continue
                    
                    days_left = 20
                    parent = a.find_parent("div")
                    parent_text = parent.get_text(separator=" ", strip=True) if parent else raw_text
                    
                    dday_match = re.search(r'D[-+](?:Day|\d+)', parent_text)
                    if dday_match:
                        d_day_val = dday_match.group(0)
                        num_m = re.search(r'D-(\d+)', d_day_val)
                        if num_m:
                            days_left = int(num_m.group(1))
                        elif "D-Day" in d_day_val or "D-0" in d_day_val:
                            days_left = 0
                    
                    title = re.sub(r'D[-+](?:Day|\d+)', '', raw_text).strip()
                    title = re.sub(r'[\r\n\t]+', ' ', title).strip()
                    if len(title) < 5:
                        continue

                    full_url = href if href.startswith("http") else (f"https://ilovecontest.com{href}" if href.startswith("/") else f"https://ilovecontest.com/bbs/{href}")

                    if any(x.title == title or x.url == full_url for x in items):
                        continue

                    category, tags = self._classify_contest(title)
                    tags.append("#알럽콘")

                    apply_end_date = (now + timedelta(days=days_left)).strftime("%Y-%m-%d")

                    item = ActivityItem(
                        source_key=self.source_key,
                        source_name=f"알럽콘 ({source_label})",
                        title=title,
                        category=category,
                        tags=tags,
                        target_age="유치부, 초등부, 청소년 및 온가족",
                        region="전국 / 온라인 접수",
                        place_name="알럽콘 공식 온라인 접수처",
                        address="전국 온라인 접수",
                        cost_type="무료",
                        cost_info="공식 요강 참조 (대부분 무료)",
                        apply_start=now.strftime("%Y-%m-%d"),
                        apply_end=apply_end_date,
                        event_start=apply_end_date,
                        event_end=apply_end_date,
                        url=full_url,
                        image_url="https://ilovecontest.com/img/logo.png",
                        description=f"{title} - 알럽콘 공식 공모전·백일장 세부 요강 및 온라인 접수 안내입니다."
                    )
                    items.append(item)
            except Exception as e:
                logger.warning(f"[{self.name}] 알럽콘 {target_url} 오류: {e}")

        # ----------------------------------------------------
        # 2. 위비티 (wevity.com) 어린이/초등학생/청소년 공모전 크롤링
        # ----------------------------------------------------
        wevity_targets = [
            ("https://www.wevity.com/?c=find&s=1&gub=1&target=1", "어린이·유아"),
            ("https://www.wevity.com/?c=find&s=1&gub=1&target=2", "초등학생"),
            ("https://www.wevity.com/?c=find&s=1&gub=1&target=3", "청소년")
        ]

        for target_url, target_label in wevity_targets:
            try:
                html = self.fetch_url(target_url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                list_items = soup.select("ul.list li")

                for li in list_items:
                    tit_el = li.select_one(".tit a")
                    if not tit_el:
                        continue

                    title = tit_el.get_text(strip=True)
                    title = re.sub(r'(신규|HOT|SPECIAL|IDEA|대기업|\s+)', ' ', title).strip()
                    title = re.sub(r'[\r\n\t]+', ' ', title).strip()
                    if len(title) < 5:
                        continue

                    href = tit_el.get("href", "")
                    full_url = f"https://www.wevity.com/{href}" if (href.startswith("?") or href.startswith("/")) else href

                    if any(x.title == title or x.url == full_url for x in items):
                        continue

                    organ_el = li.select_one(".organ")
                    organ = organ_el.get_text(strip=True) if organ_el else "공식 주최사"

                    dday_el = li.select_one(".dday")
                    dday_text = dday_el.get_text(strip=True) if dday_el else ""

                    days_left = 30
                    if "D-" in dday_text:
                        num_m = re.search(r'D-(\d+)', dday_text)
                        if num_m:
                            days_left = int(num_m.group(1))
                    elif "마감임박" in dday_text or "D-Day" in dday_text:
                        days_left = 3
                    elif "접수예정" in dday_text:
                        days_left = 45

                    apply_end_date = (now + timedelta(days=days_left)).strftime("%Y-%m-%d")
                    category, tags = self._classify_contest(title)
                    tags.extend(["#위비티", f"#{organ}"])

                    item = ActivityItem(
                        source_key=self.source_key,
                        source_name=f"위비티 ({organ})",
                        title=title,
                        category=category,
                        tags=tags,
                        target_age=f"{target_label}, 유치부, 초등부 및 가족",
                        region="전국 / 온라인 접수",
                        place_name=f"{organ} 공식 온라인 접수처",
                        address="전국 온라인 접수",
                        cost_type="무료",
                        cost_info="공식 요강 참조 (대부분 참가비 무료)",
                        apply_start=now.strftime("%Y-%m-%d"),
                        apply_end=apply_end_date,
                        event_start=apply_end_date,
                        event_end=apply_end_date,
                        url=full_url,
                        image_url="https://www.wevity.com/images/common/logo.png",
                        description=f"{title}\n- 주최: {organ}\n- 대상: {target_label} 및 전국 어린이/청소년\n- 접수: 위비티 공식 요강 및 온라인 접수처 참조"
                    )
                    items.append(item)

            except Exception as e:
                logger.warning(f"[{self.name}] 위비티 {target_url} 오류: {e}")

        # ----------------------------------------------------
        # 3. 실시간 대기업·기관 공모전 뉴스 RSS (현대차·구몬 수소 스토리 등)
        # ----------------------------------------------------
        rss_queries = [
            '("현대차" OR "현대자동차" OR "구몬학습" OR "수소 스토리") AND ("공모전" OR "문학상")',
            '("어린이" OR "초등" OR "청소년") AND ("공모전" OR "그림대회" OR "글짓기" OR "창작대회" OR "미술대회")'
        ]

        for query_str in rss_queries:
            try:
                encoded_q = urllib.parse.quote(query_str)
                rss_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=ko&gl=KR&ceid=KR:ko"
                r = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                if r.status_code == 200:
                    rss_soup = BeautifulSoup(r.text, "xml")
                    for news_el in rss_soup.find_all("item")[:10]:
                        title_raw = news_el.title.get_text(strip=True) if news_el.title else ""
                        link = news_el.link.get_text(strip=True) if news_el.link else ""
                        if not title_raw or not link:
                            continue

                        # " - 언론사" 분리
                        parts = title_raw.rsplit(" - ", 1)
                        title = parts[0].strip()
                        source_media = parts[1].strip() if len(parts) > 1 else "언론사 보도자료"

                        # 제목 정제 및 따옴표 제거
                        title = re.sub(r'^[“"\'\[\(]+|[”"\'\]\)]+$', '', title).strip()
                        if len(title) < 8:
                            continue

                        if any(x.title == title or x.url == link for x in items):
                            continue

                        # 주최 기관 추론
                        organ = "대기업/공공기관"
                        if "현대차" in title or "현대자동차" in title or "구몬" in title:
                            organ = "현대차그룹·구몬학습"
                        elif "iM뱅크" in title or "대구은행" in title:
                            organ = "iM뱅크"
                        elif "삼성" in title:
                            organ = "삼성전자"

                        category, tags = self._classify_contest(title)
                        tags.extend(["#대기업공모전", "#보도자료", f"#{organ}"])

                        # 기본 마감일은 30~60일 뒤로 설정
                        days_left = 60 if "구몬" in title or "현대차" in title else 30
                        apply_end_date = (now + timedelta(days=days_left)).strftime("%Y-%m-%d")

                        item = ActivityItem(
                            source_key=self.source_key,
                            source_name=f"{organ} ({source_media})",
                            title=title,
                            category=category,
                            tags=tags,
                            target_age="유치부, 초등부, 청소년 및 온가족",
                            region="전국 / 공식 접수처",
                            place_name=f"{organ} 공식 공모전 접수처",
                            address="전국 온라인 접수",
                            cost_type="무료",
                            cost_info="참가비 무료 (공식 요강 참조)",
                            apply_start=now.strftime("%Y-%m-%d"),
                            apply_end=apply_end_date,
                            event_start=apply_end_date,
                            event_end=apply_end_date,
                            url=link,
                            image_url="https://www.wevity.com/images/common/logo.png",
                            description=f"{title}\n- 주최: {organ}\n- 대상: 유아부, 초등부, 중고등부 및 가족\n- 접수 및 세부 요강: 공식 보도자료 및 주최사 접수 페이지 참조"
                        )
                        items.append(item)
            except Exception as e:
                logger.warning(f"[{self.name}] 뉴스 RSS {query_str} 크롤링 오류: {e}")

        logger.info(f"[{self.name}] 3중 공모전 엔진 실시간 수집 완료: 총 {len(items)}건")
        return items

    def _classify_contest(self, title: str):
        """제목 기반 지능형 카테고리 및 태그 자동 분류"""
        category = "미술글짓기"
        tags = ["#전국공모전", "#공식접수"]
        
        if any(kw in title for kw in ["AI", "코딩", "소프트웨어", "SW", "디지털", "로봇", "앱", "과학", "수소"]):
            category = "AI코딩대회"
            tags += ["#AI대회", "#SW코딩대회", "#과학창작"]
        elif any(kw in title for kw in ["미술", "그림", "포스터", "웹툰", "만화", "사생", "사진", "디자인"]):
            category = "미술글짓기"
            tags += ["#어린이미술대회", "#그림공모전"]
        elif any(kw in title for kw in ["백일장", "글짓기", "독후감", "문학", "스토리", "시", "수필", "동시", "산문"]):
            category = "미술글짓기"
            tags += ["#창작문학", "#글짓기대회", "#백일장"]

        return category, tags
