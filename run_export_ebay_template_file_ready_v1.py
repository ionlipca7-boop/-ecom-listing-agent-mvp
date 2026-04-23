import json
import shutil
from datetime import datetime, UTC
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
PACKAGES_DIR = BASE_DIR / "storage" / "publish_packages"
STATUS_JSON = EXPORTS_DIR / "control_room_template_status_v1.json"
SOURCE_CSV = EXPORTS_DIR / "real_ebay_template_header_mapped_v1.csv"
OUTPUT_INDEX_JSON = PACKAGES_DIR / "publish_index_v1.json"

def utc_now_compact():
    fmt = chr(37) + "Y" + chr(37) + "m" + chr(37) + "d_" + chr(37) + "H" + chr(37) + "M" + chr(37) + "S"
    return datetime.now(UTC).strftime(fmt)

def utc_now_iso():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    status_data = load_json(STATUS_JSON)
    template_status = status_data.get("template_status", "BLOCKED")
    if template_status != "READY":
        raise RuntimeError(f"Template status is not READY: {template_status}")
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Source CSV not found: {SOURCE_CSV}")
    package_id = f"ebay_template_ready_{utc_now_compact()}"
    package_dir = PACKAGES_DIR / package_id
    package_dir.mkdir(parents=True, exist_ok=True)
    output_csv = package_dir / "ebay_template_upload_ready_v1.csv"
    shutil.copy2(SOURCE_CSV, output_csv)
    manifest = {
        "package_id": package_id,
        "created_at_utc": utc_now_iso(),
        "template_status": template_status,
        "source_csv": str(SOURCE_CSV),
        "output_csv": str(output_csv),
        "next_step": "UPLOAD_TO_EBAY_OR_RUN_FINAL_PACKAGE_CHECK",
    }
    manifest_path = package_dir / "manifest_v1.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    index_data = {
        "latest_package_id": package_id,
        "latest_package_dir": str(package_dir),
        "latest_output_csv": str(output_csv),
        "updated_at_utc": utc_now_iso(),
    }
    OUTPUT_INDEX_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_INDEX_JSON.open("w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    print("EXPORT_EBAY_TEMPLATE_FILE_READY_V1:")
    print(f"package_id: {package_id}")
    print(f"package_dir: {package_dir}")
    print(f"output_csv: {output_csv}")
    print(f"manifest_path: {manifest_path}")
    print(f"index_json: {OUTPUT_INDEX_JSON}")

if __name__ == "__main__":
    main()
