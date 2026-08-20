push_content = """@echo off
cd /d "%~dp0"
title GitHub Push
echo ========================================================
echo   Pushing latest changes to GitHub...
echo ========================================================
echo.
git push -u origin main
echo.
echo [Done] GitHub push completed!
pause
"""

with open(r"G:\My Program\Kids_Activity_Finder\push_to_github.bat", "wb") as f:
    f.write(push_content.replace("\n", "\r\n").encode("ascii"))

print("push_to_github.bat created successfully.")
