import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
UPLOAD_RESULTS_DIR = BASE_DIR / "storage" / "upload_results"
INBOX_FILE = EXPORTS_DIR / "post_reupload_result_inbox_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "next_cycle_parser_trigger_v1.json"

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")

def main():
    inbox = read_json(INBOX_FILE)
    inbox_status = inbox.get("inbox_status", "")
    inbox_gate = inbox.get("inbox_gate", "")
    inbox_next_step = inbox.get("next_step", "")
    expected_name = inbox.get("expected_result_file_name", "")
    expected_path_text = inbox.get("expected_result_file_path", "")
    expected_path = Path(expected_path_text)
    file_exists = expected_path.exists()
    if inbox_status == "READY" and inbox_gate == "OPEN" and inbox_next_step == "WAIT_FOR_NEW_UPLOAD_RESULT_FILE" and file_exists:
        trigger_status = "READY"
        trigger_gate = "OPEN"
        next_step = "RUN_UPLOAD_RESULT_PARSER_ON_NEW_FILE"
    elif inbox_status == "READY" and inbox_gate == "OPEN":
        trigger_status = "WAITING"
        trigger_gate = "PENDING_FILE"
        next_step = "WAIT_FOR_EXPECTED_UPLOAD_RESULT_FILE"
    else:
        trigger_status = "BLOCKED"
        trigger_gate = "CLOSED"
        next_step = "RETURN_TO_POST_REUPLOAD_INBOX"
    output = {}
    output["trigger_status"] = trigger_status
    output["trigger_gate"] = trigger_gate
    output["next_step"] = next_step
    output["inbox_status"] = inbox_status
    output["inbox_gate"] = inbox_gate
    output["expected_result_file_name"] = expected_name
    output["expected_result_file_path"] = str(expected_path)
    output["expected_file_exists"] = file_exists
    output["source_files"] = {}
    output["source_files"]["post_reupload_result_inbox"] = str(INBOX_FILE)
    write_json(OUTPUT_FILE, output)
    print("NEXT_CYCLE_PARSER_TRIGGER_V1:")
    print("trigger_status:", trigger_status)
    print("trigger_gate:", trigger_gate)
    print("next_step:", next_step)
    print("expected_file_exists:", file_exists)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
