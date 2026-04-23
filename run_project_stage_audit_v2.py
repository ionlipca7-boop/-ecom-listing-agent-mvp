import json, pathlib
root = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP")
def exists(rel):
    return (root / rel).exists()
checks = {}
checks["project_manifest_json"] = exists(r"storage\control_layer\project_manifest.json")
checks["control_rules_json"] = exists(r"storage\control_layer\control_rules.json")
checks["project_state_json"] = exists(r"storage\control_layer\project_state.json")
checks["project_history_jsonl"] = exists(r"storage\control_layer\project_history.jsonl")
checks["control_agent_py"] = exists(r"control_agent.py") or exists(r"agents\control_agent.py") or exists(r"storage\control_layer\control_agent.py")
checks["archivist_agent_py"] = exists(r"archivist_agent.py") or exists(r"agents\archivist_agent.py") or exists(r"storage\control_layer\archivist_agent.py")
checks["runner_agent_py"] = exists(r"runner_agent.py") or exists(r"agents\runner_agent.py") or exists(r"storage\control_layer\runner_agent.py")
checks["n8n_connection_step"] = exists(r"storage\state_transition\compact_core_transition_front_v1_verified.json") or exists(r"storage\memory\archive\compact_core_transition_front_v1_verified_archive.json")
checks["compact_core_transition_after_control_layer"] = exists(r"storage\state_transition\compact_core_transition_front_v1_verified.json")
order = ["project_manifest_json","control_rules_json","project_state_json","project_history_jsonl","control_agent_py","archivist_agent_py","runner_agent_py","n8n_connection_step","compact_core_transition_after_control_layer"]
for item in order:
    if checks[item]:
        reached = reached + 
    else:
        break
done_steps = order[:reached]
remaining_steps = order[reached:]
if len(done_steps) > 0:
    last_completed_step = done_steps[-1]
else:
    last_completed_step = "none"
if len(remaining_steps) > 0:
    next_logical_step = remaining_steps[0]
else:
    next_logical_step = "canon_line_complete"
result = {"status":"OK","project":"ECOM_LISTING_AGENT_MVP_CONTROL_ROOM","audit_type":"CURRENT_PROJECT_STAGE_AUDIT_V2","phase_8_canon_complete":True,"compact_transition_verified":checks["compact_core_transition_after_control_layer"],"reached_step_count":reached,"last_completed_step":last_completed_step,"next_logical_step":next_logical_step,"remaining_count":len(remaining_steps),"done_steps":done_steps,"remaining_steps":remaining_steps,"checks":checks}
out_json = root / r"storage\memory\archive\current_project_stage_audit_v2.json"
out_txt = root / r"storage\audit\current_project_stage_audit_v2.txt"
out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
lines = []
lines.append("CURRENT_PROJECT_STAGE_AUDIT_V2")
lines.append("status = OK")
lines.append("phase_8_canon_complete = True")
lines.append("compact_transition_verified = " + str(result["compact_transition_verified"]))
lines.append("reached_step_count = " + str(reached))
lines.append("last_completed_step = " + last_completed_step)
lines.append("next_logical_step = " + next_logical_step)
lines.append("remaining_count = " + str(len(remaining_steps)))
out_txt.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
