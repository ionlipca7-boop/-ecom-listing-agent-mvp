import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INDEX_JSON = BASE_DIR / "storage" / "publish_packages" / "publish_index_v1.json"
OUTPUT_JSON = BASE_DIR / "storage" / "exports" / "final_package_check_v1.json"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    index_data = load_json(INDEX_JSON)
    csv_path = Path(index_data["latest_output_csv"])
    if not csv_path.exists():
        raise FileNotFoundError(f"Package CSV not found: {csv_path}")
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = list(csv.reader(f, delimiter=";"))
    row_count_including_header = len(reader)
    if reader:
        header_count = len(reader[0])
    data_row_count = max(0, row_count_including_header - 1)
    status = "READY" if (header_count == 96 and data_row_count >= 1) else "BLOCKED"
    output = {
        "package_csv": str(csv_path),
        "header_count": header_count,
        "data_row_count": data_row_count,
        "final_status": status,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("FINAL_PACKAGE_CHECK_V1:")
    print(f"package_csv: {csv_path}")
    print(f"header_count: {header_count}")
    print(f"data_row_count: {data_row_count}")
    print(f"final_status: {status}")
    print(f"output_json: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
