push_content = """@echo off
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
"""

with open(r"G:\My Program\Kids_Activity_Finder\push_to_github.bat", "wb") as f:
    f.write(push_content.replace("\n", "\r\n").encode("ascii"))

print("push_to_github.bat updated with -f flag.")
