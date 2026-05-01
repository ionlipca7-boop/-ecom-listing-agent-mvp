from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class CriticResult:
    status: str
    issues: List[str]
    protected_fields_ok: bool
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CriticAgentV1:
    """Mandatory local critic gate for sandbox artifacts."""

    ENGLISH_FORBIDDEN = [
        "fast charging",
        "data sync",
        "built-in",
        "hands-free",
        "braided cable",
    ]

    def run(
        self,
        source_packet: Dict[str, Any],
        passport: Dict[str, Any],
        photo_blueprint: Dict[str, Any],
        title_result: Dict[str, Any],
        specifics_result: Dict[str, Any],
        html_result: Dict[str, Any],
    ) -> CriticResult:
        issues: List[str] = []

        for name, obj in [
            ("source_packet", source_packet),
            ("product_passport", passport),
            ("photo_blueprint", photo_blueprint),
            ("title", title_result),
            ("specifics", specifics_result),
            ("html", html_result),
        ]:
            if obj.get("status") != "PASS":
                issues.append(f"{name}_not_pass")

        # Photo rules: 1 and 2 must be clean/no text.
        for slot in photo_blueprint.get("slots", [])[:2]:
            if not slot.get("clean_no_text_required"):
                issues.append(f"photo_slot_{slot.get('slot')}_clean_rule_missing")
            if slot.get("allowed_text_de"):
                issues.append(f"photo_slot_{slot.get('slot')}_has_text")

        # German-only check for generated text fields.
        text_blob = " ".join([
            title_result.get("recommended_title", ""),
            " ".join(str(x.get("title", "")) for x in title_result.get("candidates", [])),
            " ".join(str(v) for v in (specifics_result.get("specifics") or {}).values()),
            " ".join(" ".join(s.get("allowed_text_de", [])) for s in photo_blueprint.get("slots", [])),
        ]).lower()
        for forbidden in self.ENGLISH_FORBIDDEN:
            if forbidden in text_blob:
                issues.append(f"english_text_detected:{forbidden}")

        # Evidence sanity.
        if not passport.get("confirmed_features"):
            issues.append("confirmed_features_empty")
        if not passport.get("included_items"):
            issues.append("included_items_empty")

        status = "PASS" if not issues else "BLOCKED"
        return CriticResult(
            status=status,
            issues=issues,
            protected_fields_ok=True,
            next_allowed_action="TELEGRAM_REVIEW_OR_IMAGE_ADAPTER" if status == "PASS" else "FIX_BLOCKED_ISSUES",
        )
