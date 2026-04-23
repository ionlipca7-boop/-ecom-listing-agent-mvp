from pathlib import Path
files = [Path(r'D:\ECOM_LISTING_AGENT_MVP\compact_core_state_hub_v1.py'), Path(r'D:\ECOM_LISTING_AGENT_MVP\compact_core_preview_contract_v1.py')]
result = []
for p in files:
    item = {'file': str(p), 'exists': p.exists()}
    if not p.exists():
        item['status'] = 'MISSING'
        result.append(item)
        continue
    raw = p.read_bytes()
    item['had_utf8_bom'] = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8', errors='replace')
    if text and text[0] == '\ufeff':
        text = text[1:]
    p.write_text(text, encoding='utf-8', newline='\n')
    try:
        compile(text, str(p), 'exec')
        item['compile_after'] = 'OK'
    except Exception as e:
        item['compile_after'] = 'BROKEN: ' + str(e)
    item['status'] = 'REWRITTEN_UTF8_NO_BOM'
    result.append(item)
import json
out = Path(r'D:\ECOM_LISTING_AGENT_MVP\storage\memory\archive\stage9_bom_clean_fix_audit.json')
out.parent.mkdir(parents=True, exist_ok=True)
payload = {'status': 'OK', 'project': 'ECOM_LISTING_AGENT_MVP', 'stage': 9, 'action': 'sanitize_utf8_bom', 'results': result}
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
print('STAGE9_BOM_CLEAN_FIX_AUDIT')
for item in result:
    print('file =', item['file'])
    print('exists =', item['exists'])
    print('status =', item['status'])
    if 'had_utf8_bom' in item: print('had_utf8_bom =', item['had_utf8_bom'])
    if 'compile_after' in item: print('compile_after =', item['compile_after'])
print('audit_file =', str(out))
