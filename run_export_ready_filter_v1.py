import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / 'storage'
EXPORTS_DIR = STORAGE_DIR / 'exports'
READY_FILE = EXPORTS_DIR / 'ready_report_v2.json'
LISTINGS_FILE = EXPORTS_DIR / 'generated_listings.json'
OUTPUT_FILE = EXPORTS_DIR / 'ready_listings_v1.json'

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception:
        return default

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    ready_report = read_json(READY_FILE, {})
    listings = read_json(LISTINGS_FILE, [])

    ready_items = ready_report.get('items', [])
    ready_skus = set()

    for item in ready_items:
        if item.get('status') == 'ready':
            sku = str(item.get('sku', '')).strip()
            if sku:
                ready_skus.add(sku)

    ready_listings = []
    skipped_listings = []

    for listing in listings:
        if not isinstance(listing, dict):
            continue

        sku = str(listing.get('sku', '')).strip()
        if sku in ready_skus:
            ready_listings.append(listing)
        else:
            skipped_listings.append(sku)

    result = {
        'summary': {
            'ready_sku_count': len(ready_skus),
            'ready_listing_count': len(ready_listings),
            'skipped_listing_count': len(skipped_listings)
        },
        'ready_skus': sorted(ready_skus),
        'ready_listings': ready_listings,
        'skipped_listings': skipped_listings
    }

    OUTPUT_FILE.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print('EXPORT READY FILTER V1:')
    print(f'ready_sku_count: {len(ready_skus)}')
    print(f'ready_listing_count: {len(ready_listings)}')
    print(f'skipped_listing_count: {len(skipped_listings)}')
    print(f'output_file: {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
