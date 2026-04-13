from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel

TutorMode = Literal["standard", "future-self"]
ProblemId = Literal["fibonacci", "bayes"]
SessionNumber = Literal[1, 2]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    timestamp: str  # ISO-8601


class SurveyResponse(BaseModel):
    session_number: SessionNumber
    tutor_mode: TutorMode
    problem_id: ProblemId
    motivation: int
    engagement: int
    perceived_support: int
    self_confidence: int
    enjoyment: int
    most_helpful: str
    least_helpful: str
    submitted_at: str


class ReflectionResponse(BaseModel):
    more_motivating_session: Optional[int] = None
    more_motivating_reason: str
    free_form_comments: str
    submitted_at: str


class SessionRecord(BaseModel):
    session_number: SessionNumber
    tutor_mode: TutorMode
    problem_id: ProblemId
    started_at: str
    ended_at: Optional[str] = None
    messages: list[ChatMessage] = []


class ParticipantRecord(BaseModel):
    id: str
    name: str
    created_at: str
    session_order: tuple[TutorMode, TutorMode]
    background_cs: str = ""
    background_math: str = ""
    sessions: list[Optional[SessionRecord]] = [None, None]
    surveys: list[SurveyResponse] = []
    reflection: Optional[ReflectionResponse] = None
    completed_at: Optional[str] = None


class CreateParticipantRequest(BaseModel):
    name: str
    background_cs: str = ""
    background_math: str = ""


class PatchParticipantRequest(BaseModel):
    action: Literal[
        "start_session",
        "end_session",
        "update_messages",
    ]
    session_number: Optional[SessionNumber] = None
    tutor_mode: Optional[TutorMode] = None
    problem_id: Optional[ProblemId] = None
    messages: Optional[list[ChatMessage]] = None


class ChatRequest(BaseModel):
    participant_id: str
    session_number: SessionNumber
    tutor_mode: TutorMode
    problem_id: ProblemId
    messages: list[ChatMessage]


class SubmitSurveyRequest(BaseModel):
    participant_id: str
    survey: SurveyResponse


class SubmitReflectionRequest(BaseModel):
    participant_id: str
    reflection: ReflectionResponse


class AdminLoginRequest(BaseModel):
    password: str
