from pathlib import Path
root = Path(rD:\ECOM_LISTING_AGENT_MVP)
pats = [build_new_listing_from_clone_baseline_v1,clone_baseline,listing_clone_baseline_v1,draft_generation,listing_draft,new_listing]
skip = {__pycache__,.git}
hits = []
for p in root.rglob(*):
    if any(part in skip for part in p.parts):
        continue
    if p.is_file() and p.suffix.lower() in (.py,.json,.txt,.md):
        try:
            text = p.read_text(encoding=utf-8, errors=ignore)
        except Exception:
            continue
        found = [k for k in pats if k.lower() in text.lower() or k.lower() in p.name.lower()]
        if found:
            hits.append((str(p), found))
for path, found in hits[:200]:
    print(path)
    print(  ->  + , .join(found))