@echo off
setlocal
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

echo ===== ECOM_OS_V3_E2E_VIRTUAL_PIPELINE_V1 =====
echo NO_SERVER=YES
echo NO_LIVE_EBAY=YES
echo NO_DELETE=YES
echo NO_EPS=YES

cd /d "%~dp0\..\..\.."

if not exist "storage\tools\ecom_os_v3\e2e_virtual_pipeline_v1.py" (
  echo STATUS=BLOCKED_MISSING_E2E_RUNNER
  exit /b 2
)

py "storage\tools\ecom_os_v3\e2e_virtual_pipeline_v1.py"
set EXITCODE=%ERRORLEVEL%

echo ===== DONE_ECOM_OS_V3_E2E_VIRTUAL_PIPELINE_V1_EXIT_%EXITCODE% =====
exit /b %EXITCODE%
