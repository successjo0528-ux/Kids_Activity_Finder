/**
 * Kids Activity Finder - 메인 프론트엔드 인터랙션 로직
 * - 고유 data-category 및 data-region 기반 1:1 매칭 (중복 활성화 버그 100% 방지)
 */

// 전역 상태
let allActivities = [];
let filteredActivities = [];
let currentMainRegion = "경기권역"; // 기본값: '경기권역' (성남+경기+서울+전국대회)
let currentCategory = "전체";
let currentView = "cards"; // 'cards', 'calendar', 'bookmarks'
let currentCalendarDate = new Date();
let selectedCalendarDateStr = null;
let currentModalActivity = null;

// 로컬 스토리지 북마크 키
const BOOKMARKS_KEY = "kids_finder_bookmarks_v1";

// 1. 초기 로드
document.addEventListener("DOMContentLoaded", () => {
  initBookmarks();
  loadData();
  setupSearchEvents();
});

// 2. 데이터 불러오기
async function loadData() {
  const updateBadgeElem = document.getElementById("last-updated-text");
  const updateBadgeMobile = document.getElementById("last-updated-text-mobile");
  const refreshIcon = document.getElementById("refresh-icon");
  if (refreshIcon) refreshIcon.classList.add("fa-spin");

  function processActivitiesData(data) {
    if (!data) return false;
    if (Array.isArray(data)) {
      allActivities = data;
    } else if (data && data.items) {
      allActivities = data.items;
      if (data.metadata && data.metadata.updated_at) {
        const timeStr = data.metadata.updated_at.slice(0, 16);
        if (updateBadgeElem) updateBadgeElem.textContent = `${timeStr} 갱신`;
        if (updateBadgeMobile) updateBadgeMobile.textContent = `${timeStr.slice(5)} 갱신`;
      }
    }
    // 메타데이터가 없는 레거시 구조 대응
    if ((!data.metadata || !data.metadata.updated_at) && allActivities.length > 0) {
      const dates = allActivities.map(a => a.created_at || '').filter(Boolean).sort().reverse();
      if (dates.length > 0) {
        const fallbackDate = dates[0].replace('T', ' ').slice(0, 16);
        if (updateBadgeElem) updateBadgeElem.textContent = `${fallbackDate} 갱신`;
        if (updateBadgeMobile) updateBadgeMobile.textContent = `${fallbackDate.slice(5)} 갱신`;
      }
    }
    applyFilters();
    return true;
  }

  // 1단계: data.js를 통한 즉시 로드 (로컬 더블클릭 및 네트워크 0초 렌더링)
  let loadedFromWindow = false;
  if (window.__ACTIVITIES_DATA__) {
    loadedFromWindow = processActivitiesData(window.__ACTIVITIES_DATA__);
  }

  // 2단계: 최신 activities.json 비동기 fetch 시도 (서버/웹 환경 최신화)
  try {
    const res = await fetch("activities.json?t=" + new Date().getTime(), {
      cache: "no-store",
      headers: { "Pragma": "no-cache", "Cache-Control": "no-cache" }
    });
    if (res.ok) {
      const data = await res.json();
      processActivitiesData(data);
    } else if (!loadedFromWindow) {
      throw new Error("JSON 파일을 찾을 수 없습니다.");
    }
  } catch (err) {
    if (!loadedFromWindow) {
      console.error("데이터 로드 실패:", err);
      if (updateBadgeElem) updateBadgeElem.textContent = "데이터 로드 실패";
      if (updateBadgeMobile) updateBadgeMobile.textContent = "로드 실패";
      document.getElementById("cards-grid").innerHTML = `
        <div class="col-span-full text-center py-12 text-slate-500">
          <p class="text-base font-semibold mb-2">데이터를 불러오는 중입니다...</p>
          <p class="text-xs">잠시 후 새로고침 버튼을 눌러주세요.</p>
        </div>
      `;
    }
  } finally {
    if (refreshIcon) {
      setTimeout(() => refreshIcon.classList.remove("fa-spin"), 300);
    }
  }
}

function refreshData() {
  loadData();
}

// 3. 북마크 관리
function getBookmarks() {
  try {
    return JSON.parse(localStorage.getItem(BOOKMARKS_KEY)) || [];
  } catch {
    return [];
  }
}

