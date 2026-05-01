from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class TeacherLesson:
    lesson_id: str
    lesson_type: str
    target_agents: List[str]
    lesson: str
    rule_candidate: str


@dataclass
class TeacherResult:
    status: str
    lessons: List[Dict[str, Any]]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TeacherAgentV1:
    """Learns from the local sandbox run summary.

    This deterministic V1 does not rewrite agent files automatically. It emits
    lessons that can be archived and reviewed.
    """

    def run(self, run_context: Dict[str, Any]) -> TeacherResult:
        lessons: List[TeacherLesson] = []
        critic_issues = run_context.get("critic_issues") or []
        image_issues = run_context.get("image_critic_issues") or []

        if not critic_issues and not image_issues:
            lessons.append(TeacherLesson(
                lesson_id="LESSON_LOCAL_SANDBOX_PASS",
                lesson_type="SUCCESS_PATTERN",
                target_agents=["PHOTO_AGENT", "TITLE_AGENT", "HTML_AGENT", "CRITIC_AGENT"],
                lesson="Local sandbox produced a complete artifact package without critic issues.",
                rule_candidate="Keep Product Passport -> Evidence -> Photo Blueprint -> Text -> Critic order.",
            ))

        for issue in critic_issues + image_issues:
            lessons.append(TeacherLesson(
                lesson_id=f"LESSON_FIX_{str(issue).replace(':', '_').replace(' ', '_')[:60]}",
                lesson_type="FAILURE_PATTERN",
                target_agents=["CRITIC_AGENT", "AFFECTED_AGENT"],
                lesson=f"Sandbox issue detected: {issue}",
                rule_candidate="Block next step until the issue is fixed and rerun critic.",
            ))

        return TeacherResult(
            status="PASS",
            lessons=[asdict(x) for x in lessons],
            next_allowed_action="ARCHIVE_LESSONS_AND_REVIEW",
        )
