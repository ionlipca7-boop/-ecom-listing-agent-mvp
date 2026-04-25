import json
from pathlib import Path

def main():
    required = [
        "project_manifest.json",
        "control_rules.json",
        "project_state.json",
        "project_history.jsonl",
        "control_agent.py",
        "archivist_agent.py",
        "runner_agent.py",
        "n8n_orchestration.json",
        "compact_core_migration.json"
    ]
    result = {}
    for name in required:
        result[name] = Path(name).exists()
    control = json.loads(Path("control_layer_review.json").read_text(encoding="utf-8"))
    print("DIRECT_LINE_VERIFICATION")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("status =", control.get("status"))
    print("mode =", control.get("mode"))
    print("canonical_line_complete =", control.get("canonical_line_complete"))
    print("history_valid =", control.get("history_valid"))

if __name__ == "__main__":
    main()
