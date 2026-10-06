@echo off
chcp 65001 >nul
setlocal DisableDelayedExpansion
cd /d "%~dp0\..\.."
title 无辜实验室 - 上传新 APK
if not exist "%~dp0.venv\Scripts\python.exe" goto missing
if "%~1"=="" goto help
:next
if not exist "%~f1" goto invalid
set "HOSTLAB_UPLOAD_ATTEMPT=0"
:retry
set /a HOSTLAB_UPLOAD_ATTEMPT+=1 >nul
echo.
echo 正在上传："%~nx1"
"%~dp0.venv\Scripts\python.exe" "%~dp0hostlab.py" upload "%~f1"
if not errorlevel 1 goto uploaded
if %HOSTLAB_UPLOAD_ATTEMPT% GEQ 3 goto failed
echo 本次未成功，稍后自动重试。已上传的数据块可继续复用。
timeout /t 5 /nobreak >nul
goto retry
:uploaded
shift
if not "%~1"=="" goto next
echo.
echo 全部处理完成。新样本发布后将请求云端审计。
goto done
:help
echo 将一个或多个 APK 文件拖到本文件上，即可依次上传。
echo 也可以在终端执行：tools\hostlab\hostlab.cmd upload "APK完整路径"
goto done
:missing
echo 运行环境尚未配置，请先执行 setup-client.cmd。
goto done
:invalid
echo 文件不存在，未进行上传。
goto done
:failed
echo 连续三次未完成，请保留窗口中的错误信息。再次拖入同一文件即可重试。
:done
pause
