@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Inspect Latest ===
python inspect_run.py
if errorlevel 1 (
  echo.
  echo [ERROR] Inspect failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Inspect completed successfully.
popd
pause
exit /b 0
