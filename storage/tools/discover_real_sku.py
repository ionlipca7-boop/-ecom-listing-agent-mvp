import json, pathlib, datetime, re 
root = pathlib.Path.cwd() 
out = root / r'storage\state_control\discover_real_sku_candidate_v1.json' 
files = [p for p in (root / 'storage').rglob('*.json')] 
candidates = [] 
for p in files: 
    try: 
        txt = p.read_text(encoding='utf-8', errors='replace') 
        found = re.findall(r'[A-Z0-9][A-Za-z0-9_-]{6,80}', txt) 
        for x in found: 
            if x != 'REPLACE_WITH_RESOLVED_LIVE_IDENTIFIER': 
                candidates.append(x) 
    except: 
        pass 
selected = candidates[0] if candidates else None 
data = { 
    'status': 'OK' if selected else 'BLOCKED', 
    'layer': 'DISCOVER_REAL_SKU_CANDIDATE_V1', 
    'selected_sku_candidate': selected, 
    'candidate_count': len(candidates), 
    'next_allowed_action': 'build_identifier_resolution_from_real_sku_v1' if selected else 'manual_provide_real_sku_v1', 
    'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat() 
} 
out.parent.mkdir(parents=True, exist_ok=True) 
out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8') 
print(json.dumps(data, ensure_ascii=False, indent=2)) 
