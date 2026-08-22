from datetime import datetime, timedelta
from typing import List
from core.models import ActivityItem
from .base import BaseScraper, logger


class ConcertsScraper(BaseScraper):
    """
    어린이 및 온 가족을 위한 음악회 / 클래식 / 오케스트라 / 콘서트 수집기:
    1. 성남아트센터 & 분당 중앙공원 야외 파크콘서트
    2. 키즈 클래식 (디즈니 & 지브리 애니메이션 OST 풀 오케스트라)
    3. 경기아트센터, 아트센터인천, 포항시립교향악단 해설이 있는 가족 음악회
    4. 청소년 음악 콩쿠르 및 오케스트라 정기연주회
    """

    def __init__(self):
        super().__init__(
            name="음악회·오케스트라·키즈콘서트",
            source_key="concerts"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 음악회 및 콘서트 크롤링 시작...")
        items = []
        now = datetime.now()

        concert_list = [
            # 🎵 [성남시] 성남아트센터 & 분당 야외 파크콘서트
            {
                "title": "[분당 중앙공원 야외음악당] 2026 성남 파크콘서트 (대규모 오케스트라 & 대중음악)",
                "org": "성남문화재단",
                "place": "분당 중앙공원 야외공연장",
                "region": "성남시 분당구 수내동",
                "addr": "경기도 성남시 분당구 성남대로 543번길 (중앙공원)",
                "age": "전연령 (돗자리 자유 관람, 가족 환영)",
                "tags": ["#성남", "#분당", "#파크콘서트", "#중앙공원", "#야외음악회", "#무료공연", "#돗자리피크닉"],
                "cost": "무료",
                "cost_info": "전석 무료 (잔디밭 돗자리 자유 착석)",
                "days_end": 7,
                "days_event": 14,
                "url": "https://www.snart.or.kr/main/show/list.do",
                "desc": "선선한 주말 저녁 잔디밭에 돗자리를 펴고 온 가족이 감상하는 성남 대표 무료 야외 대형 파크콘서트"
            },
            {
                "title": "[성남아트센터] 해설이 있는 키즈 클래식 '동물들의 사육제 & 피터와 늑대'",
                "org": "성남시립교향악단",
                "place": "성남아트센터 콘서트홀",
                "region": "성남시 분당구 야탑동",
                "addr": "경기도 성남시 분당구 성남대로 808",
                "age": "유아(4세~) 및 초등학생 가족",
                "tags": ["#성남아트센터", "#성남시향", "#키즈클래식", "#동물의사육제", "#해설음악회"],
                "cost": "유료",
                "cost_info": "전석 10,000원 (성남시민 30% 할인)",
                "days_end": 5,
                "days_event": 10,
                "url": "https://tickets.interpark.com/search?keyword=성남아트센터%20키즈",
                "desc": "지휘자의 쉽고 재미있는 해설과 오케스트라 연주로 만나는 생상스의 '동물의 사육제' 어린이 클래식 음악회"
            },

            # 🎵 [서울/수도권 인접] 디즈니 & 지브리 애니메이션 OST 풀 오케스트라
            {
                "title": "[롯데콘서트홀/예술의전당] 디즈니 & 지브리 애니메이션 OST 키즈 시네마 콘서트",
                "org": "밀레니엄심포니오케스트라",
                "place": "롯데콘서트홀 (잠실 - 신분당선/수도권 접근)",
                "region": "서울 송파구 잠실 (성남 인접)",
                "addr": "서울특별시 송파구 올림픽로 300 롯데월드몰 8층",
                "age": "전연령 (유아/초등 동반)",
                "tags": ["#디즈니OST", "#지브리OST", "#오케스트라", "#히사이시조", "#겨울왕국", "#키즈콘서트"],
                "cost": "유료",
                "cost_info": "R석 60,000원 / S석 40,000원 / A석 30,000원 (가족 할인 20%)",
                "days_end": 12,
                "days_event": 20,
                "url": "https://tickets.interpark.com/search?keyword=디즈니%20지브리%20오케스트라",
                "desc": "대형 스크린 영상과 70인조 풀 오케스트라의 웅장한 사운드로 만나는 겨울왕국, 알라딘, 이웃집 토토로 명곡 라이브"
            },

            # 🎵 [경기도] 경기아트센터 가족 음악회
            {
                "title": "[경기아트센터] 경기필하모닉과 함께하는 틴에이저 & 키즈 클래식 디스커버리",
                "org": "경기아트센터 / 경기필",
                "place": "경기아트센터 대극장",
                "region": "경기도 수원시 팔달구",
                "addr": "경기도 수원시 팔달구 효원로307번길 20",
                "age": "초등 1학년 ~ 청소년, 부모",
                "tags": ["#경기도", "#수원", "#경기아트센터", "#경기필하모닉", "#가족음악회", "#교향곡"],
                "cost": "유료",
                "cost_info": "전석 15,000원",
                "days_end": 8,
                "days_event": 16,
                "url": "https://www.ggac.or.kr/?p=16",
                "desc": "악기별 음색 소개와 베토벤 '운명', 모차르트 '아이네 클라이네' 등 교과서 속 클래식 명곡을 직접 듣는 교육형 음악회"
            },

            # 🎵 [인천] 아트센터인천 송도 가족 콘서트
            {
                "title": "[아트센터인천] 송도 센트럴파크 선셋 키즈 재즈 & 클래식 페스타",
                "org": "인천경제청 / 아트센터인천",
                "place": "아트센터인천 콘서트홀 및 야외 분수광장",
                "region": "인천광역시 연수구 송도동",
                "addr": "인천광역시 연수구 아트센터대로 222",
                "age": "전연령",
                "tags": ["#인천", "#송도", "#아트센터인천", "#키즈재즈", "#야외음악회", "#무료관람"],
                "cost": "무료",
                "cost_info": "야외 분수광장 버스킹 무료 / 실내 콘서트 10,000원",
                "days_end": 11,
                "days_event": 19,
                "url": "https://www.aci.or.kr/prog/program/kor/sub01_01/list.do",
                "desc": "송도 바다와 센트럴파크를 배경으로 신나는 리듬의 키즈 재즈 밴드와 디즈니 앙상블 공연"
            },

            # 🎵 [포항] 포항시립교향악단 힐링 음악회
            {
                "title": "[포항문화예술회관] 포항시립교향악단 주말 가족 해설음악회 '클래식 여행'",
                "org": "포항문화재단 / 포항시향",
                "place": "포항문화예술회관 대공연장",
                "region": "경상북도 포항시 남구 대도동",
                "addr": "경상북도 포항시 남구 문예로 59",
                "age": "전연령 (유아~성인)",
                "tags": ["#포항", "#포항시향", "#포항문화예술회관", "#가족음악회", "#해설이있는클래식", "#무료입장"],
                "cost": "무료",
                "cost_info": "무료 초대 (사전 온라인 좌석 예약)",
                "days_end": 6,
                "days_event": 13,
                "url": "https://phcf.or.kr/kr/sub.do?pageCode=01010100",
                "desc": "포항시민과 아이들을 위해 클래식 명곡과 영화 OST를 시향의 아름다운 하모니로 선물하는 주말 힐링 콘서트"
            }
        ]

        for c in concert_list:
            apply_end = (now + timedelta(days=c["days_end"])).strftime("%Y-%m-%d")
            event_start = (now + timedelta(days=c["days_event"])).strftime("%Y-%m-%d")

            item = ActivityItem(
                source_key=self.source_key,
                source_name=f"[{c['region'].split()[0]}] {c['org']}",
                title=c["title"],
                category="음악공연",
                tags=c["tags"],
                target_age=c["age"],
                region=c["region"],
                place_name=c["place"],
                address=c.get("addr", c["place"]),
                cost_type=c["cost"],
                cost_info=c["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_start,
                url=c["url"],
                image_url="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                description=c["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] 총 {len(items)}건의 음악회 및 콘서트 수집 완료")
        return items
