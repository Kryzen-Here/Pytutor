#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║           PyTutor Pro - Interactive Python Learning System       ║
║                  Your Personal Python Tutor                      ║
║                                                                  ║
║  Topics: Variables, Print, Types, Input, Strings, Arithmetic,   ║
║          Operators, If/While/For, Lists, Tuples, Range           ║
╚══════════════════════════════════════════════════════════════════╝

Author     : PyTutor Pro
Version    : 3.0
Python     : 3.7+
Libraries  : time, sys, os, random, textwrap (all built-in)

Install colorama for colors: pip install colorama
(Script works without it too!)
"""

import time
import sys
import os
import random
import textwrap
from typing import Optional

# ──────────────────────────────────────────────────────────────────
# COLOR / STYLE SYSTEM  (graceful fallback if colorama missing)
# ──────────────────────────────────────────────────────────────────
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Create dummy classes so the rest of the code never throws
    class _Dummy:
        def __getattr__(self, _): return ""
    Fore = Back = Style = _Dummy()

# Semantic color aliases
C_TITLE   = Fore.CYAN    + Style.BRIGHT
C_HEADER  = Fore.BLUE    + Style.BRIGHT
C_SUCCESS = Fore.GREEN   + Style.BRIGHT
C_ERROR   = Fore.RED     + Style.BRIGHT
C_WARN    = Fore.YELLOW  + Style.BRIGHT
C_INFO    = Fore.WHITE   + Style.BRIGHT
C_CODE    = Fore.MAGENTA + Style.BRIGHT
C_PROMPT  = Fore.CYAN
C_RESET   = Style.RESET_ALL
C_DIM     = Style.DIM
C_BOLD    = Style.BRIGHT


# ──────────────────────────────────────────────────────────────────
# PROGRESS TRACKER
# ──────────────────────────────────────────────────────────────────
class ProgressTracker:
    """Tracks score, streaks, and topic completion across the session."""

    ALL_TOPICS = [
        "Variables", "Print Function", "Type Conversion",
        "User Input", "Strings", "Arithmetic Operations",
        "Operator Precedence", "Comparison Operators",
        "Logical Operators", "If Statements", "While Loops",
        "Lists", "List Methods", "For Loops",
        "Range Function", "Tuples"
    ]

    def __init__(self):
        self.total_questions  = 0
        self.correct_answers  = 0
        self.current_streak   = 0
        self.best_streak      = 0
        self.completed_topics = []
        self.topic_scores     = {}   # topic → (correct, total)
        self.start_time       = time.time()

    # ── score helpers ──────────────────────────────────────────────
    def record_answer(self, topic: str, correct: bool):
        self.total_questions += 1
        c, t = self.topic_scores.get(topic, (0, 0))
        t += 1
        if correct:
            self.correct_answers += 1
            self.current_streak  += 1
            self.best_streak = max(self.best_streak, self.current_streak)
            c += 1
        else:
            self.current_streak = 0
        self.topic_scores[topic] = (c, t)

    def complete_topic(self, topic: str):
        if topic not in self.completed_topics:
            self.completed_topics.append(topic)

    def accuracy(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100

    def topic_accuracy(self, topic: str) -> float:
        c, t = self.topic_scores.get(topic, (0, 0))
        return (c / t * 100) if t > 0 else 0.0

    def elapsed_minutes(self) -> float:
        return (time.time() - self.start_time) / 60

    # ── display ───────────────────────────────────────────────────
    def show_dashboard(self):
        print_header("📊 LEARNING DASHBOARD")
        elapsed = self.elapsed_minutes()

        rows = [
            ("⏱  Time Studied",       f"{elapsed:.1f} minutes"),
            ("❓  Questions Answered", str(self.total_questions)),
            ("✅  Correct",            str(self.correct_answers)),
            ("🎯  Accuracy",           f"{self.accuracy():.1f}%"),
            ("🔥  Current Streak",     str(self.current_streak)),
            ("⭐  Best Streak",        str(self.best_streak)),
            ("📚  Topics Completed",   f"{len(self.completed_topics)}/{len(self.ALL_TOPICS)}"),
        ]
        for label, value in rows:
            print(f"  {C_INFO}{label:<24}{C_RESET}: {C_SUCCESS}{value}{C_RESET}")

        # progress bar
        pct = len(self.completed_topics) / len(self.ALL_TOPICS)
        bar = progress_bar(pct, width=40, label="Course Progress")
        print(f"\n  {bar}\n")

        # per-topic breakdown
        if self.topic_scores:
            print(f"  {C_HEADER}── Topic Breakdown ──{C_RESET}")
            for topic, (c, t) in self.topic_scores.items():
                acc = (c / t * 100) if t else 0
                star = "⭐" if acc >= 80 else ("✅" if acc >= 60 else "📖")
                print(f"  {star} {topic:<30} {c}/{t} ({acc:.0f}%)")

        print()


# ──────────────────────────────────────────────────────────────────
# DISPLAY / UI HELPERS
# ──────────────────────────────────────────────────────────────────
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text: str, delay: float = 0.025, color: str = ""):
    """Print text character by character for a typing effect."""
    for ch in text:
        sys.stdout.write(color + ch + C_RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_divider(char: str = "─", width: int = 65, color: str = ""):
    print(f"{color}{char * width}{C_RESET}")

def print_header(title: str, width: int = 65):
    print()
    print_divider("═", width, C_TITLE)
    pad = (width - len(title) - 2) // 2
    print(f"{C_TITLE}{'═' * pad} {title} {'═' * (width - pad - len(title) - 2)}═{C_RESET}")
    print_divider("═", width, C_TITLE)
    print()

def print_section(title: str):
    print()
    print_divider("─", 65, C_HEADER)
    print(f"  {C_HEADER}{title}{C_RESET}")
    print_divider("─", 65, C_HEADER)
    print()

def print_box(lines: list, border_color: str = ""):
    width = max(len(l) for l in lines) + 4
    bc = border_color or C_INFO
    print(f"{bc}┌{'─' * width}┐{C_RESET}")
    for line in lines:
        pad = width - len(line) - 2
        print(f"{bc}│{C_RESET} {line}{' ' * pad} {bc}│{C_RESET}")
    print(f"{bc}└{'─' * width}┘{C_RESET}")
    print()

def code_block(code: str, title: str = "Example"):
    lines = code.strip().split("\n")
    width = max(len(l) for l in lines) + 6
    print(f"\n  {C_CODE}╔{'═' * width}╗{C_RESET}")
    print(f"  {C_CODE}║  📝 {title:<{width-5}}║{C_RESET}")
    print(f"  {C_CODE}╠{'═' * width}╣{C_RESET}")
    for line in lines:
        pad = width - len(line) - 2
        print(f"  {C_CODE}║{C_RESET}  {Fore.WHITE}{line}{' ' * pad}{C_CODE}║{C_RESET}")
    print(f"  {C_CODE}╚{'═' * width}╝{C_RESET}\n")

def progress_bar(fraction: float, width: int = 40, label: str = "") -> str:
    filled = int(fraction * width)
    bar    = "█" * filled + "░" * (width - filled)
    pct    = fraction * 100
    color  = C_SUCCESS if pct >= 70 else (C_WARN if pct >= 40 else C_ERROR)
    return f"{color}[{bar}] {pct:.1f}%  {label}{C_RESET}"

def animate_loading(message: str = "Loading", duration: float = 1.2):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {C_WARN}{frames[i % len(frames)]}  {message}...{C_RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()

def celebrate(msg: str = "Excellent!"):
    animations = ["🎉", "⭐", "🏆", "🚀", "💡", "🌟", "✨", "🎯"]
    e = random.choice(animations)
    print(f"\n  {C_SUCCESS}{e}  {msg}  {e}{C_RESET}\n")

def error_msg(msg: str):
    print(f"\n  {C_ERROR}✗  {msg}{C_RESET}\n")

def info_msg(msg: str):
    print(f"  {C_INFO}ℹ  {msg}{C_RESET}")

def explain(text: str):
    """Word-wrap and pretty-print an explanation paragraph."""
    wrapped = textwrap.fill(text.strip(), width=63)
    for line in wrapped.split("\n"):
        print(f"  {C_DIM}{line}{C_RESET}")
    print()


# ──────────────────────────────────────────────────────────────────
# INPUT / QUIZ HELPERS
# ──────────────────────────────────────────────────────────────────
def get_input(prompt: str, color: str = "") -> str:
    c = color or C_PROMPT
    try:
        return input(f"  {c}{prompt}{C_RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  [Session interrupted. Goodbye!]")
        sys.exit(0)

def get_choice(options: list, prompt: str = "Your choice") -> str:
    """Display a numbered menu and return the chosen option string."""
    for i, opt in enumerate(options, 1):
        print(f"    {C_WARN}{i}.{C_RESET} {opt}")
    while True:
        raw = get_input(f"{prompt} (1-{len(options)}): ")
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        error_msg(f"Please enter a number between 1 and {len(options)}.")

def pause(msg: str = "Press Enter to continue..."):
    get_input(f"\n  {C_DIM}{msg}{C_RESET}", color=C_DIM)

def yes_no(question: str) -> bool:
    ans = get_input(f"{question} (y/n): ").lower()
    return ans in ("y", "yes")


# ──────────────────────────────────────────────────────────────────
# QUIZ ENGINE
# ──────────────────────────────────────────────────────────────────
def run_quiz(tracker: ProgressTracker, topic: str,
             questions: list, passes_needed: int = 3) -> bool:
    """
    Generic quiz runner.

    Each question dict has:
        q      : question text
        a      : correct answer (str, compared case-insensitively)
        hint   : shown after 1 wrong attempt
        explain: full explanation shown after answer
        choices: optional list → displayed as MCQ
    Returns True if learner passed (>= passes_needed correct).
    """
    print_section(f"🧠 Quiz — {topic}")
    score    = 0
    pool     = questions[:]
    random.shuffle(pool)
    asked    = pool[:min(len(pool), max(passes_needed + 1, 4))]

    for idx, q_data in enumerate(asked, 1):
        print(f"  {C_BOLD}Q{idx}:{C_RESET} {q_data['q']}\n")

        is_mcq   = "choices" in q_data
        attempts = 0
        hint_shown = False

        if is_mcq:
            choices = q_data["choices"][:]
            random.shuffle(choices)
            for ci, ch in enumerate(choices, 1):
                print(f"    {C_WARN}{ci}.{C_RESET} {ch}")
            correct_choice = q_data["a"]

        while True:
            if is_mcq:
                raw = get_input("Your answer (number): ")
                if raw.isdigit() and 1 <= int(raw) <= len(choices):
                    user_ans = choices[int(raw) - 1]
                else:
                    error_msg("Enter a valid option number.")
                    continue
            else:
                user_ans = get_input("Your answer: ")

            attempts += 1
            correct_ans = q_data["a"]
            is_correct  = user_ans.strip().lower() == correct_ans.strip().lower()

            if is_correct:
                celebrate("Correct!" if attempts == 1 else "Got it after the hint!")
                if "explain" in q_data:
                    print(f"  {C_INFO}💡 {q_data['explain']}{C_RESET}\n")
                tracker.record_answer(topic, True)
                score += 1
                break
            else:
                tracker.record_answer(topic, False)
                if not hint_shown and "hint" in q_data:
                    print(f"  {C_WARN}💭 Hint: {q_data['hint']}{C_RESET}\n")
                    hint_shown = True
                elif attempts >= 2:
                    print(f"  {C_ERROR}✗ The correct answer is: {C_SUCCESS}{correct_ans}{C_RESET}")
                    if "explain" in q_data:
                        print(f"  {C_INFO}💡 {q_data['explain']}{C_RESET}\n")
                    break
                else:
                    error_msg("Not quite. Try again!")

        time.sleep(0.5)

    # result
    pct = score / len(asked) * 100
    print_divider()
    print(f"\n  {C_BOLD}Quiz Score: {score}/{len(asked)}  ({pct:.0f}%){C_RESET}")
    bar = progress_bar(score / len(asked), width=35, label=topic)
    print(f"  {bar}\n")

    passed = score >= passes_needed
    if passed:
        print(f"  {C_SUCCESS}🏆  You passed the {topic} quiz!{C_RESET}\n")
    else:
        print(f"  {C_WARN}📖  Review the material and try again — you've got this!{C_RESET}\n")
    return passed


def run_coding_exercise(tracker: ProgressTracker, topic: str,
                        exercises: list) -> None:
    """
    Interactive fill-in-the-blank / short-answer coding exercises.
    """
    print_section(f"💻 Coding Exercises — {topic}")
    for i, ex in enumerate(exercises, 1):
        print(f"  {C_BOLD}Exercise {i}:{C_RESET} {ex['task']}\n")
        if "code_template" in ex:
            code_block(ex["code_template"], "Fill in the blank")

        attempts = 0
        while attempts < 3:
            ans = get_input("Your answer: ")
            attempts += 1
            if any(ans.strip().lower() == a.lower() for a in ex["answers"]):
                celebrate("Perfect!")
                tracker.record_answer(topic, True)
                if "solution" in ex:
                    code_block(ex["solution"], "✅ Solution")
                if "note" in ex:
                    info_msg(ex["note"])
                break
            else:
                tracker.record_answer(topic, False)
                if attempts < 3:
                    if "hint" in ex:
                        print(f"  {C_WARN}💭 Hint: {ex['hint']}{C_RESET}\n")
                    error_msg("Not quite — try again!")
                else:
                    print(f"  {C_ERROR}Answer: {C_SUCCESS}{ex['answers'][0]}{C_RESET}")
                    if "solution" in ex:
                        code_block(ex["solution"], "✅ Solution")
                    if "note" in ex:
                        info_msg(ex["note"])
        time.sleep(0.4)


# ══════════════════════════════════════════════════════════════════
#  CHAPTER DEFINITIONS
#  Each chapter = teach() + quiz_questions + exercises
# ══════════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────────────────
# CHAPTER 1 — VARIABLES
# ──────────────────────────────────────────────────────────────────
def chapter_variables(tracker: ProgressTracker):
    clear_screen()
    print_header("📦 CHAPTER 1 — Variables")
    animate_loading("Preparing Chapter 1")

    # ── Teach ──────────────────────────────────────────────────────
    slow_print("  Welcome to your first Python concept: Variables! 🎉", 0.02, C_INFO)
    print()
    explain(
        "A variable is like a labelled box where you store information. "
        "You give the box a name (the label) and put a value inside it. "
        "Later, you can look at the box, change its contents, or use its "
        "value in your program."
    )

    code_block("""
