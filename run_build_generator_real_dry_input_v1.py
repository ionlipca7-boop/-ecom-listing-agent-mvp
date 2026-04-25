import json
from pathlib import Path

ROOT = Path(".")
EXPORT = ROOT / "storage" / "exports"
ARCHIVE = ROOT / "storage" / "memory" / "archive"
EXPORT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

payload = {
"product_name": "USB-C Ladekabel 2m 60W",
"category": "Kabel",
"features": ["2m", "60W", "Schnellladen", "Datenkabel"],
"price_hint": 6.75,
"mode": "dry_run_test"
}

(EXPORT / "generator_real_dry_input_v1.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
(ARCHIVE / "generator_real_dry_input_v1.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

print("GENERATOR_REAL_DRY_INPUT_READY")
print("file =", EXPORT / "generator_real_dry_input_v1.json")
