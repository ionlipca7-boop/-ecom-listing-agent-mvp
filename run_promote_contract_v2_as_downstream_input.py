import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "generator_output_contract_v2.json"
OUT = BASE_DIR / "storage" / "exports" / "downstream_input_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "promote_contract_v2_as_downstream_input_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    archive = {
        "date": "2026-04-18",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "status": "OK",
        "decision": "promote_contract_v2_as_downstream_input_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "promoted_file": str(OUT.relative_to(BASE_DIR)).replace("/", "\\"),
        "contract_version": data.get("contract_version"),
        "title_present": bool(data.get("title")),
        "description_present": bool(data.get("description")),
        "price_present": data.get("price") is not None,
        "next_step": "build_publish_payload_probe_v1_from_downstream_input"
    }
    ARCH.write_text(json.dumps(archive, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PROMOTE_CONTRACT_V2_AS_DOWNSTREAM_INPUT_AUDIT")
    print("status = OK")
    print("decision = promote_contract_v2_as_downstream_input_completed")
    print("promoted_file =", str(OUT.relative_to(BASE_DIR)).replace("/", "\\"))
    print("contract_version =", data.get("contract_version"))
    print("title_present =", bool(data.get("title")))
    print("description_present =", bool(data.get("description")))
    print("price_present =", data.get("price") is not None)
    print("next_step = build_publish_payload_probe_v1_from_downstream_input")

if __name__ == "__main__":
    main()
