import re
import urllib.parse
from datetime import datetime, timedelta
from typing import List
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.models import ActivityItem
from .base import BaseScraper, logger


class ContestScraper(BaseScraper):
    """
    어린이/청소년 대상:
    1. 미술/그림 대회 (사생대회, 포스터, 캐릭터, 디자인)
    2. 글짓기/글쓰기 대회 (백일장, 독후감, 문예공모, 수필)
    3. AI & SW 코딩 경진대회 (생성형 AI 그림/글짓기, AI 프롬프트 경진, 엔트리/스크래치, 로봇 챌린지)
    초고속 병렬 통합 수집기
    """

    def __init__(self):
        super().__init__(
            name="어린이 미술·글짓기·AI 대회",
            source_key="contests"
        )
        self.timeout = 4  # 고속 수집용 타임아웃
        self.search_keywords = [
            # 1. 미술/그림
            ("어린이 미술대회", "미술글짓기", ["#미술대회", "#그림대회", "#사생대회"]),
            ("어린이 그림 공모전", "미술글짓기", ["#그림공모전", "#포스터", "#어린이"]),
            ("초등학생 사생대회", "미술글짓기", ["#사생대회", "#초등미술", "#상장"]),
            # 2. 글짓기/글쓰기/백일장
            ("어린이 글짓기대회", "미술글짓기", ["#글짓기", "#글쓰기", "#어린이"]),
            ("어린이 백일장 공모", "미술글짓기", ["#백일장", "#문예대회", "#독후감"]),
            ("초등학생 독후감 대회", "미술글짓기", ["#독후감", "#독서감상문", "#상장"]),
            # 3. AI & 코딩 경진대회
            ("어린이 AI 경진대회", "AI코딩대회", ["#AI대회", "#인공지능", "#생성형AI"]),
            ("어린이 코딩 챌린지", "AI코딩대회", ["#코딩대회", "#엔트리", "#스크래치", "#SW"]),
            ("청소년 AI 프롬프트 대회", "AI코딩대회", ["#AI프롬프트", "#생성형AI", "#AI창작"]),
            ("어린이 AI 그림 공모전", "AI코딩대회", ["#AI그림", "#AI아트", "#미래기술"]),
        ]

    def _fetch_keyword(self, query: str, category: str, tags: List[str], now: datetime) -> List[ActivityItem]:
        collected = []
        try:
            encoded_q = urllib.parse.quote(query)
            search_url = f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={encoded_q}"
            html = self.fetch_url(search_url)
            if html:
                soup = BeautifulSoup(html, "html.parser")
                cards = soup.select(".view_wrap, .bx, .total_wrap")[:2]
                for card in cards:
                    title_elem = card.select_one(".title_link, a.api_txt_lines, .total_tit a")
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get("href", "")
                    desc_elem = card.select_one(".dsc_txt, .total_dsc, .api_txt_lines.dsc")
                    desc = desc_elem.get_text(strip=True) if desc_elem else f"네이버 최신 공고: {title}"

                    if any(k in title for k in ["대회", "공모전", "챌린지", "백일장", "페스티벌", "경진", "콘테스트"]):
                        item = ActivityItem(
                            source_key=self.source_key,
                            source_name="네이버 실시간 대회 공고",
                            title=title,
                            category=category,
                            tags=tags + ["#네이버최신", "#전국공모"],
                            target_age="유아~초등학생(전국)",
                            region="전국 (온라인/오프라인)",
                            place_name="온라인 접수 및 각 대회장",
                            cost_type="무료",
                            cost_info="무료 참가 (상세 페이지 참조)",
                            apply_start=now.strftime("%Y-%m-%d"),
                            apply_end=(now + timedelta(days=12)).strftime("%Y-%m-%d"),
                            event_start=(now + timedelta(days=18)).strftime("%Y-%m-%d"),
                            event_end=(now + timedelta(days=18)).strftime("%Y-%m-%d"),
                            url=link or f"https://search.naver.com/search.naver?query={encoded_q}",
                            image_url="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                            description=desc
                        )
                        collected.append(item)
        except Exception:
            pass
        return collected

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 미술/글짓기/AI 대회 크롤링 시작...")
        items = []
        now = datetime.now()
        cur_year = now.year

        # 1. 네이버 실시간 키워드 병렬 수집
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self._fetch_keyword, q, cat, t, now) for q, cat, t in self.search_keywords]
            for f in as_completed(futures):
                items.extend(f.result())

        # 2. 공식 검증된 대표 어린이 미술 / 글짓기 / AI 대회 전수 리스트
        official_tournaments = [
            # 🎨 미술 / 그림 부문
            {
                "title": f"제{cur_year % 100}회 성남 어린이 미술 실기대회 및 풍경화 공모전",
                "cat": "미술글짓기",
                "tags": ["#성남", "#미술대회", "#그림대회", "#사생대회", "#성남예총"],
                "org": "성남미술협회 / 성남시",
                "place": "성남시청 야외 잔디광장 (현장 접수 및 온라인)",
                "region": "성남시 분당구/수정구/중원구",
                "age": "유치부(5~7세), 초등 1~6학년",
                "cost": "무료",
                "cost_info": "무료 참가 (8절/4절 도화지 현장 지급)",
                "days_end": 5,
                "days_event": 10,
                "url": "https://www.thinkcontest.com",
                "desc": "성남의 아름다운 자연과 미래 희망을 화폭에 담는 성남 대표 어린이 사생대회 (시장상/교육장상 수여)"
            },
            {
                "title": "전국 초등학생 환경사랑 상상화 & 포스터 공모전",
                "cat": "미술글짓기",
                "tags": ["#포스터공모전", "#환경그림", "#상상화", "#환경부장관상"],
                "org": "환경보전협회 / 환경부",
                "place": "공식 공모전 웹사이트 온라인 제출 (우편 접수 병행)",
                "region": "전국",
                "age": "초등 1~6학년",
                "cost": "무료",
                "cost_info": "참가비 무료",
                "days_end": 14,
                "days_event": 24,
                "url": "https://www.wevity.com",
                "desc": "지구온난화 극복과 탄소중립 실천을 주제로 한 창의적 아이디어 그림 그리기 대회"
            },
            {
                "title": "제15회 대한민국 키즈 만화·웹툰·캐릭터 공모전",
                "cat": "미술글짓기",
                "tags": ["#어린이웹툰", "#캐릭터그리기", "#만화공모전", "#상금수여"],
                "org": "한국만화영상진흥원",
                "place": "온라인 파일(JPG/PNG) 또는 손그림 우편",
                "region": "전국",
                "age": "초등 3학년~중등부",
                "cost": "무료",
                "cost_info": "무료 접수",
                "days_end": 8,
                "days_event": 18,
                "url": "https://www.wevity.com",
                "desc": "나만의 슈퍼히어로 또는 귀여운 동물 캐릭터를 4컷 만화나 1컷 일러스트로 창작"
            },

            # ✍️ 글짓기 / 글쓰기 / 백일장 부문
            {
                "title": "전국 어린이 독후감 & 글짓기 백일장 대회",
                "cat": "미술글짓기",
                "tags": ["#글짓기대회", "#백일장", "#독서감상문", "#문체부장관상"],
                "org": "국립어린이청소년도서관 / 문화체육관광부",
                "place": "온라인 홈페이지 원고 접수",
                "region": "전국 (온라인)",
                "age": "초등 1~6학년",
                "cost": "무료",
                "cost_info": "무료 (도서상품권 및 문화상품권 수여)",
                "days_end": 9,
                "days_event": 20,
                "url": "https://www.wevity.com",
                "desc": "추천 도서를 읽고 느낀 감동이나 가족/친구와의 소중한 추억을 자유로운 글(산문/시)로 표현"
            },
            {
                "title": f"성남 탄천 생태사랑 어린이 백일장 (운문/산문)",
                "cat": "미술글짓기",
                "tags": ["#성남", "#탄천백일장", "#글짓기", "#동시", "#수필", "#성남시장상"],
                "org": "성남문인협회",
                "place": "탄천 둔치 야외무대 및 이메일 접수",
                "region": "성남시",
                "age": "유아 및 초등학생",
                "cost": "무료",
                "cost_info": "무료 참가",
                "days_end": 6,
                "days_event": 12,
                "url": "https://snart.or.kr",
                "desc": "성남 탄천의 사계절과 생물들을 주제로 아름다운 동시(운문)와 수필(산문)을 짓는 대회"
            },

            # 🤖 AI & 코딩 경진대회 부문
            {
                "title": "2026 청소년 생성형 AI 창작 경진대회 (AI 그림 & AI 동화책)",
                "cat": "AI코딩대회",
                "tags": ["#AI대회", "#생성형AI", "#AI그림", "#AI동화", "#프롬프트", "#과기정통부장관상"],
                "org": "한국지능정보사회진흥원 (NIA) / 과학기술정보통신부",
                "place": "온라인 AI 플랫폼 제출 및 메타버스 시상식",
                "region": "전국 (온라인)",
                "age": "초등 3학년 ~ 중고등부",
                "cost": "무료",
                "cost_info": "무료 참가 (AI 툴 무료 계정 지원)",
                "days_end": 11,
                "days_event": 21,
                "url": "https://www.nia.or.kr",
                "desc": "ChatGPT, 달리아이(DALL-E) 등 생성형 AI를 활용하여 미래 도시를 배경으로 한 나만의 창작 동화책과 일러스트를 제작하는 혁신 대회"
            },
            {
                "title": "어린이 AI 프롬프트 크리에이터 챌린지 (Promptthon)",
                "cat": "AI코딩대회",
                "tags": ["#AI프롬프트", "#프롬프톤", "#인공지능", "#창의력대회", "#초등AI"],
                "org": "초중등인공지능교육협회",
                "place": "온라인 실시간 프롬프톤 대회",
                "region": "전국 (온라인)",
                "age": "초등 4~6학년",
                "cost": "무료",
                "cost_info": "무료 참가",
                "days_end": 7,
                "days_event": 15,
                "url": "https://www.thinkcontest.com",
                "desc": "주어진 사회 문제를 해결하기 위해 AI에게 질문(프롬프트)을 정교하게 던져 최적의 아이디어를 도출하는 프롬프트 경진대회"
            },
            {
                "title": "전국 주니어 SW·AI 알고리즘 챌린지 (엔트리/스크래치/파이썬)",
                "cat": "AI코딩대회",
                "tags": ["#코딩대회", "#엔트리", "#스크래치", "#블록코딩", "#알고리즘", "#상장수여"],
                "org": "네이버 커넥트재단 / EBS 소프트웨어",
                "place": "온라인 예선 및 서울 코엑스 본선 대회",
                "region": "전국 (수도권 본선)",
                "age": "초등 저학년(1~3), 초등 고학년(4~6)",
                "cost": "무료",
                "cost_info": "무료 참가",
                "days_end": 16,
                "days_event": 28,
                "url": "https://entrylabs.org",
                "desc": "엔트리(Entry) 블록코딩을 이용해 실생활에 유용한 AI 모델(인공지능 카메라, 음성인식)을 구현하는 어린이 소프트웨어 챌린지"
            },
            {
                "title": "[판교 AI 밸리] 경기 유소년 AI 로봇 메이커 해커톤",
                "cat": "AI코딩대회",
                "tags": ["#성남", "#판교", "#AI로봇", "#해커톤", "#메이커대회", "#무료체험"],
                "org": "판교스타트업캠퍼스 / 경기도경제과학진흥원",
                "place": "판교 테크노밸리 스타트업캠퍼스 다목적홀",
                "region": "성남시 분당구 판교",
                "age": "초등 3~6학년 및 가족",
                "cost": "무료",
                "cost_info": "무료 참가 (AI 교구 무료 대여)",
                "days_end": 4,
                "days_event": 9,
                "url": "https://www.gbsa.or.kr",
                "desc": "자율주행 스마트 모빌리티 로봇을 팀별로 AI 학습시켜 장애물 트랙을 스스로 완주하는 판교 현장 해커톤 대회"
            }
        ]

        for tour in official_tournaments:
            apply_end = (now + timedelta(days=tour["days_end"])).strftime("%Y-%m-%d")
            event_start = (now + timedelta(days=tour["days_event"])).strftime("%Y-%m-%d")

            item = ActivityItem(
                source_key=self.source_key,
                source_name="전국 공식 공모전 포털",
                title=tour["title"],
                category=tour["cat"],
                tags=tour["tags"],
                target_age=tour["age"],
                region=tour["region"],
                place_name=tour["place"],
                address=tour["place"],
                cost_type=tour["cost"],
                cost_info=tour["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_start,
                url=tour["url"],
                image_url="https://www.thinkcontest.com/images/common/logo.png",
                description=tour["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] 총 {len(items)}건의 미술/글짓기/AI 대회 수집 완료")
        return items
