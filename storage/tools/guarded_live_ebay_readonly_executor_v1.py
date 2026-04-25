import json,pathlib,subprocess,datetime,sys
root=pathlib.Path(__file__).resolve().parents[2]
executor=root/r"run_build_real_inventory_read_call_v2.py"
forbidden=["additem","revise","enditem","delete","publish","bulk_update"]
txt=executor.read_text(encoding="utf-8",errors="replace").lower() if executor.exists() else ""
ok=executor.exists() and not any(x in txt for x in forbidden)
out=root/r"storage/state_control/execute_live_ebay_active_listings_read_only_v1.json"
res={"status":"BLOCKED","layer":"EXECUTE_LIVE_EBAY_ACTIVE_LISTINGS_READ_ONLY_V1","project":"ECOM_LISTING_AGENT_MVP","executor":str(executor),"guard_ok":ok,"publish_allowed":False,"revise_allowed":False,"delete_allowed":False,"destructive_actions_forbidden":True,"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
if ok:
    cp=subprocess.run([sys.executable,str(executor)],cwd=str(root),capture_output=True,text=True,encoding="utf-8",errors="replace")
    res.update({"status":"OK" if cp.returncode==0 else "ERROR","returncode":cp.returncode,"stdout_tail":cp.stdout[-3000:],"stderr_tail":cp.stderr[-3000:],"next_allowed_action":"parse_live_ebay_active_listings_snapshot_v1" if cp.returncode==0 else "repair_live_readonly_execution_v1"})
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(res,ensure_ascii=False,indent=2))
