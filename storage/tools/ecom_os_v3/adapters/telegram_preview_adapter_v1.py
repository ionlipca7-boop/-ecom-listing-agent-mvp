from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
import json


@dataclass
class TelegramPreviewAdapterResult:
    status: str
    adapter: str
    preview_file: str
    blocked_reasons: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TelegramPreviewAdapterV1:
    """Safe local Telegram preview stub.

    This does not send messages. It creates the exact Russian preview packet that
    later Telegram runtime can send after bot integration.
    """

    def run(self, artifacts: Dict[str, Any], output_dir: Path) -> TelegramPreviewAdapterResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        preview_path = output_dir / "telegram_preview_packet_v1.json"

        packet = {
            "status": "READY_FOR_TELEGRAM_ADAPTER_NOT_SENT",
            "adapter": "TelegramPreviewAdapterV1",
            "language": "ru",
            "message_title": "ECOM OS V3 — предпросмотр листинга",
            "sections": {
                "product": artifacts.get("product_passport"),
                "evidence_status": artifacts.get("evidence_status"),
                "photo_blueprint": artifacts.get("photo_blueprint"),
                "title": artifacts.get("title_result"),
                "specifics": artifacts.get("specifics_result"),
                "html_preview_path": artifacts.get("html_preview_path"),
                "critic": artifacts.get("critic"),
            },
            "operator_commands": [
                "одобрить черновик",
                "переделать фото",
                "переделать title",
                "показать HTML",
                "стоп",
                "не публиковать"
            ],
            "hard_rules": [
                "This packet is preview only.",
                "No live eBay action from preview.",
                "Voice commands must be transcribed and confirmed before risky actions."
            ]
        }
        preview_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")

        return TelegramPreviewAdapterResult(
            status="READY_NOT_SENT",
            adapter="TelegramPreviewAdapterV1",
            preview_file=str(preview_path),
            blocked_reasons=["telegram_runtime_not_connected_in_local_sandbox"],
            next_allowed_action="CONNECT_TELEGRAM_RUNTIME_AFTER_LOCAL_PASS",
        )
