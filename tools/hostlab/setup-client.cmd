@echo off
cd /d "%~dp0\..\.."
title Host APK Library - Client Setup
python -m venv Temp\hf-hostlab-venv
if errorlevel 1 goto done
Temp\hf-hostlab-venv\Scripts\python.exe -m pip install -r tools\hostlab\requirements.txt
if errorlevel 1 goto done
Temp\hf-hostlab-venv\Scripts\python.exe tools\hostlab\hostlab.py login
if errorlevel 1 goto done
Temp\hf-hostlab-venv\Scripts\python.exe tools\hostlab\hostlab.py configure innocent-lab-dev/bilibili-host-apks
:done
pause
