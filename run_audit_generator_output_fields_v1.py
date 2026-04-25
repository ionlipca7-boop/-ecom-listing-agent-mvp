import json
from pathlib import Path

ROOT = Path(".")
EXPORT = ROOT / "storage" / "exports"
ARCHIVE = ROOT / "storage" / "memory" / "archive"
EXPORT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

p = EXPORT / "generator_output_v4.json"
data = json.loads(p.read_text(encoding="utf-8"))
keys = list(data.keys()) if isinstance(data, dict) else []

result = {
"status": "OK",
"decision": "generator_output_fields_audited",
"is_dict": isinstance(data, dict),
"keys": keys,
"has_title": "title" in keys,
"has_description": "description" in keys,
"has_price": "price" in keys,
"next_step": "build_title_recovery_layer_v1" if "title" not in keys else "promote_generator_v4_as_operational_entrypoint"
}

(EXPORT / "generator_output_fields_audit_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
(ARCHIVE / "generator_output_fields_audit_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("GENERATOR_OUTPUT_FIELDS_AUDIT")
print("status =", result["status"])
print("decision =", result["decision"])
print("is_dict =", result["is_dict"])
print("keys =", result["keys"])
print("has_title =", result["has_title"])
print("has_description =", result["has_description"])
print("has_price =", result["has_price"])
print("next_step =", result["next_step"])
