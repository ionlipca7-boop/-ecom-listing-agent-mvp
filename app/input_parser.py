class InputParser:
    def parse_text(self, raw_text):
        raw = str(raw_text).lower()

        if "kabel" in raw or "cable" in raw:
            product_type = "USB-C Ladekabel"
        elif "ladegerät" in raw or "charger" in raw or "netzteil" in raw:
            product_type = "USB-C Ladegerät"
        else:
            product_type = "Zubehör"

        if "60w" in raw:
            power = "60W"
        elif "67w" in raw:
            power = "67W"
        elif "20w" in raw:
            power = "20W"
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
