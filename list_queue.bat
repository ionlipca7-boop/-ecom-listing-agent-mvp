@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Control Room Queue ===
python list_queue.py
if errorlevel 1 (
  echo.
  echo [ERROR] Queue listing failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Queue listing completed successfully.
popd
pause
exit /b 0
