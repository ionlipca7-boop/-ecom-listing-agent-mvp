import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAYLOAD_PATH = ROOT / "storage" / "exports" / "adapter_001_full_inventory_revise_payload_v1.json"
RESPONSE_PATH = ROOT / "storage" / "exports" / "adapter_001_full_inventory_revise_response_v1.json"
OUT = ROOT / "storage" / "memory" / "archive" / "adapter_001_full_inventory_revise_400_audit_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    payload = load_json(PAYLOAD_PATH)
    response = load_json(RESPONSE_PATH)
    product = payload.get("product", {})
    title = product.get("title", "")
    image_urls = product.get("imageUrls", [])
    aspects = product.get("aspects", {})
    errors = response.get("errors", []) if isinstance(response, dict) else []
    warnings = response.get("warnings", []) if isinstance(response, dict) else []
    first_error = errors[0] if errors else {}
    first_warning = warnings[0] if warnings else {}
    result = {}
    result["status"] = "OK"
    result["decision"] = "adapter_001_full_inventory_revise_400_audit_v1_completed"
    result["payload_top_keys"] = sorted(list(payload.keys()))
    result["product_keys"] = sorted(list(product.keys()))
    result["sku"] = payload.get("sku", "")
    result["title"] = title
    result["title_length"] = len(title)
    result["image_count"] = len(image_urls)
    result["aspect_keys"] = sorted(list(aspects.keys()))
    result["errors_count"] = len(errors)
    result["warnings_count"] = len(warnings)
    result["first_error"] = first_error
    result["first_warning"] = first_warning
    result["raw_response_keys"] = sorted(list(response.keys())) if isinstance(response, dict) else []
    result["next_step"] = "fix_payload_by_exact_ebay_error_and_retry_full_inventory_revise"
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_FULL_INVENTORY_REVISE_400_AUDIT_V1")
    print("status =", result["status"])
    print("errors_count =", result["errors_count"])
    print("warnings_count =", result["warnings_count"])
    print("first_error =", result["first_error"])
    print("first_warning =", result["first_warning"])
if __name__ == "__main__":
    main()
