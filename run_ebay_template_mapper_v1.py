import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / 'storage'
EXPORTS_DIR = STORAGE_DIR / 'exports'
READY_LISTINGS_FILE = EXPORTS_DIR / 'ready_listings_v1.json'
OUTPUT_CSV_FILE = EXPORTS_DIR / 'ebay_template_mapped_v1.csv'
OUTPUT_JSON_FILE = EXPORTS_DIR / 'ebay_template_mapped_v1.json'

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception:
        return default

def build_row(listing):
    title = str(listing.get('title', '')).strip()
    description = str(listing.get('description', '')).strip()
    price = listing.get('price', '')
    sku = str(listing.get('sku', '')).strip()

    return {
        'Action': 'Add',
        'SKU': sku,
        'Title': title,
        'Description': description,
        'Price': price,
        'Quantity': 1,
        'Condition': 'New',
        'Format': 'FixedPrice'
    }

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    ready_data = read_json(READY_LISTINGS_FILE, {})
    ready_listings = ready_data.get('ready_listings', [])

    rows = []
    for listing in ready_listings:
        if not isinstance(listing, dict):
            continue
        rows.append(build_row(listing))

    fieldnames = [
        'Action',
        'SKU',
        'Title',
        'Description',
        'Price',
        'Quantity',
        'Condition',
        'Format'
    ]

    with OUTPUT_CSV_FILE.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

    result = {
        'summary': {
            'mapped_rows': len(rows),
            'csv_file': str(OUTPUT_CSV_FILE)
        },
        'fieldnames': fieldnames,
        'rows': rows
    }

    OUTPUT_JSON_FILE.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print('EBAY TEMPLATE MAPPER V1:')
    print(f'mapped_rows: {len(rows)}')
    print(f'csv_file: {OUTPUT_CSV_FILE}')
    print(f'json_file: {OUTPUT_JSON_FILE}')

if __name__ == '__main__':
    main()
