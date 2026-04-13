import json
from datetime import datetime
from pathlib import Path


def detect_listing_kind(product):
    product_type = str(product.get("type") or product.get("name", "")).lower()

    if any(keyword in product_type for keyword in ("ladegerät", "ladegerat", "charger", "netzteil", "adapter")):
        return "charger"
    if any(keyword in product_type for keyword in ("kabel", "cable")):
        return "cable"
    return "generic"


def generate_title(product):
    """
    eBay SEO Title Generator
    Structure:
    Power + Product Type + Length + Keywords
    """

    power = product.get("power", "")
    length = product.get("length", "")
    product_type = product.get("type") or product.get("name", "Kabel")
    listing_kind = detect_listing_kind(product)

    parts = []

    # Power (например 60W)
    if power:
        parts.append(f"{power}")

    # Product type (например USB-C Ladekabel)
    if listing_kind == "charger":
        parts.append("USB-C Ladegerät")
    elif "usb-c" in product_type.lower():
        parts.append("USB-C Ladekabel")
    else:
        parts.append(product_type)

    # Length (например 2m)
    if length and listing_kind != "charger":
        parts.append(f"{length}")

    # SEO Keywords
    parts.append("Schnellladen")
    if listing_kind == "charger":
        parts.append("Netzteil")
    else:
        parts.append("Datenkabel")

    # Финальная сборка
    title = " ".join(parts)

    # Ограничение eBay (80 символов)
    return title[:80]


