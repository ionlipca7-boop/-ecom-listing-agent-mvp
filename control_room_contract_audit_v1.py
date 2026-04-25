import json
from pathlib import Path

base = Path(".")
generator_file = base / "generator_output_extended.json"
runner_file = base / "runner_agent.py"
preview_file = base / "storage" / "preview" / "runner_preview_v2.json"

result = {}
result["status"] = "OK"
result["layer"] = "CONTROL_ROOM_CONTRACT_AUDIT_V1"
result["mode"] = "PROJECT_SPECIFIC_ONLY"
result["goal"] = "verify_generator_to_runner_contract_before_next_step"
result["runner_agent_exists"] = runner_file.exists()
result["generator_output_exists"] = generator_file.exists()
result["preview_file_exists"] = preview_file.exists()

if not generator_file.exists():
    result["status"] = "STOPPED"
    result["reason"] = "generator_output_missing"
    print("CONTROL_ROOM_CONTRACT_AUDIT_V1")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0)

data = json.loads(generator_file.read_text(encoding="utf-8"))
result["generator_type"] = type(data).__name__

if isinstance(data, dict):
    result["top_level_keys"] = list(data.keys())
    result["has_main_title"] = "main_title" in data
    result["has_title"] = "title" in data
    result["has_titles"] = "titles" in data
    result["has_price"] = "price" in data
    result["has_html"] = "html" in data
    result["has_description"] = "description" in data
    result["has_images"] = "images" in data
    result["main_title_type"] = type(data.get("main_title")).__name__ if "main_title" in data else None
    result["title_type"] = type(data.get("title")).__name__ if "title" in data else None
    result["titles_type"] = type(data.get("titles")).__name__ if "titles" in data else None
    result["price_type"] = type(data.get("price")).__name__ if "price" in data else None
    result["html_type"] = type(data.get("html")).__name__ if "html" in data else None
    result["images_type"] = type(data.get("images")).__name__ if "images" in data else None
    result["main_title_preview"] = str(data.get("main_title"))[:120] if "main_title" in data else None
    result["title_preview"] = str(data.get("title"))[:120] if "title" in data else None
    result["price_preview"] = str(data.get("price"))[:120] if "price" in data else None
    result["html_preview"] = str(data.get("html"))[:120] if "html" in data else None
    result["images_preview"] = str(data.get("images"))[:120] if "images" in data else None
    if isinstance(data.get("titles"), dict):
        result["titles_keys"] = list(data["titles"].keys())
    else:
        result["titles_keys"] = None
else:
    result["top_level_keys"] = None

result["current_truth"] = "runner_connected_but_generator_contract_not_mapped_for_preview"
result["correct_next_step"] = "build_runner_preview_mapping_layer_from_real_generator_shape"

print("CONTROL_ROOM_CONTRACT_AUDIT_V1")
print(json.dumps(result, indent=2, ensure_ascii=False))
