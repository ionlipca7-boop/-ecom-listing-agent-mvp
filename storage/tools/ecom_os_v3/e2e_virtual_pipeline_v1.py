from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[2]
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from agents.system_audit_agent_v1 import SystemAuditAgentV1


TEST_INPUTS = [
    CURRENT_DIR / "test_inputs" / "usb_c_cable_stand_v1.json",
    CURRENT_DIR / "test_inputs" / "usb_adapter_6pcs_v1.json",
]


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def run_subprocess(args: List[str]) -> Dict[str, Any]:
    proc = subprocess.run(args, cwd=str(PROJECT_ROOT), text=True, encoding="utf-8", errors="replace", capture_output=True)
    return {
        "args": args,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def latest_run_dirs(before: set[str]) -> List[Path]:
    root = PROJECT_ROOT / "storage" / "outputs" / "ecom_os_v3" / "local_sandbox"
    if not root.exists():
        return []
    dirs = [p for p in root.iterdir() if p.is_dir() and p.name not in before]
    return sorted(dirs, key=lambda p: p.name)


def main() -> int:
    e2e_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    e2e_out = PROJECT_ROOT / "storage" / "outputs" / "ecom_os_v3" / "e2e_virtual" / e2e_id
    e2e_out.mkdir(parents=True, exist_ok=True)

    sandbox_root = PROJECT_ROOT / "storage" / "outputs" / "ecom_os_v3" / "local_sandbox"
    before = {p.name for p in sandbox_root.iterdir()} if sandbox_root.exists() else set()

    step_results: List[Dict[str, Any]] = []
    run_dirs: List[Path] = []
    runner = CURRENT_DIR / "local_sandbox_runner_v1.py"

    for test_input in TEST_INPUTS:
        if not test_input.exists():
            step_results.append({"status": "BLOCKED_INPUT_MISSING", "input": str(test_input)})
            continue
        result = run_subprocess([sys.executable, str(runner), str(test_input)])
        step_results.append({
            "status": "PASS" if result["returncode"] == 0 else "BLOCKED",
            "input": str(test_input),
            "returncode": result["returncode"],
            "stdout_tail": result["stdout"][-4000:],
            "stderr_tail": result["stderr"][-2000:],
        })

    run_dirs = latest_run_dirs(before)
    audit = SystemAuditAgentV1().run(run_dirs).to_dict()
    write_json(e2e_out / "01_system_audit_report.json", audit)

    final_report = {
        "status": "FINISH_STOP" if audit.get("status", "").startswith("PASS") else "BLOCKED_STOP",
        "layer": "ECOM_OS_V3_E2E_VIRTUAL_PIPELINE_V1",
        "e2e_id": e2e_id,
        "route": "A_INPUTS -> B_LOCAL_RUNNER -> C_ARTIFACTS -> D_SYSTEM_AUDIT -> FINISH -> STOP",
        "test_inputs": [str(x) for x in TEST_INPUTS],
        "step_results": step_results,
        "run_dirs": [str(x) for x in run_dirs],
        "audit_report": "01_system_audit_report.json",
        "audit_status": audit.get("status"),
        "pass_agents": audit.get("pass_agents"),
        "blocked_agents": audit.get("blocked_agents"),
        "not_configured_adapters": audit.get("not_configured_adapters"),
        "missing_files": audit.get("missing_files"),
        "recommendations": audit.get("recommendations"),
        "no_server": True,
        "no_live_ebay": True,
        "no_delete": True,
        "next_allowed_action": audit.get("next_allowed_action"),
    }
    write_json(e2e_out / "02_e2e_final_report.json", final_report)
    print(json.dumps(final_report, ensure_ascii=False, indent=2))
    return 0 if final_report["status"] == "FINISH_STOP" else 2


if __name__ == "__main__":
    raise SystemExit(main())