# Creating variables (assignment)
name    = "Alice"        # stores text (a string)
age     = 14             # stores a whole number (integer)
height  = 5.4            # stores a decimal (float)
is_cool = True           # stores True/False (boolean)

# Using variables
print(name)              # Output: Alice
print(age)               # Output: 14
print(age + 1)           # Output: 15  (use in expressions!)
""", "Variables in Action")

    explain(
        "Rules for variable names: "
        "(1) Start with a letter or underscore (_). "
        "(2) Can contain letters, numbers, underscores. "
        "(3) CANNOT start with a number. "
        "(4) CANNOT be a Python keyword (like 'if', 'for', 'print'). "
        "(5) Python is case-sensitive: 'Name' ≠ 'name'."
    )

    print_box([
        "✅  Valid names : my_name, _count, score1, firstName",
        "❌  Invalid     : 1score, my-name, for, class",
        "📌  Convention  : use snake_case (words separated by _)",
    ], C_SUCCESS)

    explain(
        "You can also assign multiple variables at once, "
        "or assign the same value to several variables:"
    )
    code_block("""
# Multiple assignment
x, y, z = 1, 2, 3
print(x, y, z)          # Output: 1 2 3

# Same value
a = b = c = 0
print(a, b, c)          # Output: 0 0 0

# Swap two variables (Python magic!)
a, b = 10, 20
a, b = b, a
print(a, b)             # Output: 20 10
""", "Advanced Assignment")

    pause()

    # ── Interactive demo ──────────────────────────────────────────
    print_section("🎮 Interactive Demo — Variables")
    slow_print("  Let's create YOUR own variables!", 0.03, C_INFO)
    print()
    your_name = get_input("Enter your name: ")
    your_age  = get_input("Enter your age : ")
    print()
    animate_loading("Creating variables")
    print(f"  {C_CODE}name = \"{your_name}\"{C_RESET}")
    print(f"  {C_CODE}age  = {your_age}{C_RESET}")
    print()
    print(f"  Hello, {C_SUCCESS}{your_name}{C_RESET}! "
          f"In 10 years you'll be {C_SUCCESS}{_safe_add(your_age, 10)}{C_RESET}.")
    pause()

    # ── Quiz ──────────────────────────────────────────────────────
    questions = [
        {
            "q": "Which of the following is a VALID variable name?",
            "choices": ["2score", "my-name", "first_name", "for"],
            "a": "first_name",
            "hint": "Variable names can use letters, numbers, and underscores — but cannot START with a digit or be a keyword.",
            "explain": "'first_name' follows all rules: starts with a letter and uses only letters and underscores."
        },
        {
            "q": "What is stored in the variable  x  after:  x = 7  ?",
            "choices": ["'7'", "7", "True", "None"],
            "a": "7",
            "hint": "The = sign assigns the VALUE on the right to the variable on the left.",
            "explain": "x = 7 stores the integer 7 inside x."
        },
        {
            "q": "After  a, b = b, a  with a=5, b=10 — what is a?",
            "choices": ["5", "10", "15", "Error"],
            "a": "10",
            "hint": "Python swaps both values simultaneously.",
            "explain": "Tuple unpacking swaps a and b, so a becomes 10 and b becomes 5."
        },
        {
            "q": "What keyword is used to create a variable in Python?",
            "choices": ["var", "let", "No keyword needed", "define"],
            "a": "No keyword needed",
            "hint": "Unlike JavaScript or C++, Python doesn't need a declaration keyword.",
            "explain": "In Python you simply write  name = value  — no keyword required."
        },
        {
            "q": "Python variable names are case-sensitive. True or False?",
            "choices": ["True", "False"],
            "a": "True",
            "hint": "'Name' and 'name' would be treated as different variables.",
            "explain": "Python distinguishes uppercase and lowercase, so Score ≠ score ≠ SCORE."
        },
    ]
    run_quiz(tracker, "Variables", questions, passes_needed=3)

    exercises = [
        {
            "task": "What is the output of:  x = 5; x = x + 3; print(x)",
            "answers": ["8"],
            "hint": "Start with x=5, then add 3 to it.",
            "note": "Variables can be reassigned. x = x + 3 means 'take the current value of x, add 3, store the result back in x'.",
            "solution": "x = 5\nx = x + 3\nprint(x)   # Output: 8"
        },
        {
            "task": "Write just the variable name that follows Python naming convention for storing a person's last name.",
            "answers": ["last_name", "lastName"],
            "hint": "Python convention uses snake_case (words separated by underscores).",
            "note": "last_name is the Pythonic (snake_case) style. lastName (camelCase) works but is less idiomatic.",
            "solution": "last_name = 'Smith'   # snake_case is preferred in Python"
        },
    ]
    run_coding_exercise(tracker, "Variables", exercises)
    tracker.complete_topic("Variables")
    pause("Chapter 1 complete! Press Enter for Chapter 2...")


def _safe_add(age_str: str, n: int) -> str:
    try:
        return str(int(age_str) + n)
    except ValueError:
        return f"{age_str} + {n}"


# ──────────────────────────────────────────────────────────────────
# CHAPTER 2 — PRINT FUNCTION
# ──────────────────────────────────────────────────────────────────
def chapter_print(tracker: ProgressTracker):
    clear_screen()
    print_header("🖨  CHAPTER 2 — The print() Function")
    animate_loading("Preparing Chapter 2")

    slow_print("  print() is Python's megaphone — it shouts things to the screen!", 0.025, C_INFO)
    print()
    explain(
        "The print() function displays output in the terminal. "
        "You can print strings, numbers, variables, and even "
        "complex expressions — all with one line of code!"
    )

    code_block("""
# Basic printing
print("Hello, World!")           # Output: Hello, World!
print(42)                        # Output: 42
print(3.14)                      # Output: 3.14
print(True)                      # Output: True

# Multiple values (separated by space by default)
print("Age:", 25)                # Output: Age: 25
print("x =", 10, "y =", 20)     # Output: x = 10 y = 20

# Custom separator
print("a", "b", "c", sep="-")   # Output: a-b-c
print("a", "b", "c", sep="")    # Output: abc

# Custom end character (default is newline)
print("Hello", end=" ")
print("World!")                  # Output: Hello World!  (same line)
""", "print() Examples")

    explain(
        "print() can also format output neatly using f-strings (formatted strings). "
        "An f-string starts with the letter f before the quote marks. "
        "Variables and expressions inside curly braces {} are automatically substituted."
    )

    code_block("""
name = "Bob"
score = 95

# f-string formatting
print(f"Hello, {name}!")                  # Hello, Bob!
print(f"Your score is {score}/100")       # Your score is 95/100
print(f"Double: {score * 2}")             # Double: 190
print(f"Pi ≈ {3.14159:.2f}")             # Pi ≈ 3.14  (2 decimal places)
""", "f-Strings")

    pause()

    # ── Interactive demo ──────────────────────────────────────────
    print_section("🎮 Interactive Demo — print()")
    user_word = get_input("Enter any word: ")
    user_num  = get_input("Enter a number: ")
    print()
    try:
        n = float(user_num)
        print(f"  {C_CODE}print('{user_word}', {user_num}){C_RESET}")
        print(f"  ➜  {C_SUCCESS}{user_word} {user_num}{C_RESET}")
        print()
        print(f"  {C_CODE}print(f\"The word is {{word}} and number × 2 = {{{n*2}}}\"){C_RESET}")
        print(f"  ➜  {C_SUCCESS}The word is {user_word} and number × 2 = {n*2}{C_RESET}")
    except ValueError:
        print(f"  ➜  {C_SUCCESS}{user_word} {user_num}{C_RESET}")
    pause()

    questions = [
        {
            "q": "What does  print(\"Hi\", \"there\", sep=\"!\")  output?",
            "choices": ["Hi there", "Hi!there", "Hi! there", "HiThere"],
            "a": "Hi!there",
            "hint": "sep= sets the separator placed BETWEEN each item.",
            "explain": "sep='!' puts an exclamation mark between 'Hi' and 'there', giving Hi!there."
        },
        {
            "q": "Which parameter controls what is printed AFTER the output?",
            "choices": ["sep", "end", "after", "tail"],
            "a": "end",
            "hint": "By default, print() moves to a new line at the end.",
            "explain": "end= controls the terminator. Default is '\\n' (newline). Change it to '' to stay on the same line."
        },
        {
            "q": "What is the output of: print(f\"{2 + 3} is five\")?",
            "choices": ["2 + 3 is five", "5 is five", "{2 + 3} is five", "Error"],
            "a": "5 is five",
            "hint": "Inside f-strings, {} evaluates the Python expression inside.",
            "explain": "2 + 3 is evaluated to 5 inside the f-string, producing '5 is five'."
        },
        {
            "q": "How do you print a blank line in Python?",
            "choices": ["print()", "print(' ')", "print(None)", "All of the above"],
            "a": "print()",
            "hint": "Calling print with no arguments prints just the newline character.",
            "explain": "print() with no arguments prints only the default end character (\\n), creating a blank line."
        },
    ]
    run_quiz(tracker, "Print Function", questions, passes_needed=3)

    exercises = [
        {
            "task": "What does print('A', 'B', 'C', sep='*') output?",
            "answers": ["A*B*C"],
            "hint": "sep goes BETWEEN items.",
            "solution": "print('A', 'B', 'C', sep='*')   # Output: A*B*C"
        },
    ]
    run_coding_exercise(tracker, "Print Function", exercises)
    tracker.complete_topic("Print Function")
    pause("Chapter 2 complete! Press Enter for Chapter 3...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 3 — TYPE CONVERSION
# ──────────────────────────────────────────────────────────────────
def chapter_type_conversion(tracker: ProgressTracker):
    clear_screen()
    print_header("🔄 CHAPTER 3 — Type Conversion")
    animate_loading("Preparing Chapter 3")

    slow_print("  Python data has types — and we can convert between them!", 0.025, C_INFO)
    print()
    explain(
        "Every value in Python has a data type. The main built-in types are: "
        "int (whole numbers), float (decimals), str (text), and bool (True/False). "
        "Type conversion lets you change a value from one type to another — "
        "essential when working with user input or different data sources."
    )

    code_block("""
