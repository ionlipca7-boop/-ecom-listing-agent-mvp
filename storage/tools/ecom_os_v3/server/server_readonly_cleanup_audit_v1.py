from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


PROTECTED_NAMES = {
    ".env",
    "CURRENT_POINTER.json",
    "ebay_access_token.txt",
    "ebay_refresh_token.txt",
    "bot.py",
}

PROTECTED_PARTS = {
    "storage/secrets",
    "storage/control_room",
    ".git",
}

EXPERIMENT_HINTS = [
    "photo_v3",
    "photo_v4",
    "photo_v5",
    "temp",
    "tmp",
    "rebuild",
    "experiment",
]


@dataclass
class AuditItem:
    path: str
    size: int
    modified_utc: str
    sha256: str | None
    classification: str
    reason: str


class ServerReadonlyCleanupAuditV1:
    """Readonly server runtime pollution audit.

    This script never deletes, moves, archives, uploads, or edits files.
    It only scans and writes a JSON report.
    """

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def run(self, output_path: Path) -> Dict[str, Any]:
        if not self.root.exists():
            return {
                "status": "BLOCKED_ROOT_NOT_FOUND",
                "root": str(self.root),
                "next_allowed_action": "FIX_SERVER_ROOT_PATH",
            }

        items: List[AuditItem] = []
        for p in self.root.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(self.root).as_posix()
            try:
                st = p.stat()
            except OSError:
                continue
            classification, reason = self.classify(rel, p)
            sha = self.sha256_file(p) if st.st_size <= 5_000_000 else None
            items.append(AuditItem(
                path=rel,
                size=st.st_size,
                modified_utc=datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
                sha256=sha,
                classification=classification,
                reason=reason,
            ))

        counts: Dict[str, int] = {}
        for item in items:
            counts[item.classification] = counts.get(item.classification, 0) + 1

        report = {
            "status": "READONLY_AUDIT_COMPLETE",
            "layer": "SERVER_READONLY_CLEANUP_AUDIT_V1",
            "root": str(self.root),
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "counts": counts,
            "items": [asdict(x) for x in items],
            "hard_rules": [
                "No delete performed.",
                "No archive performed.",
                "No runtime changes performed.",
                "Operator approval required before any cleanup."
            ],
            "next_allowed_action": "REVIEW_CLEANUP_AUDIT_WITH_OPERATOR",
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report

    def classify(self, rel: str, path: Path) -> tuple[str, str]:
        rel_low = rel.lower()
        name = path.name
        if name in PROTECTED_NAMES or any(part in rel for part in PROTECTED_PARTS):
            return "DELETE_FORBIDDEN", "protected runtime/control/secrets path"
        if rel_low.endswith((".zip", ".sha256")) or "archive" in rel_low or "proof" in rel_low:
            return "KEEP_FINAL_PROOF", "archive/proof artifact"
        if any(h in rel_low for h in EXPERIMENT_HINTS):
            return "ARCHIVE_THEN_DELETE_CANDIDATE", "experiment/temp/photo route hint"
        if rel_low.endswith((".py", ".json", ".env", ".txt", ".html", ".md")):
            return "KEEP_WORKING_RUNTIME", "normal runtime/source artifact"
        return "UNCERTAIN", "manual review required"

    def sha256_file(self, path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/home/ionlipca7/runtime_eco_v1")
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("server_readonly_cleanup_audit_v1.json")
    report = ServerReadonlyCleanupAuditV1(root).run(output)
    print(json.dumps({
        "status": report.get("status"),
        "root": report.get("root"),
        "output": str(output),
        "counts": report.get("counts"),
        "next_allowed_action": report.get("next_allowed_action"),
        "no_delete": True,
    }, ensure_ascii=False, indent=2))
    return 0 if report.get("status") == "READONLY_AUDIT_COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
