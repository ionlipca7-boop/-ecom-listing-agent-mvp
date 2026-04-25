import json,pathlib,datetime,base64,urllib.request,urllib.parse
root=pathlib.Path.cwd()
env=root/".env.local"
raw=env.read_text(encoding="utf-8",errors="replace").splitlines() if env.exists() else []
kv={}

for l in raw:
    if "=" in l and not l.strip().startswith("#"):
        k,v=l.split("=",1)
        kv[k.strip()]=v.strip()

required=["EBAY_REFRESH_TOKEN","EBAY_CLIENT_ID","EBAY_CLIENT_SECRET"]
ok=all(kv.get(k) for k in required)
status="BLOCKED"
code=None
token=False
exp=None
error=None

if ok:
    auth=base64.b64encode((kv["EBAY_CLIENT_ID"]+":"+kv["EBAY_CLIENT_SECRET"]).encode()).decode()
    data=urllib.parse.urlencode({"grant_type":"refresh_token","refresh_token":kv["EBAY_REFRESH_TOKEN"],"scope":"https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory"}).encode()
    req=urllib.request.Request("https://api.ebay.com/identity/v1/oauth2/token",data=data,headers={"Authorization":"Basic "+auth,"Content-Type":"application/x-www-form-urlencoded"})
    try:
        resp=urllib.request.urlopen(req,timeout=30)
        code=resp.status
        body=resp.read().decode("utf-8","replace")
        j=json.loads(body)
        new_token=j.get("access_token")
        exp=j.get("expires_in")
        token=bool(new_token)
        status="OK" if token else "BLOCKED"
        if new_token:
            out_lines=[]
            seen=False
            for l in raw:
                if l.startswith("EBAY_ACCESS_TOKEN="):
                    out_lines.append("EBAY_ACCESS_TOKEN="+new_token)
                    seen=True
                else:
                    out_lines.append(l)
            if not seen:
                out_lines.append("EBAY_ACCESS_TOKEN="+new_token)
            env.write_text(chr(10).join(out_lines)+chr(10),encoding="utf-8")
    except Exception as e:
        error=type(e).__name__

d={"status":status,"layer":"RUN_SAFE_EBAY_TOKEN_REFRESH_V2","project":"ECOM_LISTING_AGENT_MVP","env_exists":env.exists(),"required_keys_present":ok,"http_status":code,"token_refreshed":token,"expires_in_seconds":exp,"error_type":error,"secrets_printed":False,"publish_allowed":False,"revise_allowed":False,"delete_allowed":False,"auto_publish_allowed":False,"timestamp":datetime.datetime.now(datetime.UTC).isoformat(),"next_allowed_action":"verify_ebay_access_token_read_only_v1" if token else "manual_oauth_required_v1"}
out=root/"storage"/"state_control"/"run_safe_ebay_token_refresh_v2.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
print("OK")
print(out)
