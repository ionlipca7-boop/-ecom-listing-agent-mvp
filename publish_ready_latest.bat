@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Publish Ready Latest ===
python approval_action.py publish_ready
if errorlevel 1 (
  echo.
  echo [ERROR] Publish-ready action failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Publish-ready action completed successfully.
popd
pause
exit /b 0
