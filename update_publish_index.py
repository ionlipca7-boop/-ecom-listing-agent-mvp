import json
from datetime import UTC, datetime
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_datetime(value: str) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _load_meta(meta_path: Path) -> dict | None:
    try:
        raw = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(raw, dict):
        return None

    package_id = raw.get("package_id")
    generated_at = raw.get("generated_at")
    total_items = raw.get("total_items")

    if not isinstance(package_id, str) or not package_id:
        return None
    if not isinstance(generated_at, str) or not generated_at:
        return None
    if not isinstance(total_items, int):
        return None

    return {
        "package_id": package_id,
        "generated_at": generated_at,
        "total_items": total_items,
        "path": meta_path.parent.as_posix(),
    }


def _discover_packages() -> tuple[int, list[dict]]:
    scanned_packages = 0
    indexed_packages: list[dict] = []

    if not PUBLISH_PACKAGES_DIR.exists() or not PUBLISH_PACKAGES_DIR.is_dir():
        return scanned_packages, indexed_packages

    for package_dir in sorted(PUBLISH_PACKAGES_DIR.glob("package_*")):
        if not package_dir.is_dir():
            continue
        scanned_packages += 1
        meta = _load_meta(package_dir / "meta.json")
        if meta is not None:
            indexed_packages.append(meta)

    return scanned_packages, indexed_packages


def _latest_package(packages: list[dict]) -> str | None:
    if not packages:
        return None

    def _sort_key(item: dict) -> tuple[datetime, str]:
        parsed = _parse_datetime(item.get("generated_at", ""))
        if parsed is None:
            parsed = datetime.min.replace(tzinfo=UTC)
        return parsed, str(item.get("package_id", ""))

    return max(packages, key=_sort_key)["package_id"]


def main() -> int:
    scanned_packages, packages = _discover_packages()

    payload = {
        "generated_at": _utc_now_iso(),
        "total_packages": len(packages),
        "latest_package": _latest_package(packages),
        "packages": packages,
    }

    PUBLISH_PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"scanned_packages: {scanned_packages}")
    print(f"indexed_packages: {len(packages)}")
    print(f"output_file: {INDEX_PATH.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
