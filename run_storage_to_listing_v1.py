import json
from pathlib import Path
from typing import Any

PRODUCTS_DIR = Path("storage/products")
OUTPUT_FILE = Path("storage/exports/generated_listings.json")


def load_products() -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []

    if not PRODUCTS_DIR.exists() or not PRODUCTS_DIR.is_dir():
        return products

    for product_dir in PRODUCTS_DIR.iterdir():
        if not product_dir.is_dir() or product_dir.name == "_template":
            continue

        product_file = product_dir / "product.json"
        if not product_file.exists():
            continue

        try:
            with product_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                data["__dir__"] = str(product_dir)
                products.append(data)
        except (OSError, json.JSONDecodeError):
            continue

    return products


def generate_title(product: dict[str, Any]) -> str:
    parts: list[str] = []

    power = str(product.get("power", "")).strip()
    name = str(product.get("name", "")).strip()
    length = str(product.get("length", "")).strip()

    if power:
        parts.append(power)
    if name:
        parts.append(name)
    if length:
        parts.append(length)

    title = " ".join(parts).strip()
    return title[:80]


def generate_description(product: dict[str, Any]) -> str:
    lines: list[str] = []

    name = str(product.get("name", "")).strip()
    power = str(product.get("power", "")).strip()
    length = str(product.get("length", "")).strip()
    features = product.get("features", [])

    if name:
        lines.append(f"Produkt: {name}")
    if power:
        lines.append(f"Leistung: {power}")
    if length:
        lines.append(f"Länge: {length}")

    if isinstance(features, list):
        for feature in features:
            feature_text = str(feature).strip()
            if feature_text:
                lines.append(f"- {feature_text}")

    return "\n".join(lines)


def generate_price(product: dict[str, Any]) -> float:
    cost = product.get("cost_price", 0)

    try:
        cost_value = float(cost)
    except (TypeError, ValueError):
        cost_value = 0.0

    if cost_value > 0:
        return round(cost_value * 2.2, 2)

    return 5.5


def generate_listing(product: dict[str, Any]) -> dict[str, Any]:
    return {
        "sku": product.get("sku"),
        "title": generate_title(product),
        "description": generate_description(product),
        "price": generate_price(product),
        "status": "draft",
    }


def main() -> None:
    products = load_products()
    listings = [generate_listing(product) for product in products]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8-sig") as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

    print("GENERATED LISTINGS:")
    print(f"products_found: {len(products)}")
    print(f"listings_created: {len(listings)}")
    print(f"output_file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()