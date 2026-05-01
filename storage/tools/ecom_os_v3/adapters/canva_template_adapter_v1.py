from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
import json


@dataclass
class CanvaTemplateAdapterResult:
    status: str
    adapter: str
    template_plan_file: str
    blocked_reasons: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CanvaTemplateAdapterV1:
    """Safe stub for future Canva editable template generation.

    Canva is for editable product infographic/layout templates, not for backend
    evidence, eBay live, Telegram approval, or server runtime control.
    """

    def run(self, product_packet: Dict[str, Any], photo_blueprint: Dict[str, Any], output_dir: Path) -> CanvaTemplateAdapterResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        plan_path = output_dir / "canva_template_plan_v1.json"
        plan = {
            "status": "BLOCKED_NOT_CONFIGURED",
            "adapter": "CanvaTemplateAdapterV1",
            "reason": "Canva provider/template not configured in local sandbox.",
            "intended_use": [
                "editable German infographic templates",
                "feature cards",
                "gallery contact sheet templates",
                "listing preview boards"
            ],
            "not_for": [
                "eBay live publish",
                "server runtime control",
                "evidence validation",
                "automatic price/title/photo revise"
            ],
            "product_identity": product_packet.get("product_identity") or product_packet.get("raw_title"),
            "photo_slots": photo_blueprint.get("slots", []),
            "hard_rules": [
                "Canva output must still pass Image Critic and Marketplace Critic.",
                "German only for eBay Germany visuals.",
                "Main image template must not add text, border, watermark, or marketing badges."
            ]
        }
        plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        return CanvaTemplateAdapterResult(
            status="BLOCKED_NOT_CONFIGURED",
            adapter="CanvaTemplateAdapterV1",
            template_plan_file=str(plan_path),
            blocked_reasons=["canva_provider_not_configured"],
            next_allowed_action="CONFIGURE_CANVA_TEMPLATE_OR_SKIP_TO_HTML_PREVIEW",
        )
