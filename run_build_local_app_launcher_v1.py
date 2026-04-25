import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
LAUNCHER_DIR = BASE_DIR / "storage" / "app_launcher"
OUTPUT_FILE = EXPORTS_DIR / "local_app_launcher_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LAUNCHER_DIR.mkdir(parents=True, exist_ok=True)

    ai_data = read_json(EXPORTS_DIR / "ai_system_layer_v1.json")
    system_status = ai_data.get("ai_system_status", "")
    package_id = ai_data.get("package_id", "")
    bundle_dir = ai_data.get("bundle_dir", "")
    selected_title = ai_data.get("selected_title", "")

    launcher_bat = LAUNCHER_DIR / "launch_control_room_v1.bat"
    launcher_readme = LAUNCHER_DIR / "README_LAUNCHER.txt"

    bat_lines = []
    bat_lines.append("@echo off")
    bat_lines.append("cd /d " + str(BASE_DIR))
    bat_lines.append("chcp 65001")
    bat_lines.append("echo ===== ECOM CONTROL ROOM =====")
    bat_lines.append("type storage\\exports\\ai_system_layer_v1.json")
    bat_lines.append("echo.")
    bat_lines.append("echo ===== OPEN BUNDLE =====")
    bat_lines.append("start " + '"" "' + bundle_dir + '"')
    bat_lines.append("echo.")
    bat_lines.append("echo ===== OPEN EXPORTS =====")
    bat_lines.append('start "" "' + str(EXPORTS_DIR) + '"')
    bat_lines.append("pause")
    launcher_bat.write_text("\n".join(bat_lines) + "\n", encoding="utf-8")

    readme_text = "LOCAL APP LAUNCHER READY" + "\n" + "Open launch_control_room_v1.bat for the first local control entry point." + "\n" + "Package ID: " + str(package_id) + "\n" + "Title: " + str(selected_title)
    launcher_readme.write_text(readme_text, encoding="utf-8")

    launcher_status = "READY" if system_status == "READY" else "BLOCKED"
    next_step = "BUILD_DESKTOP_APP_SHELL" if system_status == "READY" else "FIX_AI_SYSTEM_LAYER"

    result = {
        "checked_at": utc_now(),
        "launcher_status": launcher_status,
        "next_step": next_step,
        "package_id": package_id,
        "selected_title": selected_title,
        "launcher_dir": str(LAUNCHER_DIR),
        "launcher_bat": str(launcher_bat),
        "launcher_readme": str(launcher_readme)
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("LOCAL_APP_LAUNCHER_V1:")
    print("launcher_status:", result["launcher_status"])
    print("next_step:", result["next_step"])
    print("package_id:", result["package_id"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
