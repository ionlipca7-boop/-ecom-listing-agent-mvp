from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class OrchestratorStep:
    step: str
    agent_or_runner: str
    purpose: str
    required_status: str
    next_if_pass: str
    next_if_blocked: str


@dataclass
class ControlOrchestratorResult:
    status: str
    route_id: str
    current_stage: str
    steps: List[Dict[str, Any]]
    gates: List[str]
    blocked_reasons: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ControlOrchestratorAgentV1:
    """Single brain for ECOM OS V3 route control.

    It does not generate images, publish, revise, delete, or deploy by itself.
    It defines the safe order of agents/runners and blocks unsafe jumps.
    """

    def run(self, route_id: str = "ECOM_OS_V3_DEFAULT", current_stage: str = "WINDOWS_LOCAL") -> ControlOrchestratorResult:
        steps = [
            OrchestratorStep("A0", "SecuritySecretsGuardAgent", "scan package for secret-like values", "PASS", "A1", "STOP_FIX_SECRETS"),
            OrchestratorStep("A1", "PackageAudit", "syntax and no-live scan", "PASS", "A2", "STOP_FIX_PACKAGE"),
            OrchestratorStep("A2", "BootstrapVerify", "verify required files exist", "PASS", "B1", "STOP_FIX_MISSING_FILES"),
            OrchestratorStep("B1", "E2EVirtualPipeline", "run two-product listing creation route", "FINISH_STOP", "B2", "STOP_FIX_E2E"),
            OrchestratorStep("B2", "PortfolioStrategyRunner", "run post-listing lifecycle strategy", "PASS", "C1", "STOP_FIX_PORTFOLIO"),
            OrchestratorStep("C1", "ServerExistingRuntimeAuditAndDiff", "readonly server diff after Windows PASS", "READONLY_SERVER_DIFF_COMPLETE", "C2", "STOP_REVIEW_SERVER_DIFF"),
            OrchestratorStep("C2", "DeployFilter", "filter clean deploy package", "DEPLOY_FILTER_READY", "C3", "STOP_FIX_DEPLOY_FILTER"),
            OrchestratorStep("C3", "MergeManifest", "prepare operator-reviewed merge plan", "REVIEW_READY", "D1", "STOP_REVIEW_MERGE"),
            OrchestratorStep("D1", "MarketplaceAccessGate", "token/security/live-scope gate", "PASS_MARKETPLACE_ACCESS_OPEN", "LIVE_GATE", "STOP_FIX_ACCESS_GATE"),
        ]
        gates = [
            "no_server_before_windows_pass",
            "no_live_ebay_before_access_gate",
            "no_delete_without_cleanup_gate",
            "no_secret_commit",
            "no_blind_overwrite_server_runtime",
            "human_visual_review_before_photo_live_update",
        ]
        blocked: List[str] = []
        if current_stage not in {"WINDOWS_LOCAL", "SERVER_READONLY", "MERGE_REVIEW", "LIVE_GATE"}:
            blocked.append("unknown_current_stage")
        status = "PASS" if not blocked else "BLOCKED"
        return ControlOrchestratorResult(
            status=status,
            route_id=route_id,
            current_stage=current_stage,
            steps=[asdict(s) for s in steps],
            gates=gates,
            blocked_reasons=blocked,
            next_allowed_action="RUN_FULL_LOCAL_CHECK_V1" if status == "PASS" else "FIX_ORCHESTRATOR_STAGE",
        )


def main() -> int:
    current_stage = sys.argv[1] if len(sys.argv) > 1 else "WINDOWS_LOCAL"
    package_root = Path(__file__).resolve().parents[1]
    result = ControlOrchestratorAgentV1().run(current_stage=current_stage).to_dict()
    out = package_root / "control_orchestrator_result_v1.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
