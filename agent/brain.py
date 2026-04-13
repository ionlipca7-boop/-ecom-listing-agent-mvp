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

    def generate_description(self, product):
        product_type = product.get("type") or product.get("name", "Kabel")
        power = product.get("power", "")
        length = product.get("length", "")

        lines = [f"Typ: {product_type}"]
        lines.append(f"Leistung: {power} + Schnellladen" if power else "Leistung: Schnellladen")
        lines.append(f"Länge: {length}" if length else "Länge: Praktisch")
        lines.append("Zuverlässige Qualität für hohe Kompatibilität.")
        return "\n".join(lines)

    def generate_price(self, product):
        return 5.5

    def create_listing(self, product):
        return {
            "title": self.generate_title(product),
            "description": self.generate_description(product),
            "price": self.generate_price(product),
            "status": "draft",
        }

    # Совместимость с test_run.py
    def create_listing_plan(self, product):
        return self.create_listing(product)
