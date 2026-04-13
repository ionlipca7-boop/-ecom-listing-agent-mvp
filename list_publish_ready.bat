@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Queue (Publish Ready) ===
python list_queue.py publish_ready
if errorlevel 1 (
  echo.
  echo [ERROR] Publish-ready queue listing failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Publish-ready queue listing completed successfully.
popd
pause
exit /b 0