# Checking types
print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
print(type("hello"))   # <class 'str'>
print(type(True))      # <class 'bool'>

# Explicit conversion (casting)
x = int("42")          # str  → int    :  42
y = float("3.14")      # str  → float  :  3.14
z = str(100)           # int  → str    : '100'
b = bool(0)            # int  → bool   :  False
b2 = bool(1)           # int  → bool   :  True
n = int(True)          # bool → int    :  1

# Implicit conversion (Python handles automatically)
result = 3 + 1.0       # int + float → float : 4.0
""", "Type Conversion")

    print_box([
        "int()   → whole number  (int('42') = 42)",
        "float() → decimal       (float('3.14') = 3.14)",
        "str()   → text          (str(100) = '100')",
        "bool()  → True/False    (bool(0) = False)",
        "",
        "Truthy: any non-zero number, non-empty string",
        "Falsy : 0, 0.0, '', None, [], {}",
    ], C_INFO)

    explain(
        "A common use: input() always returns a STRING. "
        "If you want the user to type a number and do math with it, "
        "you MUST convert it first using int() or float()."
    )

    code_block("""
age_str = input("Enter age: ")   # always returns str!
age     = int(age_str)           # convert to int
print(f"In 5 years: {age + 5}") # now math works

# Or, in one line:
age = int(input("Enter age: "))
""", "Handling User Input Types")

    pause()

    questions = [
        {
            "q": "What is the output of: print(type(int('42')))?",
            "choices": ["<class 'str'>", "<class 'int'>", "<class 'float'>", "42"],
            "a": "<class 'int'>",
            "hint": "int() converts '42' (a string) to the integer 42.",
            "explain": "int('42') produces the integer 42, and type(42) is <class 'int'>."
        },
        {
            "q": "What does bool(0) evaluate to?",
            "choices": ["True", "False", "0", "None"],
            "a": "False",
            "hint": "Zero is falsy in Python.",
            "explain": "Any zero value (0, 0.0, '') converts to False. Any non-zero converts to True."
        },
        {
            "q": "What happens when you run: int('hello')?",
            "choices": ["Returns 0", "Returns None", "Raises a ValueError", "Returns 'hello'"],
            "a": "Raises a ValueError",
            "hint": "'hello' cannot be parsed as a number.",
            "explain": "int() raises ValueError if the string doesn't represent a valid integer."
        },
        {
            "q": "What is the result of: 3 + 1.0 in Python?",
            "choices": ["4", "4.0", "Error", "'3 + 1.0'"],
            "a": "4.0",
            "hint": "When int and float are combined, Python automatically widens to float.",
            "explain": "Python implicitly converts 3 (int) to 3.0 so the result is 4.0 (float)."
        },
        {
            "q": "Which function converts a number to a string?",
            "choices": ["int()", "float()", "str()", "bool()"],
            "a": "str()",
            "hint": "str() is the string constructor.",
            "explain": "str(42) returns '42', converting the integer to its text representation."
        },
    ]
    run_quiz(tracker, "Type Conversion", questions, passes_needed=3)

    exercises = [
        {
            "task": "What is the output of: print(int(3.9))?",
            "answers": ["3"],
            "hint": "int() truncates (chops off) the decimal — it does NOT round.",
            "solution": "print(int(3.9))   # Output: 3  (truncation, not rounding)"
        },
        {
            "task": "What conversion function turns the string '25' into the integer 25?",
            "answers": ["int()", "int"],
            "hint": "Look at the integer constructor.",
            "solution": "age = int('25')   # '25' (str) → 25 (int)"
        },
    ]
    run_coding_exercise(tracker, "Type Conversion", exercises)
    tracker.complete_topic("Type Conversion")
    pause("Chapter 3 complete! Press Enter for Chapter 4...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 4 — USER INPUT
# ──────────────────────────────────────────────────────────────────
def chapter_user_input(tracker: ProgressTracker):
    clear_screen()
    print_header("⌨️  CHAPTER 4 — Receiving User Input")
    animate_loading("Preparing Chapter 4")

    slow_print("  Make your programs talk back to the user with input()!", 0.025, C_INFO)
    print()
    explain(
        "The input() function pauses your program and waits for the user to type "
        "something and press Enter. Whatever the user types is returned as a string. "
        "You can display a prompt by passing text inside the parentheses."
    )

    code_block("""
# Basic input
name = input("What is your name? ")
print(f"Hello, {name}!")

# Input with type conversion
age    = int(input("How old are you? "))
height = float(input("Your height in meters? "))

print(f"In 10 years you'll be {age + 10}")
print(f"Height in cm: {height * 100:.1f} cm")
""", "input() Examples")

    explain(
        "Always validate user input! Users might type letters when you expect "
        "numbers. Wrap conversions in try/except to handle errors gracefully."
    )

    code_block("""
# Safe integer input
def get_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer!")

age = get_number("Enter your age: ")
print(f"Age: {age}")
""", "Safe Input Validation")

    pause()

    # Interactive practice
    print_section("🎮 Practice — Your Own Input")
    slow_print("  Let's build a tiny calculator together!", 0.025, C_INFO)
    print()
    a = _safe_float_input("Enter first number : ")
    b = _safe_float_input("Enter second number: ")
    print()
    animate_loading("Calculating")
    print(f"  {C_SUCCESS}{a} + {b} = {a + b}{C_RESET}")
    print(f"  {C_SUCCESS}{a} - {b} = {a - b}{C_RESET}")
    print(f"  {C_SUCCESS}{a} × {b} = {a * b}{C_RESET}")
    if b != 0:
        print(f"  {C_SUCCESS}{a} ÷ {b} = {a / b:.4f}{C_RESET}")
    pause()

    questions = [
        {
            "q": "What type does input() always return?",
            "choices": ["int", "float", "str", "bool"],
            "a": "str",
            "hint": "Even if the user types '42', it comes back as text.",
            "explain": "input() always returns a string. You must convert it if you need a number."
        },
        {
            "q": "How do you get an integer from the user in one line?",
            "choices": [
                "input(int('Enter: '))",
                "int(input('Enter: '))",
                "input('Enter: ', int)",
                "integer(input('Enter: '))"
            ],
            "a": "int(input('Enter: '))",
            "hint": "Wrap input() inside int().",
            "explain": "int(input('prompt')) first calls input() to get a string, then int() converts it."
        },
        {
            "q": "What does input() do when it is called?",
            "choices": [
                "Reads from a file",
                "Pauses and waits for user to type something",
                "Generates random input",
                "Reads environment variables"
            ],
            "a": "Pauses and waits for user to type something",
            "hint": "The program cannot proceed until the user presses Enter.",
            "explain": "input() blocks execution until the user types text and presses Enter."
        },
    ]
    run_quiz(tracker, "User Input", questions, passes_needed=2)
    tracker.complete_topic("User Input")
    pause("Chapter 4 complete! Press Enter for Chapter 5...")


def _safe_float_input(prompt: str) -> float:
    while True:
        raw = get_input(prompt)
        try:
            return float(raw)
        except ValueError:
            error_msg("Please enter a valid number.")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 5 — STRINGS
# ──────────────────────────────────────────────────────────────────
def chapter_strings(tracker: ProgressTracker):
    clear_screen()
    print_header("💬 CHAPTER 5 — Strings")
    animate_loading("Preparing Chapter 5")

    slow_print("  Strings are how Python handles text — super powerful!", 0.025, C_INFO)
    print()
    explain(
        "A string is a sequence of characters enclosed in quotes. "
        "You can use single quotes, double quotes, or triple quotes. "
        "Strings are immutable — you cannot change individual characters, "
        "but you can create new strings from existing ones."
    )

    code_block("""
# Creating strings
s1 = 'Hello'
s2 = "World"
s3 = '''This is a
multi-line string'''

# Concatenation (joining)
full = s1 + ", " + s2 + "!"   # Hello, World!

# Repetition
line = "-" * 20               # --------------------

# Length
print(len("Python"))          # 6

# Indexing  (0-based, negative from end)
word = "Python"
print(word[0])    # P    (first character)
print(word[-1])   # n    (last character)

# Slicing  [start : stop : step]
print(word[0:3])  # Pyt  (chars 0,1,2)
print(word[::2])  # Pto  (every other char)
print(word[::-1]) # nohtyP (reversed!)
""", "String Basics")

    explain(
        "Strings come with many built-in methods. "
        "Methods are called using dot notation: string.method()"
    )

    code_block("""
s = "  Hello, World!  "

print(s.upper())         # '  HELLO, WORLD!  '
print(s.lower())         # '  hello, world!  '
print(s.strip())         # 'Hello, World!'  (removes spaces)
print(s.strip().title()) # 'Hello, World!'
print(s.replace("World", "Python"))  # '  Hello, Python!  '
print("Hello".startswith("He"))      # True
print("Hello".endswith("lo"))        # True
print("Hello World".split())         # ['Hello', 'World']
print(",".join(["a", "b", "c"]))     # 'a,b,c'
print("hello".count("l"))            # 2
print("Hello".find("ll"))            # 2  (index where found)
""", "Common String Methods")

    pause()

    # Interactive string explorer
    print_section("🎮 String Explorer")
    s = get_input("Type any string to explore: ")
    if s:
        print()
        print(f"  Original  : {C_SUCCESS}'{s}'{C_RESET}")
        print(f"  Length    : {C_SUCCESS}{len(s)}{C_RESET}")
        print(f"  Upper     : {C_SUCCESS}'{s.upper()}'{C_RESET}")
        print(f"  Lower     : {C_SUCCESS}'{s.lower()}'{C_RESET}")
        print(f"  Reversed  : {C_SUCCESS}'{s[::-1]}'{C_RESET}")
        print(f"  First char: {C_SUCCESS}'{s[0]}'{C_RESET}")
        print(f"  Last char : {C_SUCCESS}'{s[-1]}'{C_RESET}")
    pause()

    questions = [
        {
            "q": "What is the index of the FIRST character in a Python string?",
            "choices": ["1", "0", "-1", "None"],
            "a": "0",
            "hint": "Python uses zero-based indexing.",
            "explain": "Python indexes start at 0, so the first character is at index 0."
        },
        {
            "q": "What does 'Python'[::-1] return?",
            "choices": ["Python", "nohtyP", "Pyt", "hon"],
            "a": "nohtyP",
            "hint": "A step of -1 means go backwards through the string.",
            "explain": "[::-1] reverses the string by stepping backwards from the end."
        },
        {
            "q": "Which method removes leading and trailing whitespace?",
            "choices": ["strip()", "clean()", "trim()", "remove()"],
            "a": "strip()",
            "hint": "Think of stripping the edges off.",
            "explain": "str.strip() removes whitespace (spaces, tabs, newlines) from both ends."
        },
        {
            "q": "What does len('Hello') return?",
            "choices": ["4", "5", "6", "Error"],
            "a": "5",
            "hint": "Count every character: H-e-l-l-o",
            "explain": "'Hello' has 5 characters, so len('Hello') is 5."
        },
        {
            "q": "What does 'ha' * 3 produce?",
            "choices": ["ha ha ha", "hahaha", "ha3", "Error"],
            "a": "hahaha",
            "hint": "String * number repeats the string.",
            "explain": "'ha' * 3 concatenates 'ha' three times: 'hahaha'."
        },
    ]
    run_quiz(tracker, "Strings", questions, passes_needed=3)

    exercises = [
        {
            "task": "What is the output of: 'Python'[2:5] ?",
            "answers": ["tho"],
            "hint": "Slice from index 2 (inclusive) to index 5 (exclusive).",
            "solution": "'Python'[2:5]   # 't','h','o'  → 'tho'"
        },
        {
            "task": "Which method splits 'a,b,c' on commas to give ['a','b','c']?",
            "answers": ["split(',')", "split(',')", ".split(',')"],
            "hint": "The split method takes the delimiter as its argument.",
            "solution": "'a,b,c'.split(',')   # → ['a', 'b', 'c']"
        },
    ]
    run_coding_exercise(tracker, "Strings", exercises)
    tracker.complete_topic("Strings")
    pause("Chapter 5 complete! Press Enter for Chapter 6...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 6 — ARITHMETIC OPERATIONS
# ──────────────────────────────────────────────────────────────────
def chapter_arithmetic(tracker: ProgressTracker):
    clear_screen()
    print_header("➕ CHAPTER 6 — Arithmetic Operations")
    animate_loading("Preparing Chapter 6")

    slow_print("  Python is a fantastic calculator! Let's explore the operators.", 0.025, C_INFO)
    print()

    code_block("""
