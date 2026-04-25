import json, pathlib, datetime, importlib.util, traceback
root = pathlib.Path.cwd()
gate = root / r"storage\state_control\prepare_real_ebay_inventory_read_execution_gate_v1.json"
out = root / r"storage\state_control\execute_real_ebay_inventory_read_only_v1.json"
x = json.loads(gate.read_text(encoding="utf-8")) if gate.exists() else {}
ok = gate.exists() and x.get("status") == "OK" and x.get("next_allowed_action") == "execute_real_ebay_inventory_read_only_v1"
api = {"ok": False, "api_call_used": False, "items": [], "error": "gate_blocked"}
err = ""
saved = False
count = 0
if ok:
    try:
        spec = importlib.util.spec_from_file_location("ebay_inventory_fetcher", root / r"publisher\ebay_inventory_fetcher.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        api = m.fetch_inventory_items()
        count = len(api.get("items", []))
        if api.get("ok"):
            saved = m.save_snapshot(api.get("items", [])).get("status") == "OK"
    except Exception as e:
        err = type(e).__name__ + ": " + str(e)
d = {"status": "OK" if api.get("ok") else "BLOCKED", "layer": "EXECUTE_REAL_EBAY_INVENTORY_READ_ONLY_V1", "project": "ECOM_LISTING_AGENT_MVP", "input_layer": x.get("layer"), "api_call_used": api.get("api_call_used", False), "read_only": True, "items_read": count, "snapshot_saved": saved, "error": err or api.get("error"), "write_allowed": False, "publish_allowed": False, "next_allowed_action": "verify_ebay_inventory_snapshot_56_v1" if api.get("ok") else "repair_or_refresh_ebay_access_token_v1", "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("REAL_EBAY_READ_OK" if api.get("ok") else "REAL_EBAY_READ_BLOCKED_OR_FAILED")
