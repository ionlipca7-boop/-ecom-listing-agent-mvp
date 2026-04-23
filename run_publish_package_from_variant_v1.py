import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
PACKAGES_DIR = BASE_DIR / "storage" / "publish_variant_packages"
EXECUTION_FILE = EXPORTS_DIR / "execution_variant_export_v1.json"
INDEX_FILE = PACKAGES_DIR / "publish_variant_index_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "publish_package_from_variant_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def make_package_id():
    return "variant_package_" + datetime.now().strftime("%Y%m%d_%H%M%S")

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    execution_data = read_json(EXECUTION_FILE)
    package_status = "WAITING"
    next_step = "CHECK_EXECUTION_EXPORT_FIRST"
    package_id = ""
    package_dir_text = ""
    payload_file_text = ""
    manifest_file_text = ""
    selected_variant_id = ""
    selected_title = ""

    if execution_data and execution_data.get("export_status") == "READY":
        package_id = make_package_id()
        package_dir = PACKAGES_DIR / package_id
        package_dir.mkdir(parents=True, exist_ok=True)
        execution_payload = execution_data.get("execution_payload", {})
        summary = execution_data.get("summary", {})
        selected_variant_id = summary.get("selected_variant_id", "")
        selected_title = summary.get("selected_title", "")
        payload_file = package_dir / "execution_payload_v1.json"
        manifest_file = package_dir / "manifest_v1.json"
        manifest = {}
        manifest["package_id"] = package_id
        manifest["package_status"] = "READY"
        manifest["selected_variant_id"] = selected_variant_id
        manifest["selected_title"] = selected_title
        manifest["payload_file"] = str(payload_file)
        manifest["source_file"] = str(EXECUTION_FILE)
        manifest["created_at"] = datetime.now().isoformat(timespec="seconds")
        write_json(payload_file, execution_payload)
        write_json(manifest_file, manifest)
        index_data = {}
        index_data["latest_package_id"] = package_id
        index_data["latest_package_dir"] = str(package_dir)
        index_data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        write_json(INDEX_FILE, index_data)
        package_status = "READY"
        next_step = "READY_FOR_PUBLISH_CONTROL_ROOM"
        package_dir_text = str(package_dir)
        payload_file_text = str(payload_file)
        manifest_file_text = str(manifest_file)

    output = {}
    output["package_status"] = package_status
    output["next_step"] = next_step
    output["package_id"] = package_id
    output["package_dir"] = package_dir_text
    output["payload_file"] = payload_file_text
    output["manifest_file"] = manifest_file_text
    output["selected_variant_id"] = selected_variant_id
    output["selected_title"] = selected_title
    write_json(OUTPUT_FILE, output)
    print("PUBLISH_PACKAGE_FROM_VARIANT_V1:")
    print("package_status:", output["package_status"])
    print("package_id:", output["package_id"])
    print("selected_variant_id:", output["selected_variant_id"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
