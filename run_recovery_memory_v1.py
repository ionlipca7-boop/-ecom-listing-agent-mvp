import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_PATH = EXPORTS_DIR / "recovery_memory_v1.json"

def main():
    memory = {
        "status": "OK",
        "memory_type": "recovery_registry",
        "created_at": datetime.utcnow().isoformat(),

        "known_failures": [
            {
                "error": "401 Invalid access token",
                "cause": "expired or wrong token type",
                "solution": "use refresh_token flow and verify token",
                "do_not_do": "do not rewrite API scripts immediately"
            },
            {
                "error": "invalid Content-Language",
                "cause": "missing or incorrect header",
                "solution": "add Content-Language: de-DE for EBAY_DE",
                "do_not_do": "do not change payload"
            },
            {
                "error": "invalid SKU format",
                "cause": "non-alphanumeric or too long",
                "solution": "sanitize SKU to alphanumeric <= 50 chars",
                "do_not_do": "do not send raw SKU"
            },
            {
                "error": "SKU not found in eBay inventory",
                "cause": "inventory item not created before offer",
                "solution": "create or verify inventory item before creating offer",
                "do_not_do": "do not retry offer blindly"
            }
        ],

        "working_paths": [
            "legacy OAuth recovery",
            "refresh_token -> access_token",
            "smoke test validation",
            "policy fetch API",
            "category suggestion API",
            "payload injection pipeline"
        ],

        "cmd_traps": [
            "avoid echo. usage",
            "do not combine type and python in one line",
            "avoid > inside echo strings",
            "avoid broken echo blocks",
            "ensure all lines are written correctly"
        ]
    }

    OUTPUT_PATH.write_text(json.dumps(memory, indent=2, ensure_ascii=False), encoding="utf-8")

    print("RECOVERY_MEMORY_V1_CREATED")
    print("known_failures =", len(memory["known_failures"]))
    print("working_paths =", len(memory["working_paths"]))
    print("cmd_traps =", len(memory["cmd_traps"]))

if __name__ == "__main__":
    main()
