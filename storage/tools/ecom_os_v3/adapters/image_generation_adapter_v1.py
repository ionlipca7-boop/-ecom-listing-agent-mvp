from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ImageGenerationAdapterResult:
    status: str
    adapter: str
    generated_files: List[str]
    blocked_reasons: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ImageGenerationAdapterV1:
    """Safe stub for future image generation/edit adapter.

    This adapter intentionally does not call OpenAI image generation, Photoshop,
    Canva, or any external service yet. It only writes an image-generation plan
    from the photo blueprint so local sandbox can stay honest.
    """

    def run(self, photo_blueprint: Dict[str, Any], output_dir: Path) -> ImageGenerationAdapterResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        plan_path = output_dir / "image_generation_plan_v1.json"

        import json
        plan = {
            "status": "BLOCKED_NOT_CONFIGURED",
            "adapter": "ImageGenerationAdapterV1",
            "reason": "No image generation provider configured in local sandbox.",
            "photo_blueprint_status": photo_blueprint.get("status"),
            "slots": photo_blueprint.get("slots", []),
            "allowed_future_providers": [
                "openai_image_generation",
                "photoshop_adapter",
                "canva_template_adapter"
            ],
            "hard_rules": [
                "Do not claim generated images exist until files are created.",
                "Photo 1 and 2 must be clean/no overlay text.",
                "German text only for eBay Germany secondary images.",
                "Human visual preview required before live update."
            ]
        }
        plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

        return ImageGenerationAdapterResult(
            status="BLOCKED_NOT_CONFIGURED",
            adapter="ImageGenerationAdapterV1",
            generated_files=[str(plan_path)],
            blocked_reasons=["image_generation_provider_not_configured"],
            next_allowed_action="CONFIGURE_IMAGE_PROVIDER_OR_USE_CHATGPT_VISUAL_PROOF_MANUALLY",
        )
