"""API routes for submitting post-session surveys."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.models import SubmitSurveyRequest
from src.storage import get_participant, save_participant

router = APIRouter(prefix="/api/surveys", tags=["surveys"])


@router.post("")
def submit_survey(body: SubmitSurveyRequest) -> JSONResponse:
    record = get_participant(body.participant_id)
    if not record:
        raise HTTPException(status_code=404, detail="Participant not found")

    # Remove any existing survey for this session number then append
    record.surveys = [
        s for s in record.surveys if s.session_number != body.survey.session_number
    ]
    record.surveys.append(body.survey)
    save_participant(record)
    return JSONResponse({"ok": True})