function initBookmarks() {
  updateBookmarkBadge();
}

function updateBookmarkBadge() {
  const bookmarks = getBookmarks();
  const badge = document.getElementById("bookmark-badge");
  if (bookmarks.length > 0) {
    badge.textContent = bookmarks.length;
    badge.classList.remove("hidden");
  } else {
    badge.classList.add("hidden");
  }
}

function toggleBookmark(id, event) {
  if (event) event.stopPropagation();
  let bookmarks = getBookmarks();
  const idx = bookmarks.indexOf(id);
  if (idx > -1) {
    bookmarks.splice(idx, 1);
  } else {
    bookmarks.push(id);
  }
  localStorage.setItem(BOOKMARKS_KEY, JSON.stringify(bookmarks));
  updateBookmarkBadge();
  
  if (currentView === "bookmarks") {
    applyFilters();
  } else {
    renderCards();
  }
  if (currentModalActivity && currentModalActivity.id === id) {
    updateModalBookmarkBtn(id);
  }
}

// 4. 검색 이벤트
function setupSearchEvents() {
  const input = document.getElementById("search-input");
  const clearBtn = document.getElementById("clear-search");

  input.addEventListener("input", (e) => {
    if (e.target.value.trim().length > 0) {
      clearBtn.classList.remove("hidden");
    } else {
      clearBtn.classList.add("hidden");
    }
    applyFilters();
  });
}

function clearSearch() {
  const input = document.getElementById("search-input");
  input.value = "";
  document.getElementById("clear-search").classList.add("hidden");
  applyFilters();
}

// 5. 메인 권역 퀵 전환 (data-region 1:1 매칭)
function setMainRegion(region) {
  currentMainRegion = region;
  document.querySelectorAll("#region-chips .region-chip").forEach(chip => {
    if (chip.dataset.region === region) {
      chip.classList.add("active");
    } else {
      chip.classList.remove("active");
    }
  });

  // 드롭다운 세부 지역도 초기화
  document.getElementById("filter-region").value = "전체";
  applyFilters();
}

// 6. 카테고리 칩 선택 (고유 data-category 1:1 매칭으로 중복 선택 100% 방지)
function setCategory(category) {
  currentCategory = category;
  document.querySelectorAll("#category-chips .chip").forEach(chip => {
    if (chip.dataset.category === category) {
      chip.classList.add("active");
    } else {
      chip.classList.remove("active");
    }
  });
  applyFilters();
}

// 7. 뷰 모드 전환
function switchView(viewName) {
  currentView = viewName;
  const tabCards = document.getElementById("tab-cards");
  const tabCalendar = document.getElementById("tab-calendar");
  const tabBookmarks = document.getElementById("tab-bookmarks");
  const viewCards = document.getElementById("view-cards-container");
  const viewCalendar = document.getElementById("view-calendar-container");

  [tabCards, tabCalendar, tabBookmarks].forEach(t => {
    t.className = "px-3 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900";
  });

  if (viewName === "cards") {
    tabCards.className = "px-3 py-1.5 rounded-lg transition-all active-tab shadow-sm bg-white text-indigo-600 font-bold";
    viewCards.classList.remove("hidden");
    viewCalendar.classList.add("hidden");
    applyFilters();
  } else if (viewName === "calendar") {
    tabCalendar.className = "px-3 py-1.5 rounded-lg transition-all active-tab shadow-sm bg-white text-indigo-600 font-bold";
    viewCards.classList.add("hidden");
    viewCalendar.classList.remove("hidden");
    renderCalendar();
  } else if (viewName === "bookmarks") {
    tabBookmarks.className = "px-3 py-1.5 rounded-lg transition-all active-tab shadow-sm bg-white text-rose-600 font-bold flex items-center gap-1";
    viewCards.classList.remove("hidden");
    viewCalendar.classList.add("hidden");
    applyFilters();
  }
}

