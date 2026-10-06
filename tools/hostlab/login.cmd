@echo off
cd /d "%~dp0\..\.."
title Hugging Face Host APK Library - Login
echo Paste your dedicated Hugging Face token below. Input is hidden.
echo Never send the token to chat.
tools\hostlab\.venv\Scripts\python.exe tools\hostlab\hostlab.py login
if errorlevel 1 goto done
tools\hostlab\.venv\Scripts\python.exe tools\hostlab\hostlab.py configure innocent-lab-dev/bilibili-host-apks
:done
pause
