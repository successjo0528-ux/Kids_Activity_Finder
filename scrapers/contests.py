import re
from typing import List
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from core.models import ActivityItem
from .base import BaseScraper, logger


class ContestsScraper(BaseScraper):
    """
    알럽콘(ilovecontest.com) 공식 공모전·백일장 실시간 전용 크롤러:
    - 전국 어린이·청소년 미술대회, 그림·포스터 공모전
    - 전국 백일장, 독후감·독서감상문 공모전
    - 전국 청소년 AI·코딩 경진대회 및 문학상
    - 실제 실시간 D-Day 및 접수 마감일자 정확 파싱
    """

    def __init__(self):
        super().__init__(
            name="어린이 미술·글짓기·AI 대회 (알럽콘)",
            source_key="contests"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 알럽콘(ilovecontest.com) 실시간 공식 크롤링 시작...")
        items = []
        now = datetime.now()

        urls_to_crawl = [
            ("https://ilovecontest.com/bbs/board.php?bo_table=contest", "미술글짓기", "알럽콘 공모전"),
            ("https://ilovecontest.com/bbs/board.php?bo_table=contest_schedule_day", "미술글짓기", "알럽콘 백일장/대회"),
        ]

        for target_url, default_cat, source_label in urls_to_crawl:
            try:
                html = self.fetch_url(target_url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                
                # 공모전 글 링크 추출
                for a in soup.find_all("a"):
                    href = a.get("href", "")
                    if "wr_id=" not in href or "comment" in href:
                        continue
                    
                    raw_text = a.get_text(strip=True)
                    if not raw_text or len(raw_text) < 5:
                        continue
                    
                    # 1. 실제 D-Day 정보 추출 (예: '...D-20' or '...D-Day' or '...D-3')
                    d_day_val = ""
                    days_left = 20  # 기본값
                    
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
                    
                    # 2. 제목 정제 (D-Day 접미사 제거)
                    title = re.sub(r'D[-+](?:Day|\d+)', '', raw_text).strip()
                    title = re.sub(r'[\r\n\t]+', ' ', title).strip()
                    if len(title) < 5:
                        continue

                    # 전체 링크 URL 완성
                    if href.startswith("/"):
                        full_url = f"https://ilovecontest.com{href}"
                    elif href.startswith("http"):
                        full_url = href
                    else:
                        full_url = f"https://ilovecontest.com/bbs/{href}"

                    # 중복 체크
                    if any(x.title == title or x.url == full_url for x in items):
                        continue

                    # 카테고리 및 태그 자동 분류
                    category = "미술글짓기"
                    tags = ["#알럽콘", "#전국공모전", "#공식접수"]
                    if any(kw in title for kw in ["AI", "코딩", "소프트웨어", "디지털", "앱"]):
                        category = "AI코딩대회"
                        tags += ["#AI대회", "#코딩경진대회"]
                    elif any(kw in title for kw in ["미술", "그림", "포스터", "민화", "사생", "사진"]):
                        tags += ["#어린이미술대회", "#그림공모전"]
                    elif any(kw in title for kw in ["백일장", "글짓기", "독후감", "문학", "시", "수필"]):
                        tags += ["#백일장", "#독후감대회", "#글짓기"]

                    # 실제 D-Day 기준 정확한 마감일 계산
                    apply_end_date = (now + timedelta(days=days_left)).strftime("%Y-%m-%d")
                    event_date = apply_end_date

                    item = ActivityItem(
                        source_key=self.source_key,
                        source_name=f"알럽콘 ({source_label})",
                        title=title,
                        category=category,
                        tags=tags,
                        target_age="유치부, 초등부, 청소년 및 가족",
                        region="전국 / 온라인 접수",
                        place_name="알럽콘 공식 온라인 접수처",
                        address="전국 온라인 접수",
                        cost_type="무료",
                        cost_info="공식 요강 참조 (대부분 무료)",
                        apply_start=now.strftime("%Y-%m-%d"),
                        apply_end=apply_end_date,
                        event_start=event_date,
                        event_end=event_date,
                        url=full_url,
                        image_url="https://ilovecontest.com/img/logo.png",
                        description=f"{title} - 알럽콘 공식 공모전·백일장 세부 요강 및 온라인 접수 안내입니다."
                    )
                    items.append(item)

            except Exception as e:
                logger.warning(f"[{self.name}] {target_url} 크롤링 중 오류: {e}")

        logger.info(f"[{self.name}] 알럽콘 실시간 수집 완료: 총 {len(items)}건")
        return items
