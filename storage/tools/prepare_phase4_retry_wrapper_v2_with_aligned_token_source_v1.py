import json,pathlib,datetime
root=pathlib.Path.cwd()
prev=root/r"storage\\state_control\\verify_aligned_publish_executor_token_source_v1.json"
refresh=root/r"storage\\tools\\safe_ebay_token_refresh_v1.py"
aligned=root/r"storage\\tools\\run_ebay_publish_offer_v6_env_token_wrapper_v1.py"
wrapper=root/r"storage\\tools\\phase4_retry_wrapper_v2_with_aligned_token_source_v1.py"
p=json.loads(prev.read_text(encoding="utf-8")) if prev.exists() else {}
ok=prev.exists() and p.get("status")=="OK" and p.get("decision",{}).get("token_source_aligned")==True and refresh.exists() and aligned.exists()
code="""import json,pathlib,datetime,subprocess,sys
root=pathlib.Path.cwd()
refresh=root/r"storage\\tools\\safe_ebay_token_refresh_v1.py"
aligned=root/r"storage\\tools\\run_ebay_publish_offer_v6_env_token_wrapper_v1.py"
out=root/r"storage\\state_control\\execute_phase4_retry_wrapper_v2_with_aligned_token_source_v1.json"
rr=subprocess.run([sys.executable,str(refresh)],cwd=str(root),capture_output=True,text=True,encoding="utf-8",errors="replace")
pr=None
if rr.returncode==0:
    pr=subprocess.run([sys.executable,str(aligned)],cwd=str(root),capture_output=True,text=True,encoding="utf-8",errors="replace")
d={"status":"CHECK_REQUIRED","layer":"EXECUTE_PHASE4_RETRY_WRAPPER_V2_WITH_ALIGNED_TOKEN_SOURCE_V1","token_guard_ran":True,"token_guard_returncode":rr.returncode,"publish_called":pr is not None,"publish_returncode":pr.returncode if pr else None,"refresh_stdout_tail":rr.stdout[-2000:],"refresh_stderr_tail":rr.stderr[-2000:],"publish_stdout_tail":pr.stdout[-3000:] if pr else "","publish_stderr_tail":pr.stderr[-3000:] if pr else "","safety":{"one_live_only":True,"batch_publish_allowed":False,"auto_publish_allowed":False,"revise_allowed":False,"delete_allowed":False},"next_allowed_action":"verify_phase4_retry_wrapper_v2_result_v1","timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("PHASE4_RETRY_WRAPPER_V2_DONE")
print(out)
"""
if ok: wrapper.write_text(code,encoding="utf-8")
d={"status":"AWAIT_CONFIRMATION" if ok else "BLOCKED","layer":"PREPARE_PHASE4_RETRY_WRAPPER_V2_WITH_ALIGNED_TOKEN_SOURCE_V1","wrapper_created":wrapper.exists(),"wrapper_path":str(wrapper),"confirmation_required":True,"operator_must_confirm_exact_phrase":"CONFIRM RUN PHASE4 RETRY V2 ALIGNED TOKEN ONE LIVE PUBLISH NOW","publish_called":False,"safety":{"one_live_only":True,"batch_publish_allowed":False,"auto_publish_allowed":False,"revise_allowed":False,"delete_allowed":False},"next_allowed_action":"await_confirmation_run_phase4_retry_wrapper_v2_v1" if ok else "repair_wrapper_v2_inputs_first","timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
out=root/r"storage\\state_control\\prepare_phase4_retry_wrapper_v2_with_aligned_token_source_v1.json"
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("WRAPPER_V2_GATE_WRITTEN")
print(out)
