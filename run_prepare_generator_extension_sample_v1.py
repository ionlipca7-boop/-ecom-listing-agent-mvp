import json
from pathlib import Path

def main():
    data = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "GENERATOR_EXTENSION_SAMPLE",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "based_on": "generator_extension_contract.json",
        "extension_input": {
            "html_template": "^<h2^>{title}^</h2^>^<p^>{description}^</p^>",
            "category_hint": "USB-Kabel",
            "images_hint": [
                "image_1_main.jpg",
                "image_2_detail.jpg",
                "image_3_usage.jpg"
            ]
        },
        "live_operations_enabled": False,
        "next_step": "connect_generator_extension_to_output"
    }
    Path("generator_extension_sample.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("GENERATOR_EXTENSION_SAMPLE_CREATED")

if __name__ == "__main__":
    main()
