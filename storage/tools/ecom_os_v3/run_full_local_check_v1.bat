@echo off
setlocal
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

echo ===== ECOM_OS_V3_FULL_LOCAL_CHECK_V4 =====
echo NO_SERVER=YES
echo NO_LIVE_EBAY=YES
echo NO_DELETE=YES
echo NO_EPS=YES
echo NO_AUTO_REORDER=YES

cd /d "%~dp0\..\..\.."

echo ----- STEP 0: CONTROL ORCHESTRATOR -----
py "storage\tools\ecom_os_v3\agents\control_orchestrator_agent_v1.py" WINDOWS_LOCAL
if errorlevel 1 goto :blocked

echo ----- STEP 1: SECURITY SECRETS GUARD -----
py "storage\tools\ecom_os_v3\agents\security_secrets_guard_agent_v1.py" "storage\tools\ecom_os_v3"
if errorlevel 1 goto :blocked

echo ----- STEP 2: PACKAGE AUDIT -----
py "storage\tools\ecom_os_v3\package_audit_v1.py"
if errorlevel 1 goto :blocked

echo ----- STEP 3: BOOTSTRAP VERIFY -----
py "storage\tools\ecom_os_v3\bootstrap_verify_local_package_v1.py"
if errorlevel 1 goto :blocked

echo ----- STEP 4: E2E LISTING PIPELINE -----
py "storage\tools\ecom_os_v3\e2e_virtual_pipeline_v1.py"
if errorlevel 1 goto :blocked

echo ----- STEP 5: PORTFOLIO STRATEGY PIPELINE -----
py "storage\tools\ecom_os_v3\portfolio_strategy_runner_v1.py"
if errorlevel 1 goto :blocked

echo ----- SHOW OUTPUTS -----
if exist "storage\outputs\ecom_os_v3\e2e_virtual" dir "storage\outputs\ecom_os_v3\e2e_virtual" /ad /o-d
if exist "storage\outputs\ecom_os_v3\local_sandbox" dir "storage\outputs\ecom_os_v3\local_sandbox" /ad /o-d
if exist "storage\outputs\ecom_os_v3\portfolio_strategy" dir "storage\outputs\ecom_os_v3\portfolio_strategy" /ad /o-d

echo ===== FINISH_ECOM_OS_V3_FULL_LOCAL_CHECK_V4_PASS_STOP =====
exit /b 0

:blocked
echo ===== BLOCKED_ECOM_OS_V3_FULL_LOCAL_CHECK_V4_STOP =====
exit /b 2
