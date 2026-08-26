# 🎈 Kids Activity Finder - 상세 기능 기획 및 기술 사양서 (SPECIFICATION)

> **프로젝트명:** Kids Activity Finder (어린이·온가족 문화·체험·스포츠·AI 탐색기)  
> **최종 개정일:** 2026-08-26  
> **버전:** v2.8.0 (마감 데이터 자동 제외, 본문 실시간 포스터 이미지 뷰어, 10개 출처 실시간 정밀 파싱 및 GitHub Actions 자동 교차 검증 CI 탑재)

---

## 1. 프로젝트 개요 및 목적
* **핵심 목적:** 성남시 및 인접 수도권(경기/인천/서울)과 포항 지역의 **어린이 문화체험, 과학관/박물관/미술관, 야외 파크콘서트/오케스트라, 유소년 및 성인 스포츠대회(태권도 격파/수영 등), AI·코딩·미술·글짓기 경진대회**를 자동 수집하여 PC와 스마트폰(LTE)에서 원클릭으로 탐색.
* **접속 환경:**
  - 💻 **PC:** `Tool_Dashboard` ➡️ [Kids Activity Finder] 원클릭 실행 (Edge 단독 데스크톱 앱 모드)
  - 📱 **모바일:** `https://successjo0528-ux.github.io/Kids_Activity_Finder/` (LTE/Wi-Fi 24시간 언제 어디서나 접속)
  - 🔗 **GitHub 저장소:** `https://github.com/successjo0528-ux/Kids_Activity_Finder`

---

## 2. 10대 수집 채널 및 데이터 소스 정의

1. **📚 성남시 공공도서관 실시간 크롤러 (`scrapers/seongnam_lib.py`)**
   - 운중, 판교어린이, 분당, 판교, 위례, 중원어린이, 서현 등 성남 7대 공공도서관 공지 실시간 크롤링.
   - **상세 본문 정밀 파싱**: 접수일시(`apply_start` ~ `apply_end`), 운영일시(`event_start`), 대상, 장소 및 접수 링크 자동 추출.
   - **본문 포스터 이미지 실시간 추출**: 공지 상세 본문의 포스터/안내문 그림 절대 URL 추출 및 연동.
2. **🤖🎨 어린이 미술·글짓기·AI 대회 (`scrapers/contests.py`)**
   - 알럽콘(ilovecontest.com) 전국 공모전·백일장·경진대회 실시간 크롤러.
   - 웹사이트 실제 D-Day(`D-16`, `D-20`, `D-35`, `D-65` 등)를 파싱하여 실시간 마감일자 정확 매핑.
3. **🏛️ 지자체 시청 & 청소년재단 (`scrapers/seongnam_city.py`)**
   - 성남시 판교환경생태학습원 생태체험, 판교청소년수련관 메이커, 포항 흥해문화의집 등 지자체 공식 프로그램.
4. **🔬 경기·인천·포항 박물관/미술관/체육관 (`scrapers/regional_museums_sports.py`)**
   - 경기도어린이박물관, 국립현대미술관 과천, 인천어린이과학관, 포항 로보라이프뮤지엄 등.
5. **🎪 코엑스 & 킨텍스 전시 (`scrapers/conventions.py`)**
   - 서울/경기 대형 키즈페어, 베이비페어, 유아교육전 공식 일정.
6. **🎵 음악회 & 키즈콘서트 (`scrapers/concerts.py`)**
   - 분당 중앙공원 파크콘서트, 성남아트센터 해설 클래식, 롯데콘서트홀 키즈 오케스트라.
7. **🥋 스포츠 대회 및 시범공연 (`scrapers/sports_events.py`)**
   - 전국 태권도 격파왕 최강전, K-타이거즈 시범공연, 마스터즈 수영 선수권.
8. **🔬 국립과천과학관 (`scrapers/gwacheon_sci.py`)**
   - 천문대 천체관측 및 유아체험관, 창의과학교실 공식 예약.
9. **🏛️ 국립중앙박물관 (`scrapers/museum.py`)**
   - 어린이박물관 상설체험 및 특별전 공식 예약.
10. **🏢 키즈플랫폼 & 백화점 문화센터 (`scrapers/kids_platforms.py`)**
    - 현대/신세계 백화점 아카데미 키즈 원데이 클래스 공식 연동.

---

## 3. 핵심 기능 사양

### ① 마감 및 지난 행사 자동 제외 (Auto-Purge Pipeline)
* **저장 단계 자동 필터링 (`core/storage.py`):**
  - 상태가 `마감`, `종료`이거나 마감일(`apply_end`)과 행사일(`event_start`)이 오늘보다 과거인 데이터는 `activities.json` 저장 단계에서 원천 제외.
  - 항상 유효하고 참여 가능한 최신 데이터만 화면에 노출.
* **프론트엔드 2중 필터 (`app.js`):**
  - 클라이언트 사이드에서도 마감/종료 행사를 기본 제외하여 쾌적한 탐색 환경 제공.

### ② 상세 본문 실시간 포스터 이미지 뷰어 (Modal Poster View)
* 카드 클릭 시 상세 모달 상단에 실제 주최 기관의 **공식 행사 포스터/안내문 이미지**를 선명하게 렌더링.
* 포스터 클릭/터치 시 새 창에서 **원본 고화질 이미지**로 확대 보기 지원.

### ③ 일정 산출 및 D-Day 상태 판정 모델 (`core/models.py`)
* **접수 시작 전 (`today < apply_start`):**
  - 상태: **`접수예정`** / D-Day: **`D-N`** (접수 시작일까지 남은 일수)
  - UI 뱃지: 하늘색 `접수예정 (D-N)`
* **접수 기간 중 (`apply_start <= today <= apply_end`):**
  - 상태: **`접수중`** (마감 3일 전 이내는 **`마감임박`**)
  - D-Day: **`D-N`** 또는 **`오늘마감`** (마감일까지 남은 일수)

---

## 4. GitHub Actions CI 자동 교차 검증 파이프라인 (`.github/workflows/daily_crawler.yml`)

1. **매일 한국 시간 오전 6시 자동 실행:**
   - 크롤러 실행 (`python crawler_runner.py`)
   - **10개 출처 전수 교차 검증 (`python verify_all.py`) 자동 실행**:
     * 10개 채널별 최소 수집 건수 및 파일 무결성 검증
     * 날짜 포맷(YYYY-MM-DD), 과거 연도 오염 여부 전수 검사
     * 상태 및 D-Day 매핑 일치성 검증
     * GitHub Step Summary에 마크다운 리포트 자동 생성
2. **검증 통과(PASS) 시에만 자동 배포:**
   - 3중 동기화(`data/activities.json`, `web/activities.json`, `activities.json`) 커밋 및 `main` 브랜치 자동 푸시.
   - 무중단 GitHub Pages 배포 완료.
