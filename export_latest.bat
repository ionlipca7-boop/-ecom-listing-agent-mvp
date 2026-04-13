@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Export Latest ===
python export_run.py
if errorlevel 1 (
  echo.
  echo [ERROR] Export failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Export completed successfully.
popd
pause
exit /b 0
