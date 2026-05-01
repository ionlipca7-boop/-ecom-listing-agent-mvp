from __future__ import annotations

import ast
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[2]

ALLOWED_ROOTS = [
    "agents",
    "adapters",
    "templates",
    "test_inputs",
    "server",
    "workflows",
]

LIVE_FORBIDDEN_PATTERNS = [
    "publishOffer",
    "reviseInventoryStatus",
    "deleteOffer",
    "bulk_update_price_quantity",
    "requests.post(",
    "requests.put(",
    "requests.delete(",
    "api.ebay.com",
    "api.sandbox.ebay.com",
]


@dataclass
class PackageAuditResult:
    status: str
    package_root: str
    python_files: int
    json_files: int
    bat_files: int
    html_files: int
    txt_files: int
    suspicious_files: List[str]
    syntax_errors: List[str]
    live_risk_patterns: List[str]
    recommendations: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def audit_python_syntax(py_files: List[Path]) -> List[str]:
    errors: List[str] = []
    for p in py_files:
        try:
            ast.parse(safe_read(p))
        except SyntaxError as e:
            errors.append(f"{p.relative_to(CURRENT_DIR).as_posix()}: {e}")
    return errors


def scan_live_risks(files: List[Path]) -> List[str]:
    hits: List[str] = []
    for p in files:
        text = safe_read(p)
        for pattern in LIVE_FORBIDDEN_PATTERNS:
            if pattern in text:
                hits.append(f"{p.relative_to(CURRENT_DIR).as_posix()}::{pattern}")
    return hits


def main() -> int:
    all_files = [p for p in CURRENT_DIR.rglob("*") if p.is_file()]
    py_files = [p for p in all_files if p.suffix.lower() == ".py"]
    json_files = [p for p in all_files if p.suffix.lower() == ".json"]
    bat_files = [p for p in all_files if p.suffix.lower() == ".bat"]
    html_files = [p for p in all_files if p.suffix.lower() == ".html"]
    txt_files = [p for p in all_files if p.suffix.lower() == ".txt"]

    suspicious: List[str] = []
    for p in all_files:
        rel = p.relative_to(CURRENT_DIR).as_posix()
        if rel.startswith("__pycache__/") or "/__pycache__/" in rel:
            suspicious.append(rel)
        if p.suffix.lower() in {".log", ".tmp", ".bak"}:
            suspicious.append(rel)

    syntax_errors = audit_python_syntax(py_files)
    live_risks = scan_live_risks(py_files + json_files + txt_files)

    recommendations: List[str] = []
    if syntax_errors:
        recommendations.append("Fix Python syntax errors before Windows run.")
    if live_risks:
        recommendations.append("Review live-risk patterns; local package must stay no-live.")
    if suspicious:
        recommendations.append("Review suspicious/generated files before server deploy.")
    if not syntax_errors and not live_risks:
        recommendations.append("Package syntax and no-live scan are clean for local Windows test.")

    status = "PASS" if not syntax_errors and not live_risks else "BLOCKED"
    result = PackageAuditResult(
        status=status,
        package_root=str(CURRENT_DIR),
        python_files=len(py_files),
        json_files=len(json_files),
        bat_files=len(bat_files),
        html_files=len(html_files),
        txt_files=len(txt_files),
        suspicious_files=suspicious,
        syntax_errors=syntax_errors,
        live_risk_patterns=live_risks,
        recommendations=recommendations,
        next_allowed_action="RUN_BOOTSTRAP_VERIFY_THEN_E2E" if status == "PASS" else "FIX_PACKAGE_AUDIT_BLOCKERS",
    )
    out = CURRENT_DIR / "package_audit_result_v1.json"
    out.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
