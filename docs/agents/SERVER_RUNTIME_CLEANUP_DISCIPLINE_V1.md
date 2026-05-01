# SERVER_RUNTIME_CLEANUP_DISCIPLINE_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Prevent production server pollution and define a safe cleanup route.

## Core Rule
Do not delete server files directly. Cleanup requires readonly audit, classification, archive, hash verification, manifest, explicit operator approval, deletion, and runtime verification.

## Server Role
Server is production/runtime only:
- Telegram
- eBay
- EPS
- final approved implementation
- readonly verification
- controlled live actions after gate

Server is not:
- experiment sandbox
- V3/V4/V5/V6 playground
- uncontrolled photo generation workspace
- random temp file storage

## Cleanup Route

### 01_READONLY_SERVER_RUNTIME_POLLUTION_AUDIT_V1
Readonly only.

Collect:
- file paths
- sizes
- timestamps
- owner
- relation to V3/V4/V5/photo route
- relation to live runtime
- relation to final proof/archive

No delete.

### 02_CLASSIFY_FILES
Classes:
- KEEP_WORKING_RUNTIME
- KEEP_FINAL_PROOF
- ARCHIVE_THEN_DELETE_CANDIDATE
- DELETE_FORBIDDEN

### 03_CREATE_ARCHIVE_ZIP
Only for ARCHIVE_THEN_DELETE_CANDIDATE.
Archive path must be under controlled archive folder.

### 04_VERIFY_ARCHIVE_HASH
Compute SHA256.
Archive must exist.
Archive size must be greater than zero.
Manifest must list archived files.

### 05_CREATE_CLEANUP_MANIFEST
Manifest must include:
- timestamp
- candidates
- classification reason
- archive path
- sha256
- protected paths
- rollback notes

### 06_OPERATOR_APPROVAL_GATE
No delete before explicit approval.

Required phrase:
`APPROVE_SERVER_CLEANUP_DELETE_CANDIDATES_V1`

### 07_DELETE_CANDIDATES
Delete only paths listed in approved manifest.

Never delete:
- .env
- secrets
- token files
- active bot files
- active eBay runtime wrappers
- storage/control_room/CURRENT_POINTER.json
- final archive proofs
- active state files needed by current route

### 08_POST_CLEANUP_RUNTIME_VERIFY
Verify:
- Telegram runtime still works or service status is unchanged
- eBay token guard path still exists
- current pointer still exists
- final listing proof/archive still exists
- no protected file deleted

## Stop Conditions
- uncertain file role
- archive hash mismatch
- protected path in candidate list
- runtime pointer missing
- operator approval missing
- repeated cleanup error

## Relationship To Marketplace Visual Agent
The MARKETPLACE_VISUAL_LISTING_AGENT_V1 may create experimental assets only in GitHub design/sandbox or a controlled local sandbox.
Production server cleanup is handled only by this discipline.
No photo-agent experiment may create uncontrolled V6/V7/V8 runtime files on server.

## Next Allowed Action
Only after design docs are accepted:
`READONLY_GITHUB_DOC_CREATE_VERIFY_V1`
