from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
import html


@dataclass
class HtmlResult:
    status: str
    html_path: str
    blocked_reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HtmlAgentV1:
    """Renders a safe German HTML description from title and specifics."""

    def run(self, title_result: Dict[str, Any], specifics_result: Dict[str, Any], passport: Dict[str, Any], template_path: Path, output_path: Path) -> HtmlResult:
        blocked: List[str] = []
        if title_result.get("status") != "PASS":
            blocked.append("title_not_pass")
        if specifics_result.get("status") != "PASS":
            blocked.append("specifics_not_pass")
        if passport.get("status") != "PASS":
            blocked.append("passport_not_pass")
        if not template_path.exists():
            blocked.append("template_missing")

        title = title_result.get("recommended_title") or passport.get("product_identity") or "Produkt"
        specifics = specifics_result.get("specifics") or {}
        features = passport.get("confirmed_features") or []
        delivery = specifics.get("Lieferumfang") or "Siehe Beschreibung"

        if blocked:
            output_path.write_text("<!-- BLOCKED: HTML not rendered because required inputs failed. -->", encoding="utf-8")
            return HtmlResult(status="BLOCKED", html_path=str(output_path), blocked_reasons=blocked)

        template = template_path.read_text(encoding="utf-8")
        highlights = "\n".join(f"<li>{html.escape(str(x))}</li>" for x in (features or ["Saubere, geprüfte Produktangaben"] ))
        spec_rows = "\n".join(
            f"<tr><td style='border-bottom:1px solid #eee;padding:8px;font-weight:bold;'>{html.escape(str(k))}</td>"
            f"<td style='border-bottom:1px solid #eee;padding:8px;'>{html.escape(str(v))}</td></tr>"
            for k, v in specifics.items()
        )
        rendered = template.replace("{{TITLE}}", html.escape(str(title)))
        rendered = rendered.replace("{{HIGHLIGHTS}}", highlights)
        rendered = rendered.replace("{{SPEC_ROWS}}", spec_rows)
        rendered = rendered.replace("{{DELIVERY}}", html.escape(str(delivery)))
        output_path.write_text(rendered, encoding="utf-8")
        return HtmlResult(status="PASS", html_path=str(output_path), blocked_reasons=[])
