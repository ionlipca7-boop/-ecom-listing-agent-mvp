import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent

PIPELINE_STEPS = [
    "generate_ebay_export_v1.py",
    "generate_ebay_template_matched_export_v1.py",
    "audit_ebay_template_matched_export_v1.py",
    "prepare_ebay_upload_package_v1.py",
    "publish_execution_v1.py",
    "generate_control_room_state_v1.py",
    "decision_engine_v1.py",
    "real_publish_gate_v1.py",
]

OPTIONAL_MISSING_STEPS = {
    "generate_ebay_export_v1.py",
}

DECISION_FILE = PROJECT_ROOT / "decision_output_v1.json"
GATE_FILE = PROJECT_ROOT / "real_publish_gate_v1.json"
OUTPUT_FILE = PROJECT_ROOT / "control_room_run_v1.json"
PUBLISH_INDEX_FILE = PROJECT_ROOT / "publish_packages" / "publish_index.json"


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


def _extract_last_package_id() -> str | None:
    ok, data, _ = _safe_read_json(PUBLISH_INDEX_FILE)
    if not ok or not isinstance(data, dict):
        return None

    for key in ("last_package", "latest_package", "package_id"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    packages = data.get("packages")
    if isinstance(packages, list) and packages:
        last_item = packages[-1]
        if isinstance(last_item, dict):
            for key in ("package_id", "id", "name"):
                value = last_item.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()
        if isinstance(last_item, str) and last_item.strip():
            return last_item.strip()

    return None


def _build_command(filename: str) -> list[str]:
    path = PROJECT_ROOT / filename

    if filename == "publish_execution_v1.py":
        package_id = _extract_last_package_id()
        if package_id:
            return [sys.executable, str(path), "--package", package_id]

    return [sys.executable, str(path)]


def _run_python_file(filename: str) -> dict[str, Any]:
    path = PROJECT_ROOT / filename

    if not path.exists():
        if filename in OPTIONAL_MISSING_STEPS:
            return {
                "step": filename,
                "ok": True,
                "skipped": True,
                "returncode": None,
                "stdout": "",
                "stderr": f"optional file missing: {filename}",
            }

        return {
            "step": filename,
            "ok": False,
            "skipped": False,
            "returncode": None,
            "stdout": "",
            "stderr": f"file not found: {filename}",
        }

    command = _build_command(filename)

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    return {
        "step": filename,
        "ok": result.returncode == 0,
        "skipped": False,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "command": command,
    }


def _decision_allows_ready(decision_data: dict[str, Any]) -> bool:
    positive_keys = [
        "approved",
        "decision_ok",
        "ready_for_publish",
        "publish_ready",
        "can_publish",
        "allow_publish",
        "ok",
        "next_action",
    ]
    positive_values = {
        "APPROVED",
        "READY",
        "READY_FOR_REAL_PUBLISH",
        "ALLOW",
        "ALLOWED",
        "OPEN",
        "SUCCESS",
        "PASS",
        "PASSED",
        "OK",
        True,
    }

    for key in positive_keys:
        value = decision_data.get(key)
        if value in positive_values:
            return True
        if isinstance(value, str) and value.upper() in {
            "APPROVED",
            "READY",
            "READY_FOR_REAL_PUBLISH",
            "ALLOW",
            "ALLOWED",
            "OPEN",
            "SUCCESS",
            "PASS",
            "PASSED",
            "OK",
        }:
            return True

    for _, value in decision_data.items():
        if isinstance(value, str) and value.upper() in {
            "APPROVED",
            "READY",
            "READY_FOR_REAL_PUBLISH",
            "ALLOW",
            "ALLOWED",
            "OPEN",
            "SUCCESS",
            "PASS",
            "PASSED",
            "OK",
        }:
            return True

    return False


def _evaluate_final_status(
    step_results: list[dict[str, Any]],
    decision_ok: bool,
    decision_data: dict[str, Any] | None,
    gate_ok: bool,
    gate_data: dict[str, Any] | None,
) -> tuple[str, list[str]]:
    reasons: list[str] = []

    failed_steps = [
        step["step"]
        for step in step_results
        if not step.get("ok", False)
    ]
    if failed_steps:
        reasons.append(f"failed_steps={', '.join(failed_steps)}")

    if not decision_ok or not isinstance(decision_data, dict):
        reasons.append("decision_output_v1.json unavailable")
    elif not _decision_allows_ready(decision_data):
        reasons.append("decision output does not confirm publish readiness")

    if not gate_ok or not isinstance(gate_data, dict):
        reasons.append("real_publish_gate_v1.json unavailable")
    else:
        next_action = str(gate_data.get("next_action", "")).upper()
        gate_status = str(gate_data.get("gate_status", "")).upper()
        last_status = str(gate_data.get("last_status", "")).upper()

        if next_action != "READY_FOR_REAL_PUBLISH":
            reasons.append(f"next_action={next_action or 'MISSING'}")
        if gate_status != "OPEN":
            reasons.append(f"gate_status={gate_status or 'MISSING'}")
        if last_status and last_status != "SUCCESS":
            reasons.append(f"last_status={last_status}")

    final_status = "READY" if not reasons else "BLOCKED"
    return final_status, reasons


def main() -> int:
    run_started_at = _utc_now()
    last_package = _extract_last_package_id()

    step_results: list[dict[str, Any]] = []
    for step in PIPELINE_STEPS:
        result = _run_python_file(step)
        step_results.append(result)

    decision_ok, decision_data, decision_error = _safe_read_json(DECISION_FILE)
    gate_ok, gate_data, gate_error = _safe_read_json(GATE_FILE)

    final_status, reasons = _evaluate_final_status(
        step_results=step_results,
        decision_ok=decision_ok,
        decision_data=decision_data if isinstance(decision_data, dict) else None,
        gate_ok=gate_ok,
        gate_data=gate_data if isinstance(gate_data, dict) else None,
    )

    output = {
        "run_started_at": run_started_at,
        "checked_at": _utc_now(),
        "last_package_detected": last_package,
        "pipeline_steps": step_results,
        "decision_file": {
            "path": DECISION_FILE.name,
            "ok": decision_ok,
            "error": decision_error,
            "data": decision_data,
        },
        "gate_file": {
            "path": GATE_FILE.name,
            "ok": gate_ok,
            "error": gate_error,
            "data": gate_data,
        },
        "final_status": final_status,
        "reasons": reasons,
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("CONTROL_ROOM_RUN:")
    print(f"output_file: {OUTPUT_FILE.name}")
    print(f"last_package_detected: {last_package}")
    print(f"decision_file_ok: {decision_ok}")
    print(f"gate_file_ok: {gate_ok}")
    print(f"FINAL_STATUS: {final_status}")

    if reasons:
        print("REASONS:")
        for reason in reasons:
            print(f"- {reason}")

    return 0 if final_status == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())