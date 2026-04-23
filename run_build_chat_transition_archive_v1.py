import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
MEMORY_DIR = BASE_DIR / "storage" / "memory"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_FILE = EXPORTS_DIR / "chat_transition_archive_v1.json"
PROMPT_FILE = EXPORTS_DIR / "new_chat_continuity_prompt_v1.txt"

def main():
    data = {
        "status": "OK",
        "decision": "chat_transition_archive_built",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "project": "ECOM LISTING AGENT MVP / CONTROL ROOM",
        "verified_live_results": [
            {
                "product_key": "cable_001",
                "listing_state": "LIVE"
            },
            {
                "product_key": "adapter_001",
                "sku": "USBCOTGAdapterUSB3TypCaufUSBAq10p399",
                "offerId": "153365657011",
                "listingId": "318166440509",
                "listing_state": "LIVE"
            }
        ],
        "verified_memory_state": {
            "project_memory_exists": True,
            "active_memory_exists": True,
            "live_listings_count": 2,
            "resolved_errors_count": 7,
            "media_sources_count": 1,
            "best_working_paths": ["publish existing offer after adding Marke and imageUrls"]
        },
        "verified_repairs_and_lessons": [
            "401 fixed by access token recovery path",
            "inventory must exist before offer",
            "merchantLocationKey ECOM_DE_LOC_1 works",
            "Marke required for publish in adapter_001 case",
            "at least one imageUrl required for publish",
            "HTML generated via CMD must avoid multiline triple quote traps",
            "cleaned HTML successfully revised into live inventory item"
        ],
        "verified_files_created": [
            "storage\\memory\\project_memory_v1.json",
            "storage\\memory\\project_memory_active_v1.json",
            "storage\\exports\\publish_existing_offer_repair_v3.json",
            "storage\\exports\\adapter_001_listing_review_v1.json",
            "storage\\exports\\adapter_001_optimization_plan_v1.json",
            "storage\\exports\\adapter_001_html_description_v1.json",
            "storage\\exports\\adapter_001_html_description_clean_v1.json",
            "storage\\exports\\adapter_001_description_revise_v1.json",
            "storage\\exports\\adapter_001_competitor_review_v1.json"
        ],
        "not_completed_or_not_verified": [
            "run_build_adapter_001_specifics_upgrade_v1.py was not successfully created in this chat",
            "adapter_001 specifics upgrade json does not exist yet",
            "live revise for upgraded specifics has not been executed yet",
            "photo system 1-7 commercial redesign not implemented yet",
            "ads and offer settings were reviewed conceptually but not automated yet"
        ],
        "next_best_step": "build adapter_001 specifics upgrade v1, then revise live item specifics, then continue photo/commercial optimization"
    }
    ARCHIVE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    PROMPT_FILE.write_text(prompt, encoding="utf-8")
    print("CHAT_TRANSITION_ARCHIVE_OK")
    print("archive_file =", ARCHIVE_FILE)
    print("prompt_file =", PROMPT_FILE)

if __name__ == "__main__":
    main()
