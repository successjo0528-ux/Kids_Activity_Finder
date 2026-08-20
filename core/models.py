import hashlib
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field, asdict


@dataclass
class ActivityItem:
    """체험, 행사, 대회 통합 데이터 모델 (순수 표준 dataclass 기반)"""
    source_key: str
    source_name: str
    title: str
    category: str = "기타체험"
    tags: List[str] = field(default_factory=list)
    target_age: str = "전연령"
    region: str = "성남시"
    place_name: str = ""
    address: str = ""
    cost_type: str = "무료"
    cost_info: str = ""
    apply_start: Optional[str] = ""
    apply_end: Optional[str] = ""
    event_start: Optional[str] = ""
    event_end: Optional[str] = ""
    status: str = "진행중"
    d_day: str = ""
    url: str = ""
    image_url: str = ""
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    id: str = ""

    def __post_init__(self):
        # 고유 ID가 없으면 제목과 출처, 장소를 기반으로 해시 생성
        if not self.id:
            raw = f"{self.source_key}_{self.title}_{self.place_name}_{self.event_start}"
            self.id = hashlib.md5(raw.encode("utf-8")).hexdigest()[:12]
        
        # D-Day 및 상태 자동 계산
        self._calculate_status_and_d_day()

    def _calculate_status_and_d_day(self):
        today = date.today()
        target_date = None

        # 마감일이 있으면 마감일 기준 계산
        if self.apply_end and len(self.apply_end) >= 10:
            try:
                target_date = datetime.strptime(self.apply_end[:10], "%Y-%m-%d").date()
                diff = (target_date - today).days
                if diff < 0:
                    self.status = "마감"
                    self.d_day = "마감"
                elif diff == 0:
                    self.status = "마감임박"
                    self.d_day = "오늘마감"
                elif diff <= 3:
                    self.status = "마감임박"
                    self.d_day = f"D-{diff}"
                else:
                    self.status = "접수중"
                    self.d_day = f"D-{diff}"
            except Exception:
                pass

        # 마감일이 없고 행사 시작일이 있는 경우
        if not target_date and self.event_start and len(self.event_start) >= 10:
            try:
                target_date = datetime.strptime(self.event_start[:10], "%Y-%m-%d").date()
                diff = (target_date - today).days
                if diff < 0:
                    self.status = "종료"
                    self.d_day = "종료"
                elif diff == 0:
                    self.status = "D-Day"
                    self.d_day = "D-Day"
                else:
                    self.status = "진행예정"
                    self.d_day = f"D-{diff}"
            except Exception:
                pass

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
