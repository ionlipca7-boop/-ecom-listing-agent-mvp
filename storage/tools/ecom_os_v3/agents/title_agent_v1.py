from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class TitleCandidate:
    title: str
    length: int
    reason: str


@dataclass
class TitleResult:
    status: str
    recommended_title: str
    candidates: List[Dict[str, Any]]
    blocked_reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TitleAgentV1:
    """Creates conservative German eBay title candidates from confirmed facts."""

    MAX_LEN = 80

    def run(self, passport: Dict[str, Any]) -> TitleResult:
        blocked: List[str] = []
        if passport.get("status") != "PASS":
            blocked.append("product_passport_not_pass")

        product_type = passport.get("product_type") or "Produkt"
        connector = passport.get("connector_or_variant") or ""
        qty = passport.get("bundle_quantity")
        features = passport.get("confirmed_features") or []
        feature_text = self._compact_feature_text(features)

        base_parts = []
        if qty and qty > 1:
            base_parts.append(f"{qty}x")
        base_parts.append(product_type)
        if connector and connector != "nicht bestätigt":
            base_parts.append(connector)
        if feature_text:
            base_parts.append(feature_text)

        base = " ".join(base_parts).strip()
        if not base:
            blocked.append("title_base_empty")
            base = "Produkt"

        candidates_raw = [
            base,
            f"{base} | Neu | Für Alltag & Zubehör",
            f"{base} - robust, kompakt, praktisch",
            f"{product_type} {connector} {feature_text}".strip(),
        ]

        candidates: List[TitleCandidate] = []
        seen = set()
        for raw in candidates_raw:
            title = " ".join(raw.split())
            title = title[: self.MAX_LEN].strip(" -|")
            if title and title not in seen:
                seen.add(title)
                candidates.append(TitleCandidate(title=title, length=len(title), reason="confirmed_facts_only"))

        status = "PASS" if candidates and not blocked else "BLOCKED"
        recommended = candidates[0].title if candidates else ""
        return TitleResult(status=status, recommended_title=recommended, candidates=[asdict(c) for c in candidates], blocked_reasons=blocked)

    def _compact_feature_text(self, features: List[str]) -> str:
        joined = " ".join(features).lower()
        parts: List[str] = []
        if "240" in joined:
            parts.append("240W")
        if "usb-c" in joined:
            parts.append("USB-C")
        if "ständer" in joined or "stand" in joined:
            parts.append("mit Handy-Ständer")
        if "geflochten" in joined or "braided" in joined:
            parts.append("geflochten")
        if "adapter" in joined and "adapter" not in joined[:10]:
            parts.append("Adapter")
        return " ".join(parts[:4])
