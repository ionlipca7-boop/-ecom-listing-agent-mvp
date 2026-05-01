# RUN_WINDOWS_FULL_LOCAL_CHECK_README_V1

## Purpose
Run the full local ECOM OS V3 check on Windows.

## Location
Run in Windows CMD from project root:

`D:\ECOM_LISTING_AGENT_MVP`

## Command

```cmd
cd /d D:\ECOM_LISTING_AGENT_MVP
set PYTHONIOENCODING=utf-8
storage\tools\ecom_os_v3\run_full_local_check_v1.bat
```

## What it runs
1. `package_audit_v1.py`
2. `bootstrap_verify_local_package_v1.py`
3. `e2e_virtual_pipeline_v1.py`

## Expected outputs
- `storage/tools/ecom_os_v3/package_audit_result_v1.json`
- `storage/tools/ecom_os_v3/bootstrap_verify_local_package_result_v1.json`
- `storage/outputs/ecom_os_v3/e2e_virtual/<RUN_ID>/02_e2e_final_report.json`

## Safety
This local check does not use server, live eBay, EPS, or cleanup actions.
