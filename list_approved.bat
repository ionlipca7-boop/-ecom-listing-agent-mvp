@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Queue (Approved) ===
python list_queue.py approved
if errorlevel 1 (
  echo.
  echo [ERROR] Approved queue listing failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Approved queue listing completed successfully.
popd
pause
exit /b 0
