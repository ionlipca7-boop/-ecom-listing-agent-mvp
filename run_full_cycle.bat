@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Full Cycle ===
set /p PRODUCT_INPUT=Enter product input: 

if "%PRODUCT_INPUT%"=="" (
  echo [ERROR] Product input cannot be empty.
  popd
  pause
  exit /b 1
)

echo.
echo [1/3] Running listing pipeline...
python run_listing_pipeline.py "%PRODUCT_INPUT%"
if errorlevel 1 goto :fail

echo.
echo [2/3] Inspecting latest run...
python inspect_run.py
if errorlevel 1 goto :fail

echo.
echo [3/3] Exporting latest run...
python export_run.py
if errorlevel 1 goto :fail

echo.
echo [DONE] Full cycle completed successfully.
popd
pause
exit /b 0

:fail
echo.
echo [ERROR] Full cycle stopped due to a command failure.
popd
pause
exit /b 1
