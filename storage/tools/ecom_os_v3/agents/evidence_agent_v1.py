from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class EvidenceMapResult:
    status: str
    evidence_map: Dict[str, List[str]]
    unsupported_claims: List[str]
    blocked_reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EvidenceAgentV1:
    """Maps claims to source evidence.

    Local deterministic version. It treats source packet visible_claims and
    operator-provided confirmed_features as evidence. Future versions can add
    screenshot OCR, URL extraction, and image metadata.
    """

    def run(self, source_packet: Dict[str, Any], passport: Dict[str, Any]) -> EvidenceMapResult:
        source_claims = [str(x).lower() for x in source_packet.get("visible_claims", [])]
        features = passport.get("confirmed_features") or []
        evidence_map: Dict[str, List[str]] = {}
        unsupported: List[str] = []

        for feature in features:
            f_low = str(feature).lower()
            matched = [claim for claim in source_claims if self._soft_match(f_low, claim)]
            if matched:
                evidence_map[str(feature)] = matched
            else:
                unsupported.append(str(feature))

        blocked: List[str] = []
        if source_packet.get("status") != "PASS":
            blocked.append("source_packet_not_pass")
        if passport.get("status") != "PASS":
            blocked.append("passport_not_pass")
        if unsupported:
            blocked.append("unsupported_claims_present")

        status = "PASS" if not blocked else "BLOCKED"
        return EvidenceMapResult(status=status, evidence_map=evidence_map, unsupported_claims=unsupported, blocked_reasons=blocked)

    def _soft_match(self, feature: str, claim: str) -> bool:
        if feature in claim or claim in feature:
            return True
        feature_tokens = {t for t in feature.replace("/", " ").replace("-", " ").split() if len(t) >= 2}
        claim_tokens = {t for t in claim.replace("/", " ").replace("-", " ").split() if len(t) >= 2}
        if not feature_tokens:
            return False
        return len(feature_tokens & claim_tokens) >= max(1, min(2, len(feature_tokens)))
