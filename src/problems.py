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

<p><strong>Try this before you start:</strong> Grab a piece of paper (or just think it through) and try to trace what happens step-by-step when Python runs <code>fib(4)</code>. What functions get called, and in what order?</p>

<p><strong>Work through these with your tutor:</strong></p>
<ol>
  <li>What are the <em>base cases</em> (<code>n = 0</code> and <code>n = 1</code>) and why do they prevent infinite recursion?</li>
  <li>Trace <strong>every single call</strong> made by <code>fib(4)</code> — draw it out as a tree if it helps.</li>
  <li>Count how many times <code>fib(2)</code> is computed. Why is that wasteful?</li>
  <li>How would you fix it with <em>memoization</em>? Try writing a version yourself.</li>
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
                "The thing that finally made it click for me wasn't reading an explanation — "
                "it was actually tracing through `fib(4)` by hand, one call at a time, until "
                "I could see the whole tree. We're going to do that together.\n\n"
                "But first — **did you try tracing `fib(4)` before we started?** "
                "What did you get, or where did you get lost?"
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

PROBLEM_ORDER: list[str] = ["fibonacci", "bayes"]


def get_problem_for_session(session_number: int) -> dict:
    return PROBLEMS[PROBLEM_ORDER[session_number - 1]]
