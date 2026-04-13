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
        product_kind = str(item_specifics.get("Produktart") or "").strip().lower()

        if product_kind == "ladegerät":
            product_type = "USB-C Ladegerät"
        elif "usb-c" in product_type.lower() and "ladekabel" not in product_type.lower():
            product_type = "USB-C Ladekabel"

        seo_tail = "Netzteil" if product_kind == "ladegerät" else "Datenkabel"
        title_length = "" if product_kind == "ladegerät" else length
        parts = [part for part in (power, product_type, title_length, "Schnellladen", seo_tail) if part]
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

    def _optimize_item_specifics(self, listing):
        """
        Повышает полноту item specifics без изменения структуры listing:
        - заполняет пустые поля безопасными значениями по умолчанию;
        - восстанавливает Anschluss из контекста USB-C;
        - для Ladegerät ставит длину как "Nicht zutreffend", чтобы избежать пустого значения.
        """
        if not isinstance(listing, dict):
            return {}

        item_specifics = listing.get("item_specifics")
        if not isinstance(item_specifics, dict):
            item_specifics = {}

        product_type = str(item_specifics.get("Typ") or listing.get("category") or "").strip()
        product_kind = str(item_specifics.get("Produktart") or "").strip().lower()
        title = str(listing.get("title") or "").lower()

        if not item_specifics.get("Typ"):
            item_specifics["Typ"] = product_type or "Zubehör"
        if not item_specifics.get("Leistung"):
            item_specifics["Leistung"] = "Unbekannt"

        if not item_specifics.get("Anschluss"):
            if "usb-c" in title or "usb-c" in product_type.lower():
                item_specifics["Anschluss"] = "USB-C"
            else:
                item_specifics["Anschluss"] = "Unbekannt"

        if not item_specifics.get("Produktart"):
            if "ladegerät" in product_type.lower():
                item_specifics["Produktart"] = "Ladegerät"
            elif "kabel" in product_type.lower():
                item_specifics["Produktart"] = "Kabel"
            else:
                item_specifics["Produktart"] = "Zubehör"

        is_charger = product_kind == "ladegerät" or item_specifics.get("Produktart") == "Ladegerät"
        if not item_specifics.get("Länge"):
            item_specifics["Länge"] = "Nicht zutreffend" if is_charger else "Unbekannt"

        if not item_specifics.get("Zustand"):
            item_specifics["Zustand"] = "Neu"

        listing["item_specifics"] = item_specifics
        return item_specifics

    def optimize(self, listing):
        if not isinstance(listing, dict):
            return listing

        optimization_notes = []
        original_title = listing.get("title")
        original_price = listing.get("price")
        original_item_specifics = dict(listing.get("item_specifics", {})) if isinstance(listing.get("item_specifics"), dict) else {}

        listing["title"] = self._optimize_title(listing)
        listing["price"] = self._optimize_price(listing)
        listing["item_specifics"] = self._optimize_item_specifics(listing)

        if listing.get("title") != original_title:
            optimization_notes.append("Title optimized for SEO")
        if (
            isinstance(original_price, (int, float))
            and isinstance(listing.get("price"), (int, float))
            and listing["price"] > original_price
        ):
            optimization_notes.append("Price increased by optimizer")
        if listing.get("item_specifics") != original_item_specifics:
            optimization_notes.append("Item specifics completeness improved")

        listing["optimized"] = True
        if listing.get("optimized") is True:
            optimization_notes.append("Listing marked as optimized")

        listing["optimization_notes"] = optimization_notes

        return listing
