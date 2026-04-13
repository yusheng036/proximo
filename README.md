# Proximo

**Identity-Based AI Tutors for Learning Motivation**

A research prototype for CS 598 investigating whether framing an AI tutor as a student's *future successful self* improves motivation and engagement compared to a standard AI tutor.

---

## Research Question

How does framing an AI tutor as a student's future self affect students' motivation, engagement, and perceived learning support compared to a standard AI tutor?

---

## Study Design

Within-subjects experiment with ~8–15 college student participants. Each participant completes two tutoring sessions with counterbalanced tutor order:

| Session | Problem | Concept |
|---------|---------|---------|
| 1 | Recursive Fibonacci | Computer Science · Recursion |
| 2 | Bayes' Theorem | Mathematics · Probability |

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

## Running the App

**1. Activate the virtual environment**

```bash
source .venv/bin/activate
```

**2. Start the server**

```bash
uvicorn main:app --reload
```

**3. Open the app**

Go to [http://localhost:8000](http://localhost:8000).

---

## Study Flow

```
/ (welcome + consent + background questions)
  └─ /session/1  (tutoring chat — session 1)
       └─ /survey/1  (post-session survey)
            └─ /session/2  (tutoring chat — session 2)
                 └─ /survey/2  (post-session survey)
                      └─ /reflection  (comparative reflection)
                           └─ /done  (debrief + thank you)
```

Admin dashboard at `/admin` — password protected, shows all participant data, and provides a one-click CSV download for analysis.

---

## Features

### Participant Background Collection
On the welcome page, participants self-report their experience level in programming and math (Beginner / Some experience / Comfortable). The tutor adapts its language, pacing, and terminology accordingly:
- **Beginner** — simple language, more examples, slower pacing
- **Some experience** — tutor calibrates based on responses
- **Comfortable** — faster pacing, precise terminology, less scaffolding

### Structured Session Progress
Each session covers 4 questions in strict sequential order. The tutor never skips ahead — if a student is stuck after 1–2 attempts, the tutor gives the answer and moves on. A progress bar in the chat UI fills one segment per completed question, giving participants a clear sense of pacing and goal. The End Session button unlocks only after all 4 questions are covered.

### Counterbalanced Tutor Assignment
Tutor order alternates automatically across participants (even → Standard first, odd → Future-Self first) to control for order effects.

### Admin Dashboard
- Live table of all participants with session status, tutor order, and survey scores
- Click any row to expand survey results and reflection
- One-click CSV export for analysis

---

## Project Structure

```
proximo/
├── main.py
├── requirements.txt
├── .env.example
├── src/
│   ├── models.py
│   ├── storage.py
│   ├── problems.py
│   ├── prompts.py
│   ├── counterbalance.py
│   └── csv_export.py
├── routers/
│   ├── participants.py
│   ├── chat.py
│   ├── survey.py
│   ├── reflection.py
│   └── admin.py
├── templates/
│   ├── index.html
│   ├── session.html
│   ├── survey.html
│   ├── reflection.html
│   ├── done.html
│   ├── admin_login.html
│   └── dashboard.html
└── data/participants/
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

Yu Sheng Aow — CS 598, Boston University
