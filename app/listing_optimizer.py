class ListingOptimizer:
    TITLE_MIN_SEO_LENGTH = 40

    def _is_title_length_good(self, title):
        normalized_title = " ".join(str(title or "").split())
        if len(normalized_title) >= self.TITLE_MIN_SEO_LENGTH:
            return True

        words = normalized_title.split()
        return len(words) >= 5 and any("usb-c" in word.lower() for word in words)

    def _sync_title_improvements(self, listing):
        improvements = listing.get("listing_improvements")
        if not isinstance(improvements, list):
            return

        title_message = "Title could be longer for better SEO"
        improvements = [item for item in improvements if item != title_message]

        if not self._is_title_length_good(listing.get("title", "")):
            improvements.append(title_message)

        listing["listing_improvements"] = improvements

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
        seo_extension = "Schnellladegerät" if product_kind == "ladegerät" else "Schnellladekabel"
        title_length = "" if product_kind == "ladegerät" else length
        parts = [part for part in (power, product_type, title_length, "Schnellladen", seo_tail) if part]

        # Добавляем хвост только если заголовок реально короткий И смысл не дублируется.
        tentative_title = " ".join(parts).strip()
        tentative_lower = tentative_title.lower()
        has_speed_intent = "schnelllad" in tentative_lower or "fast" in tentative_lower
        has_product_intent = any(keyword in tentative_lower for keyword in ("kabel", "ladegerät", "ladegerat", "netzteil"))

        if (
            not self._is_title_length_good(tentative_title)
            and seo_extension.lower() not in tentative_lower
            and not (has_speed_intent and has_product_intent)
        ):
            parts.append(seo_extension)

        optimized_title = " ".join(parts).strip()

        return optimized_title[:80]

    def _optimize_price(self, listing):
        """
        Точечно повышает предсказуемость цены:
        - учитывает тип товара, мощность и длину;
        - поднимает цену только если текущая ниже ожидаемой;
        - не снижает цену и не меняет output contract.
        """
        if not isinstance(listing, dict):
            return listing

        price = listing.get("price")
        if not isinstance(price, (int, float)):
            return price

        item_specifics = listing.get("item_specifics", {})
        if not isinstance(item_specifics, dict):
            item_specifics = {}

        product_kind = str(item_specifics.get("Produktart") or "").strip().lower()
        power_raw = str(item_specifics.get("Leistung") or "")
        length_raw = str(item_specifics.get("Länge") or "")

        power_digits = "".join(ch for ch in power_raw if ch.isdigit())
        watts = int(power_digits) if power_digits else 0

        length_normalized = length_raw.replace(",", ".").lower()
        length_digits = "".join(ch for ch in length_normalized if ch.isdigit() or ch == ".")
        length_m = float(length_digits) if length_digits else 0.0

        if product_kind == "ladegerät":
            if watts >= 60:
                expected_price = 7.99
            elif watts >= 30:
                expected_price = 6.49
            else:
                expected_price = 4.99
        else:
            if watts >= 60:
                expected_price = 6.49
            elif watts >= 30:
                expected_price = 5.49
            else:
                expected_price = 4.99

            if length_m >= 3:
                expected_price += 1.0
            elif length_m >= 2:
                expected_price += 0.5

        return round(max(price, expected_price), 2)

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
        self._sync_title_improvements(listing)

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
