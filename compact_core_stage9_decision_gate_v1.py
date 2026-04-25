import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def main():
    source = BASE / Path("storage\state_compact_core\compact_core_stage9_summary_v1.json")
    payload = {}
    payload["layer"] = "COMPACT_CORE_STAGE9_DECISION_GATE_V1"
    payload["mode"] = "PROJECT_SPECIFIC_ONLY"
    payload["stage"] = 9

    if not source.exists():
        payload["status"] = "BROKEN"
        payload["source_exists"] = False
        payload["stage9_ready"] = False
        payload["decision_ready"] = False
        payload["reason"] = "stage9_summary_missing"
        payload["next_step"] = "restore_compact_core_stage9_summary_v1"

    else:
        data = json.loads(source.read_text(encoding="utf-8"))
        stage9_ready = bool(data.get("stage9_ready"))
        confirmed_layers = data.get("confirmed_layers", [])
        checks = data.get("summary_checks", {})
        title_ready = bool(checks.get("title_ready"))
        price_ready = bool(checks.get("price_ready"))
        description_ready = bool(checks.get("description_ready"))
        html_ready = bool(checks.get("html_ready"))
        images_ready = bool(checks.get("images_ready"))
        decision_ready = stage9_ready and len(confirmed_layers) == 10 and title_ready and price_ready and description_ready and html_ready and images_ready
        if decision_ready:
            payload["status"] = "OK"
            payload["decision"] = "STAGE_9_CONFIRMED"
            payload["next_step"] = "stage9_decision_gate_ready_for_archive_snapshot"
        else:
            payload["status"] = "BLOCKED"
            payload["decision"] = "STAGE_9_NOT_CONFIRMED"
            payload["next_step"] = "stage9_decision_gate_blocked_stop_here"
        payload["source_exists"] = True
        payload["source_file"] = str(source)
        payload["stage9_ready"] = stage9_ready
        payload["decision_ready"] = decision_ready
        payload["confirmed_layers_count"] = len(confirmed_layers)
        payload["decision_checks"] = {}
        payload["decision_checks"]["title_ready"] = title_ready
        payload["decision_checks"]["price_ready"] = price_ready
        payload["decision_checks"]["description_ready"] = description_ready
        payload["decision_checks"]["html_ready"] = html_ready
        payload["decision_checks"]["images_ready"] = images_ready

    out_file = BASE / Path("storage\state_compact_core\compact_core_stage9_decision_gate_v1.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("COMPACT_CORE_STAGE9_DECISION_GATE_V1_AUDIT")
    print("status =", payload["status"])
    print("layer =", payload["layer"])
    print("mode =", payload["mode"])
    print("stage =", payload["stage"])
    print("source_exists =", payload["source_exists"])
    print("stage9_ready =", payload["stage9_ready"])
    print("decision_ready =", payload["decision_ready"])
    if "confirmed_layers_count" in payload:
        print("confirmed_layers_count =", payload["confirmed_layers_count"])
    print("decision =", payload["decision"])
    print("output_file =", str(out_file))

if __name__ == "__main__":
    main()
