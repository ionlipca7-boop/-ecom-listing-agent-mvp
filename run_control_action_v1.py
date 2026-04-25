import json
import subprocess
from pathlib import Path
BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "storage" / "control_action.json"
def main():
    if not INPUT_FILE.exists():
        print("NO_CONTROL_ACTION_FILE")
        return
    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    action = data.get("action")
    if action == "update_quantity":
        print("RUNNING: increase quantity script")
        subprocess.run(["python", "run_increase_live_quantity_v1.py"])
    elif action == "update_listing":
        print("RUNNING: quantity update (price skipped for now)")
        subprocess.run(["python", "run_increase_live_quantity_v1.py"])
    else:
        print("UNKNOWN_ACTION")
if __name__ == "__main__":
    main()
