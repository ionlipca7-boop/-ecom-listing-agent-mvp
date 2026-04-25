import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
BUNDLES_DIR = BASE_DIR / "storage" / "portable_publish_bundles"
OUTPUT_FILE = EXPORTS_DIR / "portable_publish_bundle_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def copy_if_exists(source_path, target_path):
    if source_path.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        return True
    return False

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    BUNDLES_DIR.mkdir(parents=True, exist_ok=True)

    package_ready = read_json(EXPORTS_DIR / "one_click_package_ready_v1.json")
    attach_ready = read_json(EXPORTS_DIR / "attach_variant_package_assets_v1.json")

    package_status = package_ready.get("one_click_package_status", "")
    assets_status = attach_ready.get("attach_status", "")
    package_id = package_ready.get("package_id", "")
    package_dir_value = package_ready.get("package_dir", "")
    payload_file_value = package_ready.get("payload_file", "")
    manifest_file_value = package_ready.get("manifest_file", "")

    package_dir = Path(str(package_dir_value)) if package_dir_value else Path()
    payload_file = Path(str(payload_file_value)) if payload_file_value else Path()
    manifest_file = Path(str(manifest_file_value)) if manifest_file_value else Path()
    photos_dir = package_dir / "photos"

    if package_status != "READY" or assets_status != "READY" or not package_id:
        result = {
            "checked_at": utc_now(),
            "bundle_status": "BLOCKED",
            "next_step": "FIX_PREVIOUS_LAYER",
            "package_id": package_id,
            "copied_files_count": 0,
        }
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("BUILD_PORTABLE_PUBLISH_BUNDLE_V1:")
        print("bundle_status:", result["bundle_status"])
        print("next_step:", result["next_step"])
        print("output_file:", OUTPUT_FILE.name)
        return

    bundle_dir = BUNDLES_DIR / package_id
    bundle_dir.mkdir(parents=True, exist_ok=True)
    bundle_photos_dir = bundle_dir / "photos"
    bundle_photos_dir.mkdir(parents=True, exist_ok=True)

    copied_file_names = []

    if copy_if_exists(payload_file, bundle_dir / "execution_payload_v1.json"):
        copied_file_names.append("execution_payload_v1.json")
    if copy_if_exists(manifest_file, bundle_dir / "manifest_v1.json"):
        copied_file_names.append("manifest_v1.json")

    copied_photo_names = []
    if photos_dir.exists():
        for photo_file in photos_dir.iterdir():
            if photo_file.is_file():
                shutil.copy2(photo_file, bundle_photos_dir / photo_file.name)
                copied_photo_names.append(photo_file.name)

    bundle_manifest = {
        "bundle_id": package_id,
        "bundle_status": "READY",
        "title": package_ready.get("title"),
        "price": package_ready.get("price"),
        "variant_id": package_ready.get("variant_id"),
        "source_package_dir": str(package_dir),
        "created_at": utc_now(),
        "files": copied_file_names,
        "photos_count": len(copied_photo_names)
    }

    (bundle_dir / "bundle_manifest_v1.json").write_text(json.dumps(bundle_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {
        "checked_at": utc_now(),
        "bundle_status": "READY",
        "next_step": "BUILD_LOCAL_APP_LAUNCHER",
        "package_id": package_id,
        "bundle_dir": str(bundle_dir),
        "copied_files_count": len(copied_file_names) + 1,
        "copied_photos_count": len(copied_photo_names)
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("BUILD_PORTABLE_PUBLISH_BUNDLE_V1:")
    print("bundle_status:", result["bundle_status"])
    print("next_step:", result["next_step"])
    print("package_id:", result["package_id"])
    print("copied_files_count:", result["copied_files_count"])
    print("copied_photos_count:", result["copied_photos_count"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
