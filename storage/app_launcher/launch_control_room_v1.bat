@echo off
cd /d D:\ECOM_LISTING_AGENT_MVP
chcp 65001
echo ===== ECOM CONTROL ROOM =====
type storage\exports\ai_system_layer_v1.json
echo.
echo ===== OPEN BUNDLE =====
start "" "D:\ECOM_LISTING_AGENT_MVP\storage\portable_publish_bundles\variant_package_20260415_182127"
echo.
echo ===== OPEN EXPORTS =====
start "" "D:\ECOM_LISTING_AGENT_MVP\storage\exports"
pause
