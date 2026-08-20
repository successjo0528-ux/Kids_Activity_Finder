@echo off
cd /d "%~dp0"
title GitHub Force Push
echo ========================================================
echo   Pushing ALL latest changes to GitHub (Force Sync)...
echo ========================================================
echo.
git push -f origin main
echo.
echo ========================================================
echo   [Done] Finished! Check above output.
echo ========================================================
pause
