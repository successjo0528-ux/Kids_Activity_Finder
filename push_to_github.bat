@echo off
chcp 65001 > nul
cd /d "%~dp0"
title GitHub Push - Kids Activity Finder

echo ========================================================
echo   [Kids Activity Finder] GitHub Push and Deploy
echo ========================================================
echo.

git config user.name "successjo0528-ux"
git config user.email "successjo0528@gmail.com"

git branch -M main

git remote remove origin >nul 2>&1
git remote add origin https://github.com/successjo0528-ux/Kids_Activity_Finder.git

echo [*] Staging all files...
git add .

echo [*] Committing changes...
git commit -m "Deploy Kids Activity Finder update and align deployment pipeline with Global Macro Briefing" >nul 2>&1

echo.
echo [*] Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo   [성공] GitHub 업로드 및 배포가 완료되었습니다!
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo   [오류] GitHub 푸시 중 문제가 발생했습니다.
    echo ========================================================
)

echo.
pause
