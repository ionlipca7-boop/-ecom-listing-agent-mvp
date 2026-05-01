from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class SourcePacket:
    status: str
    source_type: str
    source_url: Optional[str]
    marketplace: str
    raw_title: str
    operator_note: str
    screenshots_or_photos: List[str]
    visible_claims: List[str]
    variants: List[str]
    fallback_needed: bool
    uncertainties: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class UrlIntakeAgentV1:
    """Local deterministic URL/screenshot intake agent.

    This does not browse the web yet. It creates a structured source packet from
    operator-provided local input so the rest of the pipeline can run safely.
    """

    def run(self, product_input: Dict[str, Any]) -> SourcePacket:
        source_url = product_input.get("source_url")
        raw_title = (product_input.get("raw_title") or "").strip()
        operator_note = (product_input.get("operator_note") or "").strip()
        photos = list(product_input.get("screenshots_or_photos") or [])
        visible_claims = list(product_input.get("visible_claims") or [])
        variants = list(product_input.get("variants") or [])
        marketplace = product_input.get("marketplace") or "unknown"

        uncertainties: List[str] = []
        if not source_url:
            uncertainties.append("source_url_missing")
        if not raw_title and not operator_note:
            uncertainties.append("product_identity_text_missing")
        if not photos:
            uncertainties.append("source_images_missing")

        fallback_needed = bool(source_url and not photos)
        status = "PASS" if (raw_title or operator_note) and (photos or source_url) else "BLOCKED"

        return SourcePacket(
            status=status,
            source_type="url_or_manual_fallback",
            source_url=source_url,
            marketplace=marketplace,
            raw_title=raw_title,
            operator_note=operator_note,
            screenshots_or_photos=photos,
            visible_claims=visible_claims,
            variants=variants,
            fallback_needed=fallback_needed,
            uncertainties=uncertainties,
        )
