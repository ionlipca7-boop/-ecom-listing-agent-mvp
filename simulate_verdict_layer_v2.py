import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PUBLISH_PACKAGES_DIR = Path("publish_packages")
PUBLISH_INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
OUTPUT_FILENAME = "simulation_verdict_v2.json"

CRITICAL_FILES = {
    "ebay_mapping_v2.json": "json",
    "ebay_template_output_v2.csv": "csv",
    "ebay_upload_ready_v2.csv": "csv",
    "ebay_upload_ready_v2_validation.json": "json",
    "ebay_upload_ready_v2_summary.json": "json",
}

OPTIONAL_FILES = {
    "ebay_upload_contract_v2_audit.json": "json",
    "export_bundle_v2_inspection.json": "json",
}


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _safe_read_json(path: Path) -> tuple[bool, Any | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return False, None, "missing"
    except json.JSONDecodeError as exc:
        return False, None, f"invalid_json: {exc}"
    except OSError as exc:
        return False, None, f"read_error: {exc}"

    return True, payload, None


def _safe_read_csv(path: Path) -> tuple[bool, dict[str, Any] | None, str | None]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    except FileNotFoundError:
        return False, None, "missing"
    except csv.Error as exc:
        return False, None, f"invalid_csv: {exc}"
    except OSError as exc:
        return False, None, f"read_error: {exc}"

    if not fieldnames:
        return False, None, "invalid_csv: missing_header"

    return True, {"fieldnames": fieldnames, "row_count": len(rows)}, None


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build standalone simulation verdict for v2 package artifacts.")
    parser.add_argument("--package", dest="package_id", help="Specific package id under publish_packages/")
    return parser.parse_args()


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def _load_latest_package_from_index() -> tuple[str | None, str | None]:
    ok, payload, error = _safe_read_json(PUBLISH_INDEX_PATH)
    if not ok:
        if error == "missing":
            return None, "publish_index_missing"
        return None, f"publish_index_invalid ({error})"

    if not isinstance(payload, dict):
        return None, "publish_index_invalid (root_not_object)"

    latest_package = payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package.strip():
        return None, "latest_package_missing"

    return latest_package.strip(), None


def _evaluate_package(package_id: str) -> dict[str, Any]:
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    checked_files: list[dict[str, Any]] = []
    checks_passed: list[str] = []
    checks_failed: list[str] = []
    warnings: list[str] = []
    metrics: dict[str, Any] = {}

    if not package_dir.exists() or not package_dir.is_dir():
        checks_failed.append(f"package_dir_missing: {package_dir.as_posix()}")
    else:
        checks_passed.append("package_dir_exists")

    for filename, file_type in {**CRITICAL_FILES, **OPTIONAL_FILES}.items():
        file_path = package_dir / filename
        is_critical = filename in CRITICAL_FILES

        if file_type == "json":
            ok, payload, error = _safe_read_json(file_path)
            info = {
                "file": filename,
                "exists": file_path.exists(),
                "file_type": file_type,
                "status": "ok" if ok else "error",
                "critical": is_critical,
            }
            if ok:
                checks_passed.append(f"valid_json:{filename}")
                if isinstance(payload, dict):
                    info["json_root_type"] = "object"
                elif isinstance(payload, list):
                    info["json_root_type"] = "array"
                else:
                    info["json_root_type"] = type(payload).__name__
                metric_entry: dict[str, Any] = {"json_root_type": info["json_root_type"]}
                if filename == "ebay_upload_ready_v2_validation.json" and isinstance(payload, dict):
                    metric_entry["status_values"] = {
                        key: payload.get(key) for key in ("status", "verdict", "result", "overall_status")
                    }
                if filename == "ebay_upload_ready_v2_summary.json" and isinstance(payload, dict):
                    metric_entry["total_items"] = payload.get("total_items")
                metrics[filename] = metric_entry
            else:
                info["error"] = error
                if is_critical:
                    checks_failed.append(f"critical_json_error:{filename}:{error}")
                else:
                    warnings.append(f"optional_json_issue:{filename}:{error}")
            checked_files.append(info)
            continue

        ok, csv_info, error = _safe_read_csv(file_path)
        info = {
            "file": filename,
            "exists": file_path.exists(),
            "file_type": file_type,
            "status": "ok" if ok else "error",
            "critical": is_critical,
        }
        if ok and csv_info is not None:
            checks_passed.append(f"valid_csv:{filename}")
            info["header_count"] = len(csv_info["fieldnames"])
            info["row_count"] = csv_info["row_count"]
            metrics[filename] = csv_info
            if csv_info["row_count"] == 0:
                if is_critical:
                    checks_failed.append(f"critical_csv_empty:{filename}")
                else:
                    warnings.append(f"optional_csv_empty:{filename}")
        else:
            info["error"] = error
            if is_critical:
                checks_failed.append(f"critical_csv_error:{filename}:{error}")
            else:
                warnings.append(f"optional_csv_issue:{filename}:{error}")
        checked_files.append(info)

    template_info = metrics.get("ebay_template_output_v2.csv")
    upload_ready_info = metrics.get("ebay_upload_ready_v2.csv")
    if isinstance(template_info, dict) and isinstance(upload_ready_info, dict):
        template_rows = int(template_info.get("row_count", 0))
        upload_rows = int(upload_ready_info.get("row_count", 0))
        if upload_rows > template_rows and template_rows > 0:
            checks_failed.append(
                "inconsistent_rows:ebay_upload_ready_v2.csv has more rows than ebay_template_output_v2.csv"
            )
        elif upload_rows < template_rows:
            warnings.append(
                "row_drop_detected:ebay_upload_ready_v2.csv has fewer rows than ebay_template_output_v2.csv"
            )

    validation_payload = metrics.get("ebay_upload_ready_v2_validation.json")
    if isinstance(validation_payload, dict):
        status_values = validation_payload.get("status_values")
        if not isinstance(status_values, dict):
            status_values = {}
        for key in ("status", "verdict", "result", "overall_status"):
            value = status_values.get(key)
            if isinstance(value, str) and value.strip().lower() in {"fail", "failed", "error", "block", "blocked"}:
                checks_failed.append(f"validation_reports_failure:{key}={value}")

    summary_payload = metrics.get("ebay_upload_ready_v2_summary.json")
    if isinstance(summary_payload, dict):
        total_items = summary_payload.get("total_items")
        if isinstance(total_items, int) and total_items <= 0:
            warnings.append("summary_total_items_non_positive")

    checks_failed = _dedupe_preserve_order(checks_failed)

    verdict = "SAFE"
    if checks_failed:
        verdict = "BLOCK"
    elif warnings:
        verdict = "WARNING"

    if verdict == "SAFE":
        recommended_next_action = "Proceed to next control-room step and keep artifacts unchanged."
    elif verdict == "WARNING":
        recommended_next_action = "Review warnings, fix soft issues, then re-run simulation verdict."
    else:
        recommended_next_action = "Stop release path, resolve blocking issues, then re-run simulation verdict."

    return {
        "package_id": package_id,
        "generated_at": _utc_now(),
        "checked_files": checked_files,
        "checks_passed": checks_passed,
        "checks_failed": checks_failed,
        "warnings": warnings,
        "verdict": verdict,
        "recommended_next_action": recommended_next_action,
    }


def _write_verdict(package_id: str, verdict_payload: dict[str, Any]) -> tuple[bool, str]:
    package_dir = PUBLISH_PACKAGES_DIR / package_id
    output_path = package_dir / OUTPUT_FILENAME

    try:
        package_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(verdict_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return True, output_path.as_posix()
    except OSError as exc:
        return False, f"write_error: {exc}"


def main() -> int:
    args = _parse_args()

    checks_failed: list[str] = []
    warnings: list[str] = []

    package_id = args.package_id
    if package_id:
        package_id = package_id.strip()

    if not package_id:
        latest_package, index_error = _load_latest_package_from_index()
        if index_error:
            checks_failed.append(index_error)
        package_id = latest_package

    if not package_id:
        payload = {
            "package_id": None,
            "generated_at": _utc_now(),
            "checked_files": [],
            "checks_passed": [],
            "checks_failed": checks_failed,
            "warnings": warnings,
            "verdict": "BLOCK",
            "recommended_next_action": "Create/fix publish_packages/publish_index.json with latest_package and re-run.",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    payload = _evaluate_package(package_id)

    if checks_failed:
        payload["checks_failed"] = checks_failed + payload["checks_failed"]
        payload["checks_failed"] = _dedupe_preserve_order(payload["checks_failed"])
        payload["verdict"] = "BLOCK"
        payload["recommended_next_action"] = "Fix publish index and blocking package issues, then re-run simulation verdict."

    ok, output_info = _write_verdict(package_id, payload)
    if not ok:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print(output_info)
        return 1

    print(f"package_id: {package_id}")
    print(f"verdict: {payload['verdict']}")
    print(f"checks_failed: {len(payload['checks_failed'])}")
    print(f"warnings: {len(payload['warnings'])}")
    print(f"output_file: {output_info}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
