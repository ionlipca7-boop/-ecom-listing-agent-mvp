import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
HEADER_DETECT_JSON = EXPORTS_DIR / "ebay_template_header_detect_v1.json"
SOURCE_JSON = EXPORTS_DIR / "real_ebay_template_export_v1.json"
OUTPUT_JSON = EXPORTS_DIR / "real_ebay_template_header_mapped_v1.json"
OUTPUT_CSV = EXPORTS_DIR / "real_ebay_template_header_mapped_v1.csv"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def find_template_info():
    data = load_json(HEADER_DETECT_JSON)
    results = data.get("results", [])
    if not results:
        raise RuntimeError("No template detection results found")
    item = results[0]
    return Path(item["template_file"]), item["columns"]

def load_source_rows():
    data = load_json(SOURCE_JSON)
    rows = data.get("rows", [])
    return rows if isinstance(rows, list) else []

def empty_template_row(header):
    return {col: "" for col in header}

def map_row(src, header):
    row = empty_template_row(header)
    action_header = header[0]
    row[action_header] = src.get("Action", "Add")
    row["CustomLabel"] = src.get("SKU", "")
    row["*Category"] = src.get("Category", "")
    row["*Title"] = src.get("Title", "")
    row["*ConditionID"] = src.get("ConditionID", "1000")
    row["*C:Marke"] = src.get("Brand", "")
    row["*C:Produktart"] = src.get("ProductType", "")
    row["C:Konnektivität"] = src.get("Connectivity", "")
    row["C:Kabellänge"] = src.get("CableLength", "")
    row["C:Farbe"] = src.get("Color", "")
    row["C:Herstellernummer"] = src.get("MPN", "")
    row["C:Besonderheiten"] = src.get("Features", "")
    row["PicURL"] = src.get("Photo1", "")
    row["*Description"] = src.get("Description", "")
    row["*Format"] = src.get("Format", "FixedPrice")
    row["*Duration"] = "GTC"
    row["*StartPrice"] = src.get("Price", "")
    row["*Quantity"] = src.get("Quantity", "1")
    row["ImmediatePayRequired"] = "1"
    row["*Location"] = "Delmenhorst"
    row["ShippingType"] = "Flat"
    row["ShippingService-1:Option"] = "DE_DHLPaket"
    row["ShippingService-1:Cost"] = "0.0"
    row["*DispatchTimeMax"] = "3"
    row["*ReturnsAcceptedOption"] = "ReturnsAccepted"
    row["ReturnsWithinOption"] = "Days_30"
    row["RefundOption"] = "MoneyBack"
    row["ShippingCostPaidByOption"] = "Buyer"
    return row

def main():
    template_file, header = find_template_info()
    source_rows = load_source_rows()
    mapped_rows = [map_row(src, header) for src in source_rows]
    output_data = {
        "summary": {
            "template_file": str(template_file),
            "header_column_count": len(header),
            "source_row_count": len(source_rows),
            "mapped_row_count": len(mapped_rows),
        },
        "header": header,
        "rows": mapped_rows,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter=";")
        writer.writeheader()
        writer.writerows(mapped_rows)
    print("REAL_EBAY_TEMPLATE_HEADER_MAPPER_V1:")
    print(f"template_file: {template_file}")
    print(f"header_column_count: {len(header)}")
    print(f"source_row_count: {len(source_rows)}")
    print(f"mapped_row_count: {len(mapped_rows)}")
    print(f"output_json: {OUTPUT_JSON}")
    print(f"output_csv: {OUTPUT_CSV}")
    if mapped_rows:
        sample = mapped_rows[0]
        print(f"sample_action: {sample[header[0]]}")
        print(f"sample_title: {sample['*Title']}")
        print(f"sample_category: {sample['*Category']}")
        print(f"sample_brand: {sample['*C:Marke']}")

if __name__ == "__main__":
    main()
