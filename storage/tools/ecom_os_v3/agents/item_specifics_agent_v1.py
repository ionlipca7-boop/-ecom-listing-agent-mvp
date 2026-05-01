from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class ItemSpecificsResult:
    status: str
    specifics: Dict[str, str]
    blocked_reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ItemSpecificsAgentV1:
    """Creates conservative German item specifics from confirmed passport fields."""

    def run(self, passport: Dict[str, Any]) -> ItemSpecificsResult:
        blocked: List[str] = []
        if passport.get("status") != "PASS":
            blocked.append("product_passport_not_pass")

        product_type = passport.get("product_type") or "Nicht bestätigt"
        connector = passport.get("connector_or_variant") or "Nicht bestätigt"
        color = passport.get("color") or "Nicht bestätigt"
        features = passport.get("confirmed_features") or []
        qty = passport.get("bundle_quantity")

        specifics: Dict[str, str] = {
            "Produkttyp": product_type,
            "Marke": "Neutral / nicht bestätigt",
            "Zustand": "Neu",
            "Farbe": color,
            "Anschluss / Variante": connector,
            "Besonderheiten": ", ".join(features) if features else "Nicht bestätigt",
            "Lieferumfang": self._delivery_text(passport),
        }
        if qty:
            specifics["Anzahl pro Packung"] = str(qty)

        if product_type == "Nicht bestätigt":
            blocked.append("product_type_missing")

        return ItemSpecificsResult(status="PASS" if not blocked else "BLOCKED", specifics=specifics, blocked_reasons=blocked)

    def _delivery_text(self, passport: Dict[str, Any]) -> str:
        included = passport.get("included_items") or []
        if included:
            return ", ".join(included)
        qty = passport.get("bundle_quantity")
        product_type = passport.get("product_type") or "Produkt"
        if qty:
            return f"{qty}x {product_type}"
        return f"1x {product_type}"
