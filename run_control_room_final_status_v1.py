import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
PUBLISH_DIR = BASE_DIR / "storage" / "publish_packages"
TEMPLATE_STATUS_JSON = EXPORTS_DIR / "control_room_template_status_v1.json"
FINAL_CHECK_JSON = EXPORTS_DIR / "final_package_check_v1.json"
PUBLISH_INDEX_JSON = PUBLISH_DIR / "publish_index_v1.json"
OUTPUT_JSON = EXPORTS_DIR / "control_room_final_status_v1.json"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    template_status_data = load_json(TEMPLATE_STATUS_JSON)
    final_check_data = load_json(FINAL_CHECK_JSON)
    publish_index_data = load_json(PUBLISH_INDEX_JSON)

    template_status = template_status_data.get("template_status", "BLOCKED")
    final_status = final_check_data.get("final_status", "BLOCKED")

    system_status = "READY" if template_status == "READY" and final_status == "READY" else "BLOCKED"
    next_step = "UPLOAD_TO_EBAY_MANUALLY" if system_status == "READY" else "FIX_PIPELINE_BLOCKERS"

    output = {
        "system_status": system_status,
        "template_status": template_status,
        "final_package_status": final_status,
        "latest_package_id": publish_index_data.get("latest_package_id", ""),
        "latest_output_csv": publish_index_data.get("latest_output_csv", ""),
        "header_count": final_check_data.get("header_count", 0),
        "data_row_count": final_check_data.get("data_row_count", 0),
        "next_step": next_step,
    }

    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("CONTROL_ROOM_FINAL_STATUS_V1:")
    print(f"system_status: {system_status}")
    print(f"template_status: {template_status}")
    print(f"final_package_status: {final_status}")
    print(f"latest_package_id: {publish_index_data.get('latest_package_id', '')}")
    print(f"header_count: {final_check_data.get('header_count', 0)}")
    print(f"data_row_count: {final_check_data.get('data_row_count', 0)}")
    print(f"next_step: {next_step}")
    print(f"output_json: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
