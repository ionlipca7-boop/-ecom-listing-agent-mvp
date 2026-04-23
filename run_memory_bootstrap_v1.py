import json
from datetime import datetime, UTC
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "storage" / "memory"
MEMORY_FILE = MEMORY_DIR / "project_memory_v1.json"

def main():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "status": "OK",
        "decision": "project_memory_bootstrapped",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "project": "ECOM LISTING AGENT MVP / CONTROL ROOM",
        "memory_version": "v1",
        "working_values": {
            "marketplaceId": "EBAY_DE",
            "merchantLocationKey": "ECOM_DE_LOC_1",
            "fulfillmentPolicyId": "257755855024",
            "paymentPolicyId": "257755913024",
            "returnPolicyId": "257755877024",
            "working_categoryId": "44932"
        },
        "live_listings": [
            {
                "product_key": "cable_001",
                "sku": "USBCLadekabel2m60WSchnellladenDatenkabelq10p675",
                "offerId": "153187814011",
                "listingId": "318164247570",
                "pipeline_status": "LIVE_OK",
                "listing_state": "LIVE"
            }
        ],
        "resolved_errors": [
            {
                "error": "SKU not found in system",
                "cause": "offer attempted before inventory item existed",
                "solution": "create or verify inventory item before offer creation",
                "tags": ["sku", "inventory", "offer"]
            },
            {
                "error": "Location information not found",
                "cause": "invalid or missing merchantLocationKey",
                "solution": "use merchantLocationKey ECOM_DE_LOC_1",
                "tags": ["location", "merchantLocationKey"]
            },
            {
                "error": "Produktart fehlt",
                "cause": "missing Produktart in product aspects",
                "solution": "add Produktart in product.aspects before publish",
                "tags": ["produktart", "aspects", "publish"]
            },
            {
                "error": "mindestens 1 Foto",
                "cause": "missing imageUrls",
                "solution": "add at least one image URL before publish",
                "tags": ["photo", "imageUrls", "publish"]
            },
            {
                "error": "401 Invalid access token",
                "cause": "expired or invalid access token in storage secrets",
                "solution": "first do token audit and refresh or recovery before API actions",
                "tags": ["401", "token", "oauth", "recovery"]
            }
        ],
        "cmd_traps": [
            "avoid echo. usage",
            "do not combine type and python in one line",
            "avoid broken multiline python -c blocks",
            "avoid fragile here-string style blocks for Windows CMD",
            "if python or py is missing in PATH use C:\\Python314\\python.exe"
        ],
        "working_paths": [
            "recovery memory first",
            "token audit before live API action",
            "inventory first then offer then publish",
            "verify loop after live update",
            "registry update after successful publish"
        ],
        "lessons_learned": [
            "do not start new live action blindly",
            "first read memory then decide action",
            "preserve working values centrally",
            "store blockers and fixes for reuse in next chats",
            "prefer short reliable CMD blocks"
        ],
        "next_target": {
            "product_key": "adapter_001",
            "input_file": "storage\\exports\\new_product_adapter_001.json",
            "goal": "inventory OK -> offer OK -> publish OK -> listingId -> registry update"
        }
    }
    MEMORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("MEMORY_BOOTSTRAP_OK")
    print("memory_file =", MEMORY_FILE)

if __name__ == "__main__":
    main()
