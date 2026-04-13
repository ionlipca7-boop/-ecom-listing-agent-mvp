@echo off
setlocal

pushd "%~dp0" || (
  echo [ERROR] Failed to open project directory.
  pause
  exit /b 1
)

echo === ECOM Listing Agent: Control Room Status v1 ===
python control_room_status.py
if errorlevel 1 (
  echo.
  echo [ERROR] Control room status failed.
  popd
  pause
  exit /b 1
)

echo.
echo [DONE] Control room status completed successfully.
popd
pause
exit /b 0
