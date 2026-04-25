import json
from pathlib import Path

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
EXPORTS = ROOT / "storage" / "exports"
INPUT = EXPORTS / "first_real_multi_listing_run_payload_v3.json"

data = json.loads(INPUT.read_text(encoding="utf-8"))

print("PAYLOAD_STRUCTURE_AUDIT_V1")

print("root_keys =", list(data.keys()))
print("root.blocking_fields_count =", data.get("blocking_fields_count"))
print("root.runtime_ready_for_live =", data.get("runtime_ready_for_live"))
print("root.next_step =", data.get("next_step"))

payload = data.get("payload")
print("payload_exists =", isinstance(payload, dict))
if isinstance(payload, dict):
    print("payload_keys =", list(payload.keys()))
    print("payload.blocking_fields_count =", payload.get("blocking_fields_count"))
    print("payload.runtime_ready_for_live =", payload.get("runtime_ready_for_live"))

runtime = data.get("runtime")
print("runtime_exists =", isinstance(runtime, dict))
if isinstance(runtime, dict):
    print("runtime_keys =", list(runtime.keys()))
    print("runtime.blocking_fields_count =", runtime.get("blocking_fields_count"))
    print("runtime.runtime_ready_for_live =", runtime.get("runtime_ready_for_live"))

state = data.get("state")
print("state_exists =", isinstance(state, dict))
if isinstance(state, dict):
    print("state_keys =", list(state.keys()))
    print("state.blocking_fields_count =", state.get("blocking_fields_count"))
    print("state.runtime_ready_for_live =", state.get("runtime_ready_for_live"))

meta = data.get("meta")
print("meta_exists =", isinstance(meta, dict))
if isinstance(meta, dict):
    print("meta_keys =", list(meta.keys()))
    print("meta.blocking_fields_count =", meta.get("blocking_fields_count"))
    print("meta.runtime_ready_for_live =", meta.get("runtime_ready_for_live"))

print("next_step = locate_true_blocking_fields_count_path")