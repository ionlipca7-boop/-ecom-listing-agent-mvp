from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[2]
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from agents.url_intake_agent_v1 import UrlIntakeAgentV1
from agents.product_passport_agent_v1 import ProductPassportAgentV1
from agents.evidence_agent_v1 import EvidenceAgentV1
from agents.photo_blueprint_agent_v1 import PhotoBlueprintAgentV1
from agents.image_critic_agent_v1 import ImageCriticAgentV1
from agents.title_agent_v1 import TitleAgentV1
from agents.item_specifics_agent_v1 import ItemSpecificsAgentV1
from agents.html_agent_v1 import HtmlAgentV1
from agents.critic_agent_v1 import CriticAgentV1
from agents.teacher_agent_v1 import TeacherAgentV1


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def default_product_input() -> Dict[str, Any]:
    return {
        "source_url": "LOCAL_SANDBOX_NO_LIVE_URL",
        "marketplace": "ebay_de",
        "raw_title": "USB-C auf USB-C Kabel 240W mit klappbarem Handy-Ständer",
        "operator_note": "Testprodukt aus Chat-Proof: schwarzes geflochtenes USB-C Kabel mit integriertem klappbarem Handy-Ständer.",
        "screenshots_or_photos": ["chat_visual_reference_usb_c_cable_with_stand"],
        "visible_claims": ["240 W", "480 Mbit/s", "USB-C auf USB-C", "geflochten", "klappbarer Handy-Ständer"],
        "variants": ["Schwarz/Dunkelgrau"],
        "product_identity": "USB-C auf USB-C Kabel mit klappbarem Handy-Ständer",
        "product_type": "USB-C Kabel",
        "bundle_quantity": 1,
        "color": "Schwarz/Dunkelgrau",
        "connector_or_variant": "USB-C auf USB-C",
        "included_items": ["1x USB-C Kabel mit integriertem Handy-Ständer"],
        "confirmed_features": ["USB-C auf USB-C", "240 W Schnellladen", "480 Mbit/s Datenübertragung", "Geflochtenes Kabel", "Integrierter klappbarer Handy-Ständer"],
    }


def load_product_input(path: Path | None) -> Dict[str, Any]:
    if path and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default_product_input()


def main() -> int:
    input_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = PROJECT_ROOT / "storage" / "outputs" / "ecom_os_v3" / "local_sandbox" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    product_input = load_product_input(input_path)
    write_json(out_dir / "00_product_input.json", product_input)

    source_packet = UrlIntakeAgentV1().run(product_input).to_dict()
    write_json(out_dir / "01_source_packet.json", source_packet)

    passport = ProductPassportAgentV1().run(source_packet, product_input).to_dict()
    write_json(out_dir / "02_product_passport.json", passport)

    evidence = EvidenceAgentV1().run(source_packet, passport).to_dict()
    write_json(out_dir / "03_evidence_map.json", evidence)

    photo_blueprint = PhotoBlueprintAgentV1().run(passport).to_dict()
    write_json(out_dir / "04_photo_blueprint.json", photo_blueprint)

    image_critic = ImageCriticAgentV1().run(photo_blueprint).to_dict()
    write_json(out_dir / "05_image_critic_report.json", image_critic)

    title_result = TitleAgentV1().run(passport).to_dict()
    write_json(out_dir / "06_title_candidates.json", title_result)

    specifics_result = ItemSpecificsAgentV1().run(passport).to_dict()
    write_json(out_dir / "07_item_specifics.json", specifics_result)

    template_path = CURRENT_DIR / "templates" / "ebay_description_template_v1.html"
    html_output = out_dir / "08_ebay_description_preview.html"
    html_result = HtmlAgentV1().run(title_result, specifics_result, passport, template_path, html_output).to_dict()
    write_json(out_dir / "08_html_result.json", html_result)

    critic = CriticAgentV1().run(source_packet, passport, photo_blueprint, title_result, specifics_result, html_result).to_dict()
    if evidence.get("status") != "PASS":
        critic.setdefault("issues", []).append("evidence_not_pass")
        critic["status"] = "BLOCKED"
        critic["next_allowed_action"] = "FIX_EVIDENCE_OR_SOURCE_INPUT"
    if image_critic.get("status") != "PASS":
        critic.setdefault("issues", []).append("image_critic_not_pass")
        critic["status"] = "BLOCKED"
        critic["next_allowed_action"] = "FIX_IMAGE_BLUEPRINT"
    write_json(out_dir / "09_critic_report.json", critic)

    run_context = {
        "critic_status": critic.get("status"),
        "critic_issues": critic.get("issues", []),
        "image_critic_issues": image_critic.get("issues", []),
    }
    teacher = TeacherAgentV1().run(run_context).to_dict()
    write_json(out_dir / "10_teacher_lessons.json", teacher)

    artifact_index = {
        "run_id": run_id,
        "artifacts": {
            "product_input": "00_product_input.json",
            "source_packet": "01_source_packet.json",
            "product_passport": "02_product_passport.json",
            "evidence_map": "03_evidence_map.json",
            "photo_blueprint": "04_photo_blueprint.json",
            "image_critic_report": "05_image_critic_report.json",
            "title_candidates": "06_title_candidates.json",
            "item_specifics": "07_item_specifics.json",
            "html_preview": "08_ebay_description_preview.html",
            "html_result": "08_html_result.json",
            "critic_report": "09_critic_report.json",
            "teacher_lessons": "10_teacher_lessons.json",
            "run_summary": "11_run_summary.json",
        },
    }
    write_json(out_dir / "artifact_index.json", artifact_index)

    summary = {
        "status": "PASS" if critic.get("status") == "PASS" else "BLOCKED",
        "layer": "ECOM_OS_V3_LOCAL_SANDBOX_RUNNER_V1",
        "run_id": run_id,
        "output_dir": str(out_dir),
        "files": [p.name for p in sorted(out_dir.iterdir())],
        "evidence_status": evidence.get("status"),
        "image_critic_status": image_critic.get("status"),
        "critic_status": critic.get("status"),
        "critic_issues": critic.get("issues", []),
        "teacher_status": teacher.get("status"),
        "next_allowed_action": critic.get("next_allowed_action"),
        "no_server": True,
        "no_live_ebay": True,
        "no_delete": True,
    }
    write_json(out_dir / "11_run_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
