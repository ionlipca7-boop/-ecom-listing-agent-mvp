import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "storage" / "memory" / "project_memory_v1.json"
CLEAN_FILE = BASE_DIR / "storage" / "memory" / "project_memory_active_v1.json"

def dedupe_strings(items):
    out = []
    seen = set()
    for item in items:
        key = str(item).strip()
        if key and key not in seen:
            seen.add(key)
            out.append(key)
    return out

def dedupe_dicts(items, key_fields):
    out = []
    seen = set()
    for item in items:
        sig = tuple(item.get(k) for k in key_fields)
        if sig not in seen:
            seen.add(sig)
            out.append(item)
    return out

def main():
    memory = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    active = {
        "status": "OK",
        "decision": "active_memory_built",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "project": memory.get("project"),
        "working_values": memory.get("working_values", {}),
        "live_listings": dedupe_dicts(memory.get("live_listings", []), ["product_key"]),
        "resolved_errors": dedupe_dicts(memory.get("resolved_errors", []), ["error"]),
        "cmd_traps": dedupe_strings(memory.get("cmd_traps", [])),
        "working_paths": dedupe_strings(memory.get("working_paths", [])),
        "best_working_paths": dedupe_strings(memory.get("best_working_paths", [])),
        "media_sources": dedupe_dicts(memory.get("media_sources", []), ["product_key", "source_type"])
    }
    CLEAN_FILE.write_text(json.dumps(active, ensure_ascii=False, indent=2), encoding="utf-8")
    print("MEMORY_CLEANUP_OK")
    print("decision =", active["decision"])
    print("live_listings_count =", len(active.get("live_listings", [])))
    print("resolved_errors_count =", len(active.get("resolved_errors", [])))
    print("media_sources_count =", len(active.get("media_sources", [])))

if __name__ == "__main__":
    main()
