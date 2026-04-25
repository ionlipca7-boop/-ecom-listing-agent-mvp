import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORT_PATH = BASE_DIR / "storage" / "exports" / "oauth_recovery_scan_v1.json"

TERMS = [
    "ru_name",
    "RuName",
    "redirect_uri",
    "oauth",
    "access_token",
    "refresh_token",
    "auth.ebay.com",
    "api.ebay.com/oauth" 
]

def scan_file(path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    hits = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        low = line.lower()
        for term in TERMS:
            if term.lower() in low:
                hits.append({"line": i, "term": term, "text": line[:220]})
    return hits[:20]

def main():
    results = []
    for path in BASE_DIR.rglob("*"):
        if not path.is_file():
            continue
        if ".git\\" in str(path) or "__pycache__" in str(path):
            continue
        if path.suffix.lower() not in [".py", ".json", ".txt", ".md", ".csv", ".log"]:
            continue
        hits = scan_file(path)
        if hits:
            results.append({"file": str(path.relative_to(BASE_DIR)), "hits": hits})
    audit = {
        "status": "OK",
        "decision": "oauth_recovery_scan_ready",
        "files_found": len(results),
        "results": results[:50]
    }
    EXPORT_PATH.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    print("OAUTH_RECOVERY_SCAN_V1")
    print("files_found =", len(results))
    if results:
        print("first_file =", results[0]["file"])
        print("first_hit =", results[0]["hits"][0]["term"])

if __name__ == "__main__":
    main()
