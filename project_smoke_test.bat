@echo off
setlocal

python project_integrity_audit.py
if errorlevel 1 exit /b 1

python control_room_summary.py
if errorlevel 1 exit /b 1

call run_control_room.bat
if errorlevel 1 exit /b 1

exit /b 0
