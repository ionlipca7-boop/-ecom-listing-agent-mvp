import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
MEMORY_DIR = BASE_DIR / "storage" / "memory"
def read_json_if_exists(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None
def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    project_memory = read_json_if_exists(MEMORY_DIR / "project_memory_v1.json")
    active_memory = read_json_if_exists(MEMORY_DIR / "project_memory_active_v1.json")
    transition_archive = read_json_if_exists(EXPORT_DIR / "chat_transition_archive_v1.json")
    sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
    offer_id = "153365657011"
    listing_id = "318166440509"
    recommended_item_specifics = {
        "Marke": ["Markenlos"],
        "Herstellernummer": ["Nicht zutreffend"],
        "Produktart": ["USB-C OTG Adapter"],
        "Anschluss A": ["USB-C"],
        "Anschluss B": ["USB-A"],
        "USB Standard": ["USB 3.0"],
        "Besonderheiten": ["OTG"],
        "Kompatibel mit": ["Universal"],
        "Farbe": ["Schwarz"]
    }
    payload = {
        "status": "OK",
        "decision": "adapter_001_specifics_upgrade_built",
        "product_key": "adapter_001",
        "sku": sku,
        "offerId": offer_id,
        "listingId": listing_id,
        "source_memory_files": {
            "project_memory_v1": project_memory is not None,
            "project_memory_active_v1": active_memory is not None,
            "chat_transition_archive_v1": transition_archive is not None
        },
        "recommended_item_specifics": recommended_item_specifics,
        "next_action": "revise_live_item_specifics_for_adapter_001",
        "notes": [
            "memory_first_then_action",
            "marke_included",
            "safe_specifics_upgrade_only",
            "ready_for_live_revise_layer" 
        ]
    }
    out_path = EXPORT_DIR / "adapter_001_specifics_upgrade_v1.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_SPECIFICS_UPGRADE_V1_OK")
    print("output =", str(out_path))
    print("decision =", payload["decision"])
    print("source_memory_project =", payload["source_memory_files"]["project_memory_v1"])
    print("source_memory_active =", payload["source_memory_files"]["project_memory_active_v1"])
    print("source_archive =", payload["source_memory_files"]["chat_transition_archive_v1"])
if __name__ == "__main__":
    main()
