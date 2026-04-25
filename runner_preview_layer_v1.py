import json
from pathlib import Path

BASE = Path("storage")
INPUT = BASE / "generator_output_extended.json"
OUTPUT_DIR = BASE / "preview"
OUTPUT = OUTPUT_DIR / "runner_preview_v1.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

data = json.loads(INPUT.read_text(encoding="utf-8"))

preview = {
    "status": "OK",
    "layer": "RUNNER_PREVIEW_LAYER_V1",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "title": data.get("main_title"),
    "price": data.get("price"),
    "html": data.get("html"),
    "images": data.get("images"),
    "source_file": "generator_output_extended.json"
}

OUTPUT.write_text(json.dumps(preview, indent=2, ensure_ascii=False), encoding="utf-8")

print("RUNNER_PREVIEW_LAYER_V1_READY")
