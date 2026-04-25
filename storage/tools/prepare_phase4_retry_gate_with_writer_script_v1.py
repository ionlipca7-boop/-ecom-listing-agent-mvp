import json,pathlib,datetime
root=pathlib.Path.cwd()
prev=root/r"storage\state_control\verify_phase4_result_and_token_state_before_any_retry_v1.json"
confirm=root/r"storage\state_control\await_explicit_operator_confirmation_for_one_live_publish_after_token_repair_v1.json"
executor=root/r"run_ebay_publish_offer_v6.py"
p=json.loads(prev.read_text(encoding="utf-8")) if prev.exists() else {}
c=json.loads(confirm.read_text(encoding="utf-8")) if confirm.exists() else {}
ok=prev.exists() and p.get("status")=="OK" and p.get("decision",{}).get("retry_possible_after_new_gate")==True and executor.exists()
d={"status":"AWAIT_CONFIRMATION" if ok else "BLOCKED","layer":"PREPARE_PHASE4_RETRY_GATE_WITH_WRITER_SCRIPT_V1","previous_layer":"VERIFY_PHASE4_RESULT_AND_TOKEN_STATE_BEFORE_ANY_RETRY_V1","executor":"run_ebay_publish_offer_v6.py","writer_script_required":True,"confirmation_required":True,"operator_must_confirm_exact_phrase":"CONFIRM PHASE4 RETRY ONE LIVE EBAY PUBLISH NOW","safety":{"publish_called":False,"retry_allowed_now":False,"one_live_only":True,"batch_publish_allowed":False,"auto_publish_allowed":False,"revise_allowed":False,"delete_allowed":False},"next_allowed_action":"await_explicit_operator_confirmation_for_phase4_retry_one_live_publish_v1" if ok else "repair_retry_gate_inputs_first","timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
out=root/r"storage\state_control\prepare_phase4_retry_gate_with_writer_script_v1.json"
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("RETRY_GATE_WRITTEN")
print(out)
