import json, pathlib 
root = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP") 
files = { 
    "post_runner_branch_decision": root / r"storage\state_control\post_runner_branch_decision_v1.json", 
    "n8n_dispatcher_checkpoint": root / r"storage\state_control\n8n_dispatcher_checkpoint_v1.json", 
    "n8n_dispatch_contract": root / r"storage\state_control\n8n_dispatch_contract_v1.json", 
    "n8n_dispatch_state_map": root / r"storage\state_control\n8n_dispatch_state_map_v1.json", 
    "n8n_dispatch_audit_flow": root / r"storage\state_control\n8n_dispatch_audit_flow_v1.json", 
    "n8n_dispatch_payload_contract": root / r"storage\state_control\n8n_dispatch_payload_contract_v1.json", 
    "n8n_dispatch_decision_gate": root / r"storage\state_control\n8n_dispatch_decision_gate_v1.json", 
    "n8n_dispatch_runner_handoff": root / r"storage\state_control\n8n_dispatch_runner_handoff_v1.json", 
    "n8n_dispatch_archivist_handoff": root / r"storage\state_control\n8n_dispatch_archivist_handoff_v1.json", 
    "n8n_dispatch_state_update_handoff": root / r"storage\state_control\n8n_dispatch_state_update_handoff_v1.json", 
    "n8n_dispatch_completion_checkpoint": root / r"storage\state_control\n8n_dispatch_completion_checkpoint_v1.json" 
} 
data = {} 
missing = [] 
for name, path in files.items(): 
    if path.exists(): 
        data[name] = json.loads(path.read_text(encoding="utf-8")) 
    else: 
        missing.append(name) 
expected_count = len(files) 
completed_count = len(data) 
all_present = completed_count == expected_count 
completion = data.get("n8n_dispatch_completion_checkpoint", {}) 
branch = data.get("post_runner_branch_decision", {}) 
phase_confirmed = completion.get("phase") == 8 
selected_branch_confirmed = branch.get("selected_branch") == "prepare_n8n_dispatcher_v1" 
chain_closed = completion.get("chain_closed") is True 
dispatcher_completion_ready = completion.get("dispatcher_completion_ready") is True 
execution_allowed = completion.get("execution_allowed") 
final_decision = completion.get("final_decision") 
n8n_ready = completion.get("n8n_ready") 
phase_8_canon_complete = all_present and phase_confirmed and selected_branch_confirmed and chain_closed and dispatcher_completion_ready and (execution_allowed is False) and (final_decision == "KEEP_BLOCKED") 
out = root / r"storage\audit\full_phase_8_canonical_audit_v1.txt" 
lines = [ 
    "FULL_PHASE_8_CANONICAL_AUDIT_V1", 
    "status = OK", 
    "expected_component_count = " + str(expected_count), 
    "completed_component_count = " + str(completed_count), 
    "all_components_present = " + str(all_present), 
    "missing_components = " + str(missing), 
    "phase_confirmed = " + str(phase_confirmed), 
    "selected_branch_confirmed = " + str(selected_branch_confirmed), 
    "chain_closed = " + str(chain_closed), 
    "dispatcher_completion_ready = " + str(dispatcher_completion_ready), 
    "execution_allowed = " + str(execution_allowed), 
    "final_decision = " + str(final_decision), 
    "n8n_ready = " + str(n8n_ready), 
    "phase_8_canon_complete = " + str(phase_8_canon_complete), 
    "allowed_next_after_canon = review_and_close_phase_8_then_prepare_next_front" 
] 
out.write_text("\n".join(lines), encoding="utf-8") 
print("\n".join(lines)) 
