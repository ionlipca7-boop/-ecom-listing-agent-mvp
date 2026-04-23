import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "attach_variant_package_assets_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    handoff = read_json(EXPORTS_DIR / "final_real_publish_handoff_v1.json")
    package_dir_value = handoff.get("package_dir", "")
    payload_file_value = handoff.get("payload_file", "")

    package_dir = Path(str(package_dir_value)) if package_dir_value else Path()
    payload_file = Path(str(payload_file_value)) if payload_file_value else Path()

    if not payload_file.exists():
        result = {
            "checked_at": utc_now(),
            "attach_status": "BLOCKED",
            "next_step": "FIX_MISSING_PAYLOAD",
            "package_id": handoff.get("package_id"),
            "copied_count": 0,
        }
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("ATTACH_VARIANT_PACKAGE_ASSETS_V1:")
        print("attach_status:", result["attach_status"])
        print("next_step:", result["next_step"])
        print("output_file:", OUTPUT_FILE.name)
        return

    payload = read_json(payload_file)
    photos_dir = package_dir / "photos"
    photos_dir.mkdir(parents=True, exist_ok=True)

    photo_names = []
    for index in range(1, 8):
        value = payload.get(f"Photo{index}", "")
        if isinstance(value, str) and value.strip():
            photo_names.append(value.strip())

    copied_files = []
    missing_files = []
    search_roots = [BASE_DIR / "storage", BASE_DIR / "photos", BASE_DIR / "images", BASE_DIR / "assets", BASE_DIR]

    for photo_name in photo_names:
        found_path = None
        for root in search_roots:
            if not root.exists():
                continue
            matches = list(root.rglob(photo_name))
            if matches:
                found_path = matches[0]
                break
        if found_path is None:
            missing_files.append(photo_name)
            continue
        target_path = photos_dir / photo_name
        if found_path.resolve() != target_path.resolve():
            shutil.copy2(found_path, target_path)
        copied_files.append(photo_name)

    result = {
        "checked_at": utc_now(),
        "attach_status": "READY" if not missing_files else "PARTIAL",
        "next_step": "PACKAGE_WITH_ASSETS_READY" if not missing_files else "REVIEW_MISSING_PHOTOS",
        "package_id": handoff.get("package_id"),
        "package_dir": str(package_dir),
        "photos_dir": str(photos_dir),
        "expected_count": len(photo_names),
        "copied_count": len(copied_files),
        "missing_count": len(missing_files),
        "copied_files": copied_files,
        "missing_files": missing_files
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("ATTACH_VARIANT_PACKAGE_ASSETS_V1:")
    print("attach_status:", result["attach_status"])
    print("next_step:", result["next_step"])
    print("copied_count:", result["copied_count"])
    print("missing_count:", result["missing_count"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
