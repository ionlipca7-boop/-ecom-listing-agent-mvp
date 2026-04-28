"""Safe CURRENT_POINTER loader for Brain Hard-Gate dry-run V1.

The loader is read-only. It never mutates project state and never calls live runtime.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_POINTER_PATH = Path("storage/control_room/CURRENT_POINTER.json")


@dataclass(frozen=True)
class PointerLoadResult:
    status: str
    pointer_path: str
    data: dict[str, Any]
    errors: list[str]

    @property
    def ok(self) -> bool:
        return self.status == "OK"

    @property
    def next_allowed_action(self) -> str:
        return str(self.data.get("next_allowed_action", "")).strip()

    @property
    def current_position(self) -> str:
        return str(self.data.get("current_position", "")).strip()


def load_pointer(root: Path | None = None, pointer_path: Path | None = None) -> PointerLoadResult:
    """Load CURRENT_POINTER.json safely.

    Failure policy:
    - missing file => CHECK_REQUIRED
    - invalid JSON => BLOCK
    - missing next_allowed_action => CHECK_REQUIRED
    """
    project_root = root or Path.cwd()
    relative_pointer_path = pointer_path or DEFAULT_POINTER_PATH
    full_path = project_root / relative_pointer_path

    if not full_path.exists():
        return PointerLoadResult(
            status="CHECK_REQUIRED",
            pointer_path=str(relative_pointer_path),
            data={},
            errors=["pointer_file_missing"],
        )

    try:
        raw = full_path.read_text(encoding="utf-8")
    except OSError as exc:
        return PointerLoadResult(
            status="BLOCK",
            pointer_path=str(relative_pointer_path),
            data={},
            errors=[f"pointer_read_error:{exc.__class__.__name__}"],
        )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return PointerLoadResult(
            status="BLOCK",
            pointer_path=str(relative_pointer_path),
            data={},
            errors=["pointer_invalid_json"],
        )

    if not isinstance(data, dict):
        return PointerLoadResult(
            status="BLOCK",
            pointer_path=str(relative_pointer_path),
            data={},
            errors=["pointer_not_object"],
        )

    errors: list[str] = []
    if not str(data.get("next_allowed_action", "")).strip():
        errors.append("pointer_missing_next_allowed_action")

    if errors:
        return PointerLoadResult(
            status="CHECK_REQUIRED",
            pointer_path=str(relative_pointer_path),
            data=data,
            errors=errors,
        )

    return PointerLoadResult(
        status="OK",
        pointer_path=str(relative_pointer_path),
        data=data,
        errors=[],
    )
