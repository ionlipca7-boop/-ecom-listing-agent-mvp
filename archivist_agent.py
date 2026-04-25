import json
from pathlib import Path
from datetime import datetime, UTC

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "project_manifest.json"
RULES_PATH = BASE_DIR / "control_rules.json"
STATE_PATH = BASE_DIR / "project_state.json"
HISTORY_PATH = BASE_DIR / "project_history.jsonl"

def read_text_auto(path):
    for enc in ("utf-8", "cp1251", "cp866"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            pass
    return path.read_text(encoding="utf-8", errors="replace")

def read_json(path):
    return json.loads(read_text_auto(path))

def append_history(record):
    line = json.dumps(record, ensure_ascii=False)
    with HISTORY_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def build_archive_record():
    manifest = read_json(MANIFEST_PATH)
    rules = read_json(RULES_PATH)
    state = read_json(STATE_PATH)
    return {
        "event": "ARCHIVIST_AGENT_INIT",
        "status": "OK",
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "project": manifest.get("project"),
        "layer": manifest.get("layer"),
        "phase": 6,
        "current_step": "create_archivist_agent",
        "next_step": "create_runner_agent",
        "mode": manifest.get("mode"),
        "project_specific_only": rules.get("rules", {}).get("gates", {}).get("project_specific_only"),
        "live_operations_allowed": state.get("live_operations_allowed"),
        "migration_allowed": state.get("migration_allowed")
    }

def main():
    record = build_archive_record()
    append_history(record)
    print(json.dumps(record, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
