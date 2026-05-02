from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class CleanupCandidate:
    rel_path: str
    decision: str
    reason: str
    required_gate: str


@dataclass
class CleanupArchivistResult:
    status: str
    candidates: List[Dict[str, Any]]
    forbidden_count: int
    archive_required: bool
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CleanupArchivistAgentV1:
    """Converts readonly cleanup audit items into a safe cleanup review plan.

    It never deletes. It only classifies what would need archive + approval.
    """

    def run(self, audit_report: Dict[str, Any]) -> CleanupArchivistResult:
        items = audit_report.get("items") or []
        candidates: List[CleanupCandidate] = []
        forbidden_count = 0

        for item in items:
            rel = str(item.get("rel_path") or item.get("path") or "UNKNOWN")
            classification = str(item.get("classification") or "UNCERTAIN")
            reason = str(item.get("reason") or "")
            if classification == "DELETE_FORBIDDEN" or classification == "DO_NOT_TOUCH":
                forbidden_count += 1
                continue
            if classification == "ARCHIVE_THEN_DELETE_CANDIDATE":
                candidates.append(CleanupCandidate(
                    rel_path=rel,
                    decision="ARCHIVE_THEN_DELETE_CANDIDATE",
                    reason=reason,
                    required_gate="ARCHIVE_HASH_MANIFEST_OPERATOR_APPROVAL",
                ))
            elif classification == "UNCERTAIN":
                candidates.append(CleanupCandidate(
                    rel_path=rel,
                    decision="REVIEW_MANUALLY_DO_NOT_DELETE_YET",
                    reason=reason,
                    required_gate="MANUAL_REVIEW",
                ))

        return CleanupArchivistResult(
            status="PASS",
            candidates=[asdict(x) for x in candidates],
            forbidden_count=forbidden_count,
            archive_required=bool(candidates),
            next_allowed_action="CREATE_CLEANUP_MANIFEST_AFTER_OPERATOR_REVIEW" if candidates else "NO_CLEANUP_NEEDED",
        )
