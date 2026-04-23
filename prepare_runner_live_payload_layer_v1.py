import json
from pathlib import Path

base = Path(".")
source_file = base / "storage" / "render" / "runner_render_v1.json"
output_dir = base / "storage" / "live_payload"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "runner_live_payload_v1.json"

data = json.loads(source_file.read_text(encoding="utf-8"))

title = data.get("title")
price = data.get("price")
currency = data.get("currency") or "EUR"
html = data.get("html")
visual = data.get("visual") or {}
primary_image = visual.get("primary_image")
gallery = visual.get("gallery") or []
if not isinstance(gallery, list):
    gallery = [gallery]

all_images = []
if primary_image:
    all_images.append(primary_image)
for item in gallery:
    if item and item not in all_images:
        all_images.append(item)

payload = {
    "status": "OK",
    "layer": "PREPARE_RUNNER_LIVE_PAYLOAD_LAYER_V1",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "source_file": str(source_file),
    "payload_type": "LIVE_DRAFT_ONLY",
    "title": title,
    "price": {"value": price, "currency": currency},
    "description_html": html,
    "images": all_images,
    "visual_source": visual,
    "live_execution_allowed": False,
    "next_step": "build_runner_live_guard_layer_v1"
}

output_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "PREPARE_RUNNER_LIVE_PAYLOAD_LAYER_V1",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "has_title": bool(title),
    "has_price": price is not None,
    "has_description_html": bool(html),
    "image_count": len(all_images),
    "live_execution_allowed": False,
    "next_step": "build_runner_live_guard_layer_v1"
}

print("PREPARE_RUNNER_LIVE_PAYLOAD_LAYER_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
