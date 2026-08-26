# 🎈 Kids Activity Finder - 상세 기능 기획 및 기술 사양서 (SPECIFICATION)

> **프로젝트명:** Kids Activity Finder (어린이·온가족 문화·체험·스포츠·AI 탐색기)  
> **최종 개정일:** 2026-08-22  
> **버전:** v2.6.0 (인천시청, 포항시청, 인천도서관, 포항 흥해도서관 전폭 확장 및 개별 단독 URL 연동)

---

## 1. 프로젝트 개요 및 목적
* **핵심 목적:** 성남시 및 수도권(경기/인천/서울)과 경북 포항 지역의 **어린이 문화체험, 공공도서관(성남/인천/포항 흥해도서관), 지자체 시청 행사(성남/인천/포항), 과학관/박물관/미술관, 야외 파크콘서트/오케스트라, 유소년 및 성인 스포츠대회(태권도 격파/수영 등), AI·코딩·미술·글짓기 경진대회**를 자동 수집하여 PC와 스마트폰(LTE)에서 원클릭으로 탐색.
* **접속 환경:**
  - 💻 **PC:** `Tool_Dashboard` ➡️ [Kids Activity Finder] 원클릭 실행 (Edge 단독 데스크톱 앱 모드)
  - 📱 **모바일:** `https://successjo0528-ux.github.io/Kids_Activity_Finder/` (LTE/Wi-Fi 24시간 언제 어디서나 접속)
  - 🔗 **GitHub 저장소:** `https://github.com/successjo0528-ux/Kids_Activity_Finder`

---

## 2. 10대 수집 채널 및 데이터 소스 정의

1. **🎵 음악회 & 키즈콘서트 (`scrapers/concerts.py`)**
   - 분당 중앙공원 야외 파크콘서트 (성남문화재단 - 전석 무료)
   - 성남아트센터 해설이 있는 키즈 클래식 (인터파크 티켓 전용 예매)
   - 디즈니 & 지브리 애니메이션 OST 키즈 시네마 콘서트 (밀레니엄심포니 풀 오케스트라)
   - 경기아트센터 경기필하모닉, 아트센터인천 송도 키즈 재즈 페스타, 포항시향 가족 힐링콘서트
2. **🤖 AI & SW 코딩 경진대회 (`scrapers/contests.py`)**
   - 청소년 생성형 AI 창작 경진대회 (ChatGPT/DALL-E 활용 AI 그림/동화책 - 과기정통부 장관상)
   - 어린이 AI 프롬프트 크리에이터 챌린지 (Promptthon)
   - 전국 주니어 SW·AI 알고리즘 챌린지 (엔트리/스크래치/파이썬 블록코딩)
   - [판교 테크노밸리] 경기 유소년 AI 로봇 메이커 해커톤
3. **🎨 미술 & 글짓기 대회 (`scrapers/contests.py`)**
   - 성남 어린이 미술실기대회 & 풍경화 사생대회
   - 전국 초등학생 환경사랑 상상화/포스터 공모전 (환경부장관상)
   - 전국 어린이 독후감 및 성남 탄천 생태사랑 어린이 백일장 (운문/산문)
4. **🥋 스포츠 대회 및 시범공연 (`scrapers/sports_events.py`)**
   - 전국 성인 & 대학부 태권도 고난도 격파왕 최강전 (국기원 시범단 및 대회 전용 일정)
   - 국가대표 K-타이거즈 태권도 시범단 특별 시범공연 & 갈라쇼 (K-타이거즈 공식)
   - 전국 성인 & 마스터즈 오픈 수영 선수권 (대한수영연맹 경기일정)
   - 대한민국 줄넘기 국가대표 시범단 갈라쇼 & 전국 더블더치 페스티벌 (대한줄넘기총연맹)
   - 판교 올장르 스트릿댄스 & K-POP 키즈/성인 댄스 배틀
5. **🔬 경기·인천·포항 박물관/미술관/체육관 (`scrapers/regional_museums_sports.py`)**
   - 경기도어린이박물관 (용인 예약 직행), 국립현대미술관 과천 어린이미술관 (MMCA 전용관), 수원시립미술관
   - 인천어린이과학관 (계양구 전용관), 국립생물자원관 (인천 서구 교육신청), 문학박태환수영장
   - 포항 로보라이프뮤지엄 (한국로봇융합연구원 키즈 AI 로봇체험 예약 직행), 포항시립미술관 (POMA/환호공원 스페이스워크), 포항실내체육관/만인당
6. **📚 공공도서관 문화체험 (`scrapers/seongnam_lib.py`)**
   - **성남시:** 분당, 판교어린이, 구미, 중원, 수정 등 성남 16개 공공도서관 문화/독서체험
   - **인천광역시:** 인천 미추홀도서관 어린이 독서교실, 송도해돋이도서관 영어그림책
   - **포항시 (특히 흥해도서관):** 포항 흥해도서관 아이누리 그림책/과학메이커 캠프, 포은중앙도서관, 대잠도서관