# The seven arithmetic operators
a, b = 17, 5

print(a + b)    # Addition       →  22
print(a - b)    # Subtraction    →  12
print(a * b)    # Multiplication →  85
print(a / b)    # Division       →   3.4   (always float)
print(a // b)   # Floor division →   3     (rounds DOWN)
print(a % b)    # Modulo         →   2     (remainder)
print(a ** b)   # Exponentiation → 1419857 (17^5)
""", "The 7 Arithmetic Operators")

    print_box([
        "+   Addition        5 + 3  = 8",
        "-   Subtraction     5 - 3  = 2",
        "*   Multiplication  5 * 3  = 15",
        "/   Division        5 / 2  = 2.5  (float)",
        "//  Floor Division  5 // 2 = 2    (int)",
        "%   Modulo          5 % 2  = 1    (remainder)",
        "**  Exponent        5 ** 2 = 25",
    ], C_CODE)

    explain(
        "Floor division (//) always rounds DOWN to the nearest whole number. "
        "Modulo (%) gives the REMAINDER after division — great for checking "
        "if a number is even (n % 2 == 0) or for cyclic patterns. "
        "Augmented assignment operators are shortcuts: x += 5 means x = x + 5."
    )

    code_block("""
# Augmented assignment shortcuts
x = 10
x += 3     # x = 13  (same as x = x + 3)
x -= 1     # x = 12
x *= 2     # x = 24
x /= 4     # x = 6.0
x //= 2    # x = 3.0
x **= 2    # x = 9.0
x %= 4     # x = 1.0

# Practical: is a number even?
n = 8
print(n % 2 == 0)   # True  → even
n = 7
print(n % 2 == 0)   # False → odd
""", "Augmented Assignment & Modulo Trick")

    pause()

    # calculator demo
    print_section("🎮 Live Calculator")
    a = _safe_float_input("First  number: ")
    b = _safe_float_input("Second number: ")
    print()
    animate_loading("Computing")
    ops = [
        ("+",  lambda x, y: x + y),
        ("-",  lambda x, y: x - y),
        ("*",  lambda x, y: x * y),
        ("/",  lambda x, y: x / y if y != 0 else "undefined"),
        ("//", lambda x, y: x // y if y != 0 else "undefined"),
        ("%",  lambda x, y: x % y if y != 0 else "undefined"),
        ("**", lambda x, y: x ** y),
    ]
    for sym, fn in ops:
        result = fn(a, b)
        if isinstance(result, float):
            result = round(result, 6)
        print(f"  {C_CODE}{a} {sym} {b}{C_RESET} = {C_SUCCESS}{result}{C_RESET}")
    pause()

    questions = [
        {
            "q": "What is the result of  17 % 5 ?",
            "choices": ["3", "2", "3.4", "12"],
            "a": "2",
            "hint": "17 ÷ 5 = 3 remainder 2. Modulo gives the remainder.",
            "explain": "17 = 5 × 3 + 2, so 17 % 5 = 2."
        },
        {
            "q": "What is 10 // 3 ?",
            "choices": ["3.33", "3", "4", "3.0"],
            "a": "3",
            "hint": "Floor division always rounds DOWN to the nearest integer.",
            "explain": "10 / 3 = 3.333..., floor division truncates to 3."
        },
        {
            "q": "What operator is used for exponentiation (powers)?",
            "choices": ["^", "**", "^^", "pow"],
            "a": "**",
            "hint": "In Python, caret (^) is the bitwise XOR, not power.",
            "explain": "** is Python's exponent operator. 2**10 = 1024."
        },
        {
            "q": "What does  x += 5  mean?",
            "choices": ["x = 5", "x = x + 5", "x = x == 5", "x == x + 5"],
            "a": "x = x + 5",
            "hint": "+= is augmented addition assignment.",
            "explain": "+= adds the right side to the variable and stores the result back."
        },
    ]
    run_quiz(tracker, "Arithmetic Operations", questions, passes_needed=3)

    exercises = [
        {
            "task": "What is the output of: print(2 ** 8)?",
            "answers": ["256"],
            "hint": "2 to the power of 8.",
            "solution": "print(2 ** 8)   # Output: 256"
        },
        {
            "task": "How do you check if a number n is even using modulo?",
            "answers": ["n % 2 == 0", "n % 2 == 0", "n%2==0"],
            "hint": "Even numbers have zero remainder when divided by 2.",
            "solution": "if n % 2 == 0:   # n is even"
        },
    ]
    run_coding_exercise(tracker, "Arithmetic Operations", exercises)
    tracker.complete_topic("Arithmetic Operations")
    pause("Chapter 6 complete! Press Enter for Chapter 7...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 7 — OPERATOR PRECEDENCE
# ──────────────────────────────────────────────────────────────────
def chapter_precedence(tracker: ProgressTracker):
    clear_screen()
    print_header("⚖️  CHAPTER 7 — Operator Precedence")
    animate_loading("Preparing Chapter 7")

    slow_print("  Who goes first? Python follows mathematical order of operations!", 0.025, C_INFO)
    print()
    explain(
        "When an expression has multiple operators, Python evaluates them in a "
        "specific order (just like BODMAS/PEMDAS in math). "
        "Higher precedence operators are evaluated FIRST."
    )

    code_block("""
# Precedence (high → low)
# 1. ()   Parentheses
# 2. **   Exponentiation
# 3. +x, -x, ~x   Unary operators
# 4. *, /, //, %  Multiplication / Division
# 5. +, -         Addition / Subtraction

print(2 + 3 * 4)         # 14  (not 20! * before +)
print((2 + 3) * 4)       # 20  (parentheses first)
print(2 ** 3 ** 2)       # 512 (** is RIGHT-to-left: 3**2=9, 2**9=512)
print((2 ** 3) ** 2)     # 64  (left to right with parens)
print(10 - 4 + 2)        # 8   (same precedence → left to right)
print(10 / 2 * 3)        # 15.0 (left to right)
print(10 - 3 * 2 + 1)    # 5   (3*2=6, 10-6+1=5)
""", "Precedence Examples")

    print_box([
        "🥇 () Parentheses       — always first!",
        "🥈 ** Exponentiation    — right-to-left",
        "🥉 *, /, //, %          — left-to-right",
        "4️⃣  +, -               — left-to-right",
        "",
        "💡 Tip: When in doubt, use parentheses for clarity!",
    ], C_WARN)

    pause()

    questions = [
        {
            "q": "What is the result of: 2 + 3 * 4?",
            "choices": ["20", "14", "24", "10"],
            "a": "14",
            "hint": "Multiplication happens before addition.",
            "explain": "3 * 4 = 12 first, then 2 + 12 = 14."
        },
        {
            "q": "What is: 10 - 2 + 3?",
            "choices": ["5", "11", "9", "15"],
            "a": "11",
            "hint": "Same precedence — evaluate left to right.",
            "explain": "10 - 2 = 8, then 8 + 3 = 11. Left-to-right when same precedence."
        },
        {
            "q": "What is: 2 ** 3 ** 2?",
            "choices": ["64", "512", "8", "36"],
            "a": "512",
            "hint": "Exponentiation is right-associative: evaluate the rightmost ** first.",
            "explain": "3**2 = 9 first (right-to-left), then 2**9 = 512."
        },
        {
            "q": "What is: (1 + 2) * (3 + 4)?",
            "choices": ["10", "21", "14", "11"],
            "a": "21",
            "hint": "Parentheses first: both brackets evaluated before multiplying.",
            "explain": "(1+2)=3 and (3+4)=7, then 3*7=21."
        },
    ]
    run_quiz(tracker, "Operator Precedence", questions, passes_needed=3)
    tracker.complete_topic("Operator Precedence")
    pause("Chapter 7 complete! Press Enter for Chapter 8...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 8 — COMPARISON OPERATORS
# ──────────────────────────────────────────────────────────────────
def chapter_comparison(tracker: ProgressTracker):
    clear_screen()
    print_header("⚖️  CHAPTER 8 — Comparison Operators")
    animate_loading("Preparing Chapter 8")

    slow_print("  Comparison operators return True or False — the backbone of decisions!", 0.025, C_INFO)
    print()

    code_block("""
a, b = 5, 10

print(a == b)   # False  — Equal to
print(a != b)   # True   — Not equal to
print(a <  b)   # True   — Less than
print(a >  b)   # False  — Greater than
print(a <= b)   # True   — Less than or equal
print(a >= b)   # False  — Greater than or equal

# Works on strings too!
print("apple" == "apple")   # True
print("a" < "b")            # True (alphabetical order)
print("Z" < "a")            # True (uppercase before lowercase)
""", "All 6 Comparison Operators")

    print_box([
        "==   Equal to            5 == 5   → True",
        "!=   Not equal           5 != 3   → True",
        "<    Less than           3 < 5    → True",
        ">    Greater than        5 > 3    → True",
        "<=   Less or equal       5 <= 5   → True",
        ">=   Greater or equal    6 >= 5   → True",
        "",
        "⚠️   Don't confuse = (assignment) with == (comparison)!",
    ], C_CODE)

    explain(
        "You can chain comparisons in Python naturally: "
        "'1 < x < 10' checks that x is between 1 and 10, exclusive. "
        "This is much more readable than other languages."
    )

    code_block("""
x = 7
print(1 < x < 10)    # True  — Python allows chained comparison
print(1 < x and x < 10)  # same thing, more verbose
""", "Chained Comparisons")

    pause()

    questions = [
        {
            "q": "What does 5 == 5.0 return?",
            "choices": ["True", "False", "Error", "None"],
            "a": "True",
            "hint": "Python compares values, and 5 and 5.0 have the same numeric value.",
            "explain": "Python's == checks value equality. 5 (int) and 5.0 (float) have equal values."
        },
        {
            "q": "What operator checks if two values are NOT equal?",
            "choices": ["<>", "=/=", "!=", "not=="],
            "a": "!=",
            "hint": "The ! means 'not'.",
            "explain": "!= is the 'not equal' operator. a != b returns True when a and b differ."
        },
        {
            "q": "What is the result of: 3 > 3?",
            "choices": ["True", "False", "3", "Error"],
            "a": "False",
            "hint": "3 is NOT strictly greater than 3.",
            "explain": "3 > 3 is False. Use >= if you want 'greater than or equal'."
        },
        {
            "q": "Is 1 < 5 < 10 valid Python and is it True?",
            "choices": [
                "Invalid syntax",
                "Valid and True",
                "Valid and False",
                "Valid but throws error"
            ],
            "a": "Valid and True",
            "hint": "Python allows chained comparisons.",
            "explain": "1 < 5 < 10 is valid and means (1 < 5) and (5 < 10) = True and True = True."
        },
    ]
    run_quiz(tracker, "Comparison Operators", questions, passes_needed=3)
    tracker.complete_topic("Comparison Operators")
    pause("Chapter 8 complete! Press Enter for Chapter 9...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 9 — LOGICAL OPERATORS
# ──────────────────────────────────────────────────────────────────
def chapter_logical(tracker: ProgressTracker):
    clear_screen()
    print_header("🔗 CHAPTER 9 — Logical Operators")
    animate_loading("Preparing Chapter 9")

    slow_print("  Combine conditions with and, or, not!", 0.025, C_INFO)
    print()
    explain(
        "Logical operators combine multiple boolean expressions. "
        "Python has three logical operators: and, or, not. "
        "They are written as English words — very readable!"
    )

    code_block("""
# 'and' — True only when BOTH sides are True
print(True  and True)   # True
print(True  and False)  # False
print(False and True)   # False

# 'or' — True when AT LEAST ONE side is True
print(True  or False)   # True
print(False or False)   # False

# 'not' — flips the boolean value
print(not True)         # False
print(not False)        # True

# Real-world example
age   = 20
score = 85
is_member = True

can_access = age >= 18 and score >= 80
print(can_access)       # True

gets_discount = age < 18 or is_member
print(gets_discount)    # True
""", "and, or, not Examples")

    print_box([
        "Truth Table for 'and':",
        "  True  and True  = True",
        "  True  and False = False",
        "  False and True  = False",
        "  False and False = False",
        "",
        "Truth Table for 'or':",
        "  True  or True  = True",
        "  True  or False = True",
        "  False or True  = True",
        "  False or False = False",
    ], C_INFO)

    explain(
        "Short-circuit evaluation: Python stops evaluating 'and' as soon "
        "as it sees a False (because the whole thing must be False). "
        "For 'or', it stops at the first True. This makes code efficient."
    )

    pause()

    questions = [
        {
            "q": "What does (True and False) or True evaluate to?",
            "choices": ["True", "False", "None", "Error"],
            "a": "True",
            "hint": "Evaluate left to right: (True and False) = False, then False or True = ?",
            "explain": "(True and False) = False; then False or True = True."
        },
        {
            "q": "What does not (5 > 3) return?",
            "choices": ["True", "False", "5 > 3", "Error"],
            "a": "False",
            "hint": "5 > 3 is True, and not flips it.",
            "explain": "5 > 3 is True, not True = False."
        },
        {
            "q": "Which expression checks if x is between 1 and 100 (inclusive)?",
            "choices": [
                "1 < x < 100",
                "x >= 1 and x <= 100",
                "x >= 1 or x <= 100",
                "1 and x and 100"
            ],
            "a": "x >= 1 and x <= 100",
            "hint": "Both conditions must be true simultaneously.",
            "explain": "'and' requires both to be True. 1 < x < 100 also works but excludes 1 and 100."
        },
        {
            "q": "What is False or False?",
            "choices": ["True", "False", "None", "Error"],
            "a": "False",
            "hint": "'or' needs at least one True to return True.",
            "explain": "Both sides are False, so 'or' returns False."
        },
    ]
    run_quiz(tracker, "Logical Operators", questions, passes_needed=3)
    tracker.complete_topic("Logical Operators")
    pause("Chapter 9 complete! Press Enter for Chapter 10...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 10 — IF STATEMENTS
# ──────────────────────────────────────────────────────────────────
def chapter_if_statements(tracker: ProgressTracker):
    clear_screen()
    print_header("🔀 CHAPTER 10 — If Statements")
    animate_loading("Preparing Chapter 10")

    slow_print("  Decision making — the heart of every program!", 0.025, C_INFO)
    print()
    explain(
        "If statements allow your program to make decisions. "
        "Python uses indentation (4 spaces or 1 tab) to define code blocks — "
        "there are no curly braces like in C or JavaScript!"
    )

    code_block("""
# Basic if / elif / else structure
score = 78

if score >= 90:
    print("Grade: A — Excellent!")
elif score >= 80:
    print("Grade: B — Good job!")
elif score >= 70:
    print("Grade: C — Satisfactory")
elif score >= 60:
    print("Grade: D — Needs improvement")
else:
    print("Grade: F — Please seek help")

# Output: Grade: C — Satisfactory
""", "if / elif / else")

    explain(
        "Indentation is mandatory in Python. Anything indented under an if "
        "block is part of that block. Python raises an IndentationError if "
        "you forget to indent correctly."
    )

    code_block("""
# Nested if statements
age = 20

if age >= 18:
    print("Adult")
    if age >= 65:
        print("Senior citizen")
    else:
        print("Working age adult")
else:
    print("Minor")

# One-liner (ternary) if
x = 10
label = "even" if x % 2 == 0 else "odd"
print(label)    # even
""", "Nested & Ternary If")

    pause()

    # interactive
    print_section("🎮 Grade Calculator")
    try:
        score = int(_safe_float_input("Enter a score (0-100): "))
        print()
        animate_loading("Grading")
        if score >= 90:
            grade, msg = "A", "Excellent! 🏆"
        elif score >= 80:
            grade, msg = "B", "Great job! ⭐"
        elif score >= 70:
            grade, msg = "C", "Good effort! 👍"
        elif score >= 60:
            grade, msg = "D", "Keep working! 📚"
        else:
            grade, msg = "F", "Don't give up! 💪"
        print(f"  Score: {C_SUCCESS}{score}{C_RESET}  Grade: {C_SUCCESS}{grade}{C_RESET}  — {msg}")
    except Exception:
        info_msg("Skipping demo due to invalid input.")
    pause()

    questions = [
        {
            "q": "What keyword starts a secondary condition in an if-chain?",
            "choices": ["else if", "elsif", "elif", "elseif"],
            "a": "elif",
            "hint": "It's a Python-specific shorthand.",
            "explain": "Python uses 'elif' (short for else-if) for additional conditions."
        },
        {
            "q": "What happens if no condition is True and there is no else?",
            "choices": [
                "Error is raised",
                "First block runs anyway",
                "Nothing happens",
                "Program quits"
            ],
            "a": "Nothing happens",
            "hint": "Python simply skips the entire if-block.",
            "explain": "If no condition matches and no else exists, Python skips the block quietly."
        },
        {
            "q": "What is the ternary (one-line if) syntax?",
            "choices": [
                "if x else y",
                "value_if_true if condition else value_if_false",
                "condition ? true : false",
                "(condition) -> true | false"
            ],
            "a": "value_if_true if condition else value_if_false",
            "hint": "The condition goes in the MIDDLE.",
            "explain": "Python ternary: result = val_true if condition else val_false."
        },
        {
            "q": "What does Python use to define code blocks?",
            "choices": [
                "Curly braces {}",
                "Square brackets []",
                "Indentation (spaces/tabs)",
                "Keywords begin/end"
            ],
            "a": "Indentation (spaces/tabs)",
            "hint": "This is what makes Python unique!",
            "explain": "Python uses consistent indentation (4 spaces by convention) to delimit blocks."
        },
    ]
    run_quiz(tracker, "If Statements", questions, passes_needed=3)
    tracker.complete_topic("If Statements")
    pause("Chapter 10 complete! Press Enter for Chapter 11...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 11 — WHILE LOOPS
# ──────────────────────────────────────────────────────────────────
def chapter_while_loops(tracker: ProgressTracker):
    clear_screen()
    print_header("🔁 CHAPTER 11 — While Loops")
    animate_loading("Preparing Chapter 11")

    slow_print("  Repeat actions while a condition is True!", 0.025, C_INFO)
    print()
    explain(
        "A while loop keeps executing its body as long as its condition is True. "
        "Always make sure the condition will eventually become False, "
        "otherwise you'll have an infinite loop!"
    )

    code_block("""
# Count from 1 to 5
count = 1
while count <= 5:
    print(count)
    count += 1       # IMPORTANT: update the variable!
# Output: 1 2 3 4 5

# Guess-the-number game
secret = 7
guess  = 0
while guess != secret:
    guess = int(input("Guess: "))
    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")
print("Correct! 🎉")
""", "While Loop Examples")

    explain(
        "break exits the loop immediately. "
        "continue skips the rest of the current iteration and jumps to the next. "
        "An optional else clause runs when the loop finishes normally (no break)."
    )

    code_block("""
# break — exit early
i = 0
while True:          # infinite loop!
    i += 1
    if i == 5:
        break        # exits when i reaches 5
print(f"Stopped at {i}")   # Stopped at 5

# continue — skip an iteration
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue     # skip even numbers
    print(i)         # prints 1 3 5 7 9
""", "break and continue")

    pause()

    # Guessing game
    print_section("🎮 Guess the Number!")
    secret = random.randint(1, 20)
    attempts = 0
    max_attempts = 5
    slow_print(f"  I'm thinking of a number between 1 and 20... (you have {max_attempts} tries)", 0.025, C_INFO)
    print()
    won = False
    while attempts < max_attempts:
        raw = get_input(f"Guess ({max_attempts - attempts} left): ")
        try:
            guess = int(raw)
            attempts += 1
            if guess == secret:
                celebrate(f"Correct! It was {secret}! You got it in {attempts} tries!")
                won = True
                break
            elif guess < secret:
                print(f"  {C_WARN}📈 Too low!{C_RESET}\n")
            else:
                print(f"  {C_WARN}📉 Too high!{C_RESET}\n")
        except ValueError:
            error_msg("Please enter a whole number.")
    if not won:
        print(f"  {C_ERROR}The number was {secret}. Better luck next time!{C_RESET}")
    pause()

    questions = [
        {
            "q": "What keyword immediately exits a while loop?",
            "choices": ["stop", "exit", "break", "end"],
            "a": "break",
            "hint": "Think 'break out' of the loop.",
            "explain": "break immediately terminates the enclosing loop."
        },
        {
            "q": "What happens if the while condition is never False?",
            "choices": [
                "Loop runs once",
                "Infinite loop",
                "Python raises an error",
                "Loop is skipped"
            ],
            "a": "Infinite loop",
            "hint": "The condition controls when to stop.",
            "explain": "Without a way to make the condition False, the loop runs forever — an infinite loop."
        },
        {
            "q": "What does 'continue' do inside a loop?",
            "choices": [
                "Exits the loop",
                "Skips to the next iteration",
                "Restarts the loop from the beginning",
                "Pauses execution"
            ],
            "a": "Skips to the next iteration",
            "hint": "It skips the rest of the current loop body.",
            "explain": "continue skips remaining code in this iteration and moves to the next loop cycle."
        },
        {
            "q": "What is 'while True:' called?",
            "choices": [
                "A conditional loop",
                "An infinite loop",
                "A for loop",
                "A definite loop"
            ],
            "a": "An infinite loop",
            "hint": "True never becomes False on its own.",
            "explain": "while True: runs forever unless broken by a 'break' statement inside."
        },
    ]
    run_quiz(tracker, "While Loops", questions, passes_needed=3)
    tracker.complete_topic("While Loops")
    pause("Chapter 11 complete! Press Enter for Chapter 12...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 12 — LISTS
# ──────────────────────────────────────────────────────────────────
def chapter_lists(tracker: ProgressTracker):
    clear_screen()
    print_header("📋 CHAPTER 12 — Lists")
    animate_loading("Preparing Chapter 12")

    slow_print("  Lists store multiple values in an ordered, mutable collection!", 0.025, C_INFO)
    print()
    explain(
        "A list is a collection of items in a specific order, enclosed in "
        "square brackets []. Unlike strings, lists are MUTABLE — you can "
        "change, add, or remove items. Lists can hold any mix of data types."
    )

    code_block("""
# Creating lists
fruits  = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed   = [1, "hello", 3.14, True]
empty   = []

# Indexing (same as strings)
print(fruits[0])     # apple   (first)
print(fruits[-1])    # cherry  (last)

# Slicing
print(numbers[1:4])  # [2, 3, 4]
print(numbers[::-1]) # [5, 4, 3, 2, 1]

# Length
print(len(fruits))   # 3

# Modifying (lists are mutable!)
fruits[1] = "blueberry"
print(fruits)        # ['apple', 'blueberry', 'cherry']

# Nested lists
matrix = [[1, 2], [3, 4], [5, 6]]
print(matrix[1][0])  # 3  (row 1, col 0)
""", "List Basics")

    code_block("""
# List operations
a = [1, 2, 3]
b = [4, 5, 6]

# Concatenation
print(a + b)         # [1, 2, 3, 4, 5, 6]

# Repetition
print(a * 2)         # [1, 2, 3, 1, 2, 3]

# Membership
print(2 in a)        # True
print(9 in a)        # False

# Unpacking
x, y, z = a
print(x, y, z)       # 1 2 3
""", "List Operations")

    pause()

    questions = [
        {
            "q": "What index accesses the LAST element of a list?",
            "choices": ["0", "-1", "len(list)", "last"],
            "a": "-1",
            "hint": "Python allows negative indexing from the end.",
            "explain": "Index -1 always refers to the last element of any sequence."
        },
        {
            "q": "Are lists mutable (changeable)?",
            "choices": ["Yes", "No", "Only for strings", "Only for numbers"],
            "a": "Yes",
            "hint": "Unlike strings and tuples, lists support item assignment.",
            "explain": "Lists are mutable — you can change individual elements: lst[0] = 'new'."
        },
        {
            "q": "What is the output of: [1, 2, 3][1:3]?",
            "choices": ["[1, 2]", "[2, 3]", "[1, 2, 3]", "[3]"],
            "a": "[2, 3]",
            "hint": "Slice [1:3] includes index 1 and 2 but NOT 3.",
            "explain": "list[1:3] returns elements at indexes 1 and 2 → [2, 3]."
        },
        {
            "q": "How do you check if 'x' is IN a list called items?",
            "choices": [
                "items.contains('x')",
                "'x' in items",
                "items.has('x')",
                "find('x', items)"
            ],
            "a": "'x' in items",
            "hint": "Python's 'in' operator works on lists.",
            "explain": "'x' in items returns True if 'x' is an element of the list."
        },
    ]
    run_quiz(tracker, "Lists", questions, passes_needed=3)
    tracker.complete_topic("Lists")
    pause("Chapter 12 complete! Press Enter for Chapter 13...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 13 — LIST METHODS
# ──────────────────────────────────────────────────────────────────
def chapter_list_methods(tracker: ProgressTracker):
    clear_screen()
    print_header("🛠  CHAPTER 13 — List Methods")
    animate_loading("Preparing Chapter 13")

    slow_print("  Lists have powerful built-in methods — let's explore them!", 0.025, C_INFO)
    print()

    code_block("""
fruits = ["banana", "apple", "cherry"]

# Adding
fruits.append("date")          # add to END
fruits.insert(1, "avocado")    # insert at index 1
fruits.extend(["elderberry"])  # add all items from another list

# Removing
fruits.remove("banana")        # remove by VALUE (first occurrence)
popped = fruits.pop()          # remove and return LAST item
popped2 = fruits.pop(0)        # remove and return item at index 0

# Searching & counting
print(fruits.index("apple"))   # index of 'apple'
print(fruits.count("apple"))   # how many times 'apple' appears

# Sorting
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()                    # sorts IN PLACE (ascending)
print(nums)                    # [1, 1, 2, 3, 4, 5, 6, 9]
nums.sort(reverse=True)        # descending
print(sorted([3,1,2]))         # [1,2,3]  — returns NEW list, original unchanged

# Reversing
nums.reverse()                 # reverses IN PLACE

# Copy & clear
copy = fruits.copy()           # shallow copy
fruits.clear()                 # removes ALL elements → []
""", "All Essential List Methods")

    print_box([
        "append(x)      — add x to the END",
        "insert(i, x)   — insert x at index i",
        "extend(iter)   — add all items of iterable",
        "remove(x)      — remove first occurrence of x",
        "pop([i])       — remove & return item (default: last)",
        "index(x)       — find index of x",
        "count(x)       — count occurrences of x",
        "sort()         — sort in-place",
        "reverse()      — reverse in-place",
        "copy()         — shallow copy",
        "clear()        — empty the list",
    ], C_CODE)

    pause()

    # Live list playground
    print_section("🎮 List Playground")
    slow_print("  Let's build a list together!", 0.025, C_INFO)
    my_list = []
    for i in range(3):
        item = get_input(f"Add item {i+1} to the list: ")
        my_list.append(item)
        print(f"  List: {C_SUCCESS}{my_list}{C_RESET}")
    print()
    print(f"  Sorted  : {C_SUCCESS}{sorted(my_list)}{C_RESET}")
    print(f"  Reversed: {C_SUCCESS}{list(reversed(my_list))}{C_RESET}")
    pause()

    questions = [
        {
            "q": "Which method adds an element to the END of a list?",
            "choices": ["insert()", "add()", "append()", "push()"],
            "a": "append()",
            "hint": "Think 'append = attach to the end'.",
            "explain": "list.append(x) adds x to the end of the list."
        },
        {
            "q": "What does list.pop() do by default?",
            "choices": [
                "Removes the first element",
                "Removes and returns the last element",
                "Returns the last element without removing",
                "Clears the list"
            ],
            "a": "Removes and returns the last element",
            "hint": "pop() can accept an optional index.",
            "explain": "list.pop() removes and returns the last element. list.pop(0) removes the first."
        },
        {
            "q": "What does list.sort() vs sorted(list) do differently?",
            "choices": [
                "They are identical",
                "sort() sorts in-place; sorted() returns a new list",
                "sorted() sorts in-place; sort() returns a new list",
                "sort() is faster"
            ],
            "a": "sort() sorts in-place; sorted() returns a new list",
            "hint": "In-place means the original list is modified.",
            "explain": "list.sort() modifies the list itself and returns None. sorted() returns a new sorted list."
        },
        {
            "q": "Which method removes ALL items from a list?",
            "choices": ["remove()", "delete()", "pop()", "clear()"],
            "a": "clear()",
            "hint": "The name is very descriptive.",
            "explain": "list.clear() empties the list, equivalent to del list[:]."
        },
    ]
    run_quiz(tracker, "List Methods", questions, passes_needed=3)
    tracker.complete_topic("List Methods")
    pause("Chapter 13 complete! Press Enter for Chapter 14...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 14 — FOR LOOPS
# ──────────────────────────────────────────────────────────────────
def chapter_for_loops(tracker: ProgressTracker):
    clear_screen()
    print_header("🔄 CHAPTER 14 — For Loops")
    animate_loading("Preparing Chapter 14")

    slow_print("  Iterate over any sequence elegantly with for loops!", 0.025, C_INFO)
    print()
    explain(
        "A for loop iterates over each item in a sequence (list, string, range, tuple, etc.) "
        "automatically. Python handles the counter for you — no need to manually "
        "increment an index like in C or Java."
    )

    code_block("""
# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
# apple
# banana
# cherry

# Iterate over a string
for char in "Python":
    print(char, end=" ")     # P y t h o n

# Enumerate: get index AND value
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Zip: iterate two lists together
names  = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 72]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
""", "For Loop Examples")

    code_block("""
