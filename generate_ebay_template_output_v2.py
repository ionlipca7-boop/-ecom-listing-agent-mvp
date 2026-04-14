import json
import csv
import os


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_key(key):
    return key.replace("﻿", "").replace("я╗┐", "").strip()


def load_csv(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        cleaned_rows = []
        for row in reader:
            cleaned_row = {}
            for k, v in row.items():
                cleaned_key = clean_key(k)
                cleaned_row[cleaned_key] = v
            cleaned_rows.append(cleaned_row)

        fieldnames = [clean_key(f) for f in reader.fieldnames]

        return cleaned_rows, fieldnames


def get_latest_package():
    index = load_json("publish_packages/publish_index.json")
    return index["latest_package"]


def main():
    package_id = get_latest_package()
    base_path = os.path.join("publish_packages", package_id)

    upload_csv_path = os.path.join(base_path, "ebay_upload_ready_v2.csv")
    mapping_path = os.path.join(base_path, "ebay_mapping_v2.json")
    output_path = os.path.join(base_path, "ebay_template_output_v2.csv")

    upload_rows, _ = load_csv(upload_csv_path)
    mapping = load_json(mapping_path)

    template_columns = mapping["meta"]["template_columns"]

    direct_map = mapping.get("direct_map", {})
    transform_map = mapping.get("transform_map", {})
    static_defaults = mapping.get("static_defaults", {})
    empty_fields = mapping.get("empty_fields", [])

    output_rows = []

    for row in upload_rows:
        output_row = {}

        for col in template_columns:

            # DIRECT MAP (ТОЧНОЕ СОВПАДЕНИЕ)
            if col in direct_map:
                source_field = direct_map[col]
                output_row[col] = row.get(source_field, "")

            # TRANSFORM MAP
            elif col in transform_map:
                source_field = transform_map[col]
                output_row[col] = row.get(source_field, "")

            # STATIC
            elif col in static_defaults:
                output_row[col] = static_defaults[col]

            # EMPTY
            elif col in empty_fields:
                output_row[col] = ""

            else:
                output_row[col] = ""

        output_rows.append(output_row)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=template_columns)
        writer.writeheader()
        for row in output_rows:
            writer.writerow(row)

    print("package_id:", package_id)
    print("rows_processed:", len(upload_rows))
    print("columns_output:", len(template_columns))
    print("output_file:", output_path)


if __name__ == "__main__":
    main()