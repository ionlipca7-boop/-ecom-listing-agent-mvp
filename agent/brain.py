import json
from datetime import datetime
from pathlib import Path


def generate_title(product):
    """
    eBay SEO Title Generator
    Structure:
    Power + Product Type + Length + Keywords
    """

    power = product.get("power", "")
    length = product.get("length", "")
    product_type = product.get("type") or product.get("name", "Kabel")

    parts = []

    # Power (например 60W)
    if power:
        parts.append(f"{power}")

    # Product type (например USB-C Ladekabel)
    if "usb-c" in product_type.lower():
        parts.append("USB-C Ladekabel")
    else:
        parts.append(product_type)

    # Length (например 2m)
    if length:
        parts.append(f"{length}")

    # SEO Keywords
    parts.append("Schnellladen")
    parts.append("Datenkabel")

    # Финальная сборка
    title = " ".join(parts)

    # Ограничение eBay (80 символов)
    return title[:80]


class ListingBrain:
    def generate_title(self, product):
        return generate_title(product)

    def generate_category(self, product):
        product_type = str(product.get("type") or product.get("name", "")).lower()
        if any(keyword in product_type for keyword in ("kabel", "cable", "usb-c")):
            return "Kabel & Adapter"
        if any(keyword in product_type for keyword in ("ladegerät", "charger", "netzteil")):
            return "Ladegeräte"
        return "Handy-Zubehör"

    def generate_description(self, product):
        product_type = product.get("type") or product.get("name", "Kabel")
        power = product.get("power", "")
        length = product.get("length", "")

        lines = [f"Typ: {product_type}"]
        lines.append(f"Leistung: {power} + Schnellladen" if power else "Leistung: Schnellladen")
        lines.append(f"Länge: {length}" if length else "Länge: Praktisch")
        lines.append("Zuverlässige Qualität für hohe Kompatibilität.")
        lines.append("✔ Schnellladen")
        lines.append("✔ Hohe Qualität")
        lines.append("✔ Kompatibel mit vielen Geräten")
        return "\n".join(lines)

    def generate_price(self, product):
        power = product.get("power")
        if not power:
            return 4.99

        digits = "".join(ch for ch in str(power) if ch.isdigit())
        if not digits:
            return 4.99

        watts = int(digits)
        if watts >= 60:
            return 7.99
        if watts >= 30:
            return 6.49
        return 4.99

    def generate_item_specifics(self, product):
        product_type = product.get("type") or product.get("name", "Kabel")
        length = product.get("length", "")
        power = product.get("power", "")
        connection = "USB-C" if "usb-c" in str(product_type).lower() else ""

        return {
            "Typ": product_type,
            "Länge": length,
            "Leistung": power,
            "Anschluss": connection,
            "Zustand": "Neu",
        }

    def generate_images(self, product):
        return [
            "image_main.jpg",
            "image_angle.jpg",
            "image_detail.jpg"
        ]

    def generate_quality_score(self, listing):
        score = 0

        if listing.get("title"):
            score += 20
        if listing.get("category"):
            score += 15
        if listing.get("description"):
            score += 20
        if listing.get("price") is not None:
            score += 15

        item_specifics = listing.get("item_specifics")
        if isinstance(item_specifics, dict) and item_specifics:
            score += 15

        images = listing.get("images")
        if isinstance(images, list) and len(images) >= 3:
            score += 15

        return min(score, 100)

    def create_listing(self, product):
        listing = {
            "title": self.generate_title(product),
            "category": self.generate_category(product),
            "description": self.generate_description(product),
            "price": self.generate_price(product),
            "item_specifics": self.generate_item_specifics(product),
            "images": self.generate_images(product),
            "status": "draft",
        }
        listing["listing_quality_score"] = self.generate_quality_score(listing)
        drafts_dir = Path("drafts")
        drafts_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        draft_path = drafts_dir / f"draft_{timestamp}.json"
        counter = 1
        while draft_path.exists():
            draft_path = drafts_dir / f"draft_{timestamp}_{counter}.json"
            counter += 1
        with draft_path.open("w", encoding="utf-8") as f:
            json.dump(listing, f, ensure_ascii=False, indent=2)
        return listing

    # Совместимость с test_run.py
    def create_listing_plan(self, product):
        return self.create_listing(product)
