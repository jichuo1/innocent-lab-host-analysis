@echo off
cd /d "%~dp0\..\.."
title HostLab Remote MCP Setup
where python >nul 2>nul
if errorlevel 1 goto missing
where gh >nul 2>nul
if errorlevel 1 goto missing
python -m venv Temp\hf-hostlab-remote-venv
if errorlevel 1 goto done
Temp\hf-hostlab-remote-venv\Scripts\python.exe -m pip install -r tools\hostlab\requirements-remote.txt
if errorlevel 1 goto done
gh auth status >nul 2>nul
if errorlevel 1 gh auth login
if errorlevel 1 goto done
where codex >nul 2>nul
if errorlevel 1 goto manual
codex mcp add hostlab-remote -- "%cd%\Temp\hf-hostlab-remote-venv\Scripts\python.exe" "%cd%\tools\hostlab\remote_mcp.py"
goto done
:missing
echo Install Python and official GitHub CLI first.
goto done
:manual
echo Configure your AI MCP client using the Python environment and remote_mcp.py paths.
:done
pause
