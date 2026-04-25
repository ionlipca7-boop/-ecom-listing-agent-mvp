import json,pathlib,datetime
root=pathlib.Path.cwd()
prev=root/r"storage\state_control\prepare_phase4_retry_gate_with_writer_script_v1.json"
refresh=root/r"storage\tools\safe_ebay_token_refresh_v1.py"
verify=root/r"storage\state_control\verify_ebay_access_token_read_only_v1.json"
p=json.loads(prev.read_text(encoding="utf-8")) if prev.exists() else {}
ok=prev.exists() and p.get("status")=="AWAIT_CONFIRMATION" and refresh.exists() and verify.exists()
d={"status":"OK" if ok else "BLOCKED","layer":"PREPARE_EBAY_AUTO_TOKEN_GUARD_V1","purpose":"before any eBay write action, verify token and refresh automatically if expired/invalid","previous_layer":"PREPARE_PHASE4_RETRY_GATE_WITH_WRITER_SCRIPT_V1","refresh_script_exists":refresh.exists(),"verify_state_exists":verify.exists(),"guard_rules":{"run_before_publish":True,"run_before_revise":True,"run_before_delete":True,"print_secrets":False,"write_env_allowed":True,"publish_called":False,"revise_called":False,"delete_called":False,"auto_publish_allowed":False},"integration_target":"wrap run_ebay_publish_offer_v6.py with token guard before request","next_allowed_action":"build_phase4_retry_executor_with_auto_token_guard_v1" if ok else "repair_token_guard_inputs_first","timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
out=root/r"storage\state_control\prepare_ebay_auto_token_guard_v1.json"
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("AUTO_TOKEN_GUARD_PREPARED")
print(out)
