import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def main():
    source = BASE / Path("storage\state_compact_core\compact_core_checkpoint_v1.json")
    payload = {}
    payload["layer"] = "COMPACT_CORE_STAGE9_SUMMARY_V1"
    payload["mode"] = "PROJECT_SPECIFIC_ONLY"
    payload["stage"] = 9

    if not source.exists():
        payload["status"] = "BROKEN"
        payload["source_exists"] = False
        payload["checkpoint_ready"] = False
        payload["stage9_ready"] = False
        payload["reason"] = "compact_checkpoint_missing"
        payload["next_step"] = "restore_compact_core_checkpoint_v1"

    else:
        data = json.loads(source.read_text(encoding="utf-8"))
        checkpoint_ready = bool(data.get("checkpoint_ready"))
        checks = data.get("checkpoint_checks", {})
        title_ready = bool(checks.get("title_ready"))
        price_ready = bool(checks.get("price_ready"))
        description_ready = bool(checks.get("description_ready"))
        html_ready = bool(checks.get("html_ready"))
        images_ready = bool(checks.get("images_ready"))
        stage9_ready = checkpoint_ready and title_ready and price_ready and description_ready and html_ready and images_ready
        if stage9_ready:
            payload["status"] = "OK"
            payload["next_step"] = "stage9_summary_ready_for_archive_or_next_decision"
        else:
            payload["status"] = "BLOCKED"
            payload["next_step"] = "stage9_summary_blocked_stop_here"
        payload["source_exists"] = True
        payload["source_file"] = str(source)
        payload["checkpoint_ready"] = checkpoint_ready
        payload["stage9_ready"] = stage9_ready
        payload["confirmed_layers"] = [
            "compact_core_transition_front_v1",
            "compact_core_state_hub_v1",
            "compact_core_execution_bridge_v1",
            "compact_core_preview_contract_v1",
            "compact_core_preview_verification_v1",
            "compact_core_preview_ready_gate_v1",
            "compact_core_runner_payload_v1",
            "compact_core_runner_handoff_gate_v1",
            "compact_core_delivery_state_v1",
            "compact_core_checkpoint_v1"
        ]
        payload["summary_checks"] = {}
        payload["summary_checks"]["title_ready"] = title_ready
        payload["summary_checks"]["price_ready"] = price_ready
        payload["summary_checks"]["description_ready"] = description_ready
        payload["summary_checks"]["html_ready"] = html_ready
        payload["summary_checks"]["images_ready"] = images_ready

    out_file = BASE / Path("storage\state_compact_core\compact_core_stage9_summary_v1.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("COMPACT_CORE_STAGE9_SUMMARY_V1_AUDIT")
    print("status =", payload["status"])
    print("layer =", payload["layer"])
    print("mode =", payload["mode"])
    print("stage =", payload["stage"])
    print("source_exists =", payload["source_exists"])
    print("checkpoint_ready =", payload["checkpoint_ready"])
    print("stage9_ready =", payload["stage9_ready"])
    if "confirmed_layers" in payload:
        print("confirmed_layers_count =", len(payload["confirmed_layers"]))
    print("output_file =", str(out_file))

if __name__ == "__main__":
    main()
