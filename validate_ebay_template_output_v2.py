import json
import csv
import os


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_key(key):
    return key.replace("\ufeff", "").replace("я╗┐", "").strip()


def load_csv(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = []

        for row in reader:
            cleaned_row = {}
            for k, v in row.items():
                cleaned_row[clean_key(k)] = v
            rows.append(cleaned_row)

        fieldnames = [clean_key(x) for x in (reader.fieldnames or [])]
        return rows, fieldnames


def get_latest_package():
    index = load_json("publish_packages/publish_index.json")
    return index["latest_package"]


def main():
    package_id = get_latest_package()
    base_path = os.path.join("publish_packages", package_id)

    output_csv_path = os.path.join(base_path, "ebay_template_output_v2.csv")

    rows, columns = load_csv(output_csv_path)

    columns_count = len(columns)
    rows_count = len(rows)

    missing_title = 0
    missing_price = 0

    for row in rows:
        if not str(row.get("*Title", "")).strip():
            missing_title += 1
        if not str(row.get("*StartPrice", "")).strip():
            missing_price += 1

    validation_ok = (
        columns_count == 96 and
        rows_count > 0 and
        missing_title == 0 and
        missing_price == 0
    )

    print("package_id:", package_id)
    print("columns_count:", columns_count)
    print("rows_count:", rows_count)
    print("missing_title_rows:", missing_title)
    print("missing_price_rows:", missing_price)
    print("validation_ok:", validation_ok)


if __name__ == "__main__":
    main()