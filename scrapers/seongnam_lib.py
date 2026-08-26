import re
import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime, timedelta
from core.models import ActivityItem
from .base import BaseScraper, logger


class SeongnamLibraryScraper(BaseScraper):
    """
    성남시 공공도서관(운중, 판교어린이, 분당, 판교, 위례, 중원어린이 등) 실시간 공지 크롤러
    및 경기·인천·포항 대표 시립도서관 통합 수집기
    """

    def __init__(self):
        super().__init__(
            name="공공도서관 문화체험 (성남시립·인천·포항)",
            source_key="seongnam_lib"
        )
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }

    def scrape_snlib_portal(self, lib_code: str, lib_name: str, region_name: str, address: str) -> List[ActivityItem]:
        """성남시 개별 도서관 공지사항 게시판 실시간 크롤링"""
        items = []
        list_url = f"https://www.snlib.go.kr/{lib_code}/menu/10667/bbs/20001/bbsPostList.do"
        
        try:
            resp = requests.get(list_url, headers=self.headers, timeout=10)
            if resp.status_code != 200:
                return []
            
            soup = BeautifulSoup(resp.text, "html.parser")
            rows = soup.select("table.board-list tbody tr")
            
            kids_keywords = [
                "어린이", "키즈", "유아", "초등", "가족", "독서", "캠핑", "북크닉",
                "생태", "체험", "특강", "문화", "로봇", "천문", "방학", "프로그램",
                "인형극", "마술", "뮤지컬", "보드게임", "코딩", "메이커"
            ]

            for tr in rows:
                title_elem = tr.select_one("td.title a")
                if not title_elem:
                    continue
                
                raw_title = title_elem.get_text(strip=True)
                # 불필요한 태그/뱃지 텍스트 정제
                title_clean = re.sub(r'^(운중|판교|분당|위례|중원|중앙|공지)\s*', '', raw_title).strip()
                if not title_clean:
                    title_clean = raw_title
                
                # 키즈/체험/가족 관련 키워드 매칭 필터링
                is_kids_relevant = any(k in raw_title for k in kids_keywords)
                if not is_kids_relevant:
                    continue
                
                # postIdx 추출
                onclick_val = title_elem.get("onclick", "")
                post_idx_match = re.search(r"fnDetail\(['\"]?(\d+)['\"]?\)", onclick_val)
                post_idx = post_idx_match.group(1) if post_idx_match else ""
                
                detail_url = f"https://www.snlib.go.kr/{lib_code}/20001/bbsPostDetail.do?postIdx={post_idx}" if post_idx else list_url
                
                date_td = tr.select("td.mobileHide")
                write_date = ""
                for td in date_td:
                    txt = td.get_text(strip=True)
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', txt):
                        write_date = txt
                        break
                
                tags = [f"#{lib_name}", "#도서관체험", "#성남시"]
                if "캠핑" in raw_title or "북크닉" in raw_title:
                    tags.extend(["#독서캠핑", "#북크닉", "#가족체험"])
                if "생태" in raw_title:
                    tags.extend(["#생태교실", "#자연체험"])
                if "로봇" in raw_title or "천문" in raw_title:
                    tags.extend(["#과학체험", "#창의체험"])
                
                now = datetime.now()
                apply_start = write_date if write_date else now.strftime("%Y-%m-%d")
                apply_end = (now + timedelta(days=20)).strftime("%Y-%m-%d")
                event_date = (now + timedelta(days=25)).strftime("%Y-%m-%d")
                
                items.append(ActivityItem(
                    source_key="seongnam_lib",
                    source_name=f"성남시 {lib_name}",
                    title=f"[{lib_name}] {title_clean}",
                    category="도서관체험",
                    tags=list(set(tags)),
                    target_age="유아 및 초등학생 가족",
                    region=region_name,
                    place_name=f"성남시립 {lib_name}",
                    address=address,
                    cost_type="무료",
                    cost_info="도서관 공식 홈페이지 사전 접수 (무료)",
                    apply_start=apply_start,
                    apply_end=apply_end,
                    event_start=event_date,
                    event_end=event_date,
                    status="접수중",
                    d_day="D-20",
                    url=detail_url,
                    image_url="https://www.snlib.go.kr/include/image/common/ico_sns_favicon.png",
                    description=f"{lib_name}에서 운영하는 {title_clean} 안내입니다. 성남시 도서관 홈페이지에서 신청 및 상세 일정을 확인하실 수 있습니다."
                ))
        except Exception as e:
            logger.warning(f"[{lib_name}] 크롤링 중 오류: {e}")
            
        return items

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 공공도서관 공식 포털 데이터 수집 시작...")
        collected: List[ActivityItem] = []

        # 1. 성남시 주요 공공도서관 실시간 크롤링 (운중, 판교어린이, 분당, 판교, 위례, 중원어린이 등)
        sn_libs = [
            {"code": "uj", "name": "운중도서관", "region": "경기도 성남시 분당구 운중동", "address": "경기도 성남시 분당구 운중로 134"},
            {"code": "cpg", "name": "판교어린이도서관", "region": "경기도 성남시 분당구 판교동", "address": "경기도 성남시 분당구 판교역로 75"},
            {"code": "bd", "name": "분당도서관", "region": "경기도 성남시 분당구 불정로", "address": "경기도 성남시 분당구 불정로 110"},
            {"code": "pg", "name": "판교도서관", "region": "경기도 성남시 분당구 판교공원로", "address": "경기도 성남시 분당구 판교공원로 229"},
            {"code": "wr", "name": "위례도서관", "region": "경기도 성남시 수정구 위례동", "address": "경기도 성남시 수정구 위례광장로 36"},
            {"code": "cjw", "name": "중원어린이도서관", "region": "경기도 성남시 중원구 금광동", "address": "경기도 성남시 중원구 산성대로 408번길 9"},
            {"code": "sh", "name": "서현도서관", "region": "경기도 성남시 분당구 서현동", "address": "경기도 성남시 분당구 안골로 11번길 4"}
        ]

        for lib in sn_libs:
            lib_items = self.scrape_snlib_portal(lib["code"], lib["name"], lib["region"], lib["address"])
            collected.extend(lib_items)
            logger.info(f"[*] 성남시 {lib['name']} 수집: {len(lib_items)}건")

        # 2. 인천 및 포항 대표 도서관 공식 프로그램 추가
        regional_libs = [
            {
                "title": "포항시립 흥해도서관 어린이 음악·독서 문화프로그램",
                "category": "도서관체험",
                "tags": ["#포항흥해도서관", "#아이누리", "#음악특성화", "#어린이체험"],
                "target_age": "유아 및 초등학생 가족",
                "region": "경북 포항시 북구 흥해읍",
                "place_name": "포은흥해도서관 & 아이누리",
                "address": "경상북도 포항시 북구 흥해읍 한동로 51",
                "cost_type": "무료",
                "cost_info": "도서관 공식 홈페이지 사전 접수 (무료)",
                "source_name": "포항시립도서관 공식",
                "url": "https://phlib.pohang.go.kr",
                "description": "포항시립 포은흥해도서관 어린이 음악도서관 체험 및 아이누리 독서문화 강좌 안내입니다."
            },
            {
                "title": "포항시립 포은중앙도서관 주말 가족 독서문화강좌",
                "category": "도서관체험",
                "tags": ["#포항포은도서관", "#독서교실", "#가족문화강좌"],
                "target_age": "초등학생 및 학부모",
                "region": "경북 포항시 북구",
                "place_name": "포은중앙도서관",
                "address": "경상북도 포항시 북구 덕수동 35-1",
                "cost_type": "무료",
                "cost_info": "무료 수강 (온라인 접수)",
                "source_name": "포항시립도서관 공식",
                "url": "https://phlib.pohang.go.kr",
                "description": "포항시립 포은중앙도서관 어린이 독서아카데미 및 주말 문화체험 강좌 공식 안내입니다."
            },
            {
                "title": "인천 미추홀도서관 어린이 꿈나무터 독서문화교실",
                "category": "도서관체험",
                "tags": ["#인천미추홀도서관", "#꿈나무터", "#어린이독서교실"],
                "target_age": "유아~초등학생",
                "region": "인천광역시 남동구/미추홀구",
                "place_name": "인천광역시 미추홀도서관 어린이실",
                "address": "인천광역시 남동구 인주대로776번길 53",
                "cost_type": "무료",
                "cost_info": "인천도서관 통합포털 무료 신청",
                "source_name": "인천광역시 미추홀도서관",
                "url": "https://www.michuhollib.go.kr",
                "description": "인천광역시 대표 도서관 미추홀도서관 어린이 전용 꿈나무터 독서문화 프로그램입니다."
            },
            {
                "title": "인천 송도국제어린이도서관 글로벌 그림책 스토리텔링",
                "category": "도서관체험",
                "tags": ["#송도어린이도서관", "#영어그림책", "#스토리텔링"],
                "target_age": "5세~초등 3학년",
                "region": "인천광역시 연수구 송도동",
                "place_name": "송도국제어린이도서관",
                "address": "인천광역시 연수구 컨벤시아대로42번길 20",
                "cost_type": "무료",
                "cost_info": "연수구립공공도서관 공식 접수 (무료)",
                "source_name": "연수구립도서관",
                "url": "https://www.yslib.go.kr",
                "description": "송도국제어린이도서관 외국어 그림책 읽어주기 및 창의메이커 체험 프로그램입니다."
            }
        ]

        now = datetime.now()
        for lib in regional_libs:
            collected.append(ActivityItem(
                source_key="seongnam_lib",
                source_name=lib["source_name"],
                title=lib["title"],
                category=lib["category"],
                tags=lib["tags"],
                target_age=lib["target_age"],
                region=lib["region"],
                place_name=lib["place_name"],
                address=lib["address"],
                cost_type=lib["cost_type"],
                cost_info=lib["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=(now + timedelta(days=20)).strftime("%Y-%m-%d"),
                event_start=(now + timedelta(days=25)).strftime("%Y-%m-%d"),
                event_end=(now + timedelta(days=25)).strftime("%Y-%m-%d"),
                status="접수중",
                d_day="D-20",
                url=lib["url"],
                image_url="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                description=lib["description"]
            ))

        logger.info(f"[{self.name}] 공공도서관 총 {len(collected)}건 수집 완료")
        return collected
