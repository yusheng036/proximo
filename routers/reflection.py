"""API route for submitting the final comparative reflection."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.models import SubmitReflectionRequest
from src.storage import get_participant, save_participant

router = APIRouter(prefix="/api/reflections", tags=["reflections"])


@router.post("")
def submit_reflection(body: SubmitReflectionRequest) -> JSONResponse:
    record = get_participant(body.participant_id)
    if not record:
        raise HTTPException(status_code=404, detail="Participant not found")

    record.reflection = body.reflection
    record.completed_at = datetime.now(timezone.utc).isoformat()
    save_participant(record)
    return JSONResponse({"ok": True})
