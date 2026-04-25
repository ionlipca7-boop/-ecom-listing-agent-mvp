import json
from pathlib import Path

base = Path(".")
source_file = base / "storage" / "approval" / "runner_approval_request_v1.json"
output_dir = base / "storage" / "approval"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "runner_approval_record_v1.json"

data = json.loads(source_file.read_text(encoding="utf-8"))

mode = data.get("mode")
approval_required = bool(data.get("approval_required"))
execution_allowed_now = bool(data.get("execution_allowed_now"))
block_reason = data.get("block_reason")
runner_action_now = data.get("runner_action_now")
request_summary = data.get("request_summary") or {}
requested_decision = data.get("requested_decision")
default_decision = data.get("default_decision")

final_decision = "KEEP_BLOCKED"
approval_status = "PENDING_EXPLICIT_APPROVAL"
runner_live_permission = False

record = {
    "status": "OK",
    "layer": "RUNNER_APPROVAL_RECORD_LAYER_V1",
    "mode": mode,
    "source_file": str(source_file),
    "approval_required": approval_required,
    "approval_status": approval_status,
    "requested_decision": requested_decision,
    "default_decision": default_decision,
    "final_decision": final_decision,
    "execution_allowed_now": execution_allowed_now,
    "runner_live_permission": runner_live_permission,
    "block_reason": block_reason,
    "runner_action_now": runner_action_now,
    "request_summary": request_summary,
    "next_step": "build_runner_status_snapshot_layer_v1"
}

output_file.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_APPROVAL_RECORD_LAYER_V1",
    "mode": mode,
    "approval_required": approval_required,
    "approval_status": approval_status,
    "final_decision": final_decision,
    "runner_live_permission": runner_live_permission,
    "execution_allowed_now": execution_allowed_now,
    "block_reason": block_reason,
    "next_step": "build_runner_status_snapshot_layer_v1"
}

print("RUNNER_APPROVAL_RECORD_LAYER_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
