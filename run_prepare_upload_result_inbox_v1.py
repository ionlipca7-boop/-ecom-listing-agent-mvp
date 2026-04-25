import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INBOX_DIR = BASE_DIR / "storage" / "upload_results_inbox"
OUTPUT_FILE = EXPORTS_DIR / "prepare_upload_result_inbox_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    portable_bundle = read_json(EXPORTS_DIR / "portable_publish_bundle_v1.json")
    package_id = portable_bundle.get("package_id", "")
    bundle_status = portable_bundle.get("bundle_status", "")

    sample_json = INBOX_DIR / "sample_upload_result.json"
    sample_csv = INBOX_DIR / "sample_upload_result.csv"
    readme_file = INBOX_DIR / "README_UPLOAD_RESULT.txt"

    if not sample_json.exists():
        sample_json.write_text('{' + '\n  "package_id": "",' + '\n  "status": "",' + '\n  "sku": "",' + '\n  "item_id": "",' + '\n  "errors": []' + '\n}' , encoding="utf-8")

    if not sample_csv.exists():
        sample_csv.write_text("package_id;status;sku;item_id;error_code;error_message" + "\n", encoding="utf-8")

    readme_text = "Drop real eBay upload result files here. Supported start formats: JSON or CSV." + "\n" + "Current package_id: " + str(package_id)
    readme_file.write_text(readme_text, encoding="utf-8")

    result = {
        "checked_at": utc_now(),
        "inbox_status": "READY" if bundle_status == "READY" else "BLOCKED",
        "next_step": "RUN_RESULT_PARSER_ON_REAL_UPLOAD_FILE" if bundle_status == "READY" else "FIX_PORTABLE_BUNDLE",
        "package_id": package_id,
        "inbox_dir": str(INBOX_DIR),
        "sample_json": str(sample_json),
        "sample_csv": str(sample_csv),
        "readme_file": str(readme_file)
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("PREPARE_UPLOAD_RESULT_INBOX_V1:")
    print("inbox_status:", result["inbox_status"])
    print("next_step:", result["next_step"])
    print("package_id:", result["package_id"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
