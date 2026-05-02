# NEXT_WINDOWS_STAGE_PLAN_V1

## Status
NEXT_ALLOWED_ACTION_READY

## Goal
Run the ECOM OS V3 local package on Windows and verify what works before touching server runtime.

## Environment
WINDOWS CMD

Project path:

```cmd
D:\ECOM_LISTING_AGENT_MVP
```

## Step 1 — Pull / Sync GitHub
Make sure Windows project has the latest GitHub files.

Do not edit server. Do not run live eBay.

## Step 2 — Run Full Local Check

```cmd
cd /d D:\ECOM_LISTING_AGENT_MVP
set PYTHONIOENCODING=utf-8
storage\tools\ecom_os_v3\run_full_local_check_v1.bat
```

## Step 3 — Send Back Results
Send the full CMD output and these files:

```text
storage\tools\ecom_os_v3\package_audit_result_v1.json
storage\tools\ecom_os_v3\bootstrap_verify_local_package_result_v1.json
storage\outputs\ecom_os_v3\e2e_virtual\<LATEST_RUN_ID>\02_e2e_final_report.json
storage\outputs\ecom_os_v3\portfolio_strategy\<LATEST_RUN_ID>\07_portfolio_strategy_summary.json
```

## Step 4 — Interpret Results
If PASS:
- prepare server readonly diff audit
- build merge manifest
- deploy only approved clean blocks later

If BLOCKED:
- fix only exact blockers
- rerun full local check

## Step 5 — Server Later Only
Server comes after Windows PASS.

Server route:
1. readonly server diff
2. classify keep/add/review/do-not-touch
3. merge manifest
4. operator approval
5. deploy approved only
6. verify runtime

## Hard Stops
- no server before Windows PASS
- no eBay live before gate
- no delete without cleanup gate
- no secrets committed
- no blind overwrite of working server runtime

## Next Allowed Action
`RUN_WINDOWS_FULL_LOCAL_CHECK_V1`
