@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Approve Latest ===
python approval_action.py approve
if errorlevel 1 (
  echo.
  echo [ERROR] Approve action failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Approve action completed successfully.
popd
pause
exit /b 0
