import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_JSON = BASE_DIR / "storage" / "exports" / "ebay_template_header_detect_v1.json"

def detect_header(csv_path: Path):
    best_row = []
    best_index = -1
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter=";")
        for idx, row in enumerate(reader):
            cleaned = [cell.strip() for cell in row]
            non_empty = [cell for cell in cleaned if cell]
            if len(non_empty) > len(best_row):
                best_row = cleaned
                best_index = idx
    return best_index, best_row

def main():
    csv_files = sorted(TEMPLATES_DIR.rglob("*.csv"))
    results = []
    for csv_file in csv_files:
        try:
            header_index, header_row = detect_header(csv_file)
            results.append({
                "template_file": str(csv_file),
                "header_row_index_0_based": header_index,
                "column_count": len(header_row),
                "columns": header_row,
            })
        except Exception as e:
            results.append({
                "template_file": str(csv_file),
                "error": str(e),
            })
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    output = {"template_count": len(csv_files), "results": results}
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("EBAY_TEMPLATE_HEADER_DETECT_V1:")
    print(f"template_count: {len(csv_files)}")
    print(f"output_json: {OUTPUT_JSON}")
    for item in results:
        if "error" in item:
            print(f"template_error: {item['template_file']} :: {item['error']}")
        else:
            print(f"template_file: {item['template_file']}")
            print(f"header_row_index_0_based: {item['header_row_index_0_based']}")
            print(f"column_count: {item['column_count']}")

if __name__ == "__main__":
    main()
