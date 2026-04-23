import json
from pathlib import Path

base = Path(".")
source_file = base / "generator_output_extended.json"
preview_dir = base / "storage" / "preview"
preview_dir.mkdir(parents=True, exist_ok=True)
preview_file = preview_dir / "runner_preview_v3.json"

data = json.loads(source_file.read_text(encoding="utf-8"))
output = data.get("output", {})
if not isinstance(output, dict):
    output = {}

title = output.get("main_title")
if not title:
    title = output.get("title")
if not title and isinstance(output.get("titles"), dict):
    title = output.get("titles", {}).get("main_title") or output.get("titles", {}).get("title")

price = output.get("price")
html = output.get("html")
images = output.get("images")
if images is None:
    images = []
if not isinstance(images, list):
    images = [images]

preview = {
    "status": "OK",
    "layer": "RUNNER_PREVIEW_MAPPING_LAYER_V1",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "source_file": str(source_file),
    "source_top_level_keys": list(data.keys()) if isinstance(data, dict) else [],
    "output_keys": list(output.keys()) if isinstance(output, dict) else [],
    "title": title,
    "price": price,
    "html": html,
    "images": images
}

preview_file.write_text(json.dumps(preview, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_PREVIEW_MAPPING_LAYER_V1",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "source_connected": source_file.exists(),
    "used_output_node": "output",
    "output_keys": list(output.keys()) if isinstance(output, dict) else [],
    "has_title": bool(title),
    "has_price": price is not None,
    "has_html": bool(html),
    "has_images": len(images) > 0,
    "image_count": len(images),
    "next_step": "build_runner_preview_render_layer_or_runner_validation_layer"
}

print("RUNNER_PREVIEW_MAPPING_LAYER_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
