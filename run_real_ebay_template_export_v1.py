import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
MAPPED_JSON = EXPORTS_DIR / "ebay_template_mapped_v2.json"
READY_JSON = EXPORTS_DIR / "ready_listings_v1.json"
OUTPUT_JSON = EXPORTS_DIR / "real_ebay_template_export_v1.json"
OUTPUT_CSV = EXPORTS_DIR / "real_ebay_template_export_v1.csv"

def load_json(path: Path):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}

def extract_mapped_rows(data):
    rows = data.get("rows", [])
    return rows if isinstance(rows, list) else []

def extract_ready_rows(data):
    rows = data.get("ready_listings", [])
    return rows if isinstance(rows, list) else []

def normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()

def normalize_features(value):
    if value is None:
        return ""
    if isinstance(value, list):
        cleaned = [normalize_text(x) for x in value if normalize_text(x)]
        return "; ".join(cleaned)
    text = normalize_text(value)
    if text.startswith("[") and text.endswith("]"):
        text = text.replace("[", "").replace("]", "").replace("'", "").replace(chr(34), "")
        parts = [part.strip() for part in text.split(",") if part.strip()]
        return "; ".join(parts)
    return text

def normalize_photo_files(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [normalize_text(x) for x in value if normalize_text(x)]
    text = normalize_text(value)
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        text = text.replace("[", "").replace("]", "").replace("'", "").replace(chr(34), "")
        return [part.strip() for part in text.split(",") if part.strip()]
    if "," in text:
        return [part.strip() for part in text.split(",") if part.strip()]
    if ";" in text:
        return [part.strip() for part in text.split(";") if part.strip()]
    return [text]

def to_ready_map(rows):
    ready_map = {}
    for row in rows:
        sku = normalize_text(row.get("sku") or row.get("SKU"))
        if sku:
            ready_map[sku] = row
    return ready_map

def build_row(mapped_row, ready_row):
    sku = normalize_text(mapped_row.get("SKU") or ready_row.get("sku") or ready_row.get("SKU"))
    title = normalize_text(mapped_row.get("Title") or ready_row.get("title"))
    category = normalize_text(mapped_row.get("Category") or ready_row.get("category"))
    brand = normalize_text(mapped_row.get("Brand") or ready_row.get("brand"))
    model = normalize_text(mapped_row.get("Model") or ready_row.get("model"))
    product_type = normalize_text(mapped_row.get("ProductType") or mapped_row.get("Product Type") or ready_row.get("product_type"))
    color = normalize_text(mapped_row.get("Color") or ready_row.get("color"))
    cable_length = normalize_text(mapped_row.get("CableLength") or mapped_row.get("Cable Length") or ready_row.get("cable_length"))
    connectivity = normalize_text(mapped_row.get("Connectivity") or ready_row.get("connectivity"))
    features = normalize_features(mapped_row.get("Features") or ready_row.get("features"))
    description = normalize_text(ready_row.get("description") or mapped_row.get("Description"))
    price = ready_row.get("price", mapped_row.get("Price", ""))
    photo_files = normalize_photo_files(mapped_row.get("PhotoFiles") or ready_row.get("photo_files"))
    photo_count = len(photo_files)
    photo_1 = photo_files[0] if len(photo_files) > 0 else ""
    photo_2 = photo_files[1] if len(photo_files) > 1 else ""
    photo_3 = photo_files[2] if len(photo_files) > 2 else ""
    photo_4 = photo_files[3] if len(photo_files) > 3 else ""
    photo_5 = photo_files[4] if len(photo_files) > 4 else ""
    photo_6 = photo_files[5] if len(photo_files) > 5 else ""
    photo_7 = photo_files[6] if len(photo_files) > 6 else ""
    return {
        "Action": "Add",
        "SKU": sku,
        "Category": category,
        "Title": title,
        "Description": description,
        "Format": "FixedPrice",
        "Quantity": "1",
        "Price": price,
        "ConditionID": "1000",
        "Brand": brand,
        "MPN": model,
        "Model": model,
        "ProductType": product_type,
        "Color": color,
        "CableLength": cable_length,
        "Connectivity": connectivity,
        "Features": features,
        "PhotoCount": photo_count,
        "Photo1": photo_1,
        "Photo2": photo_2,
        "Photo3": photo_3,
        "Photo4": photo_4,
        "Photo5": photo_5,
        "Photo6": photo_6,
        "Photo7": photo_7,
        "PhotoFiles": "; ".join(photo_files),
        "Source": "real_ebay_template_export_v1",
    }

def main():
    mapped_data = load_json(MAPPED_JSON)
    ready_data = load_json(READY_JSON)
    mapped_rows = extract_mapped_rows(mapped_data)
    ready_rows = extract_ready_rows(ready_data)
    ready_map = to_ready_map(ready_rows)
    export_rows = []
    for mapped_row in mapped_rows:
        sku = normalize_text(mapped_row.get("SKU"))
        ready_row = ready_map.get(sku, {})
        export_rows.append(build_row(mapped_row, ready_row))
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["Action", "SKU", "Category", "Title", "Description", "Format", "Quantity", "Price", "ConditionID", "Brand", "MPN", "Model", "ProductType", "Color", "CableLength", "Connectivity", "Features", "PhotoCount", "Photo1", "Photo2", "Photo3", "Photo4", "Photo5", "Photo6", "Photo7", "PhotoFiles", "Source"]
    output_data = {"summary": {"mapped_input_rows": len(mapped_rows), "ready_input_rows": len(ready_rows), "exported_rows": len(export_rows), "output_csv": str(OUTPUT_CSV)}, "fieldnames": fieldnames, "rows": export_rows}
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(export_rows)
    print("REAL_EBAY_TEMPLATE_EXPORT_V1:")
    print(f"mapped_input_rows: {len(mapped_rows)}")
    print(f"ready_input_rows: {len(ready_rows)}")
    print(f"exported_rows: {len(export_rows)}")
    print(f"output_json: {OUTPUT_JSON}")
    print(f"output_csv: {OUTPUT_CSV}")
    if export_rows:
        sample = export_rows[0]
        print(f"sample_sku: {sample['SKU']}")
        print(f"sample_title: {sample['Title']}")
        print(f"sample_features: {sample['Features']}")
        print(f"sample_photo_count: {sample['PhotoCount']}")

if __name__ == "__main__":
    main()
