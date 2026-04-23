import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
UPLOAD_RESULTS_DIR = BASE_DIR / "storage" / "upload_results"
HANDOFF_FILE = EXPORTS_DIR / "manual_fixed_reupload_handoff_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "post_reupload_result_inbox_v1.json"

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")

def main():
    handoff = read_json(HANDOFF_FILE)
    handoff_status = handoff.get("handoff_status", "")
    handoff_gate = handoff.get("handoff_gate", "")
    next_step_in = handoff.get("next_step", "")
    expected_file_name = "ebay_result_after_fixed_reupload_v1.json"
    expected_file_path = str(UPLOAD_RESULTS_DIR / expected_file_name)
    checklist = []
    checklist.append("Выполнить ручную повторную загрузку в eBay")
    checklist.append("Сохранить новый результат загрузки в storage\\\\upload_results")
    checklist.append("Назвать файл ebay_result_after_fixed_reupload_v1.json")
    checklist.append("После сохранения запустить parser следующего цикла")
    if handoff_status == "READY" and handoff_gate == "OPEN" and next_step_in == "DO_MANUAL_FIXED_REUPLOAD":
        inbox_status = "READY"
        inbox_gate = "OPEN"
        next_step = "WAIT_FOR_NEW_UPLOAD_RESULT_FILE"
    elif handoff_status == "READY":
        inbox_status = "PARTIAL"
        inbox_gate = "REVIEW"
        next_step = "REVIEW_MANUAL_REUPLOAD_STAGE"
    else:
        inbox_status = "BLOCKED"
        inbox_gate = "CLOSED"
        next_step = "RETURN_TO_MANUAL_HANDOFF"
    output = {}
    output["inbox_status"] = inbox_status
    output["inbox_gate"] = inbox_gate
    output["next_step"] = next_step
    output["handoff_status"] = handoff_status
    output["handoff_gate"] = handoff_gate
    output["source_handoff_next_step"] = next_step_in
    output["expected_result_file_name"] = expected_file_name
    output["expected_result_file_path"] = expected_file_path
    output["manual_checklist"] = checklist
    output["source_files"] = {}
    output["source_files"]["manual_fixed_reupload_handoff"] = str(HANDOFF_FILE)
    write_json(OUTPUT_FILE, output)
    print("POST_REUPLOAD_RESULT_INBOX_V1:")
    print("inbox_status:", inbox_status)
    print("inbox_gate:", inbox_gate)
    print("next_step:", next_step)
    print("expected_result_file_name:", expected_file_name)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
