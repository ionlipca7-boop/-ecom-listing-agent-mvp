import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
SAMPLES_DIR = STORAGE_DIR / "upload_result_samples"
TARGET_DIR = STORAGE_DIR / "upload_results"
EXPORTS_DIR = STORAGE_DIR / "exports"
OUTPUT_FILE = EXPORTS_DIR / "ebay_result_sample_loader_v1.json"

def main():
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    sample_files = [p for p in SAMPLES_DIR.iterdir() if p.is_file()]
    sample_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    if not sample_files:
        output = {
            "loader_status": "NO_SAMPLE",
            "next_step": "PLACE_TEST_EBAY_RESULT_FILE_IN_UPLOAD_RESULT_SAMPLES",
            "samples_dir": str(SAMPLES_DIR),
            "target_dir": str(TARGET_DIR),
            "sample_count": 0,
            "loaded_file": None
        }
    else:
        source_file = sample_files[0]
        target_file = TARGET_DIR / source_file.name
        shutil.copy2(source_file, target_file)
        output = {
            "loader_status": "LOADED",
            "next_step": "RUN_UPLOAD_RESULT_PARSER",
            "samples_dir": str(SAMPLES_DIR),
            "target_dir": str(TARGET_DIR),
            "sample_count": len(sample_files),
            "loaded_file": str(target_file),
            "source_file": str(source_file)
        }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("EBAY_RESULT_SAMPLE_LOADER_V1:")
    print("loader_status:", output["loader_status"])
    print("sample_count:", output["sample_count"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)
    if output.get("loaded_file"):
        print("loaded_file:", output["loaded_file"])

if __name__ == "__main__":
    main()
