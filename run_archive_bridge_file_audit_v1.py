import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "run_archive_bridge_sync_v1.py"
AUDIT = ROOT / "storage" / "memory" / "archive" / "archive_bridge_file_audit_v1.json"
def main():
    exists = TARGET.exists()
    text = TARGET.read_text(encoding="utf-8") if exists else ""
    lines = text.splitlines()
    result = {}
    result["status"] = "OK"
    result["decision"] = "archive_bridge_file_audit_v1_completed"
    result["file_exists"] = exists
    result["line_count"] = len(lines)
    result["has_has_changes_text"] = "has_changes" in text
    result["has_diff_command"] = "git diff --cached --quiet" in text
    result["sample_lines"] = lines[20:35]
    AUDIT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ARCHIVE_BRIDGE_FILE_AUDIT_V1")
    print("status =", result["status"])
    print("file_exists =", result["file_exists"])
    print("line_count =", result["line_count"])
    print("has_has_changes_text =", result["has_has_changes_text"])
    print("has_diff_command =", result["has_diff_command"])
if __name__ == "__main__":
    main()
