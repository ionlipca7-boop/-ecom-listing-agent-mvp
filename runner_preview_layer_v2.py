import json
from pathlib import Path

BASE = Path(".")
CANDIDATES = [
    BASE / "generator_output_extended.json",
    BASE / "storage" / "generator_output_extended.json",
    BASE / "storage" / "exports" / "generator_output_extended.json",
    BASE / "storage" / "outputs" / "generator_output_extended.json",
    BASE / "storage" / "generated" / "generator_output_extended.json",
]

found_input = None
for candidate in CANDIDATES:
    if candidate.exists():
        found_input = candidate
        break

preview_dir = BASE / "storage" / "preview"
preview_dir.mkdir(parents=True, exist_ok=True)
preview_file = preview_dir / "runner_preview_v2.json"
audit_file = preview_dir / "runner_preview_v2_audit.json"

if found_input is None:
    audit = {
        "status": "STOPPED",
        "layer": "RUNNER_PREVIEW_LAYER_V2",
        "reason": "generator_output_extended_not_found",
        "checked_paths": [str(p) for p in CANDIDATES],
        "preview_created": False
    }
    audit_file.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    print("RUNNER_PREVIEW_LAYER_V2_AUDIT")
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    raise SystemExit(0)

data = json.loads(found_input.read_text(encoding="utf-8"))

preview = {
    "status": "OK",
    "layer": "RUNNER_PREVIEW_LAYER_V2",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "source_file": str(found_input),
    "title": data.get("main_title") or data.get("title"),
    "price": data.get("price"),
    "html": data.get("html"),
    "images": data.get("images"),
}

preview_file.write_text(json.dumps(preview, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_PREVIEW_LAYER_V2",
    "source_file": str(found_input),
    "preview_file": str(preview_file),
    "has_title": bool(preview.get("title")),
    "has_price": preview.get("price") is not None,
    "has_html": bool(preview.get("html")),
    "has_images": isinstance(preview.get("images"), list),
    "image_count": len(preview.get("images") or [])
}

audit_file.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
print("RUNNER_PREVIEW_LAYER_V2_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
