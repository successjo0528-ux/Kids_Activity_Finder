# Kids Activity Finder (키즈 액티비티 파인더) 기획안

> **문서 버전:** v3.3.0 (cron-job.org External Webhook Single Scheduler & Concurrency Control)  
> **최종 개정일:** 2026-08-31  
> **프로젝트 위치:** `G:\My Program\Kids_Activity_Finder\`  
> **웹 라이브 URL:** [https://successjo0528-ux.github.io/Kids_Activity_Finder/](https://successjo0528-ux.github.io/Kids_Activity_Finder/)  
> **GitHub 저장소:** [https://github.com/successjo0528-ux/Kids_Activity_Finder](https://github.com/successjo0528-ux/Kids_Activity_Finder)

---

## 1. 기획 배경 및 목적
* **기획 배경:**
  * 주말마다 아이들과 함께 갈 수 있는 문화체험, 과학관 관람, 도서관 특강, 전시회, AI·미술 공모전 정보가 여러 지자체·기관 사이트에 흩어져 있어 일일이 찾아보기 번거로움.
  * 기존 포털의 링크 깨짐(404 에러), 마감된 행사 노출, 하드코딩된 가짜 데이터 및 정적 사이트 배포 실패(Jekyll 충돌 및 워크플로우 충돌) 문제를 원천 해결할 필요성 대두.
* **핵심 목적:**
  * 성남(분당/판교), 인천(송도/청라/구월), 경북 포항 및 서울 수도권 일대의 어린이·온가족 프로그램을 **스스로 웹사이트를 순회하여 수집하는 100% 실시간 웹 크롤러 엔진**으로 구축.
  * 수집된 모든 URL의 **실시간 404 생존 검증(Live URL Health Check)**을 통과한 무결점 데이터만 PC 및 스마트폰(모바일 PWA)에 서비스.
  * **Global_Macro_Briefing과 동일한 정석 GitHub Pages 아키텍처(Zero-CORS `data.js` + `.nojekyll` + `daily_crawler.yml` 자동 배포)**를 적용하여 로컬 더블클릭 오프라인 실행과 웹 배포 100% 무결점 보장.

---

## 2. 10대 수집 채널 및 데이터 구성

| 탭 / 카테고리 | 대상 기관 및 수집 내용 | 크롤링 방식 |
| :--- | :--- | :---: |
| **🎪 전시·박람회 (코엑스·킨텍스)** | • **코엑스(COEX)** 1~6페이지 전수 (AI 페스타, 한국전자전, 유아교육전, 코베, 디자인코리아 등 59건)<br>• **킨텍스(KINTEX)** & **SETEC** 유아·키즈 박람회 | ⭐ 실시간 HTML 웹 크롤러 |
| **🔬 박물관·미술관·과학관** | • **국립과천과학관** (천문대 야간관측, 유아체험관, 창의과학교실)<br>• **국립중앙박물관** (특별기획전, 어린이박물관, 가족탐구교실)<br>• **국립현대미술관 과천** (어린이미술관)<br>• **경기도어린이박물관** (용인 상갈)<br>• **인천어린이과학관** & **국립생물자원관** (생생채움) | ⭐ 실시간 연동 크롤러 |
| **🤖 AI & 코딩대회** | • 알럽콘 전국 유소년 AI/SW 경진대회, 로봇 코딩 캠프 | ⭐ 실시간 HTML 웹 크롤러 |
| **🎨 미술·글짓기** | • 전국 어린이 미술대회, 백일장, 독서감상문 공모전 | ⭐ 실시간 HTML 웹 크롤러 |
| **🥋 스포츠·태권도·수영** | • 대한태권도협회 격파왕 대회, 탄천 수영대회, 줄넘기 갈라쇼 | ⚡ 라이브 서버 커넥터 |
| **📚 공공도서관 (성남·인천·포항)** | • **성남시립 7곳** (운중, 판교어린이, 분당, 판교, 위례, 중원어린이, 서현)<br>• **인천 5곳** (청라국제, 인천시청, 미추홀, 송도, 연수청학)<br>• **포항시립 2곳** (포은흥해, 포은중앙) | ⭐ 실시간 HTML 웹 크롤러 |
| **🏛️ 시청·지자체** | • 성남시 배움숲, 판교청소년수련관, 포항 흥해문화의집, 인천청소년센터 | ⚡ 라이브 서버 커넥터 |
| **🎵 음악회·콘서트** | • 성남아트센터 키즈클래식, 롯데콘서트홀 시네마콘서트, 세종문화회관 | ⚡ 라이브 서버 커넥터 |
| **🏢 백화점·문화센터** | • **놀이의발견(Nolbal)** 주말 키즈 액티비티 & 원데이 클래스 / 키즈카페 예약<br>• **키즈노트(Kidsnote)** 영유아 오감놀이 체험단<br>• **하이클래스(HiClass)** 초등 방과후 라이브 클래스<br>• 현대백화점 판교점 문화센터, 신세계백화점 경기점 아카데미 | ⚡ 라이브 서버 커넥터 |

---

## 3. 핵심 시스템 아키텍처 및 무결성 파이프라인

1. **지능형 중복 제거 전담 에이전트 (`core/deduplicator.py`):**
   * `ActivityDeduplicator`를 통해 제목 정규화 유사도(Normalized Similarity >= 85%) 및 복합키 기반 중복 정제.
   * 다중 출처에서 동일 행사 수집 시 고화질 포스터와 상세 설명을 가진 최상위 카드 1개로 자동 병합.
2. **마감 데이터 자동 제외 (Auto-Purge Pipeline):**
   * 접수 마감일 및 행사 종료일이 지난 과거 데이터는 수집 및 저장 단계에서 100% 자동 필터링.
3. **Zero-CORS `data.js` & `activities.json` 듀얼 데이터 파이프라인:**
   * `core/storage.py`에서 `activities.json`과 함께 `window.__ACTIVITIES_DATA__`를 담은 `data.js`를 동시 생성.
   * 로컬 탐색기에서 `index.html`을 더블클릭(`file:///`)해도 보안 에러 없이 즉시 렌더링되며, 웹(GitHub Pages)에서도 0초 즉각 렌더링 및 비동기 `fetch` 갱신 지원.
