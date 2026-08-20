@echo off
@chcp 65001 >nul
cd /d "%~dp0"
title GitHub Push (Kids Activity Finder)

echo ========================================================
echo   Kids Activity Finder - GitHub Push
echo ========================================================
echo.
git push -u origin main

echo.
pause
