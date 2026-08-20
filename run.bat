@echo off
chcp 65001 > nul
title Kids Activity Finder (어린이 체험·대회 통합 탐색기)

echo ========================================================
echo   🎈 Kids Activity Finder - 성남 키즈체험 및 대회 탐색기
echo ========================================================
echo.
echo [1/2] 최신 성남시 도서관, 박물관, 스포츠대회 정보 크롤링 중...
python crawler_runner.py

echo.
echo [2/2] 웹 뷰어 서버를 실행합니다...
python local_server.py

pause
