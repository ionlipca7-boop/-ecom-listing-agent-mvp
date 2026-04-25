import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / 'storage'
EXPORTS_DIR = STORAGE_DIR / 'exports'
READY_FILE = EXPORTS_DIR / 'ready_report_v2.json'
LISTINGS_FILE = EXPORTS_DIR / 'generated_listings.json'
OUTPUT_FILE = EXPORTS_DIR / 'control_room_status_v2.json'

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception:
        return default

def build_next_action(summary, items):
    total_products = summary.get('total_products', 0)
    ready_count = summary.get('ready', 0)
    draft_count = summary.get('draft', 0)

    if total_products == 0:
        return 'ADD_FIRST_PRODUCT'

    if ready_count > 0:
        return 'EXPORT_READY_PRODUCTS_TO_EBAY_TEMPLATE'

    for item in items:
        recommendations = item.get('recommendations', [])
        if 'ADD_PHOTOS' in recommendations:
            return 'ADD_PHOTOS_TO_PRODUCTS'
        if 'COMPLETE_7_PHOTO_SET' in recommendations:
            return 'COMPLETE_PHOTO_SET'
        if 'ADD_TITLE' in recommendations:
            return 'FIX_TITLE'
        if 'ADD_DESCRIPTION' in recommendations:
            return 'FIX_DESCRIPTION'
        if 'ADD_PRICE' in recommendations:
            return 'FIX_PRICE'

    if draft_count > 0:
        return 'FIX_DRAFT_PRODUCTS'

    return 'SYSTEM_OK'

def main():
    ready_report = read_json(READY_FILE, {})
    listings = read_json(LISTINGS_FILE, [])

    summary = ready_report.get('summary', {})
    items = ready_report.get('items', [])

    total_products = summary.get('total_products', 0)
    ready_count = summary.get('ready', 0)
    draft_count = summary.get('draft', 0)
    listings_count = len(listings) if isinstance(listings, list) else 0

    blocked_products = []
    for item in items:
        if item.get('status') != 'ready':
            blocked_products.append({
                'sku': item.get('sku', ''),
                'missing': item.get('missing', []),
                'recommendations': item.get('recommendations', [])
            })

    status = 'READY' if ready_count > 0 else 'BLOCKED'
    next_action = build_next_action(summary, items)

    result = {
        'control_room_status': status,
        'next_action': next_action,
        'summary': {
            'total_products': total_products,
            'ready_products': ready_count,
            'draft_products': draft_count,
            'generated_listings': listings_count
        },
        'blocked_products': blocked_products
    }

    OUTPUT_FILE.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print('CONTROL ROOM STATUS V2:')
    print(f'control_room_status: {status}')
    print(f'next_action: {next_action}')
    print(f'total_products: {total_products}')
    print(f'ready_products: {ready_count}')
    print(f'draft_products: {draft_count}')
    print(f'output_file: {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
