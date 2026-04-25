import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
ACTION_PATH = EXPORTS_DIR / "control_action_v4.json"
AUDIT_PATH = EXPORTS_DIR / "control_action_bootstrap_v4_audit.json"
def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "actions": [
            {
                "action": "update_quantity",
                "product_key": "cable_001",
                "quantity": 35
            }
        ]
    }
    ACTION_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    audit = {
        "status": "OK",
        "action_path": str(ACTION_PATH),
        "actions_count": len(data["actions"]),
        "first_action": data["actions"][0]
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CONTROL_ACTION_BOOTSTRAP_V4_OK")
    print("action_path =", ACTION_PATH)
    print("actions_count =", len(data["actions"]))
    print("first_action =", json.dumps(data["actions"][0], ensure_ascii=False))
    print("audit_file =", AUDIT_PATH)
if __name__ == "__main__":
    main()