# List comprehension — compact for loops
squares   = [x**2 for x in range(1, 6)]
# [1, 4, 9, 16, 25]

evens     = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

upper_words = [word.upper() for word in ["hi", "there"]]
# ['HI', 'THERE']
""", "List Comprehensions (Supercharged For)")

    pause()

    questions = [
        {
            "q": "What does 'for x in [1, 2, 3]: print(x)' print?",
            "choices": ["1 2 3 on same line", "1\\n2\\n3 (each on own line)", "[1,2,3]", "x x x"],
            "a": "1\n2\n3 (each on own line)",
            "hint": "print() adds a newline by default.",
            "explain": "The loop runs 3 times, printing 1, 2, 3 each on a new line."
        },
        {
            "q": "Which built-in function gives both index and value when iterating?",
            "choices": ["zip()", "index()", "enumerate()", "count()"],
            "a": "enumerate()",
            "hint": "It adds a counter automatically.",
            "explain": "enumerate(iterable) yields (index, value) pairs."
        },
        {
            "q": "What is the output of: [x**2 for x in range(4)]?",
            "choices": ["[1, 4, 9, 16]", "[0, 1, 4, 9]", "[0, 2, 4, 6]", "[1, 2, 3, 4]"],
            "a": "[0, 1, 4, 9]",
            "hint": "range(4) gives 0, 1, 2, 3 — not 1 through 4.",
            "explain": "0²=0, 1²=1, 2²=4, 3²=9 → [0, 1, 4, 9]."
        },
        {
            "q": "Which function iterates over two lists simultaneously?",
            "choices": ["pairs()", "enumerate()", "zip()", "merge()"],
            "a": "zip()",
            "hint": "It 'zips' multiple iterables together.",
            "explain": "zip(a, b) produces tuples of (a[0],b[0]), (a[1],b[1]), etc."
        },
    ]
    run_quiz(tracker, "For Loops", questions, passes_needed=3)
    tracker.complete_topic("For Loops")
    pause("Chapter 14 complete! Press Enter for Chapter 15...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 15 — RANGE FUNCTION
# ──────────────────────────────────────────────────────────────────
def chapter_range(tracker: ProgressTracker):
    clear_screen()
    print_header("📏 CHAPTER 15 — The range() Function")
    animate_loading("Preparing Chapter 15")

    slow_print("  range() generates sequences of numbers on demand — very memory efficient!", 0.025, C_INFO)
    print()
    explain(
        "range() creates a sequence of numbers without storing all of them in memory. "
        "It has three forms: range(stop), range(start, stop), range(start, stop, step). "
        "The stop value is ALWAYS exclusive (not included)."
    )

    code_block("""
