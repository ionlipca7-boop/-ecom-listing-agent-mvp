import json
from pathlib import Path

base = Path(".")
source_file = base / "storage" / "preview" / "runner_preview_v3.json"
validation_dir = base / "storage" / "validation"
validation_dir.mkdir(parents=True, exist_ok=True)
output_file = validation_dir / "runner_validation_v2.json"

data = json.loads(source_file.read_text(encoding="utf-8"))

title = data.get("title")
price = data.get("price")
html = data.get("html")
images = data.get("images")

if html is None:
    normalized_html = ""
else:
    normalized_html = str(html).replace("^<", "<").replace("^>", ">")

if images is None:
    images = []
elif not isinstance(images, list):
    images = [images]

title_ok = isinstance(title, str) and bool(title.strip())
price_ok = isinstance(price, int) or isinstance(price, float)
html_ok = isinstance(normalized_html, str) and bool(normalized_html.strip())
images_ok = isinstance(images, list) and bool(images)
contains_caret_html = "^<" in str(html) or "^>" in str(html)
ready_for_render = title_ok and price_ok and html_ok and images_ok

result = {
    "status": "OK",
    "layer": "RUNNER_VALIDATION_LAYER_V2",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "source_file": str(source_file),
    "title": title,
    "price": price,
    "html_original": html,
    "html_normalized": normalized_html,
    "images": images,
    "checks": {
        "title_ok": title_ok,
        "price_ok": price_ok,
        "html_ok": html_ok,
        "images_ok": images_ok,
        "contains_caret_html": contains_caret_html
    },
    "image_count": len(images),
    "is_ready_for_render": ready_for_render,
    "next_step": "build_runner_render_layer_v1"
}

output_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_VALIDATION_LAYER_V2",
    "mode": "PROJECT_SPECIFIC_ONLY",
    "title_ok": title_ok,
    "price_ok": price_ok,
    "html_ok": html_ok,
    "images_ok": images_ok,
    "contains_caret_html": contains_caret_html,
    "image_count": len(images),
    "is_ready_for_render": ready_for_render,
    "next_step": "build_runner_render_layer_v1"
}

print("RUNNER_VALIDATION_LAYER_V2_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
