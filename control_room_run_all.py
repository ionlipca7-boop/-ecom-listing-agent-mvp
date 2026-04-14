import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FLOW_SCRIPT = ROOT / "run_publish_ready_flow.py"
STATUS_SCRIPT = ROOT / "control_room_publish_status.py"


def _parse_kv_lines(text: str) -> dict:
    parsed = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def _run_script(script_path: Path) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode, _parse_kv_lines(result.stdout)


def main() -> int:
    flow_rc, flow_data = _run_script(FLOW_SCRIPT)

    package_id = flow_data.get("package_id", "")
    final_publish_ready = flow_data.get("final_publish_ready", "")
    project_status = ""

    if flow_rc != 0:
        control_room_status = "ERROR"
    else:
        status_rc, status_data = _run_script(STATUS_SCRIPT)
        package_id = status_data.get("package_id", package_id)
        final_publish_ready = status_data.get("final_publish_ready", final_publish_ready)
        project_status = status_data.get("project_status", "")
        control_room_status = "OK" if status_rc == 0 else "ERROR"

    print(f"control_room_status: {control_room_status}")
    print(f"package_id: {package_id}")
    print(f"final_publish_ready: {final_publish_ready}")
    print(f"project_status: {project_status}")

    return 0 if control_room_status == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
