import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PUBLISH_INDEX_JSON = BASE_DIR / "storage" / "publish_packages" / "publish_index_v1.json"
FINAL_STATUS_JSON = BASE_DIR / "storage" / "exports" / "control_room_final_status_v1.json"
OUTPUT_JSON = BASE_DIR / "storage" / "exports" / "upload_handoff_v1.json"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    publish_index = load_json(PUBLISH_INDEX_JSON)
    final_status = load_json(FINAL_STATUS_JSON)
    output = {
        "handoff_status": "READY" if final_status.get("system_status") == "READY" else "BLOCKED",
        "package_id": publish_index.get("latest_package_id", ""),
        "final_csv": publish_index.get("latest_output_csv", ""),
        "header_count": final_status.get("header_count", 0),
        "data_row_count": final_status.get("data_row_count", 0),
        "instruction": "Open eBay bulk listing upload and use the final CSV file from final_csv",
        "next_step": "UPLOAD_TO_EBAY_MANUALLY",
    }
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("UPLOAD_HANDOFF_V1:")
    print(f"handoff_status: {output['handoff_status']}")
    print(f"package_id: {output['package_id']}")
    print(f"final_csv: {output['final_csv']}")
    print(f"header_count: {output['header_count']}")
    print(f"data_row_count: {output['data_row_count']}")
    print(f"next_step: {output['next_step']}")
    print(f"output_json: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
