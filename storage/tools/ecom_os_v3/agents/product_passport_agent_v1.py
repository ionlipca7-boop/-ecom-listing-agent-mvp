from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class ProductPassport:
    status: str
    product_identity: str
    product_type: str
    bundle_quantity: int | None
    color: str
    connector_or_variant: str
    included_items: List[str]
    confirmed_features: List[str]
    uncertainties: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ProductPassportAgentV1:
    """Builds a conservative product passport from source packet + operator hints."""

    def run(self, source_packet: Dict[str, Any], product_input: Dict[str, Any]) -> ProductPassport:
        title = source_packet.get("raw_title") or product_input.get("raw_title") or ""
        note = source_packet.get("operator_note") or product_input.get("operator_note") or ""
        product_type = product_input.get("product_type") or self._infer_type(title + " " + note)
        identity = product_input.get("product_identity") or title or note or "UNKNOWN_PRODUCT"
        bundle_quantity = product_input.get("bundle_quantity")
        color = product_input.get("color") or "nicht bestätigt"
        connector = product_input.get("connector_or_variant") or "nicht bestätigt"
        included = list(product_input.get("included_items") or [])
        features = list(product_input.get("confirmed_features") or [])

        uncertainties: List[str] = list(source_packet.get("uncertainties") or [])
        if identity == "UNKNOWN_PRODUCT":
            uncertainties.append("product_identity_unknown")
        if not included:
            uncertainties.append("included_items_missing")
        if not features:
            uncertainties.append("confirmed_features_missing")

        status = "PASS" if identity != "UNKNOWN_PRODUCT" and product_type != "unknown" else "BLOCKED"

        return ProductPassport(
            status=status,
            product_identity=identity,
            product_type=product_type,
            bundle_quantity=bundle_quantity,
            color=color,
            connector_or_variant=connector,
            included_items=included,
            confirmed_features=features,
            uncertainties=uncertainties,
        )

    def _infer_type(self, text: str) -> str:
        t = text.lower()
        if "usb-c" in t and "kabel" in t:
            return "USB-C Kabel"
        if "adapter" in t:
            return "Adapter"
        if "charger" in t or "ladegerät" in t:
            return "Ladegerät"
        return "unknown"
