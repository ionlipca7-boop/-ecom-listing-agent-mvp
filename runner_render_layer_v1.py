import json
from pathlib import Path

base = Path(".")
source_file = base / "storage" / "validation" / "runner_validation_v2.json"
render_dir = base / "storage" / "render"
render_dir.mkdir(parents=True, exist_ok=True)
output_file = render_dir / "runner_render_v1.json"

data = json.loads(source_file.read_text(encoding="utf-8"))

title = data.get("title")
price = data.get("price")
html = data.get("html_normalized")
images = data.get("images")

if images is None:
    images = []

primary_image = images[0] if len(images) else None
additional_images = images[1:] if len(images) > 1 else []

render = {
    "status": "OK",
    "layer": "RUNNER_RENDER_LAYER_V1",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "title": title,
    "price": price,
    "currency": "EUR",
    "html": html,
    "visual": {
        "primary_image": primary_image,
        "gallery": additional_images,
        "image_count": len(images)
    },
    "ready_for_live": False,
    "next_step": "prepare_runner_live_payload_layer_v1"
}

output_file.write_text(json.dumps(render, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_RENDER_LAYER_V1",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "has_title": bool(title),
    "has_price": price is not None,
    "has_html": bool(html),
    "image_count": len(images),
    "primary_image_exists": primary_image is not None,
    "ready_for_live": False,
    "next_step": "prepare_runner_live_payload_layer_v1"
}

print("RUNNER_RENDER_LAYER_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
