from __future__ import annotations

import csv
import io
from src.models import ParticipantRecord

COLUMNS = [
    "participant_id",
    "created_at",
    "session_number",
    "tutor_mode",
    "problem_id",
    "session_started_at",
    "session_ended_at",
    "message_count",
    "motivation",
    "engagement",
    "perceived_support",
    "self_confidence",
    "enjoyment",
    "clarity",
    "trust",
    "perceived_learning",
    "most_helpful",
    "least_helpful",
    "more_motivating_session",
    "more_motivating_reason",
    "more_comprehensible_session",
    "free_form_comments",
]


def participants_to_csv(participants: list[ParticipantRecord]) -> str:
    """Return a UTF-8 CSV string with one row per session (two rows per participant)."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, extrasaction="ignore")
    writer.writeheader()

    for p in participants:
        reflection = p.reflection

        for i in range(2):
            session = p.sessions[i] if i < len(p.sessions) else None
            survey = next(
                (s for s in p.surveys if s.session_number == i + 1), None
            )

            row: dict = {
                "participant_id": p.id,
                "created_at": p.created_at,
                "session_number": i + 1,
                "tutor_mode": session.tutor_mode if session else p.session_order[i],
                "problem_id": session.problem_id if session else "",
                "session_started_at": session.started_at if session else "",
                "session_ended_at": session.ended_at if session else "",
                "message_count": len(session.messages) if session else 0,
                # Survey
                "motivation": survey.motivation if survey else "",
                "engagement": survey.engagement if survey else "",
                "perceived_support": survey.perceived_support if survey else "",
                "self_confidence": survey.self_confidence if survey else "",
                "enjoyment": survey.enjoyment if survey else "",
                "clarity": survey.clarity if survey else "",
                "trust": survey.trust if survey else "",
                "perceived_learning": survey.perceived_learning if survey else "",
                "most_helpful": survey.most_helpful if survey else "",
                "least_helpful": survey.least_helpful if survey else "",
                # Reflection
                "more_motivating_session": reflection.more_motivating_session if reflection else "",
                "more_motivating_reason": reflection.more_motivating_reason if reflection else "",
                "more_comprehensible_session": reflection.more_comprehensible_session if reflection else "",
                "free_form_comments": reflection.free_form_comments if reflection else "",
            }
            writer.writerow(row)

    return buf.getvalue()
