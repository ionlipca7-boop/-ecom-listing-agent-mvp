import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PUBLISH_PACKAGES_DIR = Path("publish_packages")
MANIFEST_NAME = "manifest.json"
RESULT_FILE = "publish_result_v1.json"


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_args():
    parser = argparse.ArgumentParser(description="Simulate eBay publish execution v1.")
    parser.add_argument("--package", dest="package_id", required=True)
    return parser.parse_args()


def _safe_read_json(path: Path):
    try:
        return True, json.loads(path.read_text(encoding="utf-8")), None
    except Exception as e:
        return False, None, str(e)


def main():
    args = _parse_args()
    package_id = args.package_id

    package_dir = PUBLISH_PACKAGES_DIR / package_id / "ebay_upload_package_v1"
    manifest_path = package_dir / MANIFEST_NAME
    result_path = package_dir / RESULT_FILE

    if not manifest_path.exists():
        print("status: FAILED")
        print("reason: missing_manifest")
        return 1

    ok, manifest, err = _safe_read_json(manifest_path)
    if not ok:
        print("status: FAILED")
        print("reason: invalid_manifest")
        return 1

    # симуляция publish (пока fake)
    publish_status = "SUCCESS"

    result_payload: dict[str, Any] = {
        "package_id": package_id,
        "status": publish_status,
        "executed_at": _utc_now(),
        "source_manifest": manifest_path.as_posix(),
    }

    result_path.write_text(json.dumps(result_payload, indent=2), encoding="utf-8")

    print(f"package_id: {package_id}")
    print(f"status: {publish_status}")
    print(f"result_file: {result_path.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())