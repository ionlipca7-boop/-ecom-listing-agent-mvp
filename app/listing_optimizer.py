class ListingOptimizer:
    def _optimize_title(self, listing):
        """
        Улучшает title по eBay SEO формуле:
        Power + Product Type + Length + Keyword 1 + Keyword 2
        с ограничением до 80 символов.
        """
        item_specifics = listing.get("item_specifics", {}) if isinstance(listing, dict) else {}

        power = str(item_specifics.get("Leistung") or "").strip()
        product_type = str(item_specifics.get("Typ") or listing.get("category") or "Kabel").strip()
        length = str(item_specifics.get("Länge") or "").strip()

        if "usb-c" in product_type.lower() and "ladekabel" not in product_type.lower():
            product_type = "USB-C Ladekabel"

        parts = [part for part in (power, product_type, length, "Schnellladen", "Datenkabel") if part]
        optimized_title = " ".join(parts).strip()

        return optimized_title[:80]

    def _optimize_price(self, listing):
        """
        Может слегка скорректировать цену (+1€ или +2€).
        """
        price = listing.get("price") if isinstance(listing, dict) else None
        if not isinstance(price, (int, float)):
            return price

        increment = 2 if price >= 7 else 1
        return round(price + increment, 2)

    def optimize(self, listing):
        if not isinstance(listing, dict):
            return listing

        listing["title"] = self._optimize_title(listing)
        listing["price"] = self._optimize_price(listing)
        listing["optimized"] = True

        return listing
