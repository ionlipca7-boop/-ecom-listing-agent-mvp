import json
from pathlib import Path

base = Path(".")
preview_file = base / "storage" / "preview" / "runner_preview_v3.json"
validation_file = base / "storage" / "validation" / "runner_validation_v2.json"
render_file = base / "storage" / "render" / "runner_render_v1.json"
live_payload_file = base / "storage" / "live_payload" / "runner_live_payload_v1.json"
guard_file = base / "storage" / "guards" / "runner_live_guard_v1.json"
gate_file = base / "storage" / "gates" / "runner_execution_gate_v1.json"
approval_file = base / "storage" / "approval" / "runner_approval_record_v1.json"
output_dir = base / "storage" / "status"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "runner_status_snapshot_v1.json"

preview = json.loads(preview_file.read_text(encoding="utf-8"))
validation = json.loads(validation_file.read_text(encoding="utf-8"))
render = json.loads(render_file.read_text(encoding="utf-8"))
live_payload = json.loads(live_payload_file.read_text(encoding="utf-8"))
guard = json.loads(guard_file.read_text(encoding="utf-8"))
gate = json.loads(gate_file.read_text(encoding="utf-8"))
approval = json.loads(approval_file.read_text(encoding="utf-8"))

snapshot = {
    "status": "OK",
    "layer": "RUNNER_STATUS_SNAPSHOT_LAYER_V1",
    "mode": approval.get("mode"),
    "pipeline": {
        "preview_ready": preview.get("status") == "OK",
        "validation_ready": validation.get("status") == "OK",
        "render_ready": render.get("status") == "OK",
        "live_payload_ready": live_payload.get("status") == "OK",
        "guard_ready": guard.get("status") == "OK",
        "gate_ready": gate.get("status") == "OK",
        "approval_record_ready": approval.get("status") == "OK"
    },
    "listing_summary": {
        "title": render.get("title"),
        "price": render.get("price"),
        "currency": render.get("currency"),
        "image_count": render.get("visual", {}).get("image_count"),
        "has_html": bool(render.get("html"))
    },
    "control_summary": {
        "guard_result": guard.get("guard_result"),
        "execution_allowed": gate.get("execution_allowed"),
        "block_reason": gate.get("block_reason"),
        "approval_status": approval.get("approval_status"),
        "final_decision": approval.get("final_decision"),
        "runner_live_permission": approval.get("runner_live_permission")
    },
    "next_step": "archive_runner_status_and_prepare_transition_checkpoint_v1"
}

output_file.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_STATUS_SNAPSHOT_LAYER_V1",
    "mode": approval.get("mode"),
    "preview_ready": preview.get("status") == "OK",
    "validation_ready": validation.get("status") == "OK",
    "render_ready": render.get("status") == "OK",
    "live_payload_ready": live_payload.get("status") == "OK",
    "guard_ready": guard.get("status") == "OK",
    "gate_ready": gate.get("status") == "OK",
    "approval_record_ready": approval.get("status") == "OK",
    "execution_allowed": gate.get("execution_allowed"),
    "final_decision": approval.get("final_decision"),
    "runner_live_permission": approval.get("runner_live_permission"),
    "next_step": "archive_runner_status_and_prepare_transition_checkpoint_v1"
}

print("RUNNER_STATUS_SNAPSHOT_LAYER_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
