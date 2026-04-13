from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import TutorMode

COUNTER_FILE = Path(__file__).parent.parent / "data" / "counter.json"


def get_next_tutor_order() -> tuple["TutorMode", "TutorMode"]:
    COUNTER_FILE.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    if COUNTER_FILE.exists():
        try:
            count = json.loads(COUNTER_FILE.read_text())["count"]
        except Exception:
            count = 0

    COUNTER_FILE.write_text(json.dumps({"count": count + 1}))

    if count % 2 == 0:
        return ("standard", "future-self")
    else:
        return ("future-self", "standard")
