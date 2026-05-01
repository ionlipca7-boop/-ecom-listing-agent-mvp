from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class PhotoSlot:
    slot: int
    role: str
    title_de: str
    clean_no_text_required: bool
    allowed_text_de: List[str]
    evidence_required: bool


@dataclass
class PhotoBlueprint:
    status: str
    default_count: int
    slots: List[Dict[str, Any]]
    blocked_reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PhotoBlueprintAgentV1:
    """Creates a safe 8-image eBay Germany photo blueprint.

    This does not generate images yet. It creates the controlled plan for an
    image generation/editing adapter.
    """

    def run(self, passport: Dict[str, Any]) -> PhotoBlueprint:
        blocked: List[str] = []
        if passport.get("status") != "PASS":
            blocked.append("product_passport_not_pass")

        product_type = passport.get("product_type") or "Produkt"
        features = set(passport.get("confirmed_features") or [])

        slots = [
            PhotoSlot(1, "MAIN_CLEAN", "Hauptbild", True, [], True),
            PhotoSlot(2, "SECOND_CLEAN_ANGLE", "Zweiter Winkel", True, [], True),
            PhotoSlot(3, "FEATURE_INFOGRAPHIC", "Funktionen", False, self._feature_texts(features), True),
            PhotoSlot(4, "USE_CASE_PRIMARY", "Anwendung", False, self._use_case_texts(product_type), True),
            PhotoSlot(5, "LIFESTYLE_DESK", "Alltag / Schreibtisch", False, ["Saubere Anwendung", "Praktisch im Alltag"], True),
            PhotoSlot(6, "DETAIL_VIEW", "Detailansicht", False, ["Robuste Verarbeitung", "Klare Details"], True),
            PhotoSlot(7, "MECHANISM_OR_SIZE", "Funktion / Größe", False, ["Kompakte Größe", "Praktisches Design"], True),
            PhotoSlot(8, "PRODUCT_OVERVIEW", "Produktübersicht", False, ["Lieferumfang", "Alles auf einen Blick"], True),
        ]

        status = "PASS" if not blocked else "BLOCKED"
        return PhotoBlueprint(status=status, default_count=8, slots=[asdict(s) for s in slots], blocked_reasons=blocked)

    def _feature_texts(self, features: set[str]) -> List[str]:
        texts = []
        joined = " ".join(features).lower()
        if "240" in joined:
            texts.append("240 W Schnellladen")
        if "480" in joined:
            texts.append("480 Mbit/s Datenübertragung")
        if "geflochten" in joined or "braided" in joined:
            texts.append("Geflochtenes Kabel")
        if "ständer" in joined or "stand" in joined:
            texts.append("Integrierter Handy-Ständer")
        return texts or ["Wichtige Funktionen", "Sauberes Produktdesign"]

    def _use_case_texts(self, product_type: str) -> List[str]:
        t = product_type.lower()
        if "kabel" in t:
            return ["Laden beim Anschauen", "Freihändiges Anschauen"]
        if "adapter" in t:
            return ["Einfach verbinden", "Für Alltag und Zubehör"]
        return ["Praktische Anwendung", "Einfach zu nutzen"]
