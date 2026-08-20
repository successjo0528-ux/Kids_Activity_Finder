/**
 * Kids Activity Finder - 메인 프론트엔드 인터랙션 로직
 */

// 전역 상태
let allActivities = [];
let filteredActivities = [];
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
  try {
    const res = await fetch("activities.json?t=" + new Date().getTime());
    if (!res.ok) throw new Error("JSON 파일을 찾을 수 없습니다.");
    allActivities = await res.json();
    applyFilters();
  } catch (err) {
    console.error("데이터 로드 실패:", err);
    document.getElementById("cards-grid").innerHTML = `
      <div class="col-span-full text-center py-12 text-slate-500">
        <p class="text-base font-semibold mb-2">데이터를 불러오는 중입니다...</p>
        <p class="text-xs">PC에서 최초 수집 실행을 하지 않았거나 파일이 없을 수 있습니다.</p>
      </div>
    `;
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
  
  // 렌더링 갱신
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

// 5. 카테고리 칩 선택
function setCategory(category) {
  currentCategory = category;
  document.querySelectorAll("#category-chips .chip").forEach(chip => {
    if (chip.textContent.includes(category) || (category === "전체" && chip.textContent.includes("전체"))) {
      chip.classList.add("active");
    } else {
      chip.classList.remove("active");
    }
  });
  applyFilters();
}

// 6. 뷰 모드 전환
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

// 7. 필터 적용 로직
function applyFilters() {
  const query = document.getElementById("search-input").value.trim().toLowerCase();
  const age = document.getElementById("filter-age").value;
  const region = document.getElementById("filter-region").value;
  const cost = document.getElementById("filter-cost").value;
  const sort = document.getElementById("filter-sort").value;
  const bookmarks = getBookmarks();

  filteredActivities = allActivities.filter(item => {
    // 찜보기 모드
    if (currentView === "bookmarks" && !bookmarks.includes(item.id)) {
      return false;
    }

    // 카테고리 필터
    if (currentCategory !== "전체" && item.category !== currentCategory) {
      return false;
    }

    // 검색어 필터
    if (query) {
      const matchTitle = item.title.toLowerCase().includes(query);
      const matchPlace = item.place_name.toLowerCase().includes(query);
      const matchTags = item.tags.some(t => t.toLowerCase().includes(query));
      const matchDesc = item.description.toLowerCase().includes(query);
      if (!matchTitle && !matchPlace && !matchTags && !matchDesc) return false;
    }

    // 연령 필터
    if (age !== "전체") {
      if (!item.target_age.includes(age) && item.target_age !== "전연령") return false;
    }

    // 지역 필터
    if (region !== "전체") {
      if (!item.region.includes(region) && !item.place_name.includes(region)) return false;
    }

    // 비용 필터
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

  // 개수 갱신
  document.getElementById("total-count").textContent = filteredActivities.length;

  if (currentView === "calendar") {
    renderCalendar();
  } else {
    renderCards();
  }
}

function resetFilters() {
  document.getElementById("search-input").value = "";
  document.getElementById("clear-search").classList.add("hidden");
  document.getElementById("filter-age").value = "전체";
  document.getElementById("filter-region").value = "전체";
  document.getElementById("filter-cost").value = "전체";
  document.getElementById("filter-sort").value = "dday";
  setCategory("전체");
  switchView("cards");
}

// 8. 카드 뷰 렌더링
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
    
    // D-Day 배지 클래스
    let ddayBadgeClass = "badge-dday-normal";
    if (item.d_day === "오늘마감" || item.d_day === "D-1" || item.d_day === "D-2" || item.d_day === "D-3") {
      ddayBadgeClass = "badge-dday-urgent";
    } else if (item.d_day === "마감" || item.d_day === "종료") {
      ddayBadgeClass = "badge-dday-ended";
    }

    // 비용 뱃지
    const isFree = item.cost_type === "무료" || item.cost_type === "참관무료";
    const costBadge = isFree 
      ? `<span class="badge-free px-2 py-0.5 rounded text-[10px] font-bold">${item.cost_type}</span>`
      : `<span class="bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded text-[10px] font-bold">유료</span>`;

    return `
      <div class="activity-card" onclick="openDetailModal('${item.id}')">
        <div>
          <!-- 상단 태그 & 북마크 -->
          <div class="flex items-center justify-between gap-2 mb-2">
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[10px] font-semibold">${item.source_name}</span>
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
              <span class="truncate">${item.event_start ? '행사일: ' + item.event_start : '접수마감: ' + (item.apply_end || '상시')}</span>
            </div>
          </div>
        </div>

        <!-- 카드 하단 D-Day 및 신청 상태 -->
        <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
          <span class="${ddayBadgeClass} px-2.5 py-0.5 rounded-full text-[11px] font-bold">
            ${item.d_day || item.status}
          </span>
          <span class="text-[11px] text-indigo-600 font-semibold flex items-center gap-1">
            상세보기 <i class="fa-solid fa-chevron-right text-[9px]"></i>
          </span>
        </div>
      </div>
    `;
  }).join("");
}

