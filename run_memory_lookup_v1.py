import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "storage" / "memory" / "project_memory_v1.json"

def as_text(value):
    if isinstance(value, list):
        return " ".join(str(x) for x in value)
    if isinstance(value, dict):
        return " ".join(f"{k} {v}" for k, v in value.items())
    return str(value)

def main():
    if not MEMORY_FILE.exists():
        print("MEMORY_LOOKUP_FAILED")
        print("reason = memory_file_missing")
        print("memory_file =", MEMORY_FILE)
        raise SystemExit(1)
    data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    query = " ".join(sys.argv[1:]).strip().lower()
    print("MEMORY_LOOKUP_OK")
    print("project =", data.get("project"))
    print("memory_version =", data.get("memory_version"))
    print("updated_at_utc =", data.get("updated_at_utc"))
    print("live_listings_count =", len(data.get("live_listings", [])))
    print("resolved_errors_count =", len(data.get("resolved_errors", [])))
    print("working_paths_count =", len(data.get("working_paths", [])))
    if not query:
        print("query = summary")
        for item in data.get("working_paths", []):
            print("working_path =", item)
        return
    print("query =", query)
    for item in data.get("resolved_errors", []):
        blob = " ".join([as_text(item.get("error")), as_text(item.get("cause")), as_text(item.get("solution")), as_text(item.get("tags"))]).lower()
        if query in blob:
            found += 
            print("match_error =", item.get("error"))
            print("match_cause =", item.get("cause"))
            print("match_solution =", item.get("solution"))
            print("match_tags =", ",".join(item.get("tags", [])))
    if found == 0:
        print("match_error = NONE")
        print("decision = no_direct_match_use_summary_and_manual_reasoning")
    else:
        print("decision = use_recovery_memory_first")
        print("matches_found =", found)

if __name__ == "__main__":
    main()
