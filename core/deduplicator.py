import re
from typing import List, Tuple
from difflib import SequenceMatcher
from core.models import ActivityItem
import logging

logger = logging.getLogger("ActivityDeduplicator")


class ActivityDeduplicator:
    """
    동일 행사 및 유사 카드 지능형 중복 제거 전담 에이전트 모듈:
    - 서로 다른 출처에서 중복 수집된 동일/유사 행사를 제목 정규화 및 유사도 매칭으로 감지
    - 제목이 완전히 다른 별개의 교육/체험 프로그램은 동일 기관 URL이더라도 각각 보존
    - 더 상세한 정보(이미지, 설명, 공식 URL)를 가진 대표 카드 1개만 우선 보존하고 중복 제거
    """

    @staticmethod
    def normalize_title(title: str) -> str:
        """제목에서 특수문자, 괄호, 주최기관 수식어 등을 정규화하여 순수 핵심어 추출"""
        if not title:
            return ""
        # 1. 괄호 내용 및 태그성 수식어 제거 [국립...], (2026...), 【...】
        t = re.sub(r'\[.*?\]|\(.*?\)|【.*?】|<.*?>', ' ', title)
        # 2. 불필요한 연도, 공통 수식어 정리
        t = re.sub(r'2026|2027|주말|어린이|키즈|체험|프로그램|모집|안내|행사|공식', ' ', t)
        # 3. 특수문자 제거 및 공백 통일
        t = re.sub(r'[^\w가-힣0-9]', ' ', t)
        t = re.sub(r'\s+', ' ', t).strip().lower()
        return t

    @classmethod
    def calculate_similarity(cls, title1: str, title2: str) -> float:
        """두 제목 간의 시퀀스 유사도 (0.0 ~ 1.0) 계산"""
        norm1 = cls.normalize_title(title1)
        norm2 = cls.normalize_title(title2)
        if not norm1 or not norm2:
            return 0.0
        if norm1 == norm2:
            return 1.0
        # 길이가 4글자 이상이고 부분 포함 관계인 경우 높은 유사도 부여
        if len(norm1) >= 4 and len(norm2) >= 4:
            if norm1 in norm2 or norm2 in norm1:
                return 0.90
        return SequenceMatcher(None, norm1, norm2).ratio()

    @classmethod
    def deduplicate(cls, items: List[ActivityItem], threshold: float = 0.85) -> Tuple[List[ActivityItem], int]:
        """
        수집된 전체 아이템 리스트에서 동일/유사 중복 카드를 찾아 1개만 남기고 정제
        :param items: 수집된 ActivityItem 리스트
        :param threshold: 유사도 임계치 (기본 0.85)
        :return: (중복 제거된 고유 아이템 리스트, 제거된 중복 건수)
        """
        if not items:
            return [], 0

        unique_items: List[ActivityItem] = []
        removed_count = 0

        for item in items:
            is_duplicate = False
            for idx, existing in enumerate(unique_items):
                # 1. URL과 제목이 둘 다 완벽히 동일한 경우 -> 완전 중복
                if item.url and existing.url and item.url == existing.url and item.title == existing.title:
                    is_duplicate = True
                    if len(item.description or "") > len(existing.description or ""):
                        unique_items[idx] = item
                    break

                # 2. 제목 유사도 분석 (동일/유사 행사 중복 판정)
                sim = cls.calculate_similarity(item.title, existing.title)
                
                # 유사도가 85% 이상으로 매우 높을 때
                if sim >= threshold:
                    # 동일 날짜 또는 동일 전시장/장소인 경우 확실한 중복으로 판정
                    same_event_date = bool(item.event_start and existing.event_start and item.event_start == existing.event_start)
                    same_place = bool(item.place_name and existing.place_name and (item.place_name in existing.place_name or existing.place_name in item.place_name))

                    if sim >= 0.92 or same_event_date or same_place:
                        is_duplicate = True
                        removed_count += 1
                        logger.info(
                            f"[중복 제거 에이전트] 동일/유사 행사 중복 감지 (유사도 {sim:.2f}):\n"
                            f"  - 보존: {existing.title} ({existing.source_name})\n"
                            f"  - 제거: {item.title} ({item.source_name})"
                        )
                        # 더 우수한 데이터(포스터 이미지 유무, 설명 길이 등)를 가진 항목을 보존
                        existing_has_img = existing.image_url and "favicon" not in existing.image_url
                        item_has_img = item.image_url and "favicon" not in item.image_url
                        if item_has_img and not existing_has_img:
                            unique_items[idx] = item
                        break

            if not is_duplicate:
                unique_items.append(item)

        logger.info(f"[중복 제거 에이전트] 정제 완료: 총 {len(items)}건 중 {removed_count}건 중복 제거 -> 최종 {len(unique_items)}건 확정")
        return unique_items, removed_count
