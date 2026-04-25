import json,pathlib,datetime
root=pathlib.Path.cwd()
prev=root/r"storage\\state_control\\recover_broken_deep_audit_cmd_v1.json"
publish=root/r"run_ebay_publish_offer_v6.py"
wrapper=root/r"storage\\tools\\run_ebay_publish_offer_v6_env_token_wrapper_v1.py"
p=json.loads(prev.read_text(encoding="utf-8")) if prev.exists() else {}
ok=prev.exists() and p.get("status")=="OK" and publish.exists()
code="""import os,pathlib,runpy
root=pathlib.Path.cwd()
env=root/".env.local"
if env.exists():
    for line in env.read_text(encoding="utf-8",errors="replace").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k,v=line.split("=",1)
            os.environ[k.strip()]=v.strip()
runpy.run_path(str(root/"run_ebay_publish_offer_v6.py"),run_name="__main__")
"""
if ok: wrapper.write_text(code,encoding="utf-8")
d={"status":"OK" if ok else "BLOCKED","layer":"ALIGN_PUBLISH_EXECUTOR_TOKEN_SOURCE_V1","publish_called":False,"wrapper_created":wrapper.exists(),"wrapper_path":str(wrapper),"fix":"wrapper loads .env.local into os.environ before running publish executor","next_allowed_action":"verify_aligned_publish_executor_token_source_v1" if ok else "repair_align_inputs_first","timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
out=root/r"storage\\state_control\\align_publish_executor_token_source_v1.json"
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("ALIGN_WRITTEN")
print(out)