# range(stop) — from 0 up to (not including) stop
list(range(5))          # [0, 1, 2, 3, 4]

# range(start, stop)
list(range(2, 8))       # [2, 3, 4, 5, 6, 7]

# range(start, stop, step)
list(range(0, 10, 2))   # [0, 2, 4, 6, 8]    (evens)
list(range(10, 0, -1))  # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# Using range in for loops
for i in range(3):
    print(f"Iteration {i}")   # 0, 1, 2

# Sum of 1 to 100
total = sum(range(1, 101))
print(total)            # 5050

# Counting down
for i in range(5, 0, -1):
    print(i, end=" ")   # 5 4 3 2 1
""", "range() Examples")

    print_box([
        "range(stop)           → 0 to stop-1",
        "range(start, stop)    → start to stop-1",
        "range(start,stop,step)→ start to stop with step",
        "",
        "⚠️  stop is ALWAYS excluded from the sequence!",
        "💡  range(10) gives 0..9 — not 0..10",
    ], C_CODE)

    pause()

    # range visualizer
    print_section("🎮 Range Visualizer")
    try:
        start = int(_safe_float_input("Start : "))
        stop  = int(_safe_float_input("Stop  : "))
        step  = int(_safe_float_input("Step  : "))
        r     = list(range(start, stop, step))
        if len(r) == 0:
            info_msg("Empty range!")
        elif len(r) > 50:
            info_msg(f"Range has {len(r)} elements — showing first 20...")
            print(f"  {C_SUCCESS}{r[:20]}  ...{C_RESET}")
        else:
            print(f"  {C_SUCCESS}{r}{C_RESET}")
    except Exception as e:
        error_msg(f"Invalid input: {e}")
    pause()

    questions = [
        {
            "q": "What does range(5) generate?",
            "choices": ["[1,2,3,4,5]", "[0,1,2,3,4]", "[0,1,2,3,4,5]", "[1,2,3,4]"],
            "a": "[0,1,2,3,4]",
            "hint": "range starts at 0 by default and excludes the stop.",
            "explain": "range(5) = 0,1,2,3,4 — stop (5) is excluded."
        },
        {
            "q": "What does list(range(2, 10, 3)) produce?",
            "choices": ["[2,5,8]", "[2,5,8,11]", "[2,3,4,5,6,7,8,9]", "[3,6,9]"],
            "a": "[2,5,8]",
            "hint": "Start at 2, step by 3, stop before 10.",
            "explain": "2, 2+3=5, 5+3=8, 8+3=11 (≥10 so stop) → [2, 5, 8]."
        },
        {
            "q": "How do you count DOWN from 5 to 1 using range?",
            "choices": [
                "range(5, 1)",
                "range(5, 0, -1)",
                "range(1, 5, -1)",
                "range(-5, 0)"
            ],
            "a": "range(5, 0, -1)",
            "hint": "Use a negative step to count backwards.",
            "explain": "range(5, 0, -1) gives 5, 4, 3, 2, 1 — stopping before 0."
        },
        {
            "q": "How many iterations does 'for i in range(10):' produce?",
            "choices": ["9", "10", "11", "0"],
            "a": "10",
            "hint": "range(10) generates 0 through 9.",
            "explain": "range(10) produces 10 values: 0,1,2,...,9."
        },
    ]
    run_quiz(tracker, "Range Function", questions, passes_needed=3)
    tracker.complete_topic("Range Function")
    pause("Chapter 15 complete! Press Enter for Chapter 16...")


# ──────────────────────────────────────────────────────────────────
# CHAPTER 16 — TUPLES
# ──────────────────────────────────────────────────────────────────
def chapter_tuples(tracker: ProgressTracker):
    clear_screen()
    print_header("📦 CHAPTER 16 — Tuples")
    animate_loading("Preparing Chapter 16")

    slow_print("  Tuples: like lists but IMMUTABLE — perfect for fixed data!", 0.025, C_INFO)
    print()
    explain(
        "A tuple is an ordered, immutable collection of items enclosed in "
        "parentheses (). 'Immutable' means you cannot change the items after "
        "creation — no adding, removing, or replacing. Tuples are faster than "
        "lists and are ideal for fixed data like coordinates, RGB colours, or "
        "database records."
    )

    code_block("""