4. **9단계 전수 무결성 검증 시스템 (`verify_all.py`):**
   * **[검증 1] 데이터 파일 무결성:** `data/` 및 `web/` activities.json 구조 검증.
   * **[검증 2] 10개 출처 수집량 검사:** 전 채널 최소 수집 기준 충족 여부.
   * **[검증 3] 소스코드 감사 (Code Audit):** 10개 스크래퍼 코드 내 실제 외부 네트워크 통신 탑재 여부 (하드코딩 적발 시 FAIL).
   * **[검증 4] URL 실시간 404 생존 감사 (Live URL Health Check):** 수집된 전체 링크(120여 개) 실시간 HTTP 요청 (404 에러 0건 원칙).
   * **[검증 5] 중복 제거 무결성:** 잔여 중복 카드 0건 검사.
   * **[검증 6] 날짜 및 상태 정합성:** YYYY-MM-DD 포맷 및 D-Day 일치성 전수 검사.
   * **[검증 7] 모바일 PWA 및 data.js 검사:** 필수 웹 리소스(HTML/CSS/JS/Manifest/data.js) 존재 및 크기 검사.
   * **[검증 8] 대시보드 등록 검사:** `Tool_Dashboard/programs.json` 등록 상태.
   * **[검증 9] GitHub Pages 배포 무결성:** `.nojekyll`, `data.js`, `push_to_github.bat`, `daily_crawler.yml` 5종 정합성.

---

## 4. 실행 및 배포 환경
* **자동 스케줄링:** cron-job.org 외부 Webhook (`workflow_dispatch`)을 통해 매일 정시 GitHub Actions(`daily_crawler.yml`)를 즉시 트리거하여 전수 크롤링 및 무결성 검증 자동 배포.
* **PC 실행:** `G:\My Program\Tool_Dashboard\` 대시보드에서 [Kids Activity Finder] 원클릭 실행.
* **원클릭 배포:** `push_to_github.bat`을 실행하면 최신 데이터와 코드가 Git Staging/Commit/Push되어 즉시 라이브 사이트에 반영.
* **모바일 실행:** 웹 라이브 URL 접속 및 홈 화면에 추가 (PWA 앱 모드).
