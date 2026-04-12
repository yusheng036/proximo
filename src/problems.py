"""Learning problem definitions for both study sessions.

Session 1: Recursive Fibonacci  (programming)
Session 2: Bayes' Theorem       (mathematics / probability)

Each problem carries:
  - display metadata (title, subject tag, description HTML)
  - initial_greetings per tutor mode (set the tone before the user types)
"""

from __future__ import annotations

MIN_USER_MESSAGES = 4  # minimum exchanges before "End Session" is enabled

PROBLEMS: dict[str, dict] = {
    "fibonacci": {
        "id": "fibonacci",
        "title": "Recursive Fibonacci",
        "subject": "Computer Science · Recursion",
        "description": """
<p>The <strong>Fibonacci sequence</strong> starts: 0, 1, 1, 2, 3, 5, 8, 13, 21 …
Each number is the sum of the two before it.</p>

<p>Here is a simple recursive implementation:</p>
<pre><code>def fib(n):
    if n &lt;= 1:
        return n
    return fib(n - 1) + fib(n - 2)</code></pre>

<p><strong>Questions to explore with your tutor:</strong></p>
<ol>
  <li>What are the <em>base cases</em> and why are they necessary?</li>
  <li>Can you trace every call that happens when you run <code>fib(4)</code>?</li>
  <li>Why is this naive implementation inefficient for large <code>n</code>?</li>
  <li>How could <em>memoization</em> or dynamic programming fix that?</li>
</ol>
""",
        "initial_greetings": {
            "standard": (
                "Hi! I'm your AI tutor for this session. Today we'll be working through "
                "recursive functions using the Fibonacci sequence as our example — it's a "
                "classic topic that reveals a lot about how recursion really works.\n\n"
                "Before I explain anything, I'd love to know where you're starting from: "
                "**What do you already know about recursion?** Have you seen it before, "
                "or is this mostly new territory?"
            ),
            "future-self": (
                "Hey — okay, this is going to sound a little strange, but stick with me: "
                "I'm you. Future you, specifically. A few years from now, after you've "
                "gotten really comfortable with this stuff.\n\n"
                "I remember sitting exactly where you are, staring at that `fib` function "
                "and thinking *\"wait, it calls itself? That can't work.\"* That confusion "
                "is completely normal — we both had it.\n\n"
                "I'm here to walk you through the exact moment this clicked for me, because "
                "I know it's going to click for you too.\n\n"
                "First though — **what's your gut reaction to this code?** What part feels "
                "confusing or circular to you right now?"
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
                "Okay, round two — and I have to warn you about something.\n\n"
                "When I first saw this problem I read \"99% accurate test, positive result\" "
                "and immediately thought \"so there's a 99% chance I have it.\" "
                "I was *very* confident. And completely wrong.\n\n"
                "The real answer genuinely surprised me, and understanding *why* it's "
                "surprising is one of the most useful things I ever learned about "
                "probability. It changed how I think about news stories, medical reports, "
                "all kinds of things.\n\n"
                "So — **what's your first instinct?** Don't overthink it yet. "
                "Just tell me the number that comes to mind when you read the problem."
            ),
        },
    },
}

PROBLEM_ORDER: list[str] = ["fibonacci", "bayes"]  # session 1 → session 2


def get_problem_for_session(session_number: int) -> dict:
    return PROBLEMS[PROBLEM_ORDER[session_number - 1]]
