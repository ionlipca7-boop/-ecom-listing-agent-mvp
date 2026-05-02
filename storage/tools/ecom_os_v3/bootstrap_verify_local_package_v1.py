from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[2]

REQUIRED_FILES = [
    "local_sandbox_runner_v1.py",
    "e2e_virtual_pipeline_v1.py",
    "portfolio_strategy_runner_v1.py",
    "package_audit_v1.py",
    "deploy_filter_v1.py",
    "bootstrap_verify_local_package_v1.py",
    "run_local_sandbox_v1.bat",
    "run_e2e_virtual_pipeline_v1.bat",
    "run_full_local_check_v1.bat",
    "PACKAGE_INDEX_V1.json",
    "PACKAGE_INDEX_V2.json",
    "PACKAGE_INDEX_V3.json",
    "MERGE_MANIFEST_TEMPLATE_V1.json",
    "README_LOCAL_SANDBOX_V1.md",
    "RUN_WINDOWS_LOCAL_SANDBOX_CMD_V1.txt",
    "RUN_WINDOWS_E2E_VIRTUAL_PIPELINE_CMD_V1.txt",
    "RUN_WINDOWS_FULL_LOCAL_CHECK_README_V1.md",
    "requirements_ecom_os_v3_local.txt",
    ".env.example",
    "state_handoff_schema_v1.json",
    "test_inputs/usb_c_cable_stand_v1.json",
    "test_inputs/usb_adapter_6pcs_v1.json",
    "test_inputs/sample_portfolio_v1.json",
    "agents/url_intake_agent_v1.py",
    "agents/product_passport_agent_v1.py",
    "agents/evidence_agent_v1.py",
    "agents/marketplace_rules_agent_v1.py",
    "agents/photo_blueprint_agent_v1.py",
    "agents/image_critic_agent_v1.py",
    "agents/title_agent_v1.py",
    "agents/item_specifics_agent_v1.py",
    "agents/html_agent_v1.py",
    "agents/critic_agent_v1.py",
    "agents/teacher_agent_v1.py",
    "agents/system_audit_agent_v1.py",
    "agents/security_secrets_guard_agent_v1.py",
    "agents/marketplace_access_gate_agent_v1.py",
    "agents/archive_package_agent_v1.py",
    "agents/cleanup_archivist_agent_v1.py",
    "agents/price_competition_agent_v1.py",
    "agents/listing_lifecycle_agent_v1.py",
    "agents/promotion_offers_agent_v1.py",
    "agents/cross_sell_bundle_agent_v1.py",
    "agents/listing_health_dashboard_agent_v1.py",
    "agents/variation_agent_v1.py",
    "agents/inventory_reorder_agent_v1.py",
    "adapters/image_generation_adapter_v1.py",
    "adapters/canva_template_adapter_v1.py",
    "adapters/telegram_preview_adapter_v1.py",
    "adapters/ebay_dry_run_payload_builder_v1.py",
    "adapters/ebay_token_preflight_guard_v1.py",
    "templates/ebay_description_template_v1.html",
    "server/server_readonly_cleanup_audit_v1.py",
    "server/server_existing_runtime_audit_and_diff_v1.py",
    "workflows/n8n_listing_pipeline_v1.json",
]


@dataclass
class BootstrapVerifyResult:
    status: str
    project_root: str
    package_root: str
    python_version: str
    missing_files: List[str]
    present_files_count: int
    required_files_count: int
    safety: Dict[str, bool]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def main() -> int:
    missing = []
    for rel in REQUIRED_FILES:
        if not (CURRENT_DIR / rel).exists():
            missing.append(rel)

    result = BootstrapVerifyResult(
        status="PASS" if not missing else "BLOCKED_MISSING_FILES",
        project_root=str(PROJECT_ROOT),
        package_root=str(CURRENT_DIR),
        python_version=sys.version.split()[0],
        missing_files=missing,
        present_files_count=len(REQUIRED_FILES) - len(missing),
        required_files_count=len(REQUIRED_FILES),
        safety={
            "no_server": True,
            "no_live_ebay": True,
            "no_delete": True,
            "no_eps": True,
            "no_auto_reorder": True,
            "security_guard_required": True,
            "marketplace_access_gate_required_before_live": True,
        },
        next_allowed_action="RUN_FULL_LOCAL_CHECK_V1" if not missing else "FIX_MISSING_FILES",
    )
    out = CURRENT_DIR / "bootstrap_verify_local_package_result_v1.json"
    out.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if result.status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
