from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class VariationResult:
    status: str
    listing_mode: str
    variation_types: List[str]
    issues: List[str]
    rules: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class VariationAgentV1:
    """Decides safe listing mode: single SKU, fixed bundle, or variation candidate."""

    def run(self, product: Dict[str, Any]) -> VariationResult:
        issues: List[str] = []
        rules: List[str] = []
        variants = product.get("variants") or []
        qty = product.get("bundle_quantity")
        stock_variants = product.get("stock_variants") or []
        product_type = str(product.get("product_type") or "").lower()

        if qty and int(qty) > 1:
            mode = "MULTI_QUANTITY_SET_LISTING"
            rules.append("bundle_quantity_must_match_photos_title_and_delivery")
        elif stock_variants:
            mode = "VARIATION_LISTING_CANDIDATE"
            rules.append("marketplace_category_variation_support_required")
            rules.append("each_variation_requires_stock_and_evidence")
        else:
            mode = "SINGLE_SKU_SINGLE_LISTING"

        variation_types: List[str] = []
        joined = " ".join(str(x).lower() for x in variants + stock_variants)
        if "farbe" in joined or "color" in joined or any(c in joined for c in ["schwarz", "silber", "orange"]):
            variation_types.append("color")
        if "länge" in joined or "length" in joined or "m" in joined:
            variation_types.append("cable_length")
        if "set" in joined or qty:
            variation_types.append("set_quantity")
        if "usb" in joined or "adapter" in product_type or "kabel" in product_type:
            variation_types.append("connector_type")

        if mode == "VARIATION_LISTING_CANDIDATE" and not stock_variants:
            issues.append("stock_variants_missing")
        if qty and int(qty) > 1 and stock_variants:
            issues.append("fixed_bundle_and_variation_stock_conflict_review_required")

        status = "PASS" if not issues else "BLOCKED"
        return VariationResult(
            status=status,
            listing_mode=mode,
            variation_types=variation_types,
            issues=issues,
            rules=rules,
            next_allowed_action="PHOTO_TITLE_SPECIFICS_AGENT" if status == "PASS" else "FIX_VARIATION_INPUT",
        )
