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

    # Power (for example 60W)
    if power:
        parts.append(f"{power}")

    # Product type (for example USB-C Ladekabel)
    if "usb-c" in product_type.lower():
        parts.append("USB-C Ladekabel")
    else:
        parts.append(product_type)

    # Length (for example 2m)
    if length:
        parts.append(f"{length}")

    # SEO Keywords
    parts.append("Schnellladen")
    parts.append("Datenkabel")

    # Final assembly
    title = " ".join(parts)

    # eBay limit (80 characters)
    return title[:80]


class ListingBrain:
    def generate_title(self, product):
        return generate_title(product)

    def generate_description(self, product):
        product_type = product.get("type") or product.get("name") or "Kabel"
        power = product.get("power", "-")
        length = product.get("length", "-")

        details = [
            f"Produkt: {product_type}",
            f"Leistung: {power}",
            f"Laenge: {length}",
            "Geeignet fuer Laden und Datentransfer.",
        ]
        return "\n".join(details)

    def generate_price(self, product):
        return 5.5

    def create_listing(self, product):
        return {
            "title": self.generate_title(product),
            "description": self.generate_description(product),
            "price": self.generate_price(product),
            "status": "draft",
        }

    # Compatibility with test_run.py
    def create_listing_plan(self, product):
        return self.create_listing(product)
