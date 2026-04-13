import re


class InputParser:
    CABLE_KEYWORDS = (
        "kabel",
        "ladekabel",
        "daten kabel",
        "datenkabel",
        "usb c cable",
        "usb-c cable",
        "cable",
    )

    CHARGER_KEYWORDS = (
        "charger",
        "ladegerät",
        "ladegerat",
        "netzteil",
        "adapter",
        "power adapter",
    )

    def parse_text(self, raw_text):
        raw = str(raw_text).lower()
        raw = raw.replace("-", " ")
        raw = re.sub(r"\s+", " ", raw).strip()

        has_cable = any(keyword in raw for keyword in self.CABLE_KEYWORDS)
        has_charger = any(keyword in raw for keyword in self.CHARGER_KEYWORDS)
        has_usb_c = "usb c" in raw

        # If both are present (e.g. "67w charger with 2m cable"),
        # prefer the main product as charger and keep cable as a detail.
        if has_charger:
            product_type = "USB-C Ladegerät"
        elif has_cable or (has_usb_c and "cable" in raw):
            product_type = "USB-C Ladekabel"
        else:
            product_type = "Zubehör"

        if "60w" in raw:
            power = "60W"
        elif "67w" in raw:
            power = "67W"
        elif "20w" in raw:
            power = "20W"
        elif "10w" in raw:
            power = "10W"
        else:
            power = "10W"

        if "2m" in raw:
            length = "2m"
        elif "1m" in raw:
            length = "1m"
        else:
            length = "1m"

        return {
            "type": product_type,
            "power": power,
            "length": length,
        }
