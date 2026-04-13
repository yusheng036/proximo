"""Admin routes: login, list participants, export CSV."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets

from fastapi import APIRouter, Cookie, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response

from src.csv_export import participants_to_csv
from src.models import AdminLoginRequest
from src.storage import get_all_participants

router = APIRouter(tags=["admin"])

_COOKIE_NAME = "admin_token"


def _make_token(password: str) -> str:
    salt = os.environ.get("ADMIN_SECRET_SALT", "proximo-default-salt")
    return hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()


def _verify_token(token: str) -> bool:
    expected_password = os.environ.get("ADMIN_PASSWORD", "")
    if not expected_password:
        return False
    expected_token = _make_token(expected_password)
    return secrets.compare_digest(token, expected_token)


def _require_admin(admin_token: str | None) -> None:
    if not admin_token or not _verify_token(admin_token):
        raise HTTPException(status_code=401, detail="Unauthorized")


# ── Login ──────────────────────────────────────────────────────────────────────

@router.post("/admin/login")
def admin_login(body: AdminLoginRequest) -> JSONResponse:
    expected = os.environ.get("ADMIN_PASSWORD", "")
    if not expected or not secrets.compare_digest(body.password, expected):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = _make_token(body.password)
    res = JSONResponse({"ok": True})
    res.set_cookie(
        key=_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 8,  # 8 hours
    )
    return res


@router.post("/admin/logout")
def admin_logout(response: Response) -> JSONResponse:
    response.delete_cookie(_COOKIE_NAME)
    return JSONResponse({"ok": True})


# ── Protected data routes ──────────────────────────────────────────────────────

@router.get("/admin/participants")
def list_participants(admin_token: str | None = Cookie(default=None)) -> JSONResponse:
    _require_admin(admin_token)
    participants = get_all_participants()
    return JSONResponse([p.model_dump() for p in participants])


@router.get("/admin/export.csv")
def export_csv(admin_token: str | None = Cookie(default=None)) -> Response:
    _require_admin(admin_token)
    participants = get_all_participants()
    csv_content = participants_to_csv(participants)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=proximo_data.csv"},
    )
