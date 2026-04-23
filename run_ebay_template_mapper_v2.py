import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / 'storage'
PRODUCTS_DIR = STORAGE_DIR / 'products'
EXPORTS_DIR = STORAGE_DIR / 'exports'
READY_LISTINGS_FILE = EXPORTS_DIR / 'ready_listings_v1.json'
PHOTO_MANIFEST_FILE = EXPORTS_DIR / 'photo_manifest_v1.json'
OUTPUT_CSV_FILE = EXPORTS_DIR / 'ebay_template_mapped_v2.csv'
OUTPUT_JSON_FILE = EXPORTS_DIR / 'ebay_template_mapped_v2.json'

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception:
        return default

def find_product_data_by_sku(sku):
    if not PRODUCTS_DIR.exists():
        return {}

    for product_dir in sorted(PRODUCTS_DIR.iterdir()):
        if not product_dir.is_dir():
            continue

        product_file = product_dir / 'product.json'
        if not product_file.exists():
            continue

        try:
            product_data = json.loads(product_file.read_text(encoding='utf-8-sig'))
        except Exception:
            continue

        product_sku = str(product_data.get('sku', '')).strip()
        if product_sku == sku:
            return product_data

    return {}

def build_photo_lookup(photo_manifest):
    lookup = {}
    items = photo_manifest.get('items', [])

    for item in items:
        if not isinstance(item, dict):
            continue
        sku = str(item.get('sku', '')).strip()
        if sku:
            lookup[sku] = item

    return lookup

def join_photo_names(photo_files):
    if not isinstance(photo_files, list):
        return ''
    return ', '.join(photo_files)

def build_row(listing, product_data, photo_item):
    sku = str(listing.get('sku', '')).strip()
    title = str(listing.get('title', '')).strip()
    description = str(listing.get('description', '')).strip()
    price = listing.get('price', '')

    category = str(product_data.get('category', 'Kabel and Adapter')).strip()
    brand = str(product_data.get('brand', 'Generic')).strip()
    model = str(product_data.get('model', sku)).strip()
    product_type = str(product_data.get('product_type', 'USB-C Ladekabel')).strip()
    color = str(product_data.get('color', 'Schwarz')).strip()
    cable_length = str(product_data.get('length', '2m')).strip()
    connectivity = str(product_data.get('connectivity', 'USB-C')).strip()
    features = str(product_data.get('features', 'Schnellladen, Datenuebertragung')).strip()

    photo_count = photo_item.get('photo_count', 0) if isinstance(photo_item, dict) else 0
    photo_files = photo_item.get('photo_files', []) if isinstance(photo_item, dict) else []
    photo_names = join_photo_names(photo_files)

    return {
        'Action': 'Add',
        'SKU': sku,
        'Category': category,
        'Title': title,
        'Description': description,
        'Price': price,
        'Quantity': 1,
        'Condition': 'New',
        'Format': 'FixedPrice',
        'Brand': brand,
        'Model': model,
        'ProductType': product_type,
        'Color': color,
        'CableLength': cable_length,
        'Connectivity': connectivity,
        'Features': features,
        'PhotoCount': photo_count,
        'PhotoFiles': photo_names
    }

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    ready_data = read_json(READY_LISTINGS_FILE, {})
    photo_manifest = read_json(PHOTO_MANIFEST_FILE, {})

    ready_listings = ready_data.get('ready_listings', [])
    photo_lookup = build_photo_lookup(photo_manifest)

    rows = []
    for listing in ready_listings:
        if not isinstance(listing, dict):
            continue

        sku = str(listing.get('sku', '')).strip()
        product_data = find_product_data_by_sku(sku)
        photo_item = photo_lookup.get(sku, {})
        rows.append(build_row(listing, product_data, photo_item))

    fieldnames = [
        'Action',
        'SKU',
        'Category',
        'Title',
        'Description',
        'Price',
        'Quantity',
        'Condition',
        'Format',
        'Brand',
        'Model',
        'ProductType',
        'Color',
        'CableLength',
        'Connectivity',
        'Features',
        'PhotoCount',
        'PhotoFiles'
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

    print('EBAY TEMPLATE MAPPER V2:')
    print(f'mapped_rows: {len(rows)}')
    print(f'csv_file: {OUTPUT_CSV_FILE}')
    print(f'json_file: {OUTPUT_JSON_FILE}')

if __name__ == '__main__':
    main()
