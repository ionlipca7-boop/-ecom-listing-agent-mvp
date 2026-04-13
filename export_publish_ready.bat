@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Export Publish Ready ===
python export_publish_ready.py
if errorlevel 1 (
  echo.
  echo [ERROR] Publish-ready export failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Publish-ready export completed successfully.
popd
pause
exit /b 0