// 8. 필터 적용 로직
function applyFilters() {
  const query = document.getElementById("search-input").value.trim().toLowerCase();
  const subRegion = document.getElementById("filter-region").value;
  const age = document.getElementById("filter-age").value;
  const cost = document.getElementById("filter-cost").value;
  const sort = document.getElementById("filter-sort").value;
  const bookmarks = getBookmarks();

  filteredActivities = allActivities.filter(item => {
    // 0. 마감 및 종료된 행사는 기본 제외
    if (item.status === "마감" || item.d_day === "마감" || item.status === "종료") {
      return false;
    }

    // 찜목록 뷰
    if (currentView === "bookmarks" && !bookmarks.includes(item.id)) {
      return false;
    }

    // 1. 메인 권역 필터 (경기권역 기본값 vs 인천 vs 포항 vs 전체)
    const itemRegion = (item.region || "") + " " + (item.place_name || "") + " " + (item.source_name || "");
    if (currentMainRegion === "경기권역") {
      const isGyeonggiOrCapital = 
        itemRegion.includes("성남") || 
        itemRegion.includes("경기") || 
        itemRegion.includes("분당") || 
        itemRegion.includes("판교") || 
        itemRegion.includes("수정") || 
        itemRegion.includes("중원") || 
        itemRegion.includes("용인") || 
        itemRegion.includes("수원") || 
        itemRegion.includes("과천") || 
        itemRegion.includes("고양") || 
        itemRegion.includes("서울") || 
        itemRegion.includes("전국") || 
        item.source_key === "contests" || 
        item.source_key === "conventions" || 
        item.source_key === "museum" || 
        item.source_key === "gwacheon_sci" || 
        item.source_key === "seongnam_lib" || 
        item.source_key === "seongnam_city" || 
        item.source_key === "kids_platforms";

      if (!isGyeonggiOrCapital) {
        if (!itemRegion.includes("전국")) return false;
      }
      // 인천/포항 전용 도서관/지자체는 인천/포항 탭에서 우선 제공
      if ((itemRegion.includes("인천") || itemRegion.includes("포항")) && item.source_key === "seongnam_lib") {
        return false;
      }
    } else if (currentMainRegion === "인천") {
      if (!itemRegion.includes("인천") && !itemRegion.includes("송도") && !itemRegion.includes("계양") && !itemRegion.includes("미추홀") && !itemRegion.includes("청라")) {
        return false;
      }
    } else if (currentMainRegion === "포항") {
      if (!itemRegion.includes("포항") && !itemRegion.includes("경북") && !itemRegion.includes("흥해")) {
        return false;
      }
    }

    // 2. 세부 지역 드롭다운 필터
    if (subRegion !== "전체") {
      const regionSearchStr = `${item.region || ''} ${item.place_name || ''} ${item.address || ''} ${item.title || ''}`;
      if (!regionSearchStr.includes(subRegion)) return false;
    }

    // 3. 지능형 카테고리 필터 (다중 호환 매핑)
    if (currentCategory !== "전체") {
      if (currentCategory === "전시행사") {
        const isExpo = item.category === "전시행사" || item.category === "전시체험" || item.source_key === "conventions" || (item.tags || []).some(t => t.includes("전시") || t.includes("박람회") || t.includes("페어"));
        if (!isExpo) return false;
      } else if (currentCategory === "과학박물관") {
        const isSciMuseum = item.category === "과학박물관" || item.category === "과학체험" || item.category === "과학관체험" || item.category === "박물관체험" || item.category === "미술관체험" || item.source_key === "gwacheon_sci" || item.source_key === "museum" || item.source_key === "regional_museums_sports";
        if (!isSciMuseum) return false;
      } else if (currentCategory === "AI코딩대회") {
        const isAiCoding = item.category === "AI코딩대회" || 
          (item.tags || []).some(t => t.includes("AI") || t.includes("로봇") || t.includes("코딩") || t.includes("과학")) ||
          (item.title || "").includes("AI") || (item.title || "").includes("인공지능") || (item.title || "").includes("로봇") || (item.title || "").includes("코딩");
        if (!isAiCoding) return false;
      } else if (currentCategory === "미술글짓기") {
        const isArt = item.category === "미술글짓기" || (item.tags || []).some(t => t.includes("미술") || t.includes("그림") || t.includes("글짓기") || t.includes("백일장"));
        if (!isArt) return false;
      } else if (currentCategory === "스포츠대회") {
        const isSports = item.category === "스포츠대회" || item.source_key === "sports_events";
        if (!isSports) return false;
      } else if (currentCategory === "도서관체험") {
        const isLib = item.category === "도서관체험" || item.source_key === "seongnam_lib";
        if (!isLib) return false;
      } else if (currentCategory === "지자체체험") {
        const isCity = item.category === "지자체체험" || item.source_key === "seongnam_city";
        if (!isCity) return false;
      } else if (currentCategory === "음악공연") {
        const isMusic = item.category === "음악공연" || item.source_key === "concerts";
        if (!isMusic) return false;
      } else if (currentCategory === "키즈플랫폼") {
        const isPlatform = item.category === "키즈플랫폼" || item.category === "문화센터" || item.source_key === "kids_platforms";
        if (!isPlatform) return false;
      } else if (item.category !== currentCategory) {
        return false;
      }
    }

    // 4. 검색어 필터
    if (query) {
      const matchTitle = (item.title || "").toLowerCase().includes(query);
      const matchPlace = (item.place_name || "").toLowerCase().includes(query);
      const matchTags = (item.tags || []).some(t => t.toLowerCase().includes(query));
      const matchDesc = (item.description || "").toLowerCase().includes(query);
      if (!matchTitle && !matchPlace && !matchTags && !matchDesc) return false;
    }

    // 5. 대상 연령 필터
    if (age !== "전체") {
      if (!item.target_age.includes(age) && item.target_age !== "전연령") return false;
    }

    // 6. 비용 필터
    if (cost !== "전체") {
      if (cost === "무료" && item.cost_type !== "무료") return false;
      if (cost === "참관무료" && item.cost_type !== "참관무료") return false;
      if (cost === "유료" && item.cost_type !== "유료") return false;
    }

    return true;
  });

  // 정렬
  if (sort === "dday") {
    filteredActivities.sort((a, b) => {
      if (a.d_day.startsWith("D-") && b.d_day.startsWith("D-")) {
        const da = parseInt(a.d_day.replace("D-", "")) || 999;
        const db = parseInt(b.d_day.replace("D-", "")) || 999;
        return da - db;
      }
      return a.title.localeCompare(b.title);
    });
  } else if (sort === "event") {
    filteredActivities.sort((a, b) => (a.event_start || "").localeCompare(b.event_start || ""));
  }

  const countElem = document.getElementById("total-count");
  const countMobileElem = document.getElementById("total-count-mobile");
  if (countElem) countElem.textContent = filteredActivities.length;
  if (countMobileElem) countMobileElem.textContent = filteredActivities.length;

  if (currentView === "calendar") {
    renderCalendar();
  } else {
    renderCards();
  }
}

