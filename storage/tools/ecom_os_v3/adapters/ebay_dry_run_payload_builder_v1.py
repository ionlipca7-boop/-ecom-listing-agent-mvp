from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
import json


@dataclass
class EbayDryRunPayloadBuilderResult:
    status: str
    adapter: str
    payload_file: str
    blocked_reasons: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EbayDryRunPayloadBuilderV1:
    """Builds an eBay dry-run payload file only.

    It never sends API requests. It exists so the operator can review exact
    intended title/specifics/HTML/photo plan before any live gate.
    """

    def run(self, artifacts: Dict[str, Any], output_dir: Path) -> EbayDryRunPayloadBuilderResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        payload_path = output_dir / "ebay_dry_run_payload_v1.json"

        critic = artifacts.get("critic") or {}
        if critic.get("status") != "PASS":
            status = "BLOCKED"
            blocked = ["critic_not_pass"]
        else:
            status = "DRY_RUN_PAYLOAD_READY"
            blocked = []

        payload = {
            "status": status,
            "adapter": "EbayDryRunPayloadBuilderV1",
            "send_to_ebay": False,
            "marketplace": "EBAY_DE",
            "protected_fields": {
                "price": "DO_NOT_CHANGE_WITHOUT_SCOPE",
                "quantity": "DO_NOT_CHANGE_WITHOUT_SCOPE",
                "category": "DO_NOT_CHANGE_WITHOUT_SCOPE",
                "live_listing_id": "NOT_SET_IN_LOCAL_SANDBOX"
            },
            "draft": {
                "title": (artifacts.get("title_result") or {}).get("recommended_title"),
                "item_specifics": (artifacts.get("specifics_result") or {}).get("specifics"),
                "html_preview_path": artifacts.get("html_preview_path"),
                "photo_blueprint": artifacts.get("photo_blueprint"),
                "evidence_status": artifacts.get("evidence_status"),
            },
            "required_before_live": [
                "Telegram operator approval",
                "Marketplace Critic PASS",
                "exact payload review",
                "readonly before-state",
                "token guard",
                "live scope approval",
                "readonly after-state"
            ]
        }
        payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        return EbayDryRunPayloadBuilderResult(
            status=status,
            adapter="EbayDryRunPayloadBuilderV1",
            payload_file=str(payload_path),
            blocked_reasons=blocked,
            next_allowed_action="TELEGRAM_REVIEW" if status == "DRY_RUN_PAYLOAD_READY" else "FIX_CRITIC_FIRST",
        )