# Creating tuples
point     = (3, 7)
colors    = ("red", "green", "blue")
single    = (42,)          # ← trailing comma needed for single-element tuple!
empty     = ()
no_parens = 1, 2, 3        # parentheses optional! (packing)

# Accessing (same indexing as lists)
print(colors[0])     # red
print(colors[-1])    # blue
print(colors[1:])    # ('green', 'blue')

# Immutability
# colors[0] = "yellow"   # ← TypeError! Tuples are immutable

# Tuple unpacking
x, y = point
print(x, y)          # 3 7

lat, lon = 51.5, -0.12
print(f"London: {lat}°N, {lon}°E")

# Swapping (uses tuple packing/unpacking)
a, b = 10, 20
a, b = b, a
print(a, b)          # 20 10
""", "Tuple Basics")

    code_block("""
# Tuple methods (only 2!)
t = (1, 2, 3, 2, 4, 2)
print(t.count(2))    # 3  — how many times 2 appears
print(t.index(4))    # 4  — index of first occurrence of 4

# Tuples vs Lists comparison
coords_list  = [51.5, -0.12]  # mutable, slightly slower
coords_tuple = (51.5, -0.12)  # immutable, slightly faster

# Converting
my_list  = list(colors)       # tuple → list
my_tuple = tuple(my_list)     # list  → tuple

