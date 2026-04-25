import json,pathlib,datetime
root=pathlib.Path.cwd()
prev=root/r"storage\state_control\prepare_ebay_auto_token_guard_v1.json"
refresh=root/r"storage\tools\safe_ebay_token_refresh_v1.py"
publish=root/r"run_ebay_publish_offer_v6.py"
wrapper=root/r"storage\tools\phase4_retry_one_live_publish_with_auto_token_guard_v1.py"
p=json.loads(prev.read_text(encoding="utf-8")) if prev.exists() else {}
ok=prev.exists() and p.get("status")=="OK" and refresh.exists() and publish.exists()
wrapper_code="""import json,pathlib,datetime,subprocess,sys
root=pathlib.Path.cwd()
refresh=root/r"storage\\tools\\safe_ebay_token_refresh_v1.py"
publish=root/r"run_ebay_publish_offer_v6.py"
out=root/r"storage\\state_control\\execute_phase4_retry_one_live_publish_with_auto_token_guard_v1.json"
refresh_run=subprocess.run([sys.executable,str(refresh)],cwd=str(root),capture_output=True,text=True,encoding="utf-8",errors="replace")
refresh_ok=refresh_run.returncode==0
publish_run=None
if refresh_ok:
    publish_run=subprocess.run([sys.executable,str(publish)],cwd=str(root),capture_output=True,text=True,encoding="utf-8",errors="replace")
d={"status":"CHECK_REQUIRED","layer":"EXECUTE_PHASE4_RETRY_ONE_LIVE_PUBLISH_WITH_AUTO_TOKEN_GUARD_V1","token_guard_ran":True,"token_guard_returncode":refresh_run.returncode,"publish_called":bool(refresh_ok),"publish_returncode":publish_run.returncode if publish_run else None,"refresh_stdout_tail":refresh_run.stdout[-2000:],"refresh_stderr_tail":refresh_run.stderr[-2000:],"publish_stdout_tail":publish_run.stdout[-3000:] if publish_run else "","publish_stderr_tail":publish_run.stderr[-3000:] if publish_run else "","safety":{"one_live_only":True,"batch_publish_allowed":False,"auto_publish_allowed":False,"revise_allowed":False,"delete_allowed":False},"next_allowed_action":"verify_phase4_retry_one_live_publish_result_v1","timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("PHASE4_RETRY_WITH_TOKEN_GUARD_DONE")
print(out)
"""
if ok: wrapper.write_text(wrapper_code,encoding="utf-8")
d={"status":"OK" if ok else "BLOCKED","layer":"BUILD_PHASE4_RETRY_EXECUTOR_WITH_AUTO_TOKEN_GUARD_V1","wrapper_created":wrapper.exists(),"wrapper_path":str(wrapper),"publish_called":False,"next_allowed_action":"await_confirmation_to_run_phase4_retry_wrapper_v1" if ok else "repair_wrapper_inputs_first","timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
out=root/r"storage\state_control\build_phase4_retry_executor_with_auto_token_guard_v1.json"
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("WRAPPER_BUILD_WRITTEN")
print(out)
