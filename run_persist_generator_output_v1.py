import json
import subprocess
import sys
from pathlib import Path

def main():
    raw = subprocess.check_output([sys.executable, "generator_agent.py"], text=True, encoding="utf-8")
    data = json.loads(raw)
    Path("generator_output.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("GENERATOR_OUTPUT_PERSISTED")

if __name__ == "__main__":
    main()
