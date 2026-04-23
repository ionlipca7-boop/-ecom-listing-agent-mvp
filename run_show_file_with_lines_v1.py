from pathlib import Path

TARGET = Path("run_ebay_create_offer_from_draft_v1.py")

def main():
    if not TARGET.exists():
        print("FILE_MISSING")
        return
    lines = TARGET.read_text(encoding="utf-8").splitlines()
    i = 
    for line in lines:
        print(str(i).rjust(3), ":", line)
        i = i + 

if __name__ == "__main__":
    main()
