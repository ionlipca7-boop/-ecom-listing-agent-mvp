import json,pathlib,datetime,re
root=pathlib.Path.cwd()
files=[root/r"storage\tools\safe_ebay_token_refresh_v1.py",root/r"run_ebay_publish_offer_v6.py",root/r".env.local",root/r"storage\state_control\run_safe_ebay_token_refresh_v2.json",root/r"storage\state_control\execute_phase4_retry_one_live_publish_with_auto_token_guard_v1.json"]
scan={}
for f in files:
    item={"exists":f.exists(),"size":f.stat().st_size if f.exists() else None,"mtime":datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat() if f.exists() else None}
    if f.exists() and f.suffix==".py":
        txt=f.read_text(encoding="utf-8",errors="replace")
        item["mentions"]={"env_local":".env.local" in txt,"dotenv":"dotenv" in txt,"os_environ":"os.environ" in txt,"EBAY_ACCESS_TOKEN":"EBAY_ACCESS_TOKEN" in txt,"ACCESS_TOKEN":"ACCESS_TOKEN" in txt,"Authorization":"Authorization" in txt,"Bearer":"Bearer" in txt}
    if f.exists() and f.name==".env.local":
        lines=f.read_text(encoding="utf-8",errors="replace").splitlines()
        item["keys"]=[x.split("=",1)[0] for x in lines if "=" in x and not x.strip().startswith("#")]
    if f.exists() and f.suffix==".json":
        try:
            j=json.loads(f.read_text(encoding="utf-8"))
            item["json_status"]=j.get("status")
            item["json_http_status"]=j.get("http_status")
            item["json_token_refreshed"]=j.get("token_refreshed")
        except Exception as e:
            item["json_error"]=str(e)
    scan[str(f.relative_to(root))]=item
out=root/r"storage\state_control\diagnose_token_source_mismatch_v1.json"
d={"status":"OK","layer":"DIAGNOSE_TOKEN_SOURCE_MISMATCH_V1","publish_called":False,"problem":"refresh returncode 0 but publish still 401, likely token source mismatch","scan":scan,"decision":{"retry_allowed_now":False,"publish_allowed_now":False,"next_fix":"align_publish_executor_token_source_v1"},"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("DIAGNOSE_WRITTEN")
print(out)
