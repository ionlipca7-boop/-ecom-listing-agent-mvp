from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class ImageCriticResult:
    status: str
    issues: List[str]
    slot_checks: List[Dict[str, Any]]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ImageCriticAgentV1:
    """Critics the photo blueprint before any image-generation adapter.

    This local version does not inspect pixels yet. It enforces structural photo rules:
    - slots 1-2 must be clean/no text
    - secondary callouts must be German
    - each slot must have a role and evidence requirement
    """

    ENGLISH_FORBIDDEN = ["fast", "charging", "data sync", "built-in", "hands-free", "viewing", "braided"]

    def run(self, photo_blueprint: Dict[str, Any]) -> ImageCriticResult:
        issues: List[str] = []
        slot_checks: List[Dict[str, Any]] = []

        if photo_blueprint.get("status") != "PASS":
            issues.append("photo_blueprint_not_pass")

        slots = photo_blueprint.get("slots") or []
        if len(slots) < 8:
            issues.append("photo_slots_less_than_8")

        for slot in slots:
            slot_no = slot.get("slot")
            texts = slot.get("allowed_text_de") or []
            clean_required = bool(slot.get("clean_no_text_required"))
            role = slot.get("role")
            local_issues: List[str] = []

            if not role:
                local_issues.append("role_missing")
            if slot_no in [1, 2]:
                if not clean_required:
                    local_issues.append("main_clean_rule_missing")
                if texts:
                    local_issues.append("main_or_second_image_has_overlay_text")
            for text in texts:
                t = str(text).lower()
                for forbidden in self.ENGLISH_FORBIDDEN:
                    if forbidden in t:
                        local_issues.append(f"english_text_detected:{forbidden}")

            if local_issues:
                issues.extend([f"slot_{slot_no}:{x}" for x in local_issues])

            slot_checks.append({
                "slot": slot_no,
                "role": role,
                "status": "PASS" if not local_issues else "BLOCKED",
                "issues": local_issues,
            })

        status = "PASS" if not issues else "BLOCKED"
        return ImageCriticResult(
            status=status,
            issues=issues,
            slot_checks=slot_checks,
            next_allowed_action="IMAGE_GENERATION_ADAPTER_OR_CANVA_TEMPLATE" if status == "PASS" else "FIX_PHOTO_BLUEPRINT",
        )
