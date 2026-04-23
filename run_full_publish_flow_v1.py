import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent

FLOW_STEPS = [
    "run_control_room_v1.py",
    "create_real_publish_request_v1.py",
    "final_publish_manifest_v1.py",
    "approve_real_publish_v1.py",
]

APPROVAL_FILE = PROJECT_ROOT / "real_publish_approval_v1.json"
OUTPUT_FILE = PROJECT_ROOT / "full_publish_flow_v1.json"


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _safe_read_json(path: Path) -> tuple[bool, Any | None, str | None]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return True, json.load(f), None
    except FileNotFoundError:
        return False, None, f"file not found: {path.name}"
    except json.JSONDecodeError as exc:
        return False, None, f"invalid json in {path.name}: {exc}"
    except Exception as exc:
        return False, None, f"failed to read {path.name}: {exc}"


def _run_python_file(filename: str) -> dict[str, Any]:
    path = PROJECT_ROOT / filename

    if not path.exists():
        return {
            "step": filename,
            "ok": False,
            "returncode": None,
            "stdout": "",
            "stderr": f"file not found: {filename}",
        }

    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    return {
        "step": filename,
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "command": [sys.executable, str(path)],
    }


def _evaluate_flow_status(
    step_results: list[dict[str, Any]],
    approval_ok: bool,
    approval_data: dict[str, Any] | None,
) -> tuple[str, list[str], str | None]:
    reasons: list[str] = []
    last_package: str | None = None

    failed_steps = [step["step"] for step in step_results if not step.get("ok", False)]
    if failed_steps:
        reasons.append(f"failed_steps={', '.join(failed_steps)}")

    if not approval_ok or not isinstance(approval_data, dict):
        reasons.append("real_publish_approval_v1.json unavailable")
    else:
        package_value = approval_data.get("last_package")
        if isinstance(package_value, str) and package_value.strip():
            last_package = package_value.strip()

        approval_status = str(approval_data.get("approval_status", "")).strip().upper()
        if approval_status != "APPROVED":
            reasons.append(f"approval_status={approval_status or 'MISSING'}")

    flow_status = "APPROVED" if not reasons else "BLOCKED"
    return flow_status, reasons, last_package


def main() -> int:
    started_at = _utc_now()

    step_results: list[dict[str, Any]] = []
    for step in FLOW_STEPS:
        result = _run_python_file(step)
        step_results.append(result)

    approval_ok, approval_data, approval_error = _safe_read_json(APPROVAL_FILE)

    flow_status, reasons, last_package = _evaluate_flow_status(
        step_results=step_results,
        approval_ok=approval_ok,
        approval_data=approval_data if isinstance(approval_data, dict) else None,
    )

    output = {
        "started_at": started_at,
        "checked_at": _utc_now(),
        "last_package": last_package,
        "steps": step_results,
        "approval_file": {
            "path": APPROVAL_FILE.name,
            "ok": approval_ok,
            "error": approval_error,
            "data": approval_data,
        },
        "flow_status": flow_status,
        "reasons": reasons,
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("FULL_PUBLISH_FLOW:")
    print(f"last_package: {last_package}")
    print(f"output_file: {OUTPUT_FILE.name}")
    print(f"FLOW_STATUS: {flow_status}")

    if reasons:
        print("REASONS:")
        for reason in reasons:
            print(f"- {reason}")

    return 0 if flow_status == "APPROVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())