// 9. 캘린더 뷰 렌더링
function renderCalendar() {
  const year = currentCalendarDate.getFullYear();
  const month = currentCalendarDate.getMonth(); // 0-indexed

  document.getElementById("calendar-month-title").textContent = `${year}년 ${month + 1}월`;

  const firstDay = new Date(year, month, 1).getDay();
  const lastDate = new Date(year, month + 1, 0).getDate();
  const todayStr = new Date().toISOString().slice(0, 10);

  const grid = document.getElementById("calendar-days-grid");
  grid.innerHTML = "";

  // 빈 앞칸 채우기
  for (let i = 0; i < firstDay; i++) {
    grid.innerHTML += `<div class="cal-day opacity-30 bg-transparent border-transparent cursor-default"></div>`;
  }

  // 날짜별 행사 매핑
  for (let day = 1; day <= lastDate; day++) {
    const dayStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const isToday = dayStr === todayStr;
    const isSelected = dayStr === selectedCalendarDateStr;

    // 해당 날짜에 마감 또는 행사가 있는 아이템 검색
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
    // 오늘 날짜 기본 선택
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

  titleElem.innerHTML = `<i class="fa-solid fa-calendar-day text-indigo-500"></i> ${dateStr} 일정 (${filteredActivities.filter(item => (item.apply_end||'').slice(0,10) === dateStr || (item.event_start||'').slice(0,10) === dateStr).length}건)`;

  const dayItems = filteredActivities.filter(item => {
    const applyEnd = (item.apply_end || "").slice(0, 10);
    const eventStart = (item.event_start || "").slice(0, 10);
    return applyEnd === dateStr || eventStart === dateStr;
  });

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

// 10. 모달 제어
function openDetailModal(id) {
  const item = allActivities.find(a => a.id === id);
  if (!item) return;

  currentModalActivity = item;
  document.getElementById("modal-category-badge").textContent = item.category;
  document.getElementById("modal-dday-badge").textContent = item.d_day || item.status;
  document.getElementById("modal-cost-badge").textContent = item.cost_type;
  document.getElementById("modal-title").textContent = item.title;
  document.getElementById("modal-place").textContent = item.place_name || item.region;
  document.getElementById("modal-address").textContent = item.address || item.place_name;
  document.getElementById("modal-age").textContent = item.target_age;
  document.getElementById("modal-apply-period").textContent = `${item.apply_start || '상시'} ~ ${item.apply_end || '선착순 마감'}`;
  document.getElementById("modal-event-period").textContent = `${item.event_start || '상세 페이지 참조'} ${item.event_end && item.event_end !== item.event_start ? '~ ' + item.event_end : ''}`;
  document.getElementById("modal-cost-info").textContent = item.cost_info || item.cost_type;
  document.getElementById("modal-description").textContent = item.description || "상세 페이지를 통해 상세한 안내를 확인해 주세요.";

  // 태그 리스트
  const tagsContainer = document.getElementById("modal-tags");
  tagsContainer.innerHTML = (item.tags || []).map(t => `<span class="bg-slate-100 text-slate-600 px-2 py-1 rounded-md text-[11px] font-medium">${t}</span>`).join("");

  // 링크 버튼
  const urlBtn = document.getElementById("modal-url-btn");
  urlBtn.href = item.url || "#";

  updateModalBookmarkBtn(item.id);

  document.getElementById("detail-modal").classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function updateModalBookmarkBtn(id) {
  const bookmarks = getBookmarks();
  const isBookmarked = bookmarks.includes(id);
  const btn = document.getElementById("modal-bookmark-btn");
  if (isBookmarked) {
    btn.innerHTML = `<i class="fa-solid fa-heart text-rose-500"></i><span class="text-rose-600">찜취소</span>`;
  } else {
    btn.innerHTML = `<i class="fa-regular fa-heart text-rose-500"></i><span>찜하기</span>`;
  }
}

function toggleModalBookmark() {
  if (currentModalActivity) {
    toggleBookmark(currentModalActivity.id);
  }
}

function closeModal() {
  document.getElementById("detail-modal").classList.add("hidden");
  document.body.style.overflow = "auto";
}

// 배경 클릭 시 닫기
window.addEventListener("click", (e) => {
  const modal = document.getElementById("detail-modal");
  if (e.target === modal) {
    closeModal();
  }
});
