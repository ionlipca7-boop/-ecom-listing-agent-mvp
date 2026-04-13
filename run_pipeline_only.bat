@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Pipeline Only ===
set /p PRODUCT_INPUT=Enter product input: 

if "%PRODUCT_INPUT%"=="" (
  echo [ERROR] Product input cannot be empty.
  popd
  pause
  exit /b 1
)

echo.
echo Running listing pipeline...
python run_listing_pipeline.py "%PRODUCT_INPUT%"
if errorlevel 1 (
  echo.
  echo [ERROR] Pipeline failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Pipeline completed successfully.
popd
pause
exit /b 0
