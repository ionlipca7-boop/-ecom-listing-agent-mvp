def generate_title(product):
    """
    eBay SEO Title Generator
    Structure:
    Power + Product Type + Length + Keywords
    """

    power = product.get("power", "")
    length = product.get("length", "")
    product_type = product.get("type", "Kabel")

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