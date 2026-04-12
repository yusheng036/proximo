"""Proximo — Identity-Based AI Tutoring System

FastAPI application entry point.
Run with:  uvicorn main:app --reload
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Cookie, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

load_dotenv()

from routers import admin, chat, participants, reflection, survey
from routers.admin import _verify_token
from src.problems import get_problem_for_session
from src.storage import get_all_participants, get_participant

app = FastAPI(title="Proximo", version="0.1.0")

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(participants.router)
app.include_router(chat.router)
app.include_router(survey.router)
app.include_router(reflection.router)
app.include_router(admin.router)

# ── Templates ──────────────────────────────────────────────────────────────────
TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ── Page routes ────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/session/{session_number}", response_class=HTMLResponse)
async def session_page(request: Request, session_number: int, pid: str = ""):
    if session_number not in (1, 2):
        return RedirectResponse("/")

    if not pid:
        return RedirectResponse("/")

    participant = get_participant(pid)
    if not participant:
        return RedirectResponse("/")

    # Guard: session 2 requires session 1 to be complete
    if session_number == 2:
        s1 = participant.sessions[0]
        if not s1 or not s1.ended_at:
            return RedirectResponse(f"/session/1?pid={pid}")

    tutor_mode = participant.session_order[session_number - 1]
    problem = get_problem_for_session(session_number)
    initial_greeting = problem["initial_greetings"][tutor_mode]

    # Load existing messages if the session was already started
    session_record = participant.sessions[session_number - 1]
    existing_messages = []
    if session_record and session_record.messages:
        existing_messages = [m.model_dump() for m in session_record.messages]

    return templates.TemplateResponse("session.html", {
        "request": request,
        "pid": pid,
        "participant_name": participant.name,
        "session_number": session_number,
        "tutor_mode": tutor_mode,
        "problem_id": problem["id"],
        "problem_title": problem["title"],
        "problem_subject": problem["subject"],
        "problem_description": problem["description"],
        "initial_greeting": initial_greeting,
        "existing_messages": existing_messages,
        "session_already_started": session_record is not None,
    })


@app.get("/survey/{session_number}", response_class=HTMLResponse)
async def survey_page(request: Request, session_number: int, pid: str = ""):
    if session_number not in (1, 2) or not pid:
        return RedirectResponse("/")

    participant = get_participant(pid)
    if not participant:
        return RedirectResponse("/")

    # Guard: can only fill survey after session is ended
    session_record = participant.sessions[session_number - 1]
    if not session_record or not session_record.ended_at:
        return RedirectResponse(f"/session/{session_number}?pid={pid}")

    # Guard: already submitted
    existing_survey = next(
        (s for s in participant.surveys if s.session_number == session_number), None
    )
    if existing_survey:
        # Already done — skip forward
        if session_number == 1:
            return RedirectResponse(f"/session/2?pid={pid}")
        else:
            return RedirectResponse(f"/reflection?pid={pid}")

    tutor_mode = participant.session_order[session_number - 1]
    problem = get_problem_for_session(session_number)

    return templates.TemplateResponse("survey.html", {
        "request": request,
        "pid": pid,
        "session_number": session_number,
        "tutor_mode": tutor_mode,
        "problem_id": problem["id"],
        "problem_title": problem["title"],
    })


@app.get("/reflection", response_class=HTMLResponse)
async def reflection_page(request: Request, pid: str = ""):
    if not pid:
        return RedirectResponse("/")

    participant = get_participant(pid)
    if not participant:
        return RedirectResponse("/")

    # Guard: both sessions and surveys must be complete
    if len(participant.surveys) < 2:
        return RedirectResponse(f"/survey/2?pid={pid}")

    if participant.reflection:
        return RedirectResponse("/done")

    # Gather tutor labels for the reflection form
    s1_tutor = participant.session_order[0]
    s2_tutor = participant.session_order[1]

    return templates.TemplateResponse("reflection.html", {
        "request": request,
        "pid": pid,
        "s1_tutor": s1_tutor,
        "s2_tutor": s2_tutor,
    })


@app.get("/done", response_class=HTMLResponse)
async def done_page(request: Request):
    return templates.TemplateResponse("done.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard_page(
    request: Request,
    admin_token: str | None = Cookie(default=None),
):
    if not admin_token or not _verify_token(admin_token):
        return RedirectResponse("/admin")

    participants_data = [p.model_dump() for p in get_all_participants()]

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "participants": participants_data,
        "count": len(participants_data),
    })
