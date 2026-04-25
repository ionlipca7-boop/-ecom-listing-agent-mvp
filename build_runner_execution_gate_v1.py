import json
from pathlib import Path

base = Path(".")
source_file = base / "storage" / "guards" / "runner_live_guard_v1.json"
output_dir = base / "storage" / "gates"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "runner_execution_gate_v1.json"

data = json.loads(source_file.read_text(encoding="utf-8"))

mode = data.get("mode")
checks = data.get("checks") or {}
guard_result = data.get("guard_result")
image_count = data.get("image_count")

project_specific_only = bool(checks.get("project_specific_only"))
payload_type_live_draft_only = bool(checks.get("payload_type_live_draft_only"))
live_execution_still_blocked = bool(checks.get("live_execution_still_blocked"))
has_title = bool(checks.get("has_title"))
has_price = bool(checks.get("has_price"))
has_description_html = bool(checks.get("has_description_html"))
sufficient_images = bool(image_count)

data_ready = has_title and has_price and has_description_html and sufficient_images
execution_allowed = False
block_reason = "EXPLICIT_APPROVAL_REQUIRED"

gate = {
    "status": "OK",
    "layer": "RUNNER_EXECUTION_GATE_V1",
    "mode": mode,
    "source_file": str(source_file),
    "gate_type": "EXECUTION_GATE",
    "checks": {
        "project_specific_only": project_specific_only,
        "payload_type_live_draft_only": payload_type_live_draft_only,
        "live_execution_still_blocked": live_execution_still_blocked,
        "data_ready": data_ready,
        "has_title": has_title,
        "has_price": has_price,
        "has_description_html": has_description_html,
        "sufficient_images": sufficient_images
    },
    "guard_result": guard_result,
    "execution_allowed": execution_allowed,
    "block_reason": block_reason,
    "next_allowed_step": "build_runner_approval_request_layer_v1",
    "runner_action_now": "DO_NOT_EXECUTE_LIVE"
}

output_file.write_text(json.dumps(gate, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_EXECUTION_GATE_V1",
    "mode": mode,
    "project_specific_only": project_specific_only,
    "payload_type_live_draft_only": payload_type_live_draft_only,
    "live_execution_still_blocked": live_execution_still_blocked,
    "data_ready": data_ready,
    "execution_allowed": execution_allowed,
    "block_reason": block_reason,
    "next_allowed_step": "build_runner_approval_request_layer_v1",
    "runner_action_now": "DO_NOT_EXECUTE_LIVE"
}

print("RUNNER_EXECUTION_GATE_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
