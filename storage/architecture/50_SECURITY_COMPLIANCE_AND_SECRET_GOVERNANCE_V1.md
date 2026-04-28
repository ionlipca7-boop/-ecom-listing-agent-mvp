# 50_SECURITY_COMPLIANCE_AND_SECRET_GOVERNANCE_V1

Status: SECURITY_SECRET_GOVERNANCE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define security, compliance, and secret governance for ECOM OS.

## External practice alignment
This strategy follows:
- OWASP Secrets Management;
- OWASP secure logging;
- GitHub secret scanning / push protection;
- least privilege;
- credential lifecycle management;
- audit-safe security events.

## Core decision
Secrets are runtime assets, not source code assets.

Forbidden:
```text
secret -> GitHub commit
secret -> architecture doc
secret -> Telegram message
secret -> audit log plaintext
```

## Secret locations
Allowed:
- server runtime .env or managed secret store;
- protected local secret storage;
- GitHub environment secrets only with protection rules.

Forbidden:
- source files;
- architecture docs;
- screenshots;
- Telegram chat;
- public logs;
- state_control JSON plaintext.

## Secret lifecycle
Every secret should support:
- creation;
- rotation;
- revocation;
- expiration;
- audit of access/use;
- incident response.

## Access model
Use least privilege:
- Brain dry-run: no secrets;
- GitHub audit: no secrets;
- local engineering: no live secrets by default;
- server runtime: runtime secrets only;
- Telegram interface: no secret display.

## Logging rules
Logs/audits must not include:
- access tokens;
- refresh tokens;
- client secrets;
- API keys;
- Authorization headers;
- passwords.

Sensitive values must be redacted.

## Push protection
Enable/expect GitHub secret scanning and push protection where available.

If a secret is detected:
1. stop commit/merge;
2. remove secret;
3. rotate/revoke exposed credential;
4. record incident;
5. verify no audit/log leak remains.

## Compliance posture
System should preserve:
- action audit trails;
- approval history;
- finance event traces;
- inventory event traces;
- marketplace verification records.

## STOP conditions
STOP if:
- secret appears in code/log/doc;
- environment credential is over-privileged;
- audit contains plaintext token;
- live credential is required for dry-run;
- secret rotation path is unclear.

STOP: This document defines security/secret governance only. It does not access or modify secrets.
