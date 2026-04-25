import json, pathlib, datetime, sys
root=pathlib.Path.cwd()
entry=root/r"storage\state_control\local_control_runtime_entry_v1.json"
out=root/r"storage\runtime\local_control_runtime_output_v1.json"
e=json.loads(entry.read_text(encoding="utf-8"))
d={"status":"OK","layer":"LOCAL_CONTROL_RUNTIME_OUTPUT_V1","project":"ECOM_LISTING_AGENT_MVP","input_layer":e.get("layer"),"mode":"DRY_LOCAL_CONTROL_RUNTIME","real_ebay_api_call_allowed":False,"publish_allowed":False,"server_run_allowed":False,"telegram_run_allowed":False,"git_push_allowed":False,"local_runtime_executed":True,"next_allowed_action":"build_telegram_control_interface_v1","timestamp":datetime.datetime.now(datetime.UTC).isoformat()}
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(d,ensure_ascii=False,indent=2))