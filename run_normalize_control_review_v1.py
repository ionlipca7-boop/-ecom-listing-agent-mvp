import json
from pathlib import Path

def main():
    path = Path("control_layer_review.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("mode"):
        data["mode"] = "PROJECT_SPECIFIC_ONLY"
    if "live_operations_enabled" not in data and "live_operations_allowed" in data:
        data["live_operations_enabled"] = bool(data.get("live_operations_allowed"))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("CONTROL_REVIEW_NORMALIZED")

if __name__ == "__main__":
    main()
