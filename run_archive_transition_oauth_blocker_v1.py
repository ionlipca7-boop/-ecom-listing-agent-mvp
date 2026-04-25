import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARCHIVE_DIR = BASE_DIR / "storage" / "memory" / "archive"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = ARCHIVE_DIR / "transition_oauth_blocker_2026_04_19_v1.json"

def main():
    data = {
        "date": "2026-04-19",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "phase": "FIRST_REAL_MULTI_LISTING_RUN_BLOCKED_BY_OAUTH_SCOPE",
        "status": "OK",
        "achievements": [
            "improved_baseline_v1_archived",
            "photo_pipeline_v1_ready",
            "multi_listing_system_v1_archived",
            "first_real_multi_listing_input_stub_built",
            "first_real_multi_listing_input_filled",
            "first_real_multi_listing_run_payload_built" 
        ],
        "current_state": {
            "template_key": "baseline_template_v1",
            "selected_mode": "baseline_clone",
            "baseline_image_count": 9,
            "runtime_ready_for_live": False,
        },
        "blocker": {
            "type": "oauth_scope_missing",
            "details": "current user token lacks sell.account and sell.account.readonly scopes for Account API policy endpoints",
            "policy_fetch_http_status": 403,
            "refresh_with_current_scope_possible": False,
            "required_path": "start_new_consent_flow_with_sell_account_scope" 
        },
        "rules": [
            "inventory_first_then_offer",
            "always_use_full_payload",
            "always_read_after_each_update",
            "preserve_working_images",
            "github_as_backup_not_runtime",
            "do_not_touch_live_listing_until_policy_ids_are_real" 
        ],
        "next_step": "build_new_oauth_consent_url_v1_with_sell_account_scope" 
    }
    OUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TRANSITION_OAUTH_BLOCKER_V1_AUDIT")
    print("status = OK")
    print("phase = FIRST_REAL_MULTI_LISTING_RUN_BLOCKED_BY_OAUTH_SCOPE")
    print("runtime_ready_for_live = False")
    print("policy_fetch_http_status = 403")
    print("refresh_with_current_scope_possible = False")
    print("next_step = build_new_oauth_consent_url_v1_with_sell_account_scope")

if __name__ == "__main__":
    main()
