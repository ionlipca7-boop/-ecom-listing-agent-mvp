import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HANDOFF_JSON = BASE_DIR / "storage" / "exports" / "upload_handoff_v1.json"
OUTPUT_JSON = BASE_DIR / "storage" / "exports" / "upload_checklist_v1.json"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    handoff = load_json(HANDOFF_JSON)
    final_csv = handoff.get("final_csv", "")
    package_id = handoff.get("package_id", "")
    status = handoff.get("handoff_status", "BLOCKED")
    checklist = {
        "status": status,
        "package_id": package_id,
        "final_csv": final_csv,
        "steps": [
            "1. Open eBay bulk listing upload",
            "2. Select the final CSV file",
            "3. Upload and run eBay validation",
            "4. Review warnings or errors in eBay",
            "5. If validation passes, continue to publish",
        ]
    }
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(checklist, f, ensure_ascii=False, indent=2)
    print("UPLOAD_CHECKLIST_V1:")
    print(f"status: {status}")
    print(f"package_id: {package_id}")
    print(f"final_csv: {final_csv}")
    print(f"output_json: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
