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
                    if "wr_id=" not in href:
                        continue
                    
                    title = a.get_text(strip=True)
                    if not title or len(title) < 5:
                        continue
                    
                    # D-day 접미사 및 태그 정제 (예: '...D-24')
                    title = title.split("D-")[0].split("D+")[0].strip()
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
                    elif any(kw in title for kw in ["미술", "그림", "포스터", "민화", "사생"]):
                        tags += ["#어린이미술대회", "#그림공모전"]
                    elif any(kw in title for kw in ["백일장", "글짓기", "독후감", "문학", "시", "수필"]):
                        tags += ["#백일장", "#독후감대회", "#글짓기"]

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
                        apply_end=(now + timedelta(days=20)).strftime("%Y-%m-%d"),
                        event_start=(now + timedelta(days=25)).strftime("%Y-%m-%d"),
                        event_end=(now + timedelta(days=25)).strftime("%Y-%m-%d"),
                        url=full_url,
                        image_url="https://ilovecontest.com/img/logo.png",
                        description=f"{title} - 알럽콘 공식 공모전·백일장 세부 요강 및 온라인 접수 안내입니다."
                    )
                    items.append(item)

                    if len(items) >= 15:
                        break

            except Exception as e:
                logger.error(f"[{self.name}] 알럽콘 크롤링 에러 ({target_url}): {e}")

        logger.info(f"[{self.name}] 알럽콘 실시간 수집 완료: 총 {len(items)}건")
        return items
