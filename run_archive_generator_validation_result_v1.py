import json
from pathlib import Path

def main():
    validation = json.loads(Path("generator_output_validation.json").read_text(encoding="utf-8"))
    event = {
        "event": "GENERATOR_OUTPUT_VALIDATION_ARCHIVED",
        "status": validation.get("status"),
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": validation.get("layer"),
        "mode": validation.get("mode"),
        "next_step": validation.get("next_step")
    }
    with Path("project_history.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print("GENERATOR_VALIDATION_ARCHIVED")

if __name__ == "__main__":
    main()
