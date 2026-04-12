"""API routes for creating and updating participant records."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.counterbalance import get_next_tutor_order
from src.models import (
    ChatMessage,
    CreateParticipantRequest,
    PatchParticipantRequest,
    ParticipantRecord,
    SessionRecord,
)
from src.problems import get_problem_for_session
from src.storage import get_participant, save_participant

import uuid as _uuid

router = APIRouter(prefix="/api/participants", tags=["participants"])


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.post("")
def create_participant(body: CreateParticipantRequest) -> JSONResponse:
    tutor_order = get_next_tutor_order()
    record = ParticipantRecord(
        id=str(_uuid.uuid4()),
        name=body.name.strip(),
        created_at=_now(),
        session_order=tutor_order,
        sessions=[None, None],
        surveys=[],
        reflection=None,
        completed_at=None,
    )
    save_participant(record)
    return JSONResponse({"id": record.id, "session_order": list(record.session_order)})


@router.get("/{participant_id}")
def read_participant(participant_id: str) -> JSONResponse:
    record = get_participant(participant_id)
    if not record:
        raise HTTPException(status_code=404, detail="Participant not found")
    return JSONResponse(record.model_dump())


@router.patch("/{participant_id}")
def patch_participant(participant_id: str, body: PatchParticipantRequest) -> JSONResponse:
    record = get_participant(participant_id)
    if not record:
        raise HTTPException(status_code=404, detail="Participant not found")

    sn = body.session_number  # 1 or 2
    idx = (sn - 1) if sn else None

    if body.action == "start_session":
        if idx is None or body.tutor_mode is None or body.problem_id is None:
            raise HTTPException(status_code=400, detail="session_number, tutor_mode, and problem_id required")
        # Only create if not already started
        if record.sessions[idx] is None:
            session = SessionRecord(
                session_number=sn,
                tutor_mode=body.tutor_mode,
                problem_id=body.problem_id,
                started_at=_now(),
                messages=body.messages or [],
            )
            record.sessions[idx] = session
            save_participant(record)

    elif body.action == "end_session":
        if idx is None:
            raise HTTPException(status_code=400, detail="session_number required")
        session = record.sessions[idx]
        if session and not session.ended_at:
            session.ended_at = _now()
            save_participant(record)

    elif body.action == "update_messages":
        if idx is None or body.messages is None:
            raise HTTPException(status_code=400, detail="session_number and messages required")
        session = record.sessions[idx]
        if session:
            session.messages = body.messages
            save_participant(record)

    return JSONResponse({"ok": True})
