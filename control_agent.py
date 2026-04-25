import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "project_manifest.json"
RULES_PATH = BASE_DIR / "control_rules.json"
STATE_PATH = BASE_DIR / "project_state.json"
REVIEW_PATH = BASE_DIR / "control_layer_review.json"
HISTORY_PATH = BASE_DIR / "project_history.jsonl"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))

def count_history_lines(path):
    text = "" if not path.exists() else path.read_text(encoding="utf-8", errors="replace")
    return len([line for line in text.splitlines() if line.strip()])

def build_control_status():
    manifest = read_json(MANIFEST_PATH)
    rules = read_json(RULES_PATH)
    state = read_json(STATE_PATH)
    review = read_json(REVIEW_PATH)
    history_lines = count_history_lines(HISTORY_PATH)
    result = {
        "status": review.get("status"),
        "project": manifest.get("project"),
        "layer": review.get("layer"),
        "mode": manifest.get("mode"),
        "phase": review.get("phase"),
        "current_step": review.get("current_step"),
        "next_step": review.get("next_step"),
        "manifest_ready": MANIFEST_PATH.exists(),
        "rules_ready": RULES_PATH.exists(),
        "state_ready": STATE_PATH.exists(),
        "review_ready": REVIEW_PATH.exists(),
        "history_ready": HISTORY_PATH.exists(),
        "history_lines": history_lines,
        "live_operations_allowed": state.get("live_operations_allowed"),
        "migration_allowed": state.get("migration_allowed"),
        "side_branches_allowed": state.get("side_branches_allowed"),
        "project_specific_only": rules.get("rules", {}).get("gates", {}).get("project_specific_only"),
        "canonical_line_complete": review.get("canonical_line_complete"),
        "history_valid": review.get("history_valid")
    }
    return result

def main():
    print(json.dumps(build_control_status(), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
