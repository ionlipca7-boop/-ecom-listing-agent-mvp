import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / 'storage'
PRODUCTS_DIR = STORAGE_DIR / 'products'
EXPORTS_DIR = STORAGE_DIR / 'exports'
OUTPUT_FILE = EXPORTS_DIR / 'photo_manifest_v1.json'
SKIP_DIR_NAMES = {'_template', '__pycache__'}
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception:
        return default

def should_skip_product_dir(product_dir):
    if product_dir.name in SKIP_DIR_NAMES:
        return True
    if not (product_dir / 'product.json').exists():
        return True
    return False

def collect_photo_files(photos_dir):
    files = []
    if not photos_dir.exists():
        return files

    for file in sorted(photos_dir.iterdir()):
        if file.is_file() and file.suffix.lower() in ALLOWED_EXTENSIONS:
            files.append(file.name)

    return files

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    items = []
    total_products = 0
    total_photos = 0

    if PRODUCTS_DIR.exists():
        for product_dir in sorted(PRODUCTS_DIR.iterdir()):
            if not product_dir.is_dir():
                continue

            if should_skip_product_dir(product_dir):
                continue

            product_data = read_json(product_dir / 'product.json', {})
            if not isinstance(product_data, dict):
                product_data = {}

            sku = str(product_data.get('sku', '')).strip() or product_dir.name
            photos_dir = product_dir / 'photos'
            photo_files = collect_photo_files(photos_dir)
            photo_count = len(photo_files)
            has_photos = photo_count > 0
            has_full_set_7 = photo_count >= 7

            items.append({
                'sku': sku,
                'photos_dir': str(photos_dir),
                'photo_count': photo_count,
                'has_photos': has_photos,
                'has_full_set_7': has_full_set_7,
                'photo_files': photo_files
            })

            total_products += 1
            total_photos += photo_count

    result = {
        'summary': {
            'total_products': total_products,
            'total_photos': total_photos
        },
        'items': items
    }

    OUTPUT_FILE.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print('PHOTO MANIFEST V1:')
    print(f'total_products: {total_products}')
    print(f'total_photos: {total_photos}')
    print(f'output_file: {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
