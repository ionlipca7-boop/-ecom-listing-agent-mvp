import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLISH_PACKAGES_DIR = ROOT / "publish_packages"
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"

SCRIPTS = [
    "build_dedup_ebay_feed.py",
    "build_final_ebay_feed.py",
    "audit_final_ebay_feed.py",
    "build_publish_ready_summary.py",
]


def _run_step(script_name: str) -> bool:
    result = subprocess.run(
        [sys.executable, str(ROOT / script_name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _get_latest_package_id() -> str:
    if INDEX_PATH.exists():
        try:
            payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
            latest = payload.get("latest_package") if isinstance(payload, dict) else None
            if isinstance(latest, str) and latest:
                return latest
        except Exception:
            pass

    if not PUBLISH_PACKAGES_DIR.exists():
        return ""

    package_dirs = [
        p for p in PUBLISH_PACKAGES_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")
    ]
    if not package_dirs:
        return ""

    latest_dir = max(package_dirs, key=lambda p: p.stat().st_mtime)
    return latest_dir.name


def _read_final_publish_ready(package_id: str):
    if not package_id:
        return None

    summary_path = PUBLISH_PACKAGES_DIR / package_id / "publish_ready_summary.json"
    if not summary_path.exists():
        return None

    try:
        payload = json.loads(summary_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    if isinstance(payload, dict):
        return payload.get("publish_ready")
    return None


def main() -> int:
    steps_completed = 0
    flow_status = "OK"

    for script in SCRIPTS:
        ok = _run_step(script)
        if not ok:
            flow_status = "ERROR"
            break
        steps_completed += 1

    package_id = _get_latest_package_id()
    final_publish_ready = _read_final_publish_ready(package_id)

    print(f"flow_status: {flow_status}")
    print(f"package_id: {package_id}")
    print(f"steps_completed: {steps_completed}")
    print(f"final_publish_ready: {final_publish_ready}")

    return 0 if flow_status == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
