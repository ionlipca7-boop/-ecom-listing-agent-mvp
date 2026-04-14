import csv
import json
import re
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
TEMPLATE_PATH = Path("templates/ebay_category_template.csv")


def _load_latest_package_id(index_path: Path) -> str:
    if not index_path.exists():
        raise RuntimeError(f"latest package index not found: {index_path.as_posix()}")

    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"failed to read latest package index: {index_path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("publish index must be a JSON object")

    latest_package = payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package:
        raise RuntimeError("latest_package is missing in publish index")

    return latest_package


def _detect_template_header(template_file: Path) -> list[str]:
    if not template_file.exists():
        raise RuntimeError(f"template file not found: {template_file.as_posix()}")

    try:
        with template_file.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
    except OSError as exc:
        raise RuntimeError(f"failed to read template file: {template_file.as_posix()}") from exc

    header = None
    for row in rows:
        cleaned = [cell.strip() for cell in row]
        if not cleaned:
            continue
        if any(cell.startswith("*Action(") for cell in cleaned) and "*Category" in cleaned and "*Title" in cleaned:
            header = cleaned
            break

    if not header:
        raise RuntimeError("failed to detect template header row")

    return header


def _read_feed_rows(input_file: Path) -> list[dict[str, str]]:
    if not input_file.exists():
        raise RuntimeError(f"input file not found: {input_file.as_posix()}")

    try:
        with input_file.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise RuntimeError("input CSV has no header")
            return list(reader)
    except OSError as exc:
        raise RuntimeError(f"failed to read input CSV: {input_file.as_posix()}") from exc


def _first_non_empty(row: dict[str, str], candidates: list[str]) -> str:
    for key in candidates:
        value = row.get(key)
        if value is not None:
            text = value.strip()
            if text:
                return text
    lowered = {str(k).strip().lower(): (v or "") for k, v in row.items()}
    for key in candidates:
        value = lowered.get(key.lower())
        if value and value.strip():
            return value.strip()
    return ""


def _determine_category_name(source_row: dict[str, str]) -> str:
    return _first_non_empty(
        source_row,
        [
            "category",
            "category_name",
            "ebay_category",
            "type",
            "product_type",
        ],
    )


def _category_id(category_name: str, title: str, description: str) -> str:
    haystack = " ".join([category_name, title, description]).lower()
    if "kabel" in haystack or "adapter" in haystack:
        return "123422"
    if "ladeger" in haystack or "dock" in haystack or "netzteil" in haystack:
        return "123417"
    return "123422"


def _is_cable(category_name: str, title: str, description: str) -> bool:
    haystack = " ".join([category_name, title, description]).lower()
    return "kabel" in haystack


def _is_charger(category_name: str, title: str, description: str) -> bool:
    haystack = " ".join([category_name, title, description]).lower()
    return any(word in haystack for word in ["ladeger", "netzteil", "wandlade", "dock"])


def _produktart(is_cable: bool, is_charger: bool, text_blob: str) -> str:
    lowered = text_blob.lower()
    if is_cable:
        if any(token in lowered for token in ["usb-c", "usbc", "type-c"]):
            return "USB-C Kabel"
        return "Datenkabel"
    if is_charger:
        if "wand" in lowered:
            return "Wandladegerät"
        return "Netzteil"
    return ""


def _connectivity(text_blob: str) -> str:
    lowered = text_blob.lower()
    if any(token in lowered for token in ["usb-c", "usbc", "type-c"]):
        return "USB-C"
    return ""


def _included_items(is_cable: bool, is_charger: bool, text_blob: str) -> str:
    lowered = text_blob.lower()
    if is_cable:
        return "Ladekabel"
    if is_charger and any(token in lowered for token in ["kabel", "cable", "ladekabel"]):
        return "Ladekabel"
    return ""


def _cable_length(text_blob: str) -> str:
    lowered = text_blob.lower()
    if re.search(r"\b1\s*m\b|\b1m\b", lowered):
        return "1 m"
    if re.search(r"\b2\s*m\b|\b2m\b", lowered):
        return "2 m"
    return ""


def _color(text_blob: str) -> str:
    lowered = text_blob.lower()
    if any(token in lowered for token in ["weiß", "weiss", "white"]):
        return "Weiß"
    if any(token in lowered for token in ["schwarz", "black"]):
        return "Schwarz"
    return ""


