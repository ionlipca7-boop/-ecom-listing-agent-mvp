import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
TEMPLATE_PATH = BASE_DIR / "templates"

def find_template():
    for f in TEMPLATE_PATH.glob("*.csv"):
        return f
    return None

def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    template_file = find_template()

    if not template_file:
        print("ERROR: template not found")
        return

    with open(template_file, encoding="utf-8") as f:
        reader = list(csv.reader(f, delimiter=';'))

    if len(reader) < 2:
        print("ERROR: template invalid")
        return

    header = reader[1]

    mandatory = []
    category_specific = []

    for col in header:
        if "*" in col:
            mandatory.append(col)
        if col.startswith("C:"):
            category_specific.append(col)

    contract = {
        "status": "OK",
        "template_file": template_file.name,
        "total_columns": len(header),
        "mandatory_count": len(mandatory),
        "category_specific_count": len(category_specific),
        "mandatory_fields": mandatory,
        "category_specific_fields": category_specific,
        "minimal_export_contract": mandatory
    }

    out_path = EXPORT_DIR / "csv_template_contract_v1.json"
    out_path.write_text(json.dumps(contract, indent=2, ensure_ascii=False), encoding="utf-8")

    print("CSV TEMPLATE CONTRACT BUILT")
    print("file:", out_path)
    print("columns:", len(header))
    print("mandatory:", len(mandatory))
    print("category_specific:", len(category_specific))

if __name__ == "__main__":
    main()
