import json
from pathlib import Path
root = Path(r'D:\ECOM_LISTING_AGENT_MVP')
candidates = [
    root / 'compact_core_transition_front_v1.py',
    root / 'compact_core_state_hub_v1.py',
    root / 'compact_core_execution_bridge_v1.py',
    root / 'compact_core_preview_contract_v1.py',
    root / 'agents' / 'compact_core_transition_front_v1.py',
    root / 'agents' / 'compact_core_state_hub_v1.py',
    root / 'agents' / 'compact_core_execution_bridge_v1.py',
    root / 'agents' / 'compact_core_preview_contract_v1.py',
    root / 'storage' / 'agents' / 'compact_core_transition_front_v1.py',
    root / 'storage' / 'agents' / 'compact_core_state_hub_v1.py',
    root / 'storage' / 'agents' / 'compact_core_execution_bridge_v1.py',
    root / 'storage' / 'agents' / 'compact_core_preview_contract_v1.py',
]
found = {}
for p in candidates:
    if p.exists():
        found[p.name] = str(p)
result = {'status': 'OK', 'project': 'ECOM_LISTING_AGENT_MVP', 'stage': 9, 'files_found': found}
preview_name = 'compact_core_preview_contract_v1.py'
preview_path = found.get(preview_name)
if preview_path is None:
    result['preview_contract_exists'] = False
    result['preview_contract_compile'] = 'MISSING'
else:
    result['preview_contract_exists'] = True
    text = Path(preview_path).read_text(encoding='utf-8', errors='replace')
    lines = text.splitlines()
    result['preview_contract_line_count'] = len(lines)
    result['preview_contract_head'] = lines[:20]
    try:
        compile(text, preview_path, 'exec')
        result['preview_contract_compile'] = 'OK'
    except Exception as e:
        result['preview_contract_compile'] = 'BROKEN'
        result['preview_contract_error'] = str(e)
for stable_name in ['compact_core_transition_front_v1.py', 'compact_core_state_hub_v1.py', 'compact_core_execution_bridge_v1.py']:
    stable_path = found.get(stable_name)
    key = stable_name.replace('.py', '')
    if stable_path is None:
        result[key] = 'MISSING'
    else:
        stable_text = Path(stable_path).read_text(encoding='utf-8', errors='replace')
        try:
            compile(stable_text, stable_path, 'exec')
            result[key] = 'OK'
        except Exception as e:
            result[key] = 'BROKEN: ' + str(e)
out_dir = root / 'storage' / 'memory' / 'archive'
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / 'stage9_preview_contract_real_audit.json'
out_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print('STAGE9_PREVIEW_CONTRACT_REAL_AUDIT')
print('status =', result['status'])
print('stage =', result['stage'])
print('preview_contract_exists =', result['preview_contract_exists'])
print('preview_contract_compile =', result['preview_contract_compile'])
print('compact_core_transition_front_v1 =', result.get('compact_core_transition_front_v1'))
print('compact_core_state_hub_v1 =', result.get('compact_core_state_hub_v1'))
print('compact_core_execution_bridge_v1 =', result.get('compact_core_execution_bridge_v1'))
print('audit_file =', str(out_file))
if result.get('preview_contract_error'):
    print('preview_contract_error =', result['preview_contract_error'])
if result.get('preview_contract_head') is not None:
    print('preview_contract_head_lines =', len(result['preview_contract_head']))
