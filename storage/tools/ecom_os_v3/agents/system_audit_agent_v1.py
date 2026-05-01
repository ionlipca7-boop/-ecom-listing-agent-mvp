from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
import json


@dataclass
class SystemAuditResult:
    status: str
    pass_agents: List[str]
    blocked_agents: List[str]
    not_configured_adapters: List[str]
    missing_files: List[str]
    recommendations: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SystemAuditAgentV1:
    """Audits one or more local sandbox run outputs.

    This agent does not modify files. It reads run summaries and returns a clear
    PASS/BLOCKED system status for A -> B -> FINISH -> STOP review.
    """

    REQUIRED_FILES = [
        "00_product_input.json",
        "01_source_packet.json",
        "02_product_passport.json",
        "03_evidence_map.json",
        "04_photo_blueprint.json",
        "05_image_critic_report.json",
        "06_title_candidates.json",
        "07_item_specifics.json",
        "08_ebay_description_preview.html",
        "08_html_result.json",
        "09_critic_report.json",
        "10_teacher_lessons.json",
        "12_image_generation_adapter_result.json",
        "13_canva_template_adapter_result.json",
        "14_telegram_preview_adapter_result.json",
        "15_ebay_dry_run_payload_builder_result.json",
        "16_run_summary.json",
        "artifact_index.json",
    ]

    def run(self, run_dirs: List[Path]) -> SystemAuditResult:
        pass_agents: List[str] = []
        blocked_agents: List[str] = []
        not_configured_adapters: List[str] = []
        missing_files: List[str] = []
        recommendations: List[str] = []

        for run_dir in run_dirs:
            if not run_dir.exists():
                missing_files.append(str(run_dir))
                continue
            for fname in self.REQUIRED_FILES:
                if not (run_dir / fname).exists():
                    missing_files.append(f"{run_dir.name}/{fname}")

            summary = self._read_json(run_dir / "16_run_summary.json")
            if summary:
                self._status_to_lists("EvidenceAgent", summary.get("evidence_status"), pass_agents, blocked_agents, not_configured_adapters)
                self._status_to_lists("ImageCriticAgent", summary.get("image_critic_status"), pass_agents, blocked_agents, not_configured_adapters)
                self._status_to_lists("MarketplaceCriticAgent", summary.get("critic_status"), pass_agents, blocked_agents, not_configured_adapters)
                self._status_to_lists("TeacherAgent", summary.get("teacher_status"), pass_agents, blocked_agents, not_configured_adapters)
                self._status_to_lists("ImageGenerationAdapter", summary.get("image_generation_adapter_status"), pass_agents, blocked_agents, not_configured_adapters)
                self._status_to_lists("CanvaTemplateAdapter", summary.get("canva_template_adapter_status"), pass_agents, blocked_agents, not_configured_adapters)
                self._status_to_lists("TelegramPreviewAdapter", summary.get("telegram_preview_adapter_status"), pass_agents, blocked_agents, not_configured_adapters)
                self._status_to_lists("EbayDryRunPayloadBuilder", summary.get("ebay_dry_run_payload_status"), pass_agents, blocked_agents, not_configured_adapters)

        if not_configured_adapters:
            recommendations.append("Configure external adapters only after local core PASS: image provider, Canva, Telegram runtime.")
        if missing_files:
            recommendations.append("Fix missing output artifacts before server deployment.")
        if blocked_agents:
            recommendations.append("Fix BLOCKED core agents before Telegram/server/eBay integration.")
        if not missing_files and not blocked_agents:
            recommendations.append("Local core artifacts are complete. Next step can be adapter configuration or readonly server audit.")

        hard_blockers = [x for x in blocked_agents if "Adapter" not in x and "PayloadBuilder" not in x]
        status = "PASS_WITH_NOT_CONFIGURED_ADAPTERS" if not missing_files and not hard_blockers else "BLOCKED"
        return SystemAuditResult(
            status=status,
            pass_agents=sorted(set(pass_agents)),
            blocked_agents=sorted(set(blocked_agents)),
            not_configured_adapters=sorted(set(not_configured_adapters)),
            missing_files=missing_files,
            recommendations=recommendations,
            next_allowed_action="REVIEW_AUDIT_AND_CONFIGURE_ADAPTERS" if status.startswith("PASS") else "FIX_BLOCKERS",
        )

    def _read_json(self, path: Path) -> Dict[str, Any] | None:
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _status_to_lists(self, name: str, status: Any, passed: List[str], blocked: List[str], not_configured: List[str]) -> None:
        s = str(status or "UNKNOWN")
        if s in {"PASS", "DRY_RUN_PAYLOAD_READY", "READY_NOT_SENT"}:
            passed.append(name)
        elif s == "BLOCKED_NOT_CONFIGURED":
            not_configured.append(name)
        else:
            blocked.append(f"{name}:{s}")
