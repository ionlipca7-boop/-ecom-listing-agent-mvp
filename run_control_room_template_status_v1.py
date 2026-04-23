import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SOURCE_JSON = EXPORTS_DIR / "required_template_fields_validation_v1.json"
OUTPUT_JSON = EXPORTS_DIR / "control_room_template_status_v1.json"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    data = load_json(SOURCE_JSON)
    summary = data.get("summary", {})
    status = "READY" if summary.get("blocked_row_count", 0) == 0 else "BLOCKED"
    next_step = "EXPORT_EBAY_TEMPLATE_FILE_READY" if status == "READY" else "FIX_REQUIRED_TEMPLATE_FIELDS"
    output = {
        "template_status": status,
        "blocked_row_count": summary.get("blocked_row_count", 0),
        "ok_row_count": summary.get("ok_row_count", 0),
        "next_step": next_step,
        "source_validation_file": str(SOURCE_JSON),
    }
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("CONTROL_ROOM_TEMPLATE_STATUS_V1:")
    print(f"template_status: {status}")
    print(f"blocked_row_count: {summary.get('blocked_row_count', 0)}")
    print(f"ok_row_count: {summary.get('ok_row_count', 0)}")
    print(f"next_step: {next_step}")
    print(f"output_json: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