class ListingBrain:
    def generate_title(self, product):
        return generate_title(product)

    def generate_category(self, product):
        listing_kind = detect_listing_kind(product)
        if listing_kind == "cable":
            return "Kabel & Adapter"
        if listing_kind == "charger":
            return "Ladegeräte"
        return "Handy-Zubehör"

    def generate_description(self, product):
        product_type = product.get("type") or product.get("name", "Kabel")
        power = product.get("power", "")
        length = product.get("length", "")
        listing_kind = detect_listing_kind(product)

        lines = [f"Typ: {product_type}"]
        lines.append(f"Leistung: {power} + Schnellladen" if power else "Leistung: Schnellladen")
        if listing_kind == "charger":
            lines.append("Hinweis: Ladegerät, Kabel kann als Zubehör enthalten sein.")
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
        listing_kind = detect_listing_kind(product)
        connection = "USB-C" if "usb-c" in str(product_type).lower() else ""

        return {
            "Typ": product_type,
            "Länge": length if listing_kind == "cable" else "",
            "Leistung": power,
            "Anschluss": connection,
            "Produktart": "Ladegerät" if listing_kind == "charger" else "Kabel" if listing_kind == "cable" else "Zubehör",
            "Zustand": "Neu",
        }

    def generate_images(self, product):
        return [
            "image_main.jpg",
            "image_angle.jpg",
            "image_detail.jpg"
        ]

    def generate_search_intents(self, product):
        power = str(product.get("power", "")).lower()
        length = str(product.get("length", "")).lower()
        listing_kind = detect_listing_kind(product)

        if listing_kind == "charger":
            intents = [
                f"{power} usb c charger".strip(),
                "usb c netzteil schnellladen",
                f"{power} usb c ladegerät".strip(),
            ]
            if length:
                intents.append(f"usb c ladegerät mit {length} kabel")
            return [intent for intent in intents if intent]

        cable_intents = [
            f"usb c cable {length} fast charging".strip(),
            f"{power} usb c cable".strip(),
            "usb c kabel schnellladen",
        ]
        return [intent for intent in cable_intents if intent]

    def generate_compatibility_keywords(self, product):
        listing_kind = detect_listing_kind(product)
        if listing_kind == "charger":
            return ["USB-C Geräte", "Samsung", "Android", "iPad", "MacBook"]
        return ["USB-C Geräte", "Samsung", "Android", "MacBook"]

    def generate_use_case_keywords(self, product):
        listing_kind = detect_listing_kind(product)
        base = ["Schnellladen", "Alltag", "Reise", "Büro", "Zuhause"]
        if listing_kind == "charger":
            return base + ["Ersatznetzteil"]
        return base + ["Datenübertragung"]

    def generate_seo_keywords(self, product):
        listing_kind = detect_listing_kind(product)
        power = product.get("power", "")
        length = product.get("length", "")
        if listing_kind == "charger":
            return [f"USB-C Ladegerät {power}".strip(), "Schnelllade-Netzteil", "USB-C Charger", "Reise Ladegerät"]
        return [f"USB-C Kabel {length}".strip(), f"USB-C {power}".strip(), "Schnellladekabel", "Datenkabel"]

    def generate_buyer_questions(self, product):
        listing_kind = detect_listing_kind(product)
        length = product.get("length", "")
        if listing_kind == "charger":
            return [
                "Ist das Ladegerät für USB-C Geräte geeignet?",
                "Unterstützt das Ladegerät Schnellladen?",
                "Ist ein Kabel im Lieferumfang enthalten?",
            ]
        return [
            "Ist das Kabel für Schnellladen geeignet?",
            f"Wie lang ist das Kabel ({length})?".strip(),
            "Passt das Kabel zu meinem USB-C Gerät?",
        ]

    def generate_ai_summary(self, product):
        listing_kind = detect_listing_kind(product)
        power = product.get("power", "")
        length = product.get("length", "")
        if listing_kind == "charger":
            return (
                f"Kompaktes USB-C Ladegerät mit {power} für schnelles und zuverlässiges Laden "
                "im Alltag, im Büro und auf Reisen."
            ).strip()
        return (
            f"Robustes USB-C Kabel mit {length} Länge und {power}, geeignet für Schnellladen "
            "und tägliche Nutzung zu Hause, im Büro oder unterwegs."
        ).strip()

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

    def generate_publish_ready(self, listing):
        return listing.get("listing_quality_score", 0) >= 80

    def generate_warnings(self, listing):
        warnings = []

        if not listing.get("title"):
            warnings.append("Missing title")
        if not listing.get("category"):
            warnings.append("Missing category")
        if not listing.get("description"):
            warnings.append("Missing description")
        if not listing.get("price"):
            warnings.append("Missing price")

        item_specifics = listing.get("item_specifics")
        if not isinstance(item_specifics, dict) or not item_specifics:
            warnings.append("Missing item specifics")

        images = listing.get("images")
        if not isinstance(images, list) or len(images) < 3:
            warnings.append("Not enough images")

        if listing.get("listing_quality_score", 0) < 80:
            warnings.append("Quality score below publish threshold")

        return warnings

    def generate_improvements(self, listing):
        improvements = []

        title = listing.get("title", "")
        if len(title) < 55:
            improvements.append("Title could be longer for better SEO")

        description = listing.get("description", "")
        if "Kompatibel" not in description:
            improvements.append("Add compatibility info to description")

        item_specifics = listing.get("item_specifics")
        if not isinstance(item_specifics, dict) or len(item_specifics) < 5:
            improvements.append("Add more item specifics")

        images = listing.get("images")
        if not isinstance(images, list) or len(images) < 5:
            improvements.append("Add more product images")

        price = listing.get("price")
        if price is not None and price < 6:
            improvements.append("Review pricing strategy")

        if listing.get("listing_quality_score", 0) < 100:
            improvements.append("Improve listing to reach maximum quality score")

        return improvements

    def generate_final_listing_bundle(self, listing):
        return {
            "title": listing.get("title"),
            "category": listing.get("category"),
            "description": listing.get("description"),
            "price": listing.get("price"),
            "item_specifics": listing.get("item_specifics", {}),
            "images": listing.get("images", []),
            "search_intents": listing.get("search_intents", []),
            "compatibility_keywords": listing.get("compatibility_keywords", []),
            "use_case_keywords": listing.get("use_case_keywords", []),
            "seo_keywords": listing.get("seo_keywords", []),
            "buyer_questions": listing.get("buyer_questions", []),
            "ai_summary": listing.get("ai_summary", ""),
            "status": listing.get("status"),
            "publish_ready": listing.get("publish_ready", False),
        }

    def create_listing(self, product):
        listing = {
            "title": self.generate_title(product),
            "category": self.generate_category(product),
            "description": self.generate_description(product),
            "price": self.generate_price(product),
            "item_specifics": self.generate_item_specifics(product),
            "images": self.generate_images(product),
            "search_intents": self.generate_search_intents(product),
            "compatibility_keywords": self.generate_compatibility_keywords(product),
            "use_case_keywords": self.generate_use_case_keywords(product),
            "seo_keywords": self.generate_seo_keywords(product),
            "buyer_questions": self.generate_buyer_questions(product),
            "ai_summary": self.generate_ai_summary(product),
            "status": "draft",
        }
        listing["listing_quality_score"] = self.generate_quality_score(listing)
        listing["publish_ready"] = self.generate_publish_ready(listing)
        listing["listing_warnings"] = self.generate_warnings(listing)
        listing["listing_improvements"] = self.generate_improvements(listing)
        listing["final_listing_bundle"] = self.generate_final_listing_bundle(listing)
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
