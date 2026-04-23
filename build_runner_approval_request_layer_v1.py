import json
from pathlib import Path

base = Path(".")
source_file = base / "storage" / "gates" / "runner_execution_gate_v1.json"
output_dir = base / "storage" / "approval"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "runner_approval_request_v1.json"

data = json.loads(source_file.read_text(encoding="utf-8"))

mode = data.get("mode")
checks = data.get("checks") or {}
execution_allowed = data.get("execution_allowed")
block_reason = data.get("block_reason")
runner_action_now = data.get("runner_action_now")

data_ready = bool(checks.get("data_ready"))
project_specific_only = bool(checks.get("project_specific_only"))
live_execution_still_blocked = bool(checks.get("live_execution_still_blocked"))
has_title = bool(checks.get("has_title"))
has_price = bool(checks.get("has_price"))
has_description_html = bool(checks.get("has_description_html"))
sufficient_images = bool(checks.get("sufficient_images"))

approval_request = {
    "status": "OK",
    "layer": "RUNNER_APPROVAL_REQUEST_LAYER_V1",
    "mode": mode,
    "source_file": str(source_file),
    "approval_required": True,
    "execution_allowed_now": execution_allowed,
    "block_reason": block_reason,
    "runner_action_now": runner_action_now,
    "request_summary": {
        "project_specific_only": project_specific_only,
        "live_execution_still_blocked": live_execution_still_blocked,
        "data_ready": data_ready,
        "has_title": has_title,
        "has_price": has_price,
        "has_description_html": has_description_html,
        "sufficient_images": sufficient_images
    },
    "requested_decision": "APPROVE_OR_KEEP_BLOCKED",
    "default_decision": "KEEP_BLOCKED",
    "next_step": "build_runner_approval_record_layer_v1"
}

output_file.write_text(json.dumps(approval_request, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_APPROVAL_REQUEST_LAYER_V1",
    "mode": mode,
    "approval_required": True,
    "execution_allowed_now": execution_allowed,
    "block_reason": block_reason,
    "data_ready": data_ready,
    "default_decision": "KEEP_BLOCKED",
    "next_step": "build_runner_approval_record_layer_v1"
}

print("RUNNER_APPROVAL_REQUEST_LAYER_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
