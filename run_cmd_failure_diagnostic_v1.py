import json
from pathlib import Path

ROOT = Path(".")
EXPORT_DIR = ROOT / "storage" / "exports"
ARCHIVE_DIR = ROOT / "storage" / "memory" / "archive"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

CHECK_FILES = [
    "run_generator_agent_v1.py",
    "run_generator_agent_v2.py",
    "run_generator_agent_v3.py",
    "run_generator_agent_v4.py",
    "run_generator_agent_v5.py",
    "run_generator_layer_readiness_audit_v1_fix.py",
    "run_generator_execution_probe_v1_fix.py",
    "run_generator_entrypoint_inspect_v1.py"
]

CHECK_JSON = [
    "storage\\exports\\generator_layer_readiness_audit_v1.json",
    "storage\\exports\\generator_execution_probe_v1.json",
    "storage\\exports\\generator_entrypoint_inspect_v1.json",
    "storage\\memory\\archive\\generator_probe_error_archive_v1.json",
    "storage\\memory\\archive\\generator_entrypoint_inspect_error_archive_v1.json"
]

file_status = []
json_status = []
symptoms = []
recommendations = []

for rel in CHECK_FILES:
    p = ROOT / rel
    item = {"path": rel, "exists": p.exists(), "size": p.stat().st_size if p.exists() else 0}
    if p.exists() and p.is_file():
        text = p.read_text(encoding="utf-8", errors="ignore")
        item["has_generator_ready"] = "generator_ready =" in text
        item["has_probe_ready"] = "probe_ready =" in text
        item["has_main_guard"] = "__main__" in text
    file_status.append(item)

for rel in CHECK_JSON:
    p = ROOT / rel
    json_status.append({"path": rel, "exists": p.exists(), "size": p.stat().st_size if p.exists() else 0})

if not (ROOT / "run_generator_entrypoint_inspect_v1.py").exists():
    symptoms.append("entrypoint_inspect_file_not_created")
if not (ROOT / "storage\\exports\\generator_entrypoint_inspect_v1.json").exists():
    symptoms.append("entrypoint_inspect_json_missing")
if (ROOT / "run_generator_layer_readiness_audit_v1_fix.py").exists():
    text = (ROOT / "run_generator_layer_readiness_audit_v1_fix.py").read_text(encoding="utf-8", errors="ignore")
    if "generator_ready =" not in text:
        symptoms.append("lost_assignment_line_generator_ready")
if (ROOT / "run_generator_execution_probe_v1.py").exists():
    text = (ROOT / "run_generator_execution_probe_v1.py").read_text(encoding="utf-8", errors="ignore")
    if "probe_ready =" not in text:
        symptoms.append("lost_assignment_line_probe_ready")

recommendations.append("do_not_use_multiline_python_c_in_cmd")
recommendations.append("do_not_use_long_echo_file_build_for_logic_files")
recommendations.append("prefer_small_physical_py_writer_script_for_next_repairs")
recommendations.append("archive_each_cmd_pattern_failure_immediately")

report = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "cmd_failure_diagnostic_completed",
    "file_status": file_status,
    "json_status": json_status,
    "symptoms": symptoms,
    "recommendations": recommendations,
    "next_step": "build_safe_writer_script_v1"
}

out = EXPORT_DIR / "cmd_failure_diagnostic_v1.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("CMD_FAILURE_DIAGNOSTIC_DONE")
print("symptoms_count =", len(symptoms))
print("report =", out)
