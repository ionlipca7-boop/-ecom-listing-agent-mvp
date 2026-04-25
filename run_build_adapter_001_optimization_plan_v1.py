import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUT_FILE = BASE_DIR / "storage" / "exports" / "adapter_001_optimization_plan_v1.json"
MEMORY_FILE = BASE_DIR / "storage" / "memory" / "project_memory_active_v1.json"

def main():
    memory = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    data = {
        "status": "OK",
        "decision": "adapter_001_optimization_plan_built",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "product_key": "adapter_001",
        "listing_id": "318166440509",
        "current_state": {
            "is_live": True,
            "photos_need_optimization": True,
            "specifics_need_expansion": True,
            "description_need_html": True
        },
        "photo_plan": {
            "goal": "replace raw supplier photos with sales-oriented 1-7 photo system",
            "needed_blocks": [
                "hero_photo_clean",
                "main_benefit_fast_charge_and_data",
                "compatibility_use_case",
                "connector_closeup",
                "multi_color_or_real_variant_logic",
                "size_compact_travel",
                "package_or_delivery_info"
            ],
            "current_problem": "current photos are copied supplier images and not optimized for CTR or trust" 
        },
        "specifics_plan": {
            "required_keep": ["Marke", "Produktart", "Anschluss A", "Anschluss B"],
            "recommended_fill": [
                "Farbe strategy review",
                "EAN fallback",
                "Kompatible Marke",
                "Kompatibles Modell",
                "Herstellungsland und -region if known",
                "Herstellernummer fallback",
                "dimension fields only if reliable"
            ],
            "current_problem": "important specifics exist but commercial and search-support fields are still incomplete"
        },
        "description_plan": {
            "goal": "replace plain short text with structured German HTML description",
            "sections": [
                "Kurze Einleitung",
                "Vorteile",
                "Kompatibilitaet",
                "Technische Hinweise",
                "Lieferumfang",
                "Versandhinweis"
            ],
            "current_problem": "plain text description is too weak for trust, clarity, and conversion"
        },
        "ad_offer_plan": {
            "start_ad_rate_percent": 7,
            "rule_after_7_days_no_movement": "increase by 1 percent",
            "offer_to_buyers_min_discount_percent": 5,
            "note": "avoid chaotic price cutting; adjust ads first, then offers selectively"
        },
        "next_execution_order": [
            "build_html_description_v1",
            "build_specifics_upgrade_v1",
            "prepare_photo_upgrade_plan_v1",
            "prepare_live_revise_payload_v1"
        ],
        "memory_snapshot_keys": list(memory.keys())[:20]
    }
    OUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_OPTIMIZATION_PLAN_OK")
    print("product_key =", data["product_key"])
    print("listing_id =", data["listing_id"])
    print("ad_rate =", data["ad_offer_plan"]["start_ad_rate_percent"])
    print("offer_discount =", data["ad_offer_plan"]["offer_to_buyers_min_discount_percent"])

if __name__ == "__main__":
    main()
