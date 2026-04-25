import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "generator_output_v4.json"
OUT = BASE_DIR / "storage" / "exports" / "generator_output_v4_title_recovered.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "title_recovery_layer_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    normalized = dict(data)
    recovered_title = str(normalized.get("main_title") or normalized.get("title") or "").strip()
    if recovered_title:
        normalized["title"] = recovered_title
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    archive = {
        "date": "2026-04-18",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "status": "OK",
        "decision": "build_title_recovery_layer_v1_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "normalized_file": str(OUT.relative_to(BASE_DIR)).replace("/", "\\"),
        "title_source": "main_title",
        "had_title_before": "title" in data,
        "has_title_after": "title" in normalized,
        "has_main_title": "main_title" in normalized,
        "next_step": "use_normalized_output_contract_or_add_contract_normalizer_v2"
    }
    ARCH.write_text(json.dumps(archive, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TITLE_RECOVERY_LAYER_V1")
    print("status = OK")
    print("decision = build_title_recovery_layer_v1_completed")
    print("source_file =", str(SRC.relative_to(BASE_DIR)).replace("/", "\\"))
    print("normalized_file =", str(OUT.relative_to(BASE_DIR)).replace("/", "\\"))
    print("archive_file =", str(ARCH.relative_to(BASE_DIR)).replace("/", "\\"))
    print("had_title_before =", "title" in data)
    print("has_main_title =", "main_title" in normalized)
    print("has_title_after =", "title" in normalized)
    print("title_value =", repr(normalized.get("title", "")))

if __name__ == "__main__":
    main()
