@echo off
setlocal
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

echo ===== ECOM_OS_V3_FULL_LOCAL_CHECK_V1 =====
echo NO_SERVER=YES
echo NO_LIVE_EBAY=YES
echo NO_DELETE=YES
echo NO_EPS=YES

cd /d "%~dp0\..\..\.."

echo ----- STEP 1: PACKAGE AUDIT -----
py "storage\tools\ecom_os_v3\package_audit_v1.py"
if errorlevel 1 goto :blocked

echo ----- STEP 2: BOOTSTRAP VERIFY -----
py "storage\tools\ecom_os_v3\bootstrap_verify_local_package_v1.py"
if errorlevel 1 goto :blocked

echo ----- STEP 3: E2E VIRTUAL PIPELINE -----
py "storage\tools\ecom_os_v3\e2e_virtual_pipeline_v1.py"
if errorlevel 1 goto :blocked

echo ----- SHOW OUTPUTS -----
if exist "storage\outputs\ecom_os_v3\e2e_virtual" dir "storage\outputs\ecom_os_v3\e2e_virtual" /ad /o-d
if exist "storage\outputs\ecom_os_v3\local_sandbox" dir "storage\outputs\ecom_os_v3\local_sandbox" /ad /o-d

echo ===== FINISH_ECOM_OS_V3_FULL_LOCAL_CHECK_V1_PASS_STOP =====
exit /b 0

:blocked
echo ===== BLOCKED_ECOM_OS_V3_FULL_LOCAL_CHECK_V1_STOP =====
exit /b 2
