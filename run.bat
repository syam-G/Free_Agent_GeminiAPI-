@echo off
chcp 65001 >nul
title Funny AI Agent CLI
color 0B
cls

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

python main.py
pause
