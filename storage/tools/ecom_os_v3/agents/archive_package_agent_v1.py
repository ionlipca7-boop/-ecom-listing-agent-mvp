from __future__ import annotations

import hashlib
import json
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ArchivePackageResult:
    status: str
    archive_path: str
    sha256: str
    file_count: int
    manifest_path: str
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ArchivePackageAgentV1:
    """Creates a ZIP archive and manifest for local proof artifacts.

    It archives only a provided output folder. It does not delete or deploy.
    """

    def run(self, source_dir: Path, archive_dir: Path, archive_name: str) -> ArchivePackageResult:
        source_dir = source_dir.resolve()
        archive_dir = archive_dir.resolve()
        archive_dir.mkdir(parents=True, exist_ok=True)

        if not source_dir.exists() or not source_dir.is_dir():
            manifest_path = archive_dir / f"{archive_name}.manifest.json"
            manifest = {
                "status": "BLOCKED_SOURCE_DIR_NOT_FOUND",
                "source_dir": str(source_dir),
                "archive_name": archive_name,
            }
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
            return ArchivePackageResult(
                status="BLOCKED",
                archive_path="",
                sha256="",
                file_count=0,
                manifest_path=str(manifest_path),
                next_allowed_action="FIX_ARCHIVE_SOURCE_DIR",
            )

        archive_path = archive_dir / f"{archive_name}.zip"
        files = [p for p in source_dir.rglob("*") if p.is_file()]
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in files:
                zf.write(p, p.relative_to(source_dir).as_posix())

        sha = self.sha256_file(archive_path)
        manifest_path = archive_dir / f"{archive_name}.manifest.json"
        manifest = {
            "status": "PASS_ARCHIVE_CREATED",
            "source_dir": str(source_dir),
            "archive_path": str(archive_path),
            "sha256": sha,
            "file_count": len(files),
            "files": [p.relative_to(source_dir).as_posix() for p in files],
            "no_delete": True,
            "no_deploy": True,
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        return ArchivePackageResult(
            status="PASS",
            archive_path=str(archive_path),
            sha256=sha,
            file_count=len(files),
            manifest_path=str(manifest_path),
            next_allowed_action="REVIEW_ARCHIVE_MANIFEST",
        )

    def sha256_file(self, path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
