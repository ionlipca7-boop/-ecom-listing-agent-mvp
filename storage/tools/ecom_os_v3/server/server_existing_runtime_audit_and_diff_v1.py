from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_SERVER_ROOT = Path("/home/ionlipca7/runtime_eco_v1")
ECOM_OS_V3_REL = Path("storage/tools/ecom_os_v3")

PROTECTED_REL_HINTS = [
    ".env",
    "storage/secrets",
    "storage/control_room/CURRENT_POINTER.json",
    "bot.py",
    "ebay_access_token",
    "refresh_token",
    "token_guard",
    ".git",
]

NEW_PACKAGE_REQUIRED = [
    "local_sandbox_runner_v1.py",
    "e2e_virtual_pipeline_v1.py",
    "run_full_local_check_v1.bat",
    "package_audit_v1.py",
    "bootstrap_verify_local_package_v1.py",
    "agents/system_audit_agent_v1.py",
    "agents/teacher_agent_v1.py",
    "agents/image_critic_agent_v1.py",
    "agents/evidence_agent_v1.py",
    "adapters/ebay_dry_run_payload_builder_v1.py",
    "server/server_readonly_cleanup_audit_v1.py",
]

EXPERIMENT_HINTS = [
    "photo_v3",
    "photo_v4",
    "photo_v5",
    "experiment",
    "tmp",
    "temp",
    "rebuild",
]


@dataclass
class DiffItem:
    rel_path: str
    server_exists: bool
    package_exists: bool
    classification: str
    reason: str
    server_sha256: str | None = None
    package_sha256: str | None = None


class ServerExistingRuntimeAuditAndDiffV1:
    """Readonly diff between current server runtime and ECOM OS V3 package.

    It does not delete, copy, move, overwrite, archive, upload, or run live actions.
    It only reports what to keep/add/review.
    """

    def __init__(self, server_root: Path, package_root: Path) -> None:
        self.server_root = server_root.resolve()
        self.package_root = package_root.resolve()

    def run(self, output_path: Path) -> Dict[str, Any]:
        if not self.server_root.exists():
            report = {
                "status": "BLOCKED_SERVER_ROOT_NOT_FOUND",
                "server_root": str(self.server_root),
                "package_root": str(self.package_root),
                "next_allowed_action": "FIX_SERVER_ROOT_PATH",
            }
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            return report

        if not self.package_root.exists():
            report = {
                "status": "BLOCKED_PACKAGE_ROOT_NOT_FOUND",
                "server_root": str(self.server_root),
                "package_root": str(self.package_root),
                "next_allowed_action": "FIX_PACKAGE_PATH",
            }
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            return report

        package_files = [p for p in self.package_root.rglob("*") if p.is_file()]
        diff_items: List[DiffItem] = []

        for p in package_files:
            rel = p.relative_to(self.package_root).as_posix()
            server_p = self.server_root / ECOM_OS_V3_REL / rel
            server_exists = server_p.exists()
            p_hash = self.sha256_file(p)
            s_hash = self.sha256_file(server_p) if server_exists and server_p.is_file() else None

            if server_exists and s_hash == p_hash:
                classification = "ALREADY_PRESENT_SAME"
                reason = "same file already exists on server"
            elif server_exists and s_hash != p_hash:
                classification = "REVIEW_BEFORE_REPLACE"
                reason = "server file exists but differs; do not overwrite without approval"
            else:
                classification = "ADD_NEW_SAFE_BLOCK_CANDIDATE"
                reason = "new ECOM OS V3 file missing on server; candidate for deploy after local PASS"

            diff_items.append(DiffItem(rel, server_exists, True, classification, reason, s_hash, p_hash))

        server_items = self.audit_server_existing()
        protected = [x for x in server_items if x["classification"] == "DO_NOT_TOUCH"]
        cleanup_candidates = [x for x in server_items if x["classification"] == "ARCHIVE_THEN_DELETE_CANDIDATE"]

        counts: Dict[str, int] = {}
        for item in diff_items:
            counts[item.classification] = counts.get(item.classification, 0) + 1

        report = {
            "status": "READONLY_SERVER_DIFF_COMPLETE",
            "layer": "SERVER_EXISTING_RUNTIME_AUDIT_AND_DIFF_V1",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "server_root": str(self.server_root),
            "package_root": str(self.package_root),
            "counts": counts,
            "package_diff": [asdict(x) for x in diff_items],
            "server_existing_summary": {
                "scanned_files": len(server_items),
                "protected_do_not_touch_count": len(protected),
                "archive_then_delete_candidate_count": len(cleanup_candidates),
            },
            "protected_examples": protected[:50],
            "cleanup_candidate_examples": cleanup_candidates[:100],
            "required_package_presence": self.required_package_presence(),
            "hard_rules": [
                "No delete performed.",
                "No copy performed.",
                "No overwrite performed.",
                "No server runtime change performed.",
                "No live eBay action performed.",
                "Deploy only after Windows local PASS and operator approval.",
                "Cleanup only after archive, hash, manifest, and operator approval."
            ],
            "next_allowed_action": "REVIEW_SERVER_DIFF_AND_PREPARE_DEPLOY_MANIFEST",
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report

    def required_package_presence(self) -> Dict[str, bool]:
        return {rel: (self.package_root / rel).exists() for rel in NEW_PACKAGE_REQUIRED}

    def audit_server_existing(self) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for p in self.server_root.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(self.server_root).as_posix()
            rel_low = rel.lower()
            if any(h.lower() in rel_low for h in PROTECTED_REL_HINTS):
                classification = "DO_NOT_TOUCH"
                reason = "protected runtime/secrets/control/token/bot path"
            elif any(h in rel_low for h in EXPERIMENT_HINTS):
                classification = "ARCHIVE_THEN_DELETE_CANDIDATE"
                reason = "old experiment/temp/photo route hint"
            elif "archive" in rel_low or "proof" in rel_low or rel_low.endswith(".zip"):
                classification = "KEEP_FINAL_PROOF"
                reason = "archive/proof file"
            else:
                classification = "KEEP_SERVER_WORKING_OR_REVIEW"
                reason = "server runtime or unknown; keep until reviewed"
            out.append({
                "rel_path": rel,
                "classification": classification,
                "reason": reason,
                "size": p.stat().st_size,
            })
        return out

    def sha256_file(self, path: Path) -> str | None:
        if not path.exists() or not path.is_file():
            return None
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()


def main() -> int:
    server_root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SERVER_ROOT
    package_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd() / ECOM_OS_V3_REL
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else Path.cwd() / "storage/state_control/server_existing_runtime_audit_and_diff_v1.json"

    report = ServerExistingRuntimeAuditAndDiffV1(server_root, package_root).run(output_path)
    compact = {
        "status": report.get("status"),
        "server_root": report.get("server_root"),
        "package_root": report.get("package_root"),
        "counts": report.get("counts"),
        "server_existing_summary": report.get("server_existing_summary"),
        "output_path": str(output_path),
        "next_allowed_action": report.get("next_allowed_action"),
        "no_delete": True,
        "no_copy": True,
        "no_overwrite": True,
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    return 0 if str(report.get("status", "")).startswith("READONLY") else 2


if __name__ == "__main__":
    raise SystemExit(main())
