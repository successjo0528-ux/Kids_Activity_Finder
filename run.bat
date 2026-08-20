@echo off
cd /d "%~dp0"
python launcher.py
start "" "http://localhost:8080"
