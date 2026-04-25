import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def read_json(rel_path):
    p = BASE / Path(rel_path)
    if not p.exists():
        return {}, str(p), False
    return json.loads(p.read_text(encoding="utf-8")), str(p), True

def main():
    decision_data, decision_path, decision_exists = read_json(r"storage\state_compact_core\compact_core_stage9_decision_gate_v1.json")
    summary_data, summary_path, summary_exists = read_json(r"storage\state_compact_core\compact_core_stage9_summary_v1.json")
    archive_dir = BASE / Path(r"storage\memoryrchive")
    archive_dir.mkdir(parents=True, exist_ok=True)
    payload = {}
    payload["date"] = "2026-04-19"
    payload["project"] = "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM"
    payload["archive_type"] = "TRANSITION_POST_STAGE9_ARCHIVE_V2"
    payload["status"] = "OK"
    payload["stage"] = 9
    payload["stage9_confirmed"] = bool(decision_data.get("stage9_ready")) and bool(decision_data.get("decision_ready")) and decision_data.get("decision") == "STAGE_9_CONFIRMED"
    payload["decision"] = decision_data.get("decision", "")
    payload["confirmed_layers_count"] = decision_data.get("confirmed_layers_count", 0)
    payload["decision_exists"] = decision_exists
    payload["summary_exists"] = summary_exists
    payload["confirmed_layers"] = summary_data.get("confirmed_layers", [])
    payload["main_result"] = "STAGE_9_CONFIRMED_AND_READY_FOR_POST_STAGE9_DIRECTION_PLAN"
    payload["errors_this_chat"] = [
        "utf8_bom_or_feff_in_python_files",
        "broken_main_guard_in_preview_contract",
        "fragile_direct_echo_build_caused_missing_lines_and_missing_keys",
        "cmd_traps_with_special_characters_and_partial_writes",
        "windows_path_escape_errors_in_archive_writer",
        "non_utf8_cyrillic_in_generated_python_file",
        "late_chat_degradation_after_many_steps"
    ]
    payload["solutions_this_chat"] = [
        "first_real_audit_then_fix",
        "sanitize_bom_before_logic_repair",
        "if_file_breaks_twice_rebuild_full_file",
        "prefer_writer_script_over_fragile_direct_echo_build",
        "use_raw_windows_paths_in_generated_python_files",
        "avoid_cyrillic_inside_generated_python_source",
        "after_ok_audit_only_one_next_step",
        "archive_first_then_new_chat_prompt"
    ]
    payload["mandatory_rules_next_chat"] = [
        "start_with_canonical_9_step_audit",
        "project_specific_only",
        "one_step_only",
        "real_verification_before_action",
        "include_previous_errors_and_fixes_in_transition_prompt",
        "prefer_writer_script_when_direct_echo_build_becomes_fragile",
        "build_post_stage9_direction_plan_before_new_technical_layers"
    ]
    payload["next_step"] = "open_new_chat_and_build_post_stage9_direction_plan_v1"
    out_file = archive_dir / "transition_post_stage9_archive_v2.json"
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TRANSITION_POST_STAGE9_ARCHIVE_V2_AUDIT")
    print("status =", payload["status"])
    print("stage =", payload["stage"])
    print("stage9_confirmed =", payload["stage9_confirmed"])
    print("decision =", payload["decision"])
    print("confirmed_layers_count =", payload["confirmed_layers_count"])
    print("output_file =", str(out_file))

if __name__ == "__main__":
    main()
