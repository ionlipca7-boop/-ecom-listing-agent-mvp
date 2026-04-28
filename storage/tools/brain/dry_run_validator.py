"""Dry-run validator for Brain Hard-Gate V1.

This validator executes deterministic test cases against the Brain Hard-Gate.
It must not call marketplace APIs, server runtime, secrets, inventory mutation,
or any live adapter.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .brain_hard_gate import evaluate_action

DEFAULT_DRY_RUN_RESULT_PATH = Path("storage/state_control/brain_hard_gate_dry_run_result_v1.json")


@dataclass(frozen=True)
class DryRunCaseResult:
    name: str
    expected_status: str
    actual_status: str
    passed: bool
    reason: str


@dataclass(frozen=True)
class DryRunSummary:
    total: int
    passed: int
    failed: int
    live_called: bool = False
    server_touched: bool = False
    publish_called: bool = False


def _write_result(root: Path, result: dict[str, Any], output_path: Path | None = None) -> Path:
    relative_output_path = output_path or DEFAULT_DRY_RUN_RESULT_PATH
    full_path = root / relative_output_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return full_path


def _ensure_pointer(root: Path, next_allowed_action: str) -> None:
    pointer_path = root / "storage/control_room/CURRENT_POINTER.json"
    pointer_path.parent.mkdir(parents=True, exist_ok=True)
    pointer_path.write_text(
        json.dumps(
            {
                "status": "OK",
                "current_position": "brain_hard_gate_dry_run_v1",
                "next_allowed_action": next_allowed_action,
                "last_confirmed_layer": "BRAIN_HARD_GATE_DRY_RUN_SETUP_V1",
                "publish_allowed": False,
                "revise_allowed": False,
                "delete_allowed": False,
                "auto_publish_allowed": False,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def run_dry_run(root: Path | None = None) -> dict[str, Any]:
    """Run Brain Hard-Gate dry-run test cases.

    The function creates a temporary safe pointer state inside the provided root.
    Use a temp root in tests to avoid overwriting real project pointer.
    """
    project_root = root or Path.cwd()

    cases: list[DryRunCaseResult] = []

    # Case 1: safe read-only allowed when route matches.
    _ensure_pointer(project_root, "verify_pointer_state_v1")
    decision = evaluate_action(
        {
            "requested_action": "verify_pointer_state_v1",
            "requested_by": "operator",
            "environment": "LOCAL_WINDOWS",
            "target_module": "brain_orchestrator",
            "risk_level": "read_only",
            "approval_reference": None,
            "requires_verification": False,
        },
        root=project_root,
        dry_run=True,
    )
    cases.append(
        DryRunCaseResult(
            name="safe_read_only_matching_route",
            expected_status="ALLOW",
            actual_status=decision.status,
            passed=decision.status == "ALLOW" and not decision.live_called and not decision.server_touched and not decision.publish_called,
            reason=decision.reason,
        )
    )

    # Case 2: publish-like action from Telegram without approval is blocked before any live call.
    _ensure_pointer(project_root, "publish_offer_v1")
    decision = evaluate_action(
        {
            "requested_action": "publish_offer_v1",
            "requested_by": "telegram",
            "environment": "TELEGRAM_INTERFACE",
            "target_module": "ebay_adapter_live",
            "risk_level": "live",
            "approval_reference": None,
            "requires_verification": True,
        },
        root=project_root,
        dry_run=True,
    )
    cases.append(
        DryRunCaseResult(
            name="telegram_publish_without_approval_blocked",
            expected_status="BLOCK",
            actual_status=decision.status,
            passed=decision.status == "BLOCK" and not decision.live_called and not decision.server_touched and not decision.publish_called,
            reason=decision.reason,
        )
    )

    # Case 3: server action from GitHub audit is blocked.
    _ensure_pointer(project_root, "server_runtime_restart_v1")
    decision = evaluate_action(
        {
            "requested_action": "server_runtime_restart_v1",
            "requested_by": "operator",
            "environment": "GITHUB_AUDIT",
            "target_module": "server_runtime",
            "risk_level": "dangerous",
            "approval_reference": None,
            "requires_verification": True,
        },
        root=project_root,
        dry_run=True,
    )
    cases.append(
        DryRunCaseResult(
            name="github_audit_server_action_blocked",
            expected_status="BLOCK",
            actual_status=decision.status,
            passed=decision.status == "BLOCK" and not decision.live_called and not decision.server_touched and not decision.publish_called,
            reason=decision.reason,
        )
    )

    # Case 4: approved live-like server action remains dry-run only and requires verification.
    _ensure_pointer(project_root, "publish_offer_v1")
    decision = evaluate_action(
        {
            "requested_action": "publish_offer_v1",
            "requested_by": "operator",
            "environment": "SERVER_RUNTIME",
            "target_module": "ebay_adapter",
            "risk_level": "live",
            "approval_reference": "approved_test_reference_only",
            "requires_verification": True,
        },
        approval_data={
            "status": "APPROVED",
            "approved_action": "publish_offer_v1",
            "approval_scope": "one_live_action",
            "approved_by": "operator",
            "approval_source": "dry_run_test",
            "expires_at": "",
            "single_use": True,
            "used": False,
        },
        root=project_root,
        dry_run=True,
    )
    cases.append(
        DryRunCaseResult(
            name="approved_live_action_dry_run_only",
            expected_status="ALLOW_DRY_RUN_ONLY",
            actual_status=decision.status,
            passed=decision.status == "ALLOW_DRY_RUN_ONLY" and not decision.live_called and not decision.server_touched and not decision.publish_called,
            reason=decision.reason,
        )
    )

    passed_count = sum(1 for case in cases if case.passed)
    failed_count = len(cases) - passed_count
    summary = DryRunSummary(total=len(cases), passed=passed_count, failed=failed_count)

    result = {
        "status": "PASS" if failed_count == 0 else "FAIL",
        "layer": "BRAIN_HARD_GATE_DRY_RUN_VALIDATOR_V1",
        "test_cases": [asdict(case) for case in cases],
        "summary": asdict(summary),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    output_path = _write_result(project_root, result)
    result["output_path"] = str(output_path)
    return result


if __name__ == "__main__":
    print(json.dumps(run_dry_run(), ensure_ascii=False, indent=2))
