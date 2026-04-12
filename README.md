# Proximo

**Identity-Based AI Tutors for Learning Motivation**

A research prototype for CS 598 (UIUC) investigating whether framing an AI tutor as a student's *future successful self* improves motivation and engagement compared to a standard AI tutor.

---

## Research Question

> How does framing an AI tutor as a student's future self affect students' motivation, engagement, and perceived learning support compared to a standard AI tutor?

---

## Study Design

Within-subjects experiment with ~8–15 college student participants. Each participant completes two tutoring sessions with counterbalanced tutor order:

| Session | Problem | Concept |
|---------|---------|---------|
| 1 | Recursive Fibonacci | Computer Science · Recursion |
| 2 | Bayes' Theorem (medical test) | Mathematics · Probability |

**Two tutor modes:**
- **Standard AI Tutor** — conventional tutor that explains concepts, asks guiding questions, and supports problem-solving
- **Future-Self AI Tutor** — framed as the student's own future self who has already mastered the subject, using phrases like *"I remember when this confused us too…"*

After each session, participants complete a 5-item Likert survey (motivation, engagement, perceived support, self-confidence, enjoyment) plus open-ended questions. A final comparative reflection asks which session felt more motivating and why.

---

## Stack

- **Backend:** Python · FastAPI · Uvicorn
- **AI:** Anthropic SDK (`claude-sonnet-4-6`) with streaming
- **Frontend:** Jinja2 templates · Tailwind CSS (CDN) · Vanilla JS
- **Storage:** JSON files per participant (`data/participants/`)

---

## Setup

**1. Clone and create a virtual environment**

```bash
git clone <repo-url>
cd proximo
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**2. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
ADMIN_PASSWORD=your-chosen-password
ADMIN_SECRET_SALT=random-32-char-string
```

Generate a salt with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**3. Run**

```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000).

---

## Study Flow

```
/ (welcome + consent)
  └─ /session/1  (tutoring chat — session 1)
       └─ /survey/1  (post-session survey)
            └─ /session/2  (tutoring chat — session 2)
                 └─ /survey/2  (post-session survey)
                      └─ /reflection  (comparative reflection)
                           └─ /done  (debrief + thank you)
```

Admin dashboard at `/admin` — password protected, shows all participant data, and provides a one-click CSV download for analysis.

---

## Project Structure

```
proximo/
├── main.py                  # FastAPI app + page routes
├── requirements.txt
├── .env.example
├── src/
│   ├── models.py            # Pydantic data models
│   ├── storage.py           # Per-participant JSON file I/O
│   ├── problems.py          # Problem definitions + initial greetings
│   ├── prompts.py           # System prompt builders (both tutor modes)
│   ├── counterbalance.py    # Balanced tutor order assignment
│   └── csv_export.py        # Flat CSV for data analysis
├── routers/
│   ├── participants.py      # POST/GET/PATCH /api/participants
│   ├── chat.py              # POST /api/chat  (streaming)
│   ├── survey.py            # POST /api/surveys
│   ├── reflection.py        # POST /api/reflections
│   └── admin.py             # Admin login, list, CSV export
├── templates/               # Jinja2 HTML templates
│   ├── index.html           # Welcome + consent
│   ├── session.html         # Streaming chat UI
│   ├── survey.html          # Post-session survey
│   ├── reflection.html      # Comparative reflection
│   ├── done.html            # Thank-you + debrief
│   ├── admin_login.html     # Admin login
│   └── dashboard.html       # Admin data view
└── data/participants/       # Participant JSON files (gitignored)
```

---

## CSV Export Schema

The exported CSV has two rows per participant (one per session):

| Column | Description |
|--------|-------------|
| `participant_id` | UUID |
| `session_number` | 1 or 2 |
| `tutor_mode` | `standard` or `future-self` |
| `problem_id` | `fibonacci` or `bayes` |
| `message_count` | Total messages in session |
| `motivation` … `enjoyment` | Likert scores (1–5) |
| `most_helpful` | Open-ended response |
| `least_helpful` | Open-ended response |
| `more_motivating_session` | Final reflection (1, 2, or null) |
| `more_motivating_reason` | Open-ended |
| `free_form_comments` | Open-ended |

---

## Author

Yu Sheng Aow — CS 598, University of Illinois Urbana-Champaign