def _build_output_row(source_row: dict[str, str], template_columns: list[str]) -> dict[str, str]:
    out = {column: "" for column in template_columns}

    title = _first_non_empty(source_row, ["title", "name"])
    description = _first_non_empty(source_row, ["description", "desc"])
    price = _first_non_empty(source_row, ["price", "start_price"])
    quantity = _first_non_empty(source_row, ["quantity", "qty", "stock"])
    category_name = _determine_category_name(source_row)

    text_blob = f"{title} {description} {category_name}".strip()
    is_cable = _is_cable(category_name, title, description)
    is_charger = _is_charger(category_name, title, description)

    action_col = next((c for c in template_columns if c.startswith("*Action(")), None)
    if action_col:
        out[action_col] = "Add"

    if "*Category" in out:
        out["*Category"] = _category_id(category_name, title, description)
    if "*Title" in out:
        out["*Title"] = title
    if "*ConditionID" in out:
        out["*ConditionID"] = "1000"
    if "VAT%" in out:
        out["VAT%"] = ""
    if "C:Marke" in out:
        out["C:Marke"] = "Markenlos"
    if "C:Produktart" in out:
        out["C:Produktart"] = _produktart(is_cable, is_charger, text_blob)
    if "C:Konnektivität" in out:
        out["C:Konnektivität"] = _connectivity(text_blob)
    if "C:Inbegriffene Artikel" in out:
        out["C:Inbegriffene Artikel"] = _included_items(is_cable, is_charger, text_blob)
    if "C:Anzahl der Anschlüsse" in out:
        out["C:Anzahl der Anschlüsse"] = "1"
    if "C:Kabellänge" in out:
        out["C:Kabellänge"] = _cable_length(text_blob)
    if "C:Farbe" in out:
        out["C:Farbe"] = _color(text_blob)
    if "C:Markenkompatibilität" in out:
        out["C:Markenkompatibilität"] = "Universell"
    if "C:Material" in out:
        out["C:Material"] = "Kunststoff" if is_charger else ""
    if "C:Modellkompatibilität" in out:
        out["C:Modellkompatibilität"] = "Universal"
    if "C:Besonderheiten" in out:
        out["C:Besonderheiten"] = "Schnellladung"
    if "PicURL" in out:
        out["PicURL"] = ""
    if "*Description" in out:
        out["*Description"] = description
    if "*Format" in out:
        out["*Format"] = "FixedPrice"
    if "*Duration" in out:
        out["*Duration"] = "GTC"
    if "*StartPrice" in out:
        out["*StartPrice"] = price
    if "BuyItNowPrice" in out:
        out["BuyItNowPrice"] = ""
    if "*Quantity" in out:
        out["*Quantity"] = quantity
    if "ImmediatePayRequired" in out:
        out["ImmediatePayRequired"] = ""
    if "*Location" in out:
        out["*Location"] = "Germany"
    if "ShippingType" in out:
        out["ShippingType"] = "Flat"
    if "ShippingService-1:Option" in out:
        out["ShippingService-1:Option"] = "Standard Shipping"
    if "ShippingService-1:Cost" in out:
        out["ShippingService-1:Cost"] = "0"
    if "*DispatchTimeMax" in out:
        out["*DispatchTimeMax"] = "2"
    if "*ReturnsAcceptedOption" in out:
        out["*ReturnsAcceptedOption"] = "ReturnsAccepted"
    if "ReturnsWithinOption" in out:
        out["ReturnsWithinOption"] = "Days30"
    if "RefundOption" in out:
        out["RefundOption"] = "MoneyBack"
    if "ShippingCostPaidByOption" in out:
        out["ShippingCostPaidByOption"] = "Buyer"

    return out


def _write_output(output_file: Path, template_columns: list[str], rows: list[dict[str, str]]) -> None:
    try:
        with output_file.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=template_columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    except OSError as exc:
        raise RuntimeError(f"failed to write output CSV: {output_file.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    input_file = package_dir / "ebay_feed_final.csv"
    output_file = package_dir / "ebay_upload_ready_v2.csv"
    template_file = TEMPLATE_PATH

    template_columns = _detect_template_header(template_file)
    source_rows = _read_feed_rows(input_file)
    output_rows = [_build_output_row(row, template_columns) for row in source_rows]
    _write_output(output_file, template_columns, output_rows)

    print(f"package_id: {package_id}")
    print(f"template_file: {template_file.as_posix()}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"output_file: {output_file.as_posix()}")
    print(f"total_items: {len(output_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
