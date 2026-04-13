from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from src.models import ParticipantRecord

DATA_DIR = Path(__file__).parent.parent / "data" / "participants"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _participant_path(participant_id: str) -> Path:
    return DATA_DIR / f"{participant_id}.json"


def save_participant(record: ParticipantRecord) -> None:
    _ensure_data_dir()
    path = _participant_path(record.id)
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")


def get_participant(participant_id: str) -> Optional[ParticipantRecord]:
    path = _participant_path(participant_id)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return ParticipantRecord.model_validate(data)


def get_all_participants() -> list[ParticipantRecord]:
    _ensure_data_dir()
    records: list[ParticipantRecord] = []
    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            records.append(ParticipantRecord.model_validate(data))
        except Exception:
            pass  # skip corrupted files
    return records
