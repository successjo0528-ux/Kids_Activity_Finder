bat_content = """@echo off
cd /d "%~dp0"
python launcher.py
start "" "http://localhost:8080"
"""

with open(r"G:\My Program\Kids_Activity_Finder\run.bat", "wb") as f:
    f.write(bat_content.replace("\n", "\r\n").encode("ascii"))

print("run.bat updated with direct Windows browser open command.")
