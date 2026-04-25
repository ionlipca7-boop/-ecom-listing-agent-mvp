import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / 'storage'
PRODUCTS_DIR = STORAGE_DIR / 'products'
EXPORTS_DIR = STORAGE_DIR / 'exports'
LISTINGS_FILE = EXPORTS_DIR / 'generated_listings.json'
OUTPUT_FILE = EXPORTS_DIR / 'ready_report_v1.json'

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception:
        return default

def count_photos(product_dir):
    photos_dir = product_dir / 'photos'
    if not photos_dir.exists():
        return 0

    allowed = {'.jpg', '.jpeg', '.png', '.webp'}
    count = 0

    for file in photos_dir.iterdir():
        if file.is_file() and file.suffix.lower() in allowed:
            count += 1

    return count

def is_filled(value):
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (int, float)):
        return value > 0
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, dict):
        return len(value) > 0
    return True

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    listings = read_json(LISTINGS_FILE, [])
    listings_by_sku = {}

    for item in listings:
        if isinstance(item, dict):
            sku = str(item.get('sku', '')).strip()
            if sku:
                listings_by_sku[sku] = item

    report_items = []
    total_products = 0
    ready_count = 0
    draft_count = 0

    if PRODUCTS_DIR.exists():
        for product_dir in sorted(PRODUCTS_DIR.iterdir()):
            if not product_dir.is_dir():
                continue

            product_data = read_json(product_dir / 'product.json', {})
            if not isinstance(product_data, dict):
                product_data = {}

            sku = str(product_data.get('sku', '')).strip() or product_dir.name
            listing = listings_by_sku.get(sku, {})
            photo_count = count_photos(product_dir)

            checks = {
                'product_json_exists': (product_dir / 'product.json').exists(),
                'sku_present': is_filled(product_data.get('sku')),
                'title_present': is_filled(listing.get('title')),
                'description_present': is_filled(listing.get('description')),
                'price_present': is_filled(listing.get('price')),
                'photos_present': photo_count > 0,
                'photos_full_set_7': photo_count >= 7
            }

            missing = []
            for key, value in checks.items():
                if not value:
                    missing.append(key)

            recommendations = []
            if not checks['title_present']:
                recommendations.append('ADD_TITLE')
            if not checks['description_present']:
                recommendations.append('ADD_DESCRIPTION')
            if not checks['price_present']:
                recommendations.append('ADD_PRICE')
            if not checks['photos_present']:
                recommendations.append('ADD_PHOTOS')
            elif not checks['photos_full_set_7']:
                recommendations.append('COMPLETE_7_PHOTO_SET')

            is_ready = (
                checks['product_json_exists']
                and checks['sku_present']
                and checks['title_present']
                and checks['description_present']
                and checks['price_present']
                and checks['photos_present']
            )

            item_status = 'ready' if is_ready else 'draft'

            report_items.append({
                'sku': sku,
                'status': item_status,
                'photo_count': photo_count,
                'checks': checks,
                'missing': missing,
                'recommendations': recommendations
            })

            total_products += 1
            if is_ready:
                ready_count += 1
            else:
                draft_count += 1

    result = {
        'summary': {
            'total_products': total_products,
            'ready': ready_count,
            'draft': draft_count
        },
        'items': report_items
    }

    OUTPUT_FILE.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print('READY SYSTEM V1:')
    print(f'total_products: {total_products}')
    print(f'ready: {ready_count}')
    print(f'draft: {draft_count}')
    print(f'output_file: {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
