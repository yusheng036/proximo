"""Learning problem definitions for both study sessions.

Session 1: Recursive Fibonacci  (programming)
Session 2: Bayes' Theorem       (mathematics / probability)

Each problem carries:
  - display metadata (title, subject tag, description HTML)
  - initial_greetings per tutor mode (set the tone before the user types)
"""

from __future__ import annotations

MIN_USER_MESSAGES = 4

PROBLEMS: dict[str, dict] = {
    "weighted_intervals": {
        "id": "weighted_intervals",
        "title": "Weighted Interval Scheduling",
        "subject": "Computer Science · Dynamic Programming",
        "description": """
<p>You have <strong>5 jobs</strong>, each with a start time, finish time, and value.
Two jobs are <em>compatible</em> if they do not overlap.
Your goal: select a subset of mutually compatible jobs with <strong>maximum total value</strong>.</p>

<table style="border-collapse:collapse; font-size:0.9em; margin: 0.75rem 0;">
  <thead>
    <tr>
      <th style="border:1px solid #d1d5db; padding:6px 12px;">Job</th>
      <th style="border:1px solid #d1d5db; padding:6px 12px;">Start</th>
      <th style="border:1px solid #d1d5db; padding:6px 12px;">Finish</th>
      <th style="border:1px solid #d1d5db; padding:6px 12px;">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">1</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">1</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">3</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">2</td></tr>
    <tr><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">2</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">2</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">5</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">4</td></tr>
    <tr><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">3</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">3</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">7</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">4</td></tr>
    <tr><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">4</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">6</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">9</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">7</td></tr>
    <tr><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">5</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">5</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">10</td><td style="border:1px solid #d1d5db; padding:6px 12px; text-align:center;">3</td></tr>
  </tbody>
</table>

<p><strong>Think about this before you start:</strong> Could a simple greedy strategy — always pick the highest-value job, or the job that finishes earliest — reliably find the best answer?</p>

<p><strong>Work through these with your tutor:</strong></p>
<ol>
  <li>Why does every greedy strategy fail on some input?</li>
  <li>What is the right <em>subproblem</em>? Define <code>OPT(j)</code> and the helper <code>p(j)</code>.</li>
  <li>Derive the recurrence: for each job <em>j</em>, what are the only two choices, and which is better?</li>
  <li>Fill in the DP table from <code>OPT(0)</code> to <code>OPT(5)</code> and identify which jobs to select.</li>
</ol>
""",
        "initial_greetings": {
            "standard": (
                "Hi! I'm your AI tutor for this session. Today we're tackling "
                "**weighted interval scheduling** — a scheduling problem where greedy "
                "strategies break down and dynamic programming is the key.\n\n"
                "Before I explain anything: take a look at the five jobs in the table above. "
                "**What's your instinct for a strategy to maximise total value?** "
                "Don't worry about being right — just tell me what you'd try first."
            ),
            "future-self": (
                "Hey — it's me. Future you.\n\n"
                "This one is a scheduling problem, and I want to warn you upfront: "
                "every clean greedy idea you're about to think of is going to fail. "
                "I know because I thought of all of them too.\n\n"
                "The moment it clicked for me was when I stopped asking *\"which job should I pick next?\"* "
                "and started asking *\"what's the right subproblem?\"* — that's the whole game with DP.\n\n"
                "Take a look at the table above. "
                "**What strategy would you try first to maximise the total value?** "
                "Go with your gut — I want to see where your head is at."
            ),
        },
    },

    "bayes": {
        "id": "bayes",
        "title": "Bayes' Theorem",
        "subject": "Mathematics · Probability",
        "description": """
<p>A rare disease affects <strong>1% of the population</strong>.
A medical test for it has the following properties:</p>
<ul>
  <li>If you <strong>have</strong> the disease → test is positive <strong>99%</strong> of the time <em>(sensitivity)</em></li>
  <li>If you <strong>don't have</strong> the disease → test is positive <strong>1%</strong> of the time <em>(false positive rate)</em></li>
</ul>

<p>You take the test. <strong>The result is positive.</strong></p>
<p class="font-semibold">What is the probability you actually have the disease?</p>

<p><strong>Questions to explore with your tutor:</strong></p>
<ol>
  <li>Why is the answer <em>not</em> simply 99%?</li>
  <li>How do you set up Bayes' theorem for this problem?</li>
  <li>Can you calculate it using a "natural frequency" approach (imagine 10,000 people)?</li>
  <li>What does this tell us about testing for rare conditions?</li>
</ol>
""",
        "initial_greetings": {
            "standard": (
                "Welcome back! For this session we're shifting to probability — "
                "specifically **Bayes' theorem**, which has a famously counterintuitive "
                "result in the medical testing scenario above.\n\n"
                "Before we dig in: **what's your gut-feeling answer?** "
                "If a test is 99% accurate and it comes back positive, roughly what "
                "probability would you guess that you actually have the disease?"
            ),
            "future-self": (
                "Hey, it's me again — your future self.\n\n"
                "This one is about probability, and I want to be upfront: "
                "the answer is probably not what you'd expect. I got it wrong the first time too, "
                "and it genuinely surprised me when I worked out why.\n\n"
                "Take a moment to read through the scenario above.\n\n"
                "**What probability comes to mind when you first read it?** "
                "Just go with your gut — no wrong answers at this stage."
            ),
        },
    },
}

PROBLEM_ORDER: list[str] = ["weighted_intervals", "bayes"]


def get_problem_for_session(session_number: int) -> dict:
    return PROBLEMS[PROBLEM_ORDER[session_number - 1]]
