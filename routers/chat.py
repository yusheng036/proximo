"""Streaming chat endpoint — returns a plain text stream from the Anthropic API."""

from __future__ import annotations

import os

import anthropic
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from src.models import ChatRequest
from src.prompts import build_system_prompt
from src.storage import get_participant

router = APIRouter(prefix="/api/chat", tags=["chat"])

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")
        _client = anthropic.Anthropic(
            api_key=api_key,
            http_client=httpx.Client(transport=httpx.HTTPTransport(local_address="0.0.0.0")),
        )
    return _client


@router.post("")
def chat_stream(body: ChatRequest) -> StreamingResponse:
    participant = get_participant(body.participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    system_prompt = build_system_prompt(
        body.tutor_mode,
        body.problem_id,
        background_cs=participant.background_cs,
        background_math=participant.background_math,
    )

    # Convert to Anthropic message format (exclude system role if present)
    api_messages = [
        {"role": m.role, "content": m.content}
        for m in body.messages
        if m.role in ("user", "assistant")
    ]

    def generate():
        client = _get_client()
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=system_prompt,
            messages=api_messages,
        ) as stream:
            for text_chunk in stream.text_stream:
                yield text_chunk

    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")
