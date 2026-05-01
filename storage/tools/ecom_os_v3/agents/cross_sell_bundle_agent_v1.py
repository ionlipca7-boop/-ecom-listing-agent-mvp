from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class CrossSellCandidate:
    source_sku: str
    related_sku: str
    relation: str
    html_label_de: str
    status: str
    reasons: List[str]


@dataclass
class CrossSellBundleResult:
    status: str
    candidates: List[Dict[str, Any]]
    html_block_de: str
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CrossSellBundleAgentV1:
    """Suggests safe related products based on connector/category hints.

    No live HTML change. No fake compatibility. Recommends only.
    """

    def run(self, source_product: Dict[str, Any], catalog: List[Dict[str, Any]]) -> CrossSellBundleResult:
        source_sku = str(source_product.get("sku") or source_product.get("product_identity") or "SOURCE")
        source_text = self._text(source_product)
        candidates: List[CrossSellCandidate] = []

        for item in catalog:
            related_sku = str(item.get("sku") or "UNKNOWN")
            if related_sku == source_sku:
                continue
            rel_text = self._text(item)
            relation, reasons = self._relation(source_text, rel_text)
            if relation == "NO_CLEAR_RELATION":
                continue
            active_url = item.get("active_listing_url")
            stock_ok = int(item.get("quantity") or 0) > 0
            status = "PASS" if active_url and stock_ok else "BLOCKED"
            if not active_url:
                reasons.append("active_listing_url_missing")
            if not stock_ok:
                reasons.append("out_of_stock_or_unknown")
            candidates.append(CrossSellCandidate(
                source_sku=source_sku,
                related_sku=related_sku,
                relation=relation,
                html_label_de=self._label(relation, item),
                status=status,
                reasons=reasons,
            ))

        html = self._html_block(candidates, catalog)
        return CrossSellBundleResult(
            status="PASS",
            candidates=[asdict(x) for x in candidates],
            html_block_de=html,
            next_allowed_action="REVIEW_CROSS_SELL_CANDIDATES_WITH_OPERATOR",
        )

    def _text(self, item: Dict[str, Any]) -> str:
        return " ".join(str(v) for v in item.values()).lower()

    def _relation(self, a: str, b: str) -> tuple[str, List[str]]:
        reasons: List[str] = []
        if "usb-c" in a and "usb-c" in b:
            reasons.append("shared_usb_c")
            if "ladegerät" in b or "charger" in b:
                return "CABLE_PLUS_CHARGER", reasons
            if "adapter" in b:
                return "CABLE_PLUS_ADAPTER", reasons
            return "USB_C_RELATED", reasons
        if "adapter" in a and "kabel" in b:
            reasons.append("adapter_with_cable")
            return "ADAPTER_PLUS_CABLE", reasons
        return "NO_CLEAR_RELATION", reasons

    def _label(self, relation: str, item: Dict[str, Any]) -> str:
        title = str(item.get("title") or item.get("product_identity") or item.get("sku") or "Passender Artikel")
        return title[:90]

    def _html_block(self, candidates: List[CrossSellCandidate], catalog: List[Dict[str, Any]]) -> str:
        active = [c for c in candidates if c.status == "PASS"][:4]
        if not active:
            return ""
        url_by_sku = {str(i.get("sku")): i.get("active_listing_url") for i in catalog}
        rows = []
        for c in active:
            url = url_by_sku.get(c.related_sku, "#")
            rows.append(f'<li><a href="{url}">{c.html_label_de}</a></li>')
        return '<section class="related-products"><h2>Passt gut dazu</h2><ul>' + ''.join(rows) + '</ul></section>'