function resetFilters() {
  document.getElementById("search-input").value = "";
  document.getElementById("clear-search").classList.add("hidden");
  document.getElementById("filter-region").value = "전체";
  document.getElementById("filter-age").value = "전체";
  document.getElementById("filter-cost").value = "전체";
  document.getElementById("filter-sort").value = "dday";
  setMainRegion("경기권역");
  setCategory("전체");
  switchView("cards");
}

// 9. 카드 뷰 렌더링
function renderCards() {
  const container = document.getElementById("cards-grid");
  const emptyState = document.getElementById("empty-state");
  const bookmarks = getBookmarks();

  if (filteredActivities.length === 0) {
    container.innerHTML = "";
    emptyState.classList.remove("hidden");
    return;
  }

  emptyState.classList.add("hidden");

  container.innerHTML = filteredActivities.map(item => {
    const isBookmarked = bookmarks.includes(item.id);
    
    let ddayBadgeClass = "badge-dday-normal";
    let ddayLabel = item.d_day || "";
    if (item.status === "접수예정") {
      ddayBadgeClass = "bg-sky-50 text-sky-700 border border-sky-300 font-semibold";
      ddayLabel = `접수예정 (${item.d_day})`;
    } else if (item.d_day === "오늘마감" || item.d_day === "D-1" || item.d_day === "D-2" || item.d_day === "D-3") {
      ddayBadgeClass = "badge-dday-urgent";
    } else if (item.d_day === "마감" || item.d_day === "종료") {
      ddayBadgeClass = "badge-dday-ended";
    }

    const isFree = item.cost_type === "무료" || item.cost_type === "참관무료";
    const costBadge = isFree 
      ? `<span class="badge-free px-2 py-0.5 rounded text-[10px] font-bold">${item.cost_type}</span>`
      : `<span class="bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded text-[10px] font-bold">유료</span>`;

    // 카테고리별 예쁜 색상 배지
    let catBadgeColor = "bg-slate-100 text-slate-700";
    let catLabel = item.source_name;
    if (item.category === "음악공연") {
      catBadgeColor = "bg-sky-50 text-sky-700 border border-sky-200 font-bold";
      catLabel = "🎵 " + item.source_name;
    } else if (item.category === "AI코딩대회") {
      catBadgeColor = "bg-purple-50 text-purple-700 border border-purple-200 font-bold";
      catLabel = "🤖 AI/코딩대회";
    } else if (item.category === "미술글짓기") {
      catBadgeColor = "bg-amber-50 text-amber-700 border border-amber-200 font-bold";
      catLabel = "🎨 " + item.source_name;
    } else if (item.category === "스포츠대회") {
      catBadgeColor = "bg-emerald-50 text-emerald-700 border border-emerald-200 font-bold";
      catLabel = "🥋 " + item.source_name;
    }

    return `
      <div class="activity-card" onclick="openDetailModal('${item.id}')">
        <div>
          <!-- 상단 태그 & 북마크 -->
          <div class="flex items-center justify-between gap-2 mb-2">
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="${catBadgeColor} px-2 py-0.5 rounded text-[10px] truncate max-w-[180px]">${catLabel}</span>
              ${costBadge}
            </div>
            <button onclick="toggleBookmark('${item.id}', event)" class="text-slate-300 hover:text-rose-500 transition p-1 text-sm">
              <i class="${isBookmarked ? 'fa-solid text-rose-500' : 'fa-regular'} fa-heart"></i>
            </button>
          </div>

          <!-- 행사 제목 -->
          <h3 class="font-bold text-sm text-slate-900 leading-snug line-clamp-2 mb-2 hover:text-indigo-600 transition">
            ${item.title}
          </h3>

          <!-- 장소 & 대상 -->
          <div class="space-y-1 text-xs text-slate-500 mb-3">
            <div class="flex items-center gap-1.5 truncate">
              <i class="fa-solid fa-location-dot text-slate-400 text-[11px] w-3"></i>
              <span class="truncate">${item.place_name || item.region}</span>
            </div>
            <div class="flex items-center gap-1.5 truncate">
              <i class="fa-solid fa-child text-slate-400 text-[11px] w-3"></i>
              <span class="truncate">${item.target_age}</span>
            </div>
            <div class="flex items-center gap-1.5 truncate">
              <i class="fa-solid fa-calendar text-slate-400 text-[11px] w-3"></i>
              <span class="truncate">${item.event_start ? '일시: ' + item.event_start : '접수: ' + (item.apply_end || '상시')}</span>
            </div>
          </div>
        </div>

        <!-- 카드 하단 D-Day 및 신청 상태 -->
        <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
          <span class="${ddayBadgeClass} px-2.5 py-0.5 rounded-full text-[11px] font-bold">
            ${ddayLabel || item.status}
          </span>
          <span class="text-[11px] text-indigo-600 font-semibold flex items-center gap-1">
            상세보기 <i class="fa-solid fa-chevron-right text-[9px]"></i>
          </span>
        </div>
      </div>
    `;
  }).join("");
}

