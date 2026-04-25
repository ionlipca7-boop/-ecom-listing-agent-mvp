import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "ebay_publish_result_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "check_publish_file_v1.json"

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    result = {}
    result["status"] = "OK"
    result["publish_file_exists"] = INPUT_PATH.exists()
    result["input_path"] = str(INPUT_PATH)
    save_json(OUTPUT_PATH, result)
    print("CHECK_PUBLISH_FILE_V1_DONE")
    print("publish_file_exists =", result["publish_file_exists"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