# Nested tuples
matrix = ((1, 2), (3, 4), (5, 6))
print(matrix[1][0])  # 3
""", "Tuple Methods & Conversions")

    print_box([
        "✅ Use TUPLE when data should NOT change",
        "✅ Use LIST  when data may change",
        "",
        "Tuples:  faster, hashable (can be dict keys or set elements)",
        "Lists:   mutable, more methods",
        "",
        "Common tuple uses: coordinates, RGB colours, DB records, function return values"
    ], C_INFO)

    pause()

    questions = [
        {
            "q": "Can you change an element of a tuple after creation?",
            "choices": ["Yes", "No", "Only the first element", "Only with .update()"],
            "a": "No",
            "hint": "Tuples are immutable.",
            "explain": "Attempting to change a tuple element raises a TypeError. Tuples are immutable by design."
        },
        {
            "q": "How do you create a single-element tuple?",
            "choices": ["(42)", "(42,)", "[42]", "tuple(42)"],
            "a": "(42,)",
            "hint": "Without the trailing comma, Python treats (42) as just an integer in parentheses.",
            "explain": "The trailing comma is essential: (42,) is a tuple; (42) is just the integer 42."
        },
        {
            "q": "What is tuple unpacking?",
            "choices": [
                "Converting a tuple to a list",
                "Assigning tuple elements to multiple variables at once",
                "Removing elements from a tuple",
                "Sorting a tuple"
            ],
            "a": "Assigning tuple elements to multiple variables at once",
            "hint": "Think: a, b, c = (1, 2, 3)",
            "explain": "x, y = (3, 7) assigns 3 to x and 7 to y simultaneously."
        },
        {
            "q": "How many built-in methods do tuples have?",
            "choices": ["None", "2 (count and index)", "Same as lists", "5"],
            "a": "2 (count and index)",
            "hint": "Tuples only have read-only operations.",
            "explain": "Tuples only expose .count() and .index() since they cannot be modified."
        },
        {
            "q": "What is the output of: a, b = b, a  when a=1, b=2?",
            "choices": ["a=1, b=2", "a=2, b=1", "Error", "a=2, b=2"],
            "a": "a=2, b=1",
            "hint": "Python packs the right side into a tuple first, then unpacks.",
            "explain": "b, a creates tuple (2, 1) on the right; then a gets 2 and b gets 1."
        },
    ]
    run_quiz(tracker, "Tuples", questions, passes_needed=3)

    exercises = [
        {
            "task": "What does (1, 2, 3).count(2) return?",
            "answers": ["1"],
            "hint": "2 appears exactly once in (1, 2, 3).",
            "solution": "(1, 2, 3).count(2)   # → 1"
        },
        {
            "task": "Create a valid Python single-element tuple containing the number 5.",
            "answers": ["(5,)", "5,"],
            "hint": "Don't forget the trailing comma!",
            "solution": "my_tuple = (5,)   # the comma makes it a tuple, not just (5)"
        },
    ]
    run_coding_exercise(tracker, "Tuples", exercises)
    tracker.complete_topic("Tuples")
    pause("Chapter 16 complete! 🎉 You've finished all chapters!")


# ──────────────────────────────────────────────────────────────────
# FINAL EXAM
# ──────────────────────────────────────────────────────────────────
def final_exam(tracker: ProgressTracker):
    clear_screen()
    print_header("🏆 FINAL EXAM — All Topics")
    slow_print("  Test everything you've learned in one ultimate quiz!", 0.025, C_WARN)
    print()

    all_questions = [
        {
            "q": "What keyword creates a function in Python?",
            "choices": ["function", "def", "func", "define"],
            "a": "def",
            "hint": "Short for 'define'.",
            "explain": "def is the keyword used to define functions in Python."
        },
        {
            "q": "What is the output of: print(10 // 3)?",
            "choices": ["3.33", "3", "4", "3.0"],
            "a": "3",
            "hint": "Floor division rounds DOWN.",
            "explain": "10 // 3 = 3 (floor division, integer result)."
        },
        {
            "q": "Which operator checks equality?",
            "choices": ["=", "==", "===", "!="],
            "a": "==",
            "hint": "Assignment vs comparison.",
            "explain": "== compares values. = assigns values."
        },
        {
            "q": "What type does input() always return?",
            "choices": ["int", "float", "str", "None"],
            "a": "str",
            "hint": "Even if you type a number, it comes back as text.",
            "explain": "input() always returns a string regardless of what the user types."
        },
        {
            "q": "What is 'Python'[-1]?",
            "choices": ["P", "n", "o", "Error"],
            "a": "n",
            "hint": "Negative index -1 = last character.",
            "explain": "Index -1 refers to the last character of the string."
        },
        {
            "q": "What does list.append(x) do?",
            "choices": [
                "Inserts x at index 0",
                "Adds x to the end",
                "Removes x",
                "Returns x"
            ],
            "a": "Adds x to the end",
            "hint": "Append = attach at the end.",
            "explain": "list.append(x) adds x as the new last element."
        },
        {
            "q": "What is range(1, 6) equivalent to?",
            "choices": ["[1,2,3,4,5,6]", "[1,2,3,4,5]", "[0,1,2,3,4,5]", "[1,6]"],
            "a": "[1,2,3,4,5]",
            "hint": "Stop value (6) is excluded.",
            "explain": "range(1,6) generates 1,2,3,4,5 — the stop is never included."
        },
        {
            "q": "What is the main difference between a list and a tuple?",
            "choices": [
                "Lists use () and tuples use []",
                "Lists are mutable; tuples are immutable",
                "Tuples can hold more items",
                "They are identical"
            ],
            "a": "Lists are mutable; tuples are immutable",
            "hint": "You cannot change items in a tuple.",
            "explain": "Lists support item assignment and modification; tuples are fixed after creation."
        },
        {
            "q": "What does 'not True and False' evaluate to?",
            "choices": ["True", "False", "None", "Error"],
            "a": "False",
            "hint": "Evaluate 'not True' first, then 'and False'.",
            "explain": "not True = False; False and False = False."
        },
        {
            "q": "What is the output of: [x for x in range(5) if x % 2 == 0]?",
            "choices": ["[1,3]", "[0,2,4]", "[0,1,2,3,4]", "[2,4]"],
            "a": "[0,2,4]",
            "hint": "range(5)=0..4, filter: only evens (x%2==0).",
            "explain": "0%2=0✓, 1%2≠0✗, 2%2=0✓, 3%2≠0✗, 4%2=0✓ → [0,2,4]."
        },
    ]

    random.shuffle(all_questions)
    selected = all_questions[:8]
    score    = 0

    for idx, q in enumerate(selected, 1):
        print(f"  {C_BOLD}Q{idx} of {len(selected)}:{C_RESET} {q['q']}\n")
        choices = q["choices"][:]
        random.shuffle(choices)
        for ci, ch in enumerate(choices, 1):
            print(f"    {C_WARN}{ci}.{C_RESET} {ch}")

        raw = get_input("Your answer (number): ")
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            user_ans = choices[int(raw) - 1]
            if user_ans.lower() == q["a"].lower():
                celebrate("Correct!")
                tracker.record_answer("Final Exam", True)
                score += 1
            else:
                print(f"  {C_ERROR}✗ Correct: {q['a']}{C_RESET}")
                print(f"  {C_INFO}💡 {q['explain']}{C_RESET}")
                tracker.record_answer("Final Exam", False)
        else:
            error_msg("Invalid choice — question skipped.")

        time.sleep(0.4)
        print_divider()

    # Final result
    pct = score / len(selected) * 100
    print_header("🎓 EXAM RESULTS")
    print(f"  {C_BOLD}Score: {score}/{len(selected)}  ({pct:.0f}%){C_RESET}\n")
    bar = progress_bar(score / len(selected), width=45, label="Final Exam")
    print(f"  {bar}\n")

    if pct >= 80:
        slow_print("  🏆 Outstanding! You're a Python beginner no more!", 0.03, C_SUCCESS)
    elif pct >= 60:
        slow_print("  ✅ Good job! Review a few chapters and you'll ace it!", 0.03, C_WARN)
    else:
        slow_print("  📚 Keep practising — every expert was once a beginner!", 0.03, C_INFO)
    print()


# ──────────────────────────────────────────────────────────────────
# REVISION FLASH CARDS
# ──────────────────────────────────────────────────────────────────
FLASH_CARDS = [
    ("What does % do?",        "Modulo — returns the remainder of division"),
    ("What is //",             "Floor division — divides and rounds DOWN"),
    ("What does ** do?",       "Exponentiation — raises to a power (2**3 = 8)"),
    ("len() does?",            "Returns the number of items in a sequence"),
    ("str() does?",            "Converts a value to a string"),
    ("int() does?",            "Converts to an integer (truncates floats)"),
    ("bool(0)?",               "False — zero is falsy"),
    ("bool('hello')?",         "True — non-empty string is truthy"),
    ("list.append(x)?",        "Adds x to the END of the list"),
    ("list.pop()?",            "Removes and returns the LAST element"),
    ("range(5)?",              "Generates 0,1,2,3,4 (5 is excluded)"),
    ("Tuple vs List?",         "Tuple = immutable (), List = mutable []"),
    ("input() returns?",       "Always a STRING"),
    ("== vs = ?",              "== compares values; = assigns"),
    ("not True?",              "False — 'not' flips the boolean"),
    ("Strings are mutable?",   "No! Strings are immutable in Python"),
    ("List comprehension?",    "[expr for item in iterable if condition]"),
    ("enumerate() ?",          "Returns (index, value) pairs when looping"),
    ("zip() ?",                "Combines multiple iterables into pairs"),
    ("break vs continue?",     "break exits loop; continue skips to next iteration"),
]

def run_flash_cards():
    clear_screen()
    print_header("🃏 FLASH CARDS — Quick Revision")
    slow_print("  Test your memory! Think of the answer before it's revealed.", 0.025, C_INFO)
    print()

    cards = FLASH_CARDS[:]
    random.shuffle(cards)
    selected = cards[:10]

    for i, (question, answer) in enumerate(selected, 1):
        print(f"  {C_BOLD}Card {i}/{len(selected)}{C_RESET}")
        print(f"  {C_WARN}❓ {question}{C_RESET}\n")
        pause("Think... then press Enter to reveal the answer")
        print(f"  {C_SUCCESS}✅ {answer}{C_RESET}\n")
        print_divider()
        time.sleep(0.3)

    print(f"\n  {C_SUCCESS}🎉 Flash card session complete!{C_RESET}\n")
    pause()


# ──────────────────────────────────────────────────────────────────
# WELCOME SCREEN
# ──────────────────────────────────────────────────────────────────
def show_welcome(tracker: ProgressTracker):
    clear_screen()
    title_art = r"""
  ██████╗ ██╗   ██╗████████╗██╗   ██╗████████╗ ██████╗ ██████╗
  ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗
  ██████╔╝ ╚████╔╝    ██║   ██║   ██║   ██║   ██║   ██║██████╔╝
  ██╔═══╝   ╚██╔╝     ██║   ██║   ██║   ██║   ██║   ██║██╔══██╗
  ██║        ██║      ██║   ╚██████╔╝   ██║   ╚██████╔╝██║  ██║
  ╚═╝        ╚═╝      ╚═╝    ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    """
    print(C_TITLE + title_art + C_RESET)
    print_box([
        "  🐍  PyTutor Pro — Your Personal Python Tutor  🐍  ",
        "",
        "  16 Chapters  •  80+ Questions  •  Interactive Practice",
        "  Flash Cards  •  Final Exam  •  Progress Tracking",
    ], C_TITLE)

    slow_print("  Welcome, future Python developer! 🚀", 0.03, C_SUCCESS)
    print()
    name = get_input("  What's your name? ")
    if name:
        print(f"\n  {C_SUCCESS}Great to meet you, {name}! Let's start your Python journey!{C_RESET}\n")
    print()
    print(f"  {C_INFO}📌 Quick Tips:{C_RESET}")
    print(f"     • Read explanations carefully — understanding > memorizing")
    print(f"     • Type your best answer even if unsure — you learn from mistakes")
    print(f"     • Use the Dashboard to track your progress")
    print(f"     • Complete all chapters before the Final Exam\n")

    if not COLORS_AVAILABLE:
        print(f"  {C_WARN}💡 Tip: Run 'pip install colorama' for colourful output!{C_RESET}\n")

    pause("Press Enter to enter the main menu...")
    return name


# ──────────────────────────────────────────────────────────────────
# CHAPTER MENU
# ──────────────────────────────────────────────────────────────────
CHAPTERS = [
    ("Chapter  1 — Variables",            chapter_variables),
    ("Chapter  2 — Print Function",       chapter_print),
    ("Chapter  3 — Type Conversion",      chapter_type_conversion),
    ("Chapter  4 — User Input",           chapter_user_input),
    ("Chapter  5 — Strings",              chapter_strings),
    ("Chapter  6 — Arithmetic",           chapter_arithmetic),
    ("Chapter  7 — Operator Precedence",  chapter_precedence),
    ("Chapter  8 — Comparison Operators", chapter_comparison),
    ("Chapter  9 — Logical Operators",    chapter_logical),
    ("Chapter 10 — If Statements",        chapter_if_statements),
    ("Chapter 11 — While Loops",          chapter_while_loops),
    ("Chapter 12 — Lists",                chapter_lists),
    ("Chapter 13 — List Methods",         chapter_list_methods),
    ("Chapter 14 — For Loops",            chapter_for_loops),
    ("Chapter 15 — Range Function",       chapter_range),
    ("Chapter 16 — Tuples",               chapter_tuples),
]

def show_chapter_menu(tracker: ProgressTracker):
    clear_screen()
    print_header("📚 CHAPTER MENU")
    print(f"  {C_INFO}Choose a chapter to study or practice:{C_RESET}\n")
    for i, (title, _) in enumerate(CHAPTERS, 1):
        topic_key = title.split("—")[1].strip()
        done = any(topic_key.lower() in ct.lower() for ct in tracker.completed_topics)
        status = f"{C_SUCCESS}✅{C_RESET}" if done else f"{C_WARN}📖{C_RESET}"
        print(f"  {status} {C_BOLD}{i:>2}.{C_RESET} {title}")
    print()
    print(f"  {C_DIM}17. 🏠 Back to main menu{C_RESET}\n")

    raw = get_input("Choose chapter number: ")
    if raw == "17" or raw.lower() in ("q", "back", "menu"):
        return
    if raw.isdigit() and 1 <= int(raw) <= len(CHAPTERS):
        idx = int(raw) - 1
        CHAPTERS[idx][1](tracker)
    else:
        error_msg("Please enter a valid chapter number.")


def show_main_menu(tracker: ProgressTracker, student_name: str):
    while True:
        clear_screen()
        print_header("🐍 PyTutor Pro — Main Menu")
        completed = len(tracker.completed_topics)
        total     = len(ProgressTracker.ALL_TOPICS)
        bar = progress_bar(completed / total, width=40, label=f"{completed}/{total} topics")
        print(f"  {bar}\n")
        print(f"  {C_SUCCESS}Welcome back, {student_name}!{C_RESET}  "
              f"Streak: {C_WARN}🔥 {tracker.current_streak}{C_RESET}  "
              f"Accuracy: {C_INFO}{tracker.accuracy():.0f}%{C_RESET}\n")

        options = [
            "📚  Study a Chapter",
            "🃏  Flash Cards (Quick Revision)",
            "🏆  Final Exam (All Topics)",
            "📊  View My Dashboard",
            "🚀  Sequential Course (Start → Finish)",
            "❌  Exit",
        ]
        for i, opt in enumerate(options, 1):
            print(f"  {C_WARN}{i}.{C_RESET} {opt}")
        print()

        choice = get_input("Choose an option (1-6): ")
        if choice == "1":
            show_chapter_menu(tracker)
        elif choice == "2":
            run_flash_cards()
        elif choice == "3":
            final_exam(tracker)
        elif choice == "4":
            tracker.show_dashboard()
            pause()
        elif choice == "5":
            run_sequential_course(tracker)
        elif choice == "6":
            goodbye(tracker, student_name)
            break
        else:
            error_msg("Please enter 1–6.")


def run_sequential_course(tracker: ProgressTracker):
    """Walk through ALL chapters in order."""
    clear_screen()
    print_header("🚀 SEQUENTIAL COURSE MODE")
    slow_print("  I'll guide you through all 16 chapters in order!", 0.025, C_INFO)
    print()
    start_idx = len(tracker.completed_topics)
    # Try to resume from where they left off
    if start_idx > 0:
        info_msg(f"Resuming from Chapter {start_idx + 1}...")
    pause()

    for i, (title, fn) in enumerate(CHAPTERS[start_idx:], start_idx + 1):
        clear_screen()
        print(f"\n  {C_BOLD}Starting {title}...{C_RESET}\n")
        animate_loading(f"Loading {title}")
        fn(tracker)
        if not yes_no("\n  Continue to the next chapter?"):
            info_msg("Progress saved! You can resume anytime from the main menu.")
            pause()
            break

    else:
        # Completed all chapters
        clear_screen()
        print_header("🎓 COURSE COMPLETE!")
        slow_print("  You've completed ALL 16 chapters! Amazing work! 🏆", 0.03, C_SUCCESS)
        print()
        if yes_no("  Ready for the Final Exam?"):
            final_exam(tracker)


def goodbye(tracker: ProgressTracker, name: str):
    clear_screen()
    print_header("👋 Goodbye!")
    tracker.show_dashboard()
    elapsed = tracker.elapsed_minutes()
    completed = len(tracker.completed_topics)

    slow_print(f"  Thanks for studying with PyTutor Pro, {name}!", 0.025, C_SUCCESS)
    print()
    print(f"  {C_INFO}📊 Session Summary:{C_RESET}")
    print(f"     ⏱  {elapsed:.1f} minutes of focused learning")
    print(f"     📚  {completed} chapters completed")
    print(f"     ✅  {tracker.correct_answers}/{tracker.total_questions} questions answered correctly")
    print(f"     🔥  Best streak: {tracker.best_streak}")
    print()
    slow_print("  Keep coding every day — consistency is the secret! 🐍", 0.025, C_WARN)
    print()
    print_box([
        "💡 Next Steps:",
        "  1. Build a small project using what you've learned",
        "  2. Explore: functions, dictionaries, file I/O",
        "  3. Try: LeetCode Easy problems",
        "  4. Read: docs.python.org",
    ], C_SUCCESS)
    print()
    slow_print("  Happy coding! 🚀", 0.04, C_TITLE)
    print()


# ──────────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────────
def main():
    try:
        tracker      = ProgressTracker()
        student_name = show_welcome(tracker)
        show_main_menu(tracker, student_name or "Learner")
    except KeyboardInterrupt:
        print(f"\n\n  {C_WARN}Session interrupted. Your progress was tracked in this session.{C_RESET}")
        print(f"  {C_SUCCESS}Keep learning — see you next time! 👋{C_RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()