// 10. 캘린더 뷰 렌더링
function renderCalendar() {
  const year = currentCalendarDate.getFullYear();
  const month = currentCalendarDate.getMonth();

  document.getElementById("calendar-month-title").textContent = `${year}년 ${month + 1}월`;

  const firstDay = new Date(year, month, 1).getDay();
  const lastDate = new Date(year, month + 1, 0).getDate();
  const todayStr = new Date().toISOString().slice(0, 10);

  const grid = document.getElementById("calendar-days-grid");
  grid.innerHTML = "";

  for (let i = 0; i < firstDay; i++) {
    grid.innerHTML += `<div class="cal-day opacity-30 bg-transparent border-transparent cursor-default"></div>`;
  }

  for (let day = 1; day <= lastDate; day++) {
    const dayStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const isToday = dayStr === todayStr;
    const isSelected = dayStr === selectedCalendarDateStr;

    const dayItems = filteredActivities.filter(item => {
      const applyEnd = (item.apply_end || "").slice(0, 10);
      const eventStart = (item.event_start || "").slice(0, 10);
      return applyEnd === dayStr || eventStart === dayStr;
    });

    let dotsHtml = "";
    if (dayItems.length > 0) {
      dotsHtml = `<div class="mt-1 flex flex-wrap gap-0.5">` + 
        dayItems.slice(0, 4).map(item => {
          let dotColor = "bg-indigo-500";
          if (item.category === "음악공연") dotColor = "bg-sky-500";
          if (item.category === "AI코딩대회") dotColor = "bg-purple-500";
          if (item.category === "스포츠대회") dotColor = "bg-emerald-500";
          if (item.category === "미술글짓기") dotColor = "bg-amber-500";
          if (item.category === "도서관체험") dotColor = "bg-blue-500";
          return `<span class="cal-event-dot ${dotColor}"></span>`;
        }).join("") +
        (dayItems.length > 4 ? `<span class="text-[9px] text-slate-400 font-bold">+${dayItems.length-4}</span>` : '') +
      `</div>`;
    }

    grid.innerHTML += `
      <div class="cal-day ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''}" onclick="selectCalendarDate('${dayStr}')">
        <span class="text-xs font-semibold ${isToday ? 'text-indigo-600' : 'text-slate-700'}">${day}</span>
        ${dotsHtml}
      </div>
    `;
  }

  if (selectedCalendarDateStr) {
    showCalendarDateDetails(selectedCalendarDateStr);
  } else {
    selectCalendarDate(todayStr);
  }
}

