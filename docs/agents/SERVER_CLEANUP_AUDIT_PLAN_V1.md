# SERVER_CLEANUP_AUDIT_PLAN_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Prepare a safe readonly audit before any server cleanup or production deployment of the new listing agents.

This plan does not delete files. It defines the audit route only.

## Current Reason
Previous photo experiments V3/V4/V5 created temporary runtime files on the production server. The server must be cleaned only after a controlled audit and archive route.

## Hard Rule
No delete without:
1. readonly audit
2. classification
3. archive zip
4. SHA256 verification
5. cleanup manifest
6. explicit operator approval
7. delete only approved candidates
8. runtime verification after cleanup

## Audit Scope
Server production path memory:
- `/home/ionlipca7/runtime_eco_v1`

Expected important runtime areas:
- Telegram bot/runtime
- eBay token guard
- eBay/EPS runtime wrappers
- state_control
- control_room/current pointer
- final proof/archive files
- secrets/env/token files

## Classifications

### KEEP_WORKING_RUNTIME
Files required for active production runtime.

### KEEP_FINAL_PROOF
Final outputs, proofs, archives, checksums, readonly verification outputs.

### ARCHIVE_THEN_DELETE_CANDIDATE
Temporary experiment artifacts that are not needed for runtime after archive.

### DELETE_FORBIDDEN
Never delete:
- `.env`
- secrets
- token files
- active bot files
- active eBay runtime wrappers
- `storage/control_room/CURRENT_POINTER.json`
- final archives/proofs
- files with uncertain role

## Readonly Audit Data To Collect
- path
- file type
- size
- modified time
- hash for important candidates
- relation to V3/V4/V5/photo route
- relation to live runtime
- classification proposal
- reason

## Audit Output
Create readonly report only:

```json
{
  "status": "READONLY_AUDIT_COMPLETE",
  "root": "/home/ionlipca7/runtime_eco_v1",
  "counts": {
    "keep_working_runtime": 0,
    "keep_final_proof": 0,
    "archive_then_delete_candidate": 0,
    "delete_forbidden": 0,
    "uncertain": 0
  },
  "candidates": [],
  "protected_paths": [],
  "next_allowed_action": "REVIEW_CLEANUP_AUDIT_WITH_OPERATOR"
}
```

## Stop Conditions
- server path not found
- current pointer missing
- protected file appears as delete candidate
- classification uncertain
- audit script wants to delete anything

## Next Allowed Action
When operator is at computer:
`READONLY_SERVER_RUNTIME_POLLUTION_AUDIT_V1`

No cleanup/delete yet.
