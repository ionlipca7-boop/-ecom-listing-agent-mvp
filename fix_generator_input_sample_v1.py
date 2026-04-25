import json
from pathlib import Path

def main():
    data = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "GENERATOR_INPUT_SAMPLE",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "source_contract": "generator_input_contract.json",
        "input": {
            "product_title": "USB-C Ladekabel 2m 60W Schnellladen Datenkabel",
            "product_type": "USB-C Kabel",
            "product_specs": {
                "length": "2m",
                "power": "60W",
                "current": "6A",
                "function": "Schnellladen und Datenubertragung"
            },
            "target_marketplace": "EBAY_DE",
            "brand": "Generic",
            "price_hint": 6.75,
        },
        "live_operations_enabled": False,
        "next_step": "connect_generator_to_sample_input"
    }

    Path("generator_input_sample.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("GENERATOR_INPUT_SAMPLE_FIXED")

if __name__ == "__main__":
    main()
