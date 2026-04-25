import json,pathlib,datetime
root=pathlib.Path.cwd()
refresh=root/r"storage\\tools\\safe_ebay_token_refresh_v1.py"
out_guard=root/r"storage\\tools\\ebay_auto_token_guard_v1.py"
ok=refresh.exists()
code="""import os,pathlib,subprocess,sys,json,datetime
root=pathlib.Path.cwd()
env=root/".env.local"
refresh=root/r"storage\\tools\\safe_ebay_token_refresh_v1.py"
state=root/r"storage\\state_control\\ebay_auto_token_guard_last_run_v1.json"
def load_env():
    if env.exists():
        for line in env.read_text(encoding="utf-8",errors="replace").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k,v=line.split("=",1)
                os.environ[k.strip()]=v.strip()
def ensure_token():
    load_env()
    r=subprocess.run([sys.executable,str(refresh)],cwd=str(root),capture_output=True,text=True,encoding="utf-8",errors="replace")
    load_env()
    d={"status":"OK" if r.returncode==0 else "FAILED","layer":"EBAY_AUTO_TOKEN_GUARD_LAST_RUN_V1","returncode":r.returncode,"stdout_tail":r.stdout[-1000:],"stderr_tail":r.stderr[-1000:],"secrets_printed":False,"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    state.parent.mkdir(parents=True,exist_ok=True)
    state.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
    return r.returncode==0
if __name__=="__main__":
    ok=ensure_token()
    print("EBAY_AUTO_TOKEN_GUARD_OK" if ok else "EBAY_AUTO_TOKEN_GUARD_FAILED")
    sys.exit(0 if ok else 1)
"""
if ok: out_guard.write_text(code,encoding="utf-8")
d={"status":"OK" if ok else "BLOCKED","layer":"BUILD_PERMANENT_EBAY_AUTO_TOKEN_GUARD_V1","guard_created":out_guard.exists(),"guard_path":str(out_guard),"purpose":"permanent guard: refresh token and reload .env.local before every eBay write action","publish_called":False,"revise_called":False,"delete_called":False,"next_allowed_action":"verify_permanent_ebay_auto_token_guard_v1" if ok else "repair_refresh_script_first","timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
out=root/r"storage\\state_control\\build_permanent_ebay_auto_token_guard_v1.json"
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("PERMANENT_GUARD_WRITTEN")
print(out)
