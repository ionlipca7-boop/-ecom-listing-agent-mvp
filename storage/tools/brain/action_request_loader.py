"""Safe action request loader for Brain Hard-Gate dry-run V1.

This module validates requested actions before any runtime dispatch.
It is dry-run safe and performs no live calls.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .schemas import ActionRequest, validate_action_request

DEFAULT_ACTION_REQUEST_PATH = Path("storage/state_control/brain_hard_gate_action_request_v1.json")


@dataclass(frozen=True)
class ActionRequestLoadResult:
    status: str
    request_path: str
    request: ActionRequest | None
    errors: list[str]

    @property
    def ok(self) -> bool:
        return self.status == "OK"


def load_action_request_from_dict(data: dict[str, Any]) -> ActionRequestLoadResult:
    """Build and validate ActionRequest from a dictionary."""
    request = ActionRequest.from_dict(data)
    errors = validate_action_request(request)
    if errors:
        return ActionRequestLoadResult(
            status="BLOCK",
            request_path="<inline>",
            request=request,
            errors=errors,
        )
    return ActionRequestLoadResult(
        status="OK",
        request_path="<inline>",
        request=request,
        errors=[],
    )


def load_action_request(root: Path | None = None, request_path: Path | None = None) -> ActionRequestLoadResult:
    """Load action request JSON safely.

    Failure policy:
    - missing file => CHECK_REQUIRED
    - invalid JSON => BLOCK
    - invalid schema => BLOCK
    """
    project_root = root or Path.cwd()
    relative_request_path = request_path or DEFAULT_ACTION_REQUEST_PATH
    full_path = project_root / relative_request_path

    if not full_path.exists():
        return ActionRequestLoadResult(
            status="CHECK_REQUIRED",
            request_path=str(relative_request_path),
            request=None,
            errors=["action_request_file_missing"],
        )

    try:
        raw = full_path.read_text(encoding="utf-8")
    except OSError as exc:
        return ActionRequestLoadResult(
            status="BLOCK",
            request_path=str(relative_request_path),
            request=None,
            errors=[f"action_request_read_error:{exc.__class__.__name__}"],
        )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return ActionRequestLoadResult(
            status="BLOCK",
            request_path=str(relative_request_path),
            request=None,
            errors=["action_request_invalid_json"],
        )

    if not isinstance(data, dict):
        return ActionRequestLoadResult(
            status="BLOCK",
            request_path=str(relative_request_path),
            request=None,
            errors=["action_request_not_object"],
        )

    request = ActionRequest.from_dict(data)
    errors = validate_action_request(request)
    if errors:
        return ActionRequestLoadResult(
            status="BLOCK",
            request_path=str(relative_request_path),
            request=request,
            errors=errors,
        )

    return ActionRequestLoadResult(
        status="OK",
        request_path=str(relative_request_path),
        request=request,
        errors=[],
    )
