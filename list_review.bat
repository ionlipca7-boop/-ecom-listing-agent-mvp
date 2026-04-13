@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Queue (Review) ===
python list_queue.py review
if errorlevel 1 (
  echo.
  echo [ERROR] Review queue listing failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Review queue listing completed successfully.
popd
pause
exit /b 0
