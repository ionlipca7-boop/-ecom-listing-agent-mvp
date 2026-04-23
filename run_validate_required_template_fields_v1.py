import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SOURCE_JSON = EXPORTS_DIR / "real_ebay_template_header_mapped_v1.json"
OUTPUT_JSON = EXPORTS_DIR / "required_template_fields_validation_v1.json"

STATIC_REQUIRED_FIELDS = [
    "*Category",
    "*Title",
    "*ConditionID",
    "*C:Marke",
    "*C:Produktart",
    "*Description",
    "*Format",
    "*Duration",
    "*StartPrice",
    "*Quantity",
    "*Location",
    "*DispatchTimeMax",
    "*ReturnsAcceptedOption",
]

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def is_filled(value):
    if value is None:
        return False
    return str(value).strip() != ""

def main():
    data = load_json(SOURCE_JSON)
    header = data.get("header", [])
    rows = data.get("rows", [])
    if not header:
        raise RuntimeError("Header not found in source json")
    action_field = header[0]
    required_fields = [action_field] + STATIC_REQUIRED_FIELDS
    validation_rows = []

    for idx, row in enumerate(rows, start=1):
        missing_fields = []
        filled_fields = []
        for field in required_fields:
            value = row.get(field, "")
            if is_filled(value):
                filled_fields.append(field)
            else:
                missing_fields.append(field)

        validation_rows.append({
            "row_index_1_based": idx,
            "custom_label": row.get("CustomLabel", ""),
            "title": row.get("*Title", ""),
            "required_ok": len(missing_fields) == 0,
            "filled_required_count": len(filled_fields),
            "missing_required_count": len(missing_fields),
            "filled_required_fields": filled_fields,
            "missing_required_fields": missing_fields,
        })

    ok_rows = sum(1 for item in validation_rows if item["required_ok"])
    blocked_rows = len(validation_rows) - ok_rows

    output = {
        "summary": {
            "source_file": str(SOURCE_JSON),
            "action_field": action_field,
            "required_field_count": len(required_fields),
            "row_count": len(validation_rows),
            "ok_row_count": ok_rows,
            "blocked_row_count": blocked_rows,
            "validation_status": "PASS" if blocked_rows == 0 else "BLOCKED",
        },
        "required_fields": required_fields,
        "rows": validation_rows,
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("VALIDATE_REQUIRED_TEMPLATE_FIELDS_V1:")
    print(f"action_field: {action_field}")
    print(f"required_field_count: {len(required_fields)}")
    print(f"row_count: {len(validation_rows)}")
    print(f"ok_row_count: {ok_rows}")
    print(f"blocked_row_count: {blocked_rows}")
    print(f"validation_status: {'PASS' if blocked_rows == 0 else 'BLOCKED'}")
    print(f"output_json: {OUTPUT_JSON}")
    if validation_rows:
        sample = validation_rows[0]
        print(f"sample_custom_label: {sample['custom_label']}")
        print(f"sample_required_ok: {sample['required_ok']}")
        print(f"sample_missing_required_count: {sample['missing_required_count']}")

if __name__ == "__main__":
    main()
