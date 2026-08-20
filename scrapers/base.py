import logging
from abc import ABC, abstractmethod
from typing import List
import requests
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
        self.timeout = 15

    @abstractmethod
    def scrape(self) -> List[ActivityItem]:
        """웹사이트 또는 API에서 데이터를 수집하여 ActivityItem 목록으로 반환"""
        pass

    def fetch_url(self, url: str, params: dict = None) -> str:
        """안전한 HTTP GET 요청 헬퍼"""
        try:
            res = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            res.encoding = res.apparent_encoding or "utf-8"
            if res.status_code == 200:
                return res.text
            else:
                logger.warning(f"[{self.name}] 요청 실패 (상태코드: {res.status_code}): {url}")
                return ""
        except Exception as e:
            logger.error(f"[{self.name}] 연결 오류: {e}")
            return ""

    def fetch_json(self, url: str, params: dict = None, json_data: dict = None, method: str = "GET") -> dict:
        """안전한 JSON API 요청 헬퍼"""
        try:
            if method.upper() == "POST":
                res = requests.post(url, headers=self.headers, json=json_data, params=params, timeout=self.timeout)
            else:
                res = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            
            if res.status_code == 200:
                return res.json()
            else:
                logger.warning(f"[{self.name}] API 요청 실패 ({res.status_code}): {url}")
                return {}
        except Exception as e:
            logger.error(f"[{self.name}] JSON 파싱/연결 오류: {e}")
            return {}
