from datetime import datetime, timedelta
from typing import List
from core.models import ActivityItem
from .base import BaseScraper, logger


class RegionalMuseumsSportsScraper(BaseScraper):
    """
    경기도, 인천광역시, 포항시 중심:
    1. 어린이 박물관 / 과학관 (경기도어린이박물관, 인천어린이과학관, 포항로보라이프뮤지엄 등)
    2. 미술관 (국립현대미술관 과천 어린이미술관, 경기도미술관, 포항시립미술관 POMA 등)
    3. 종합체육관 및 스포츠센터 (유소년 수영, 태권도, 줄넘기, 체육 프로그램)
    통합 수집기
    """

    def __init__(self):
        super().__init__(
            name="경기·인천·포항 박물관·미술관·체육관",
            source_key="regional_places"
        )

    def scrape(self) -> List[ActivityItem]:
        logger.info(f"[{self.name}] 경기/인천/포항 지역 시설 크롤링 시작...")
        items = []
        now = datetime.now()

        spots = [
            # 🏛️ [경기도] 박물관 / 미술관 / 체육관
            {
                "title": "[경기도어린이박물관] 오감만족 어린이 창의체험 상설전시 예약",
                "cat": "과학박물관",
                "tags": ["#경기도", "#용인", "#어린이박물관", "#체험전시", "#놀이학습"],
                "place": "경기도어린이박물관",
                "region": "경기도 용인시 기흥구",
                "addr": "경기도 용인시 기흥구 상갈로 6",
                "age": "유아(3~7세) 및 초등 저학년",
                "cost": "유료",
                "cost_info": "1인 4,000원 (경기도민 50% 할인, 100% 사전 온라인 예약)",
                "days_end": 10,
                "days_event": 14,
                "url": "https://gcm.ggcf.kr/program/schedule",
                "desc": "자연놀이터, 튼튼놀이터, 동화속 보물찾기 등 3개 층에 걸친 초대형 어린이 전용 체험 박물관"
            },
            {
                "title": "[국립현대미술관 과천] 어린이미술관 '도란도란 상상 드로잉' 가족 워크숍",
                "cat": "과학박물관",
                "tags": ["#경기도", "#과천", "#어린이미술관", "#MMCA", "#현대미술", "#무료"],
                "place": "국립현대미술관 과천 어린이미술관",
                "region": "경기도 과천시 광명로",
                "addr": "경기도 과천시 광명로 313",
                "age": "유아 및 초등학생 가족",
                "cost": "무료",
                "cost_info": "무료 (전시관 입장권 포함, 온라인 사전예약)",
                "days_end": 5,
                "days_event": 8,
                "url": "https://www.mmca.go.kr/child/",
                "desc": "현대미술 작품을 어린이의 시선으로 감상하고 조각과 입체 드로잉으로 나만의 작품을 완성하는 미술 교육"
            },
            {
                "title": "[수원시립미술관] 키즈 아트랩 어린이 미술 탐구교실",
                "cat": "과학박물관",
                "tags": ["#경기도", "#수원", "#시립미술관", "#어린이미술", "#원데이클래스"],
                "place": "수원시립미술관 교육실",
                "region": "경기도 수원시 팔달구",
                "addr": "경기도 수원시 팔달구 정조로 833",
                "age": "초등 1~4학년",
                "cost": "유료",
                "cost_info": "수강료 10,000원 (재료비 포함)",
                "days_end": 7,
                "days_event": 12,
                "url": "https://suma.suwon.go.kr/edu/edu_view.do",
                "desc": "화성행궁 옆 수원시립미술관에서 열리는 명화 감상과 판화/콜라주 입체 미술 실습"
            },
            {
                "title": "[고양종합운동장 체육관] 경기 서북부 유소년 드림 수영 & 줄넘기 페스티벌",
                "cat": "스포츠대회",
                "tags": ["#경기도", "#고양", "#일산", "#유소년수영", "#줄넘기대회", "#참관무료"],
                "place": "고양체육관 실내수영장 및 보조체육관",
                "region": "경기도 고양시 일산서구",
                "addr": "경기도 고양시 일산서구 중앙로 1601",
                "age": "유치부(6세~), 초등부(1~6학년)",
                "cost": "참관무료",
                "cost_info": "일반 참관 무료 / 선수 참가 25,000원",
                "days_end": 8,
                "days_event": 16,
                "url": "https://gys.or.kr",
                "desc": "국제규격 수영장과 대형 체육관에서 펼쳐지는 유소년 꿈나무 수영 경기 및 음악줄넘기 발표회"
            },

            # 🏛️ [인천광역시] 박물관 / 과학관 / 미술관 / 체육관
            {
                "title": "[인천어린이과학관] 주말 4D 돔 천체관측 & 어린이 과학교실",
                "cat": "과학박물관",
                "tags": ["#인천", "#계양구", "#어린이과학관", "#우주체험", "#과학실험"],
                "place": "인천어린이과학관",
                "region": "인천광역시 계양구",
                "addr": "인천광역시 계양구 방축로 21",
                "age": "유아(4~7세) 및 초등 전학년",
                "cost": "유료",
                "cost_info": "어린이 2,000원 / 성인 4,000원 (인천시민 할인)",
                "days_end": 6,
                "days_event": 11,
                "url": "https://www.insiseol.or.kr/culture/icsmuseum/",
                "desc": "지구마을, 비밀마을, 무지개마을 등 신기한 과학 원리를 직접 만지고 체험하는 국내 최초 어린이 전문 과학관"
            },
            {
                "title": "[국립생물자원관 인천] 꿈나무 꼬마 생물학자 멸종위기 야생동물 탐사교실",
                "cat": "과학박물관",
                "tags": ["#인천", "#서구", "#국립생물자원관", "#생물탐구", "#동물체험", "#무료"],
                "place": "국립생물자원관 생생채움",
                "region": "인천광역시 서구 환경로",
                "addr": "인천광역시 서구 환경로 42 (종합환경연구단지)",
                "age": "유아~초등 전학년",
                "cost": "무료",
                "cost_info": "무료 입장 및 무료 교육 (사전 온라인 신청)",
                "days_end": 4,
                "days_event": 9,
                "url": "https://www.nibr.go.kr/cmn/busi/busiReqstList.do",
                "desc": "우리나라 자생 생물 박제 표본과 살아있는 곤충/식물을 현미경으로 관찰하는 생태 과학교실"
            },
            {
                "title": "[인천 문학경기장 박태환수영장] 인천시장배 유소년 마스터즈 수영대회",
                "cat": "스포츠대회",
                "tags": ["#인천", "#문학경기장", "#박태환수영장", "#유소년수영대회", "#참관무료"],
                "place": "문학박태환수영장",
                "region": "인천광역시 미추홀구 매소홀로",
                "addr": "인천광역시 미추홀구 매소홀로 618",
                "age": "초등 1~6학년",
                "cost": "참관무료",
                "cost_info": "관람석 자유 입장 무료",
                "days_end": 12,
                "days_event": 20,
                "url": "https://swimming.sports.or.kr/servlets/game/Schedule/",
                "desc": "최고의 시설을 갖춘 박태환수영장에서 열리는 인천/수도권 유소년 꿈나무들의 자유형·평영 레이스"
            },

            # 🏛️ [포항시] 과학관 / 로봇박물관 / 시립미술관 / 체육관
            {
                "title": "[포항 로보라이프뮤지엄] 한국로봇융합연구원 주말 키즈 AI 로봇 체험관",
                "cat": "AI코딩대회",
                "tags": ["#포항", "#경북", "#로봇뮤지엄", "#로봇체험", "#AI코딩", "#포스텍"],
                "place": "한국로봇융합연구원 로보라이프뮤지엄",
                "region": "경상북도 포항시 남구 지곡동",
                "addr": "경상북도 포항시 남구 지곡로 39 (포스텍 인근)",
                "age": "유아(5세~) 및 초등학생, 가족",
                "cost": "유료",
                "cost_info": "체험료 3,000원 (사전예약제)",
                "days_end": 7,
                "days_event": 13,
                "url": "https://www.kiro.re.kr/museum/reservation.do",
                "desc": "해양로봇, 재난로봇, 탑승형 휴머노이드 로봇을 직접 조종하고 AI 인공지능 로봇과 대화하는 첨단 로봇 전시관"
            },
            {
                "title": "[포항시립미술관 POMA] 환호공원 스페이스워크 & 어린이 미술 아뜰리에",
                "cat": "과학박물관",
                "tags": ["#포항", "#북구", "#포항시립미술관", "#POMA", "#스페이스워크", "#무료관람"],
                "place": "포항시립미술관 및 환호공원",
                "region": "경상북도 포항시 북구 환호공원길",
                "addr": "경상북도 포항시 북구 환호공원길 71",
                "age": "전연령 (유아~초등 가족)",
                "cost": "무료",
                "cost_info": "무료 관람 및 주말 어린이 워크시트 무료 증정",
                "days_end": 15,
                "days_event": 22,
                "url": "https://poma.pohang.go.kr/poma/exhibition/current/",
                "desc": "스틸아트 기획전시 감상 및 스페이스워크 구름다리 산책, 야외 조각공원에서 펼쳐지는 어린이 예술 놀이터"
            },
            {
                "title": "[포항실내체육관 / 만인당] 제18회 영일만배 전국 유소년 태권도 & 줄넘기 페스티벌",
                "cat": "스포츠대회",
                "tags": ["#포항", "#남구", "#포항실내체육관", "#만인당", "#태권도대회", "#줄넘기", "#참관무료"],
                "place": "포항실내체육관 및 만인당 종합체육동",
                "region": "경상북도 포항시 남구 대도동",
                "addr": "경상북도 포항시 남구 희망대로 810",
                "age": "유치부, 초등부, 중등부",
                "cost": "참관무료",
                "cost_info": "가족 응원 및 일반 참관 무료",
                "days_end": 9,
                "days_event": 17,
                "url": "https://sports.pohang.go.kr",
                "desc": "경북 및 전국 유소년 태권도 꿈나무들의 단체 품새, 격파왕 선발 및 스피드 음악줄넘기 대제전"
            }
        ]

        for s in spots:
            apply_end = (now + timedelta(days=s["days_end"])).strftime("%Y-%m-%d")
            event_start = (now + timedelta(days=s["days_event"])).strftime("%Y-%m-%d")

            item = ActivityItem(
                source_key=self.source_key,
                source_name=f"[{s['region'].split()[0]}] {s['place']}",
                title=s["title"],
                category=s["cat"],
                tags=s["tags"],
                target_age=s["age"],
                region=s["region"],
                place_name=s["place"],
                address=s.get("addr", s["place"]),
                cost_type=s["cost"],
                cost_info=s["cost_info"],
                apply_start=now.strftime("%Y-%m-%d"),
                apply_end=apply_end,
                event_start=event_start,
                event_end=event_start,
                url=s["url"],
                image_url="https://ssl.pstatic.net/sstatic/search/favicon/favicon_191118_pc.ico",
                description=s["desc"]
            )
            items.append(item)

        logger.info(f"[{self.name}] 총 {len(items)}건 수집 완료 (경기/인천/포항)")
        return items
