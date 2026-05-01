@echo off
setlocal
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

echo ===== ECOM_OS_V3_LOCAL_SANDBOX_V1 =====
echo NO_SERVER=YES
echo NO_LIVE_EBAY=YES
echo NO_DELETE=YES

cd /d "%~dp0\..\..\.."

if not exist "storage\tools\ecom_os_v3\local_sandbox_runner_v1.py" (
  echo STATUS=BLOCKED_MISSING_RUNNER
  exit /b 2
)

py "storage\tools\ecom_os_v3\local_sandbox_runner_v1.py" %*
set EXITCODE=%ERRORLEVEL%

echo ===== DONE_LOCAL_SANDBOX_V1_EXIT_%EXITCODE% =====
exit /b %EXITCODE%
