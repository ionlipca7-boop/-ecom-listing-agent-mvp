@echo off
cd /d D:\ECOM_LISTING_AGENT_MVP

echo ========================================
echo ECOM LISTING AGENT MVP - QUICK RUN V2
echo ========================================
echo.

echo [1/2] GENERATOR
python generate_ebay_template_output_v2.py
if errorlevel 1 goto :fail

echo.
echo [2/2] VALIDATION
python validate_ebay_template_output_v2.py
if errorlevel 1 goto :fail

echo.
echo ========================================
echo QUICK RUN V2 COMPLETED
echo ========================================
goto :end

:fail
echo.
echo ========================================
echo QUICK RUN V2 FAILED
echo ========================================

:end
pause