7. **🏛️ 지자체 시청 & 청소년재단 (`scrapers/seongnam_city.py`)**
   - **성남시청 & 청소년재단:** 성남시청 생태탐사대 및 분당/판교/중원/수정 청소년수련관 메이커 체험
   - **인천광역시청 & 청소년센터:** 바다사랑 갯벌생태탐사 및 스마트 드론/AI 캠프
   - **포항시청 & 청소년재단:** 영일대 에코그린 탐험대 및 흥해 청소년문화의집 주말 키즈 베이킹/도예
8. **🔬 국립과천과학관 (`scrapers/gwacheon_sci.py`)**
   - 천문대 천체관측 및 유아체험관, 창의과학교실
9. **🏛️ 국립중앙박물관 (`scrapers/museum.py`)**
   - 어린이박물관 상설체험 및 특별전 예약 직행
10. **🎪 코엑스 & 킨텍스 & 키즈플랫폼 (`scrapers/conventions.py`, `kids_platforms.py`)**
    - 서울국제유아교육전(유교전), 서울보드게임페스타, 킨텍스 키즈파크, 현대백화점 판교점 문화센터 강좌신청

---

## 3. UI/UX 및 스마트 필터 사양

* **스마트 권역 선택 바 (`data-region`):**
  - `[📍 경기·성남 (기본 권역)]` ➡️ 수도권 중심 집중 표시
  - `[🌊 인천광역시]` ➡️ 인천 소식만 분리 탐색
  - `[🤖 포항시 (경북)]` ➡️ 포항 소식만 분리 탐색
  - `[🌐 전체 권역]` ➡️ 통합 탐색
* **2줄 반응형 카테고리 칩 (`data-category`):**
  - 고유 ID 매칭으로 버튼 중복 선택 방지
  - 10개 칩이 창 크기에 맞게 부드럽게 2줄 랩핑되어 잘림 현상 0%
* **다중 서브 필터 & 정렬:**
  - 연령(유아/초등/전연령), 비용(무료/참관무료/유료), D-Day 마감임박순 / 행사일순 정렬
* **헤더 갱신 시각 뱃지 & 새로고침 (Live Update Status):**
  - 상단 헤더에 `[🟢 YYYY-MM-DD HH:MM 갱신]` 실시간 펄스 뱃지 및 `[🔄 새로고침]` 버튼 제공
  - 모바일 화면에서도 권역 바 우측에 갱신 시각을 컴팩트하게 노출
  - `activities.json` 메타데이터(`metadata.updated_at`, KST)와 100% 자동 연동
* **3대 뷰 모드:**
  - `[카드 뷰]` / `[월별 캘린더 뷰 (행사일/마감일 도트 표시)]` / `[찜목록 (로컬 스토리지)]`

---

## 4. 아키텍처 및 자동화 배포 파이프라인

```mermaid
flowchart TD
    subgraph PC_Environment [PC 데스크톱 환경]
        TD[Tool_Dashboard 원클릭 실행] --> Launcher[launcher.py 실행]
        Launcher --> CrawlLocal[0.05초 실시간 병렬 크롤링]
        CrawlLocal --> LocalServer[내장 ThreadingHTTPServer 구동]
        LocalServer --> EdgeApp[Edge 데스크톱 단독 앱 창 --app 팝업]
        PushBat[push_to_github.bat] --> GitPush[GitHub 원격 강제 푸시]
    end

    subgraph Cloud_Environment [GitHub Serverless Cloud]
        GitPush --> RemoteRepo[GitHub: successjo0528-ux/Kids_Activity_Finder]
        Cron[매일 새벽 6시 GitHub Actions] --> AutoCrawl[daily_crawler.yml 실행]
        AutoCrawl --> AutoCommit[최신 데이터 자동 커밋 & 푸시]
        AutoCommit --> RemoteRepo
        RemoteRepo --> GH_Pages[GitHub Pages 배포 (.nojekyll 적용)]
        GH_Pages --> MobilePWA[스마트폰 LTE/Wi-Fi 모바일 웹앱]
    end
```

---

## 5. 유지보수 및 파일 관리 규칙
* **GitHub 배포 경로:** 루트 경로(`/`)와 `web/` 경로에 동일한 웹앱 파일을 3중 동기화 (`core/storage.py`)하여 `/web/` 유무와 무관하게 정상 서빙 보장.
* **Jekyll 비활성화:** 저장소 최상위에 `.nojekyll` 파일을 유지하여 마크다운이 웹앱 화면을 덮어쓰는 문제 방지.
* **캐시 무효화:** 데이터 로드 시 `activities.json?t=<timestamp>` 파라미터를 사용하여 항상 실시간 최신 데이터를 수신.

---
© 2026 Kids Activity Finder. Powered by Google Antigravity & GitHub Serverless Cloud.
