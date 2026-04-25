import os,pathlib,runpy
root=pathlib.Path.cwd()
env=root/".env.local"
if env.exists():
    for line in env.read_text(encoding="utf-8",errors="replace").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k,v=line.split("=",1)
            os.environ[k.strip()]=v.strip()
runpy.run_path(str(root/"run_ebay_publish_offer_v6.py"),run_name="__main__")