function prevMonth() {
  currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
  renderCalendar();
}

function nextMonth() {
  currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
  renderCalendar();
}

function currentMonth() {
  currentCalendarDate = new Date();
  selectCalendarDate(new Date().toISOString().slice(0, 10));
}

function selectCalendarDate(dateStr) {
  selectedCalendarDateStr = dateStr;
  renderCalendar();
  showCalendarDateDetails(dateStr);
}

function showCalendarDateDetails(dateStr) {
  const titleElem = document.getElementById("selected-date-title");
  const listElem = document.getElementById("selected-date-list");

  const dayItems = filteredActivities.filter(item => {
    const applyEnd = (item.apply_end || "").slice(0, 10);
    const eventStart = (item.event_start || "").slice(0, 10);
    return applyEnd === dateStr || eventStart === dateStr;
  });

  titleElem.innerHTML = `<i class="fa-solid fa-calendar-day text-indigo-500"></i> ${dateStr} 일정 (${dayItems.length}건)`;

  if (dayItems.length === 0) {
    listElem.innerHTML = `
      <div class="col-span-full text-slate-400 text-xs py-4 text-center bg-slate-50 rounded-xl border border-slate-100">
        선택한 날짜에 예정된 행사나 마감 일정이 없습니다.
      </div>
    `;
    return;
  }

  listElem.innerHTML = dayItems.map(item => `
    <div class="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between gap-2 hover:border-indigo-400 cursor-pointer transition shadow-sm" onclick="openDetailModal('${item.id}')">
      <div class="truncate">
        <span class="text-[10px] font-bold text-indigo-600 bg-indigo-50 px-1.5 py-0.5 rounded">${item.source_name}</span>
        <h4 class="font-bold text-xs text-slate-800 truncate mt-1">${item.title}</h4>
        <p class="text-[11px] text-slate-500">${item.place_name} · ${item.target_age}</p>
      </div>
      <span class="shrink-0 text-xs font-bold text-rose-500 bg-rose-50 px-2 py-1 rounded-lg">${item.d_day || item.status}</span>
    </div>
  `).join("");
}

