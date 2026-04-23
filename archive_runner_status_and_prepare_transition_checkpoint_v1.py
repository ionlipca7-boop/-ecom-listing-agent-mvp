import json
from pathlib import Path

base = Path(".")
status_file = base / "storage" / "status" / "runner_status_snapshot_v1.json"
archive_dir = base / "storage" / "memory" / "archive"
checkpoint_dir = base / "storage" / "checkpoints"
archive_dir.mkdir(parents=True, exist_ok=True)
checkpoint_dir.mkdir(parents=True, exist_ok=True)
archive_file = archive_dir / "runner_status_archive_v1.json"
checkpoint_file = checkpoint_dir / "runner_transition_checkpoint_v1.json"

status_data = json.loads(status_file.read_text(encoding="utf-8"))

archive_data = {
    "status": "OK",
    "layer": "RUNNER_STATUS_ARCHIVE_V1",
    "mode": status_data.get("mode"),
    "source_file": str(status_file),
    "archived_snapshot_layer": status_data.get("layer"),
    "pipeline": status_data.get("pipeline"),
    "listing_summary": status_data.get("listing_summary"),
    "control_summary": status_data.get("control_summary"),
    "archive_purpose": "preserve_runner_control_state_before_transition",
    "next_step": "runner_transition_checkpoint_v1"
}

checkpoint_data = {
    "status": "OK",
    "layer": "RUNNER_TRANSITION_CHECKPOINT_V1",
    "mode": status_data.get("mode"),
    "source_file": str(status_file),
    "runner_pipeline_complete": all(bool(v) for v in (status_data.get("pipeline") or {}).values()),
    "execution_allowed": (status_data.get("control_summary") or {}).get("execution_allowed"),
    "final_decision": (status_data.get("control_summary") or {}).get("final_decision"),
    "runner_live_permission": (status_data.get("control_summary") or {}).get("runner_live_permission"),
    "transition_state": "SAFE_TO_CONTINUE_WITH_BLOCKED_RUNNER_FLOW",
    "next_step": "decide_next_project_specific_branch_after_runner_checkpoint"
}

archive_file.write_text(json.dumps(archive_data, indent=2, ensure_ascii=False), encoding="utf-8")
checkpoint_file.write_text(json.dumps(checkpoint_data, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "ARCHIVE_RUNNER_STATUS_AND_PREPARE_TRANSITION_CHECKPOINT_V1",
    "mode": status_data.get("mode"),
    "archive_created": archive_file.exists(),
    "checkpoint_created": checkpoint_file.exists(),
    "runner_pipeline_complete": checkpoint_data.get("runner_pipeline_complete"),
    "execution_allowed": checkpoint_data.get("execution_allowed"),
    "final_decision": checkpoint_data.get("final_decision"),
    "runner_live_permission": checkpoint_data.get("runner_live_permission"),
    "transition_state": checkpoint_data.get("transition_state"),
    "next_step": "decide_next_project_specific_branch_after_runner_checkpoint"
}

print("ARCHIVE_RUNNER_STATUS_AND_PREPARE_TRANSITION_CHECKPOINT_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
