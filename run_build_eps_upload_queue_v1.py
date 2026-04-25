import json
import requests
from pathlib import Path

def read_text(p):
    return Path(p).read_text(encoding="utf-8").strip()

def load_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))

base = Path(".")
token = read_text(base / "storage" / "secrets" / "ebay_access_token.txt")
src = load_json(base / "storage" / "memory" / "archive" / "hosted_multi_image_source_v1.json")
out_path = base / "storage" / "exports" / "eps_upload_queue_v1_result.json"

pending = src.get("pending_external_urls", [])
hosted_ready = src.get("hosted_ready_urls", [])

url = "https://apim.ebay.com/commerce/media/v1_beta/image/create_image_from_url"
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

successes = []
failures = []

for image_url in pending:
    try:
        r = requests.post(url, headers=headers, json={"imageUrl": image_url}, timeout=90)
        location = r.headers.get("Location", "")
        try:
            data = r.json()
        except Exception:
            data = {}
        eps_url = data.get("imageUrl") or data.get("image", {}).get("imageUrl") or "" if isinstance(data, dict) else ""
        if r.status_code in [200, 201]:
            successes.append({
                "source_url": image_url,
                "eps_url": eps_url,
                "location": location,
                "http_status": r.status_code
            })
        else:
            failures.append({
                "source_url": image_url,
                "http_status": r.status_code,
                "response_text": r.text[:1000]
            })
    except Exception as e:
        failures.append({
            "source_url": image_url,
            "http_status": "EXCEPTION",
            "response_text": str(e)[:1000]
        })

result = {
    "status": "OK",
    "decision": "eps_upload_queue_v1_executed",
    "sku": src["sku"],
    "offer_id": src["offer_id"],
    "pending_input_count": len(pending),
    "hosted_ready_before_count": len(hosted_ready),
    "eps_success_count": len(successes),
    "eps_failure_count": len(failures),
    "eps_successes": successes,
    "eps_failures": failures,
    "combined_hosted_count": len(hosted_ready) + len(successes),
    "next_step": "build_multi_image_inventory_update_from_eps_v1" if len(successes) > 0 else "inspect_eps_rejections_v1"
}

out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("EPS_UPLOAD_QUEUE_V1_FINAL_AUDIT")
print("status =", result["status"])
print("decision =", result["decision"])
print("sku =", result["sku"])
print("pending_input_count =", result["pending_input_count"])
print("hosted_ready_before_count =", result["hosted_ready_before_count"])
print("eps_success_count =", result["eps_success_count"])
print("eps_failure_count =", result["eps_failure_count"])
print("combined_hosted_count =", result["combined_hosted_count"])
print("next_step =", result["next_step"])
