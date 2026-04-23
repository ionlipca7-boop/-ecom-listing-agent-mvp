import json
from pathlib import Path

base = Path(".")
source_file = base / "storage" / "live_payload" / "runner_live_payload_v1.json"
output_dir = base / "storage" / "guards"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "runner_live_guard_v1.json"

data = json.loads(source_file.read_text(encoding="utf-8"))

mode = data.get("mode")
payload_type = data.get("payload_type")
live_execution_allowed = data.get("live_execution_allowed")
has_title = bool(data.get("title"))
has_price = isinstance(data.get("price"), dict) and data.get("price", {}).get("value") is not None
has_description_html = bool(data.get("description_html"))
images = data.get("images") or []
if not isinstance(images, list):
    images = [images]
image_count = len(images)

guard = {
    "status": "OK",
    "layer": "RUNNER_LIVE_GUARD_LAYER_V1",
    "mode": mode,
    "source_file": str(source_file),
    "checks": {
        "project_specific_only": mode == "PROJECT_SPECIFIC_ONLY",
        "payload_type_live_draft_only": payload_type == "LIVE_DRAFT_ONLY",
        "live_execution_still_blocked": live_execution_allowed is False,
        "has_title": has_title,
        "has_price": has_price,
        "has_description_html": has_description_html,
    },
    "image_count": image_count,
    "guard_result": "LIVE_BLOCKED_UNTIL_EXPLICIT_APPROVAL",
    "next_step": "build_runner_execution_gate_v1"
}

output_file.write_text(json.dumps(guard, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_LIVE_GUARD_LAYER_V1",
    "mode": mode,
    "project_specific_only": mode == "PROJECT_SPECIFIC_ONLY",
    "payload_type_live_draft_only": payload_type == "LIVE_DRAFT_ONLY",
    "live_execution_still_blocked": live_execution_allowed is False,
    "has_title": has_title,
    "has_price": has_price,
    "has_description_html": has_description_html,
    "image_count": image_count,
    "guard_result": "LIVE_BLOCKED_UNTIL_EXPLICIT_APPROVAL",
    "next_step": "build_runner_execution_gate_v1"
}

print("RUNNER_LIVE_GUARD_LAYER_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
