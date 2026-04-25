import json, pathlib, subprocess, sys

BASE = pathlib.Path(__file__).resolve().parent
STATE = BASE / "storage" / "state_control"
AUDIT_DIR = BASE / "storage" / "audit"
STATE.mkdir(parents=True, exist_ok=True)
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

INPUT = STATE / "listing_clone_baseline_v1.json"
BRIDGE = STATE / "control_room_runtime_bridge_v1.json"
TARGET = BASE / "scripts" / "build_new_listing_from_clone_baseline_v1.py"
OUTPUT = AUDIT_DIR / "run_control_room_route_fix_v1_output.txt"

bridge_result = {
    "status": "OK",
    "layer": "CONTROL_ROOM_RUNTIME_BRIDGE_V1",
    "input_exists": INPUT.exists(),
    "target_script_exists": TARGET.exists(),
    "live_execution": False,
    "parallel_branches": False,
    "next_allowed_action": "build_new_listing_from_clone_baseline_v1"
}

BRIDGE.write_text(json.dumps(bridge_result, indent=2, ensure_ascii=False), encoding="utf-8")

if not INPUT.exists():
    result = {
        "status": "ERROR",
        "layer": "CONTROL_ROOM_RUNTIME_ROUTE_FIX_V1",
        "reason": "listing_clone_baseline_v1_missing",
        "next_allowed_action": "restore_listing_clone_baseline_v1",
        "live_execution": False
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(1)

if not TARGET.exists():
    result = {
        "status": "ERROR",
        "layer": "CONTROL_ROOM_RUNTIME_ROUTE_FIX_V1",
        "reason": "build_new_listing_from_clone_baseline_v1_script_missing",
        "next_allowed_action": "restore_build_new_listing_from_clone_baseline_v1_script",
        "live_execution": False
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(1)

proc = subprocess.run([sys.executable, str(TARGET)], capture_output=True, text=True)
output_text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
OUTPUT.write_text(output_text, encoding="utf-8")

final_result = {
    "status": "OK" if proc.returncode == 0 else "ERROR",
    "layer": "CONTROL_ROOM_RUNTIME_ROUTE_FIX_V1",
    "route_progression_fixed": proc.returncode == 0,
    "bridge_written": True,
    "target_script": str(TARGET),
    "target_returncode": proc.returncode,
    "output_file": str(OUTPUT),
    "live_execution": False,
    "next_allowed_action": "verify_new_listing_from_clone_baseline_v1" if proc.returncode == 0 else "inspect_build_new_listing_from_clone_baseline_v1_failure"
}

print(json.dumps(final_result, indent=2, ensure_ascii=False))
if proc.stdout:
    print(proc.stdout)
if proc.stderr:
    print(proc.stderr, file=sys.stderr)
raise SystemExit(proc.returncode)
