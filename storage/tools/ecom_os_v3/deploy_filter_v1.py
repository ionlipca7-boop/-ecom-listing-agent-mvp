from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

CURRENT_DIR = Path(__file__).resolve().parent

DEPLOY_FORBIDDEN_SUFFIXES = {".pyc", ".log", ".tmp", ".bak"}
DEPLOY_FORBIDDEN_PARTS = {"__pycache__", "storage/outputs"}
SECRET_HINTS = {".env", "secret", "token", "credential"}

SAFE_ADD_PREFIXES = [
    "agents/",
    "adapters/",
    "templates/",
    "test_inputs/",
    "server/",
    "workflows/",
]
SAFE_ADD_FILES = {
    "local_sandbox_runner_v1.py",
    "e2e_virtual_pipeline_v1.py",
    "package_audit_v1.py",
    "bootstrap_verify_local_package_v1.py",
    "run_full_local_check_v1.bat",
    "run_local_sandbox_v1.bat",
    "run_e2e_virtual_pipeline_v1.bat",
    "requirements_ecom_os_v3_local.txt",
    "PACKAGE_INDEX_V1.json",
    "MERGE_MANIFEST_TEMPLATE_V1.json",
    "README_LOCAL_SANDBOX_V1.md",
    "RUN_WINDOWS_FULL_LOCAL_CHECK_README_V1.md",
    "RUN_WINDOWS_E2E_VIRTUAL_PIPELINE_CMD_V1.txt",
    "RUN_WINDOWS_LOCAL_SANDBOX_CMD_V1.txt",
}


@dataclass
class DeployFilterItem:
    rel_path: str
    classification: str
    reason: str
    sha256: str | None
    size: int


class DeployFilterV1:
    """Classifies ECOM OS V3 package files for controlled server merge.

    This script does not copy, delete, or modify deployment targets.
    It only writes a deploy filter report.
    """

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def run(self, output_path: Path) -> Dict[str, Any]:
        items: List[DeployFilterItem] = []
        for p in sorted([x for x in self.root.rglob("*") if x.is_file()]):
            rel = p.relative_to(self.root).as_posix()
            classification, reason = self.classify(rel, p)
            items.append(DeployFilterItem(
                rel_path=rel,
                classification=classification,
                reason=reason,
                sha256=self.sha256_file(p),
                size=p.stat().st_size,
            ))

        counts: Dict[str, int] = {}
        for item in items:
            counts[item.classification] = counts.get(item.classification, 0) + 1

        report = {
            "status": "DEPLOY_FILTER_READY",
            "layer": "ECOM_OS_V3_DEPLOY_FILTER_V1",
            "package_root": str(self.root),
            "counts": counts,
            "items": [asdict(x) for x in items],
            "deploy_allowed": [asdict(x) for x in items if x.classification in {"ADD_NEW_SAFE_BLOCK", "REVIEW_SAFE_DOC_OR_CONFIG"}],
            "deploy_forbidden": [asdict(x) for x in items if x.classification == "DEPLOY_FORBIDDEN"],
            "review_required": [asdict(x) for x in items if x.classification == "REVIEW_BEFORE_DEPLOY"],
            "hard_rules": [
                "No copy performed.",
                "No delete performed.",
                "No overwrite performed.",
                "Use this report only after Windows local PASS and server readonly diff."
            ],
            "next_allowed_action": "REVIEW_DEPLOY_FILTER_AND_BUILD_MERGE_MANIFEST",
        }
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({
            "status": report["status"],
            "counts": counts,
            "output_path": str(output_path),
            "next_allowed_action": report["next_allowed_action"],
            "no_copy": True,
            "no_delete": True,
        }, ensure_ascii=False, indent=2))
        return report

    def classify(self, rel: str, path: Path) -> tuple[str, str]:
        parts = set(Path(rel).parts)
        low = rel.lower()
        if any(part in parts for part in DEPLOY_FORBIDDEN_PARTS):
            return "DEPLOY_FORBIDDEN", "generated/cache/output path"
        if path.suffix.lower() in DEPLOY_FORBIDDEN_SUFFIXES:
            return "DEPLOY_FORBIDDEN", "temporary/cache/log suffix"
        if rel == ".env" or any(h in low for h in SECRET_HINTS) and rel != ".env.example":
            return "DEPLOY_FORBIDDEN", "secret/token/credential-like file"
        if rel in SAFE_ADD_FILES or any(rel.startswith(prefix) for prefix in SAFE_ADD_PREFIXES):
            return "ADD_NEW_SAFE_BLOCK", "ECOM OS V3 controlled package file"
        if path.suffix.lower() in {".md", ".txt", ".json"}:
            return "REVIEW_SAFE_DOC_OR_CONFIG", "documentation/config review before deploy"
        return "REVIEW_BEFORE_DEPLOY", "unknown file type or path"

    def sha256_file(self, path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()


def main() -> int:
    output = CURRENT_DIR / "deploy_filter_result_v1.json"
    DeployFilterV1(CURRENT_DIR).run(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
