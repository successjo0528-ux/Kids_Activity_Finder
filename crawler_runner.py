import sys
import os
import io
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Windows 콘솔 UTF-8 출력 보정
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers import ALL_SCRAPERS
from core.storage import save_activities, load_activities
from core.models import ActivityItem


def run_single_scraper(scraper_cls):
    """단일 스크래퍼 인스턴스화 및 실행"""
    try:
        scraper = scraper_cls()
        start = time.time()
        results = scraper.scrape()
        elapsed = time.time() - start
        print(f"[OK] [{scraper.name}] 수집 성공: {len(results)}건 ({elapsed:.2f}초)")
        return results
    except Exception as e:
        print(f"[FAIL] [{scraper_cls.__name__}] 수집 실패: {e}")
        return []


def run_all_crawlers(parallel: bool = False):
    """모든 등록된 스크래퍼 실행 및 데이터 저장 (403 차단 방지를 위한 순차 안전 수집)"""
    print("=" * 60)
    print("[Kids_Activity_Finder] 통합 크롤러 엔진 가동 시작")
    print(f"[*] 대상 채널 수: {len(ALL_SCRAPERS)}개")
    print("=" * 60)

    all_collected_items = []

    if parallel:
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_scraper = {executor.submit(run_single_scraper, cls): cls for cls in ALL_SCRAPERS}
            for future in as_completed(future_to_scraper):
                items = future.result()
                all_collected_items.extend(items)
    else:
        for cls in ALL_SCRAPERS:
            items = run_single_scraper(cls)
            all_collected_items.extend(items)
            time.sleep(0.5)  # 채널 간 안전 대기

    print("-" * 60)
    total_saved = save_activities(all_collected_items)
    print(f"[완료] 모든 수집 완료! 총 {total_saved}개의 활동 데이터가 data/ 및 web/ 폴더에 동기화되었습니다.")
    print("=" * 60)
    return total_saved


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kids Activity Finder Crawler Runner")
    parser.add_argument("--sync", action="store_true", help="순차 동기식 실행")
    args = parser.parse_args()

    run_all_crawlers(parallel=not args.sync)