// 11. 모달 제어
function openDetailModal(id) {
  try {
    const item = allActivities.find(a => a.id === id);
    if (!item) {
      console.warn("해당 ID의 행사를 찾을 수 없습니다:", id);
      return;
    }

    currentModalActivity = item;
    const setElemText = (elId, text) => {
      const el = document.getElementById(elId);
      if (el) el.textContent = text || "";
    };

    setElemText("modal-category-badge", item.category || "기타");
    setElemText("modal-dday-badge", item.d_day || item.status || "D-Day");
    setElemText("modal-cost-badge", item.cost_type || "무료");
    setElemText("modal-title", item.title || "행사 안내");
    setElemText("modal-place", item.place_name || item.region || "상세 안내 참조");
    setElemText("modal-address", item.address || item.place_name || "");
    setElemText("modal-source", item.source_name || "공식 주최 기관");
    setElemText("modal-age", item.target_age || "전연령");
    setElemText("modal-apply-period", `${item.apply_start || '상시'} ~ ${item.apply_end || '선착순 마감'}`);
    setElemText("modal-event-period", `${item.event_start || '상세 안내 참조'} ${item.event_end && item.event_end !== item.event_start ? '~ ' + item.event_end : ''}`);
    setElemText("modal-cost-info", item.cost_info || item.cost_type || "무료");
    setElemText("modal-description", item.description || "상세 페이지를 통해 상세한 안내를 확인해 주세요.");

    const tagsContainer = document.getElementById("modal-tags");
    if (tagsContainer) {
      tagsContainer.innerHTML = (item.tags || []).map(t => `<span class="bg-slate-100 text-slate-600 px-2 py-1 rounded-md text-[11px] font-medium">${t}</span>`).join("");
    }

    // 🖼️ 실제 포스터 / 안내 이미지 표시 (기본 파비콘 제외)
    const imgContainer = document.getElementById("modal-image-container");
    const modalImg = document.getElementById("modal-image");
    if (imgContainer && modalImg) {
      if (item.image_url && !item.image_url.includes("favicon") && !item.image_url.endsWith(".ico")) {
        modalImg.src = item.image_url;
        modalImg.alt = item.title;
        imgContainer.style.display = "block";
        imgContainer.classList.remove("hidden");
      } else {
        imgContainer.style.display = "none";
        imgContainer.classList.add("hidden");
        modalImg.src = "";
      }
    }

    // 공식 예매/상세 페이지 다이렉트 URL
    const urlBtn = document.getElementById("modal-url-btn");
    if (urlBtn) {
      urlBtn.href = item.url || "#";
    }

    updateModalBookmarkBtn(item.id);

    // 📱 모바일 뒤로가기 대응: 가상 히스토리 스택 추가
    if (!window.location.hash.includes("detail")) {
      try {
        history.pushState({ modalOpen: true }, "", "#detail");
      } catch (e) {
        console.debug("History pushState skip:", e);
      }
    }

    const modal = document.getElementById("detail-modal");
    if (modal) {
      modal.style.display = "flex";
      modal.classList.remove("hidden");
      modal.classList.add("flex");
      document.body.style.overflow = "hidden";
    }
  } catch (err) {
    console.error("openDetailModal 오류:", err);
  }
}

function openOriginalImage() {
  if (currentModalActivity && currentModalActivity.image_url) {
    window.open(currentModalActivity.image_url, "_blank");
  }
}

function updateModalBookmarkBtn(id) {
  const bookmarks = getBookmarks();
  const isBookmarked = bookmarks.includes(id);
  const btn = document.getElementById("modal-bookmark-btn");
  if (btn) {
    if (isBookmarked) {
      btn.innerHTML = `<i class="fa-solid fa-heart text-rose-500"></i><span class="text-rose-600">찜취소</span>`;
    } else {
      btn.innerHTML = `<i class="fa-regular fa-heart text-rose-500"></i><span>찜하기</span>`;
    }
  }
}

function toggleModalBookmark() {
  if (currentModalActivity) {
    toggleBookmark(currentModalActivity.id);
  }
}

function closeModal() {
  const modal = document.getElementById("detail-modal");
  if (modal) {
    modal.style.display = "none";
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    document.body.style.overflow = "auto";
    
    // URL 해시가 남아있으면 히스토리 되돌리기
    if (window.location.hash.includes("detail")) {
      try {
        history.back();
      } catch (e) {
        // ignore
      }
    }
  }
}

// 📱 스마트폰 뒤로가기(제스처/버튼) 감지하여 모달만 안전하게 닫기
window.addEventListener("popstate", () => {
  const modal = document.getElementById("detail-modal");
  if (modal && modal.style.display !== "none" && !modal.classList.contains("hidden")) {
    modal.style.display = "none";
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    document.body.style.overflow = "auto";
  }
});

// ESC 키 및 배경 클릭 시 모달 닫기
window.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeModal();
  }
});

window.addEventListener("click", (e) => {
  const modal = document.getElementById("detail-modal");
  if (e.target === modal) {
    closeModal();
  }
});
