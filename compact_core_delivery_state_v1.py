import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def main():
    source = BASE / Path("storage\state_compact_core\compact_core_runner_handoff_gate_v1.json")
    payload = {}
    payload["layer"] = "COMPACT_CORE_DELIVERY_STATE_V1"
    payload["mode"] = "PROJECT_SPECIFIC_ONLY"
    payload["stage"] = 9

    if not source.exists():
        payload["status"] = "BROKEN"
        payload["source_exists"] = False
        payload["handoff_ready"] = False
        payload["delivery_ready"] = False
        payload["reason"] = "runner_handoff_gate_missing"
        payload["next_step"] = "restore_runner_handoff_gate_v1"

    else:
        data = json.loads(source.read_text(encoding="utf-8"))
        handoff_ready = bool(data.get("handoff_ready"))
        checks = data.get("gate_checks", {})
        title_ready = bool(checks.get("title_ready"))
        price_ready = bool(checks.get("price_ready"))
        description_ready = bool(checks.get("description_ready"))
        html_ready = bool(checks.get("html_ready"))
        images_ready = bool(checks.get("images_ready"))
        delivery_ready = handoff_ready and title_ready and price_ready and description_ready and html_ready and images_ready
        if delivery_ready:
            payload["status"] = "OK"
            payload["next_step"] = "delivery_state_ready_for_next_compact_core_layer"
        else:
            payload["status"] = "BLOCKED"
            payload["next_step"] = "delivery_state_not_ready_stop_here"
        payload["source_exists"] = True
        payload["source_file"] = str(source)
        payload["handoff_ready"] = handoff_ready
        payload["delivery_ready"] = delivery_ready
        payload["delivery_checks"] = {}
        payload["delivery_checks"]["title_ready"] = title_ready
        payload["delivery_checks"]["price_ready"] = price_ready
        payload["delivery_checks"]["description_ready"] = description_ready
        payload["delivery_checks"]["html_ready"] = html_ready
        payload["delivery_checks"]["images_ready"] = images_ready

    out_file = BASE / Path("storage\state_compact_core\compact_core_delivery_state_v1.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("COMPACT_CORE_DELIVERY_STATE_V1_AUDIT")
    print("status =", payload["status"])
    print("layer =", payload["layer"])
    print("mode =", payload["mode"])
    print("stage =", payload["stage"])
    print("source_exists =", payload["source_exists"])
    print("handoff_ready =", payload["handoff_ready"])
    print("delivery_ready =", payload["delivery_ready"])
    print("output_file =", str(out_file))

if __name__ == "__main__":
    main()
