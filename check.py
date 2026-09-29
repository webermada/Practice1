"""CS 1430 Practice 1 checker.

Run this file to check your work:   python check.py

Fix the FIRST line that says FAIL, save, and run this file again.
You do not need to read or change anything in this file.
"""

import ast
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAIN = HERE / "main.py"

# Each run feeds main.py a number and a phrase, like a person typing them.
# The phrases are odd on purpose so they can't show up by accident in a prompt.
TEST_RUNS = [(4, "Zork"), (7, "Pio!")]

LOOP_NODES = (ast.For, ast.While, ast.AsyncFor,
              ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


# ---------------------------------------------------------------- output

def _use_color():
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return False
    if os.name == "nt":
        os.system("")  # turns on color codes in the Windows terminal
    return True


COLOR = _use_color()


def _paint(text, code):
    return f"\033[{code}m{text}\033[0m" if COLOR else text


LABELS = {
    "PASS": _paint("[PASS]", "32"),
    "FAIL": _paint("[FAIL]", "31"),
    "SKIP": _paint("[ -- ]", "90"),
}


class Report:
    def __init__(self):
        self.first_fail_shown = False
        self.failed = False

    def heading(self, text):
        print()
        print(_paint(text, "1"))

    def line(self, status, text, hint=""):
        print(f"  {LABELS[status]} {text}")
        if status == "FAIL":
            self.failed = True
            if hint and not self.first_fail_shown:
                for hint_line in hint.strip().splitlines():
                    print(_paint(f"         > {hint_line}", "33"))
            self.first_fail_shown = True


# ---------------------------------------------------------------- helpers

def run_git(*args, timeout=20):
    """Run a git command in this folder. Returns (ok, output)."""
    try:
        result = subprocess.run(
            ["git", *args], cwd=HERE, capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace",
        )
    except (OSError, subprocess.TimeoutExpired) as err:
        return False, str(err)
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def run_main(number, phrase):
    """Run main.py, typing the number and phrase. Returns (returncode, stdout, stderr)."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        result = subprocess.run(
            [sys.executable, str(MAIN)], cwd=HERE, input=f"{number}\n{phrase}\n",
            capture_output=True, text=True, timeout=10, env=env,
            encoding="utf-8", errors="replace",
        )
    except subprocess.TimeoutExpired:
        return None, "", "timeout"
    return result.returncode, result.stdout, result.stderr


def explain_crash(stderr):
    last = stderr.strip().splitlines()[-1] if stderr.strip() else "(no message)"
    if "invalid literal for int()" in last:
        return ("Your program tried to turn the PHRASE into an int.\n"
                "Ask for the number first, then the phrase.\n"
                f"Python said: {last}")
    if last.startswith("EOFError"):
        return ("Your program asked for input more than two times.\n"
                "It should ask exactly twice: the number, then the phrase.")
    if "can't multiply sequence by non-int" in last:
        return ("You multiplied the phrase by text, not a number.\n"
                "Wrap the number's input() in int( ... ).\n"
                f"Python said: {last}")
    return f"main.py crashed. The last line of the error was:\n{last}"


def calls_named(tree, name):
    return [n for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id == name]


# ---------------------------------------------------------------- checks

def check_code(report):
    report.heading("Toolchain")
    version = ".".join(str(p) for p in sys.version_info[:3])
    report.line("PASS", f"Python is installed ({version})")

    if not MAIN.exists():
        report.line("FAIL", "main.py is in this folder",
                    "Use File > Open Folder and open the whole Practice1 folder,\n"
                    "not a single file.")
        return
    report.line("PASS", "main.py is in this folder")

    report.heading("Your code")
    source = MAIN.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(source)
    except SyntaxError as err:
        report.line("FAIL", "main.py has no syntax errors",
                    f"Python can't read line {err.lineno}: {err.msg}\n"
                    "Look for a missing quote, parenthesis, or colon on that line.")
        for text in ("You ask for input twice", "You turn the number into an int",
                     "You use * to repeat the phrase", "You did not use a loop",
                     "main.py runs", "The phrase repeats the right number of times"):
            report.line("SKIP", text)
        return
    report.line("PASS", "main.py has no syntax errors")

    if not tree.body:
        report.line("FAIL", "main.py has code in it",
                    "main.py only has the header comment so far.\n"
                    "Write your code below it. README.md explains what to write.")
        return
    report.line("PASS", "main.py has code in it")

    inputs = len(calls_named(tree, "input"))
    if inputs >= 2:
        report.line("PASS", "You ask for input twice")
    else:
        report.line("FAIL", "You ask for input twice",
                    f"Found {inputs} input() call(s). You need two:\n"
                    "one for the number, one for the phrase.")

    if calls_named(tree, "int"):
        report.line("PASS", "You turn the number into an int")
    else:
        report.line("FAIL", "You turn the number into an int",
                    "input() always gives you text, even when someone types 5.\n"
                    "Wrap the number's input() in int( ... ) so Python can multiply by it.")

    has_times = any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult)
                    for n in ast.walk(tree))
    if has_times:
        report.line("PASS", "You use * to repeat the phrase")
    else:
        report.line("FAIL", "You use * to repeat the phrase",
                    "Repeat the phrase with the * symbol: phrase times number.")

    loops = [n for n in ast.walk(tree) if isinstance(n, LOOP_NODES)]
    if loops:
        where = ", ".join(str(n.lineno) for n in loops)
        report.line("FAIL", "You did not use a loop",
                    f"Found a loop on line {where}.\n"
                    "This practice is about the * operator. Take the loop out\n"
                    "and let * do the repeating.")
    else:
        report.line("PASS", "You did not use a loop")

    number, phrase = TEST_RUNS[0]
    code, out, err = run_main(number, phrase)
    if code is None:
        report.line("FAIL", "main.py runs",
                    "main.py was still running after 10 seconds.\n"
                    "Make sure it asks for input only twice and has no loop.")
        report.line("SKIP", "The phrase repeats the right number of times")
        return
    if code != 0:
        report.line("FAIL", "main.py runs", explain_crash(err))
        report.line("SKIP", "The phrase repeats the right number of times")
        return
    report.line("PASS", f"main.py runs (typed {number} and {phrase})")

    for number, phrase in TEST_RUNS:
        code, out, err = run_main(number, phrase)
        found = out.count(phrase)
        if code != 0 or found != number:
            detail = explain_crash(err) if code != 0 else (
                f"Typed {number} and {phrase}. Expected {phrase} {number} times,\n"
                f"but it showed up {found} time(s).\n"
                "Print only the repeated phrase. Don't print the phrase by itself too.")
            report.line("FAIL", "The phrase repeats the right number of times", detail)
            return
    report.line("PASS", "The phrase repeats the right number of times")


def check_git(report):
    report.heading("Git and GitHub")

    if not shutil.which("git"):
        report.line("FAIL", "Git is installed",
                    "Close every terminal, then close and reopen VS Code.\n"
                    "If that doesn't fix it, reinstall Git from Assignment 1.")
        for text in ("This folder is a Git repository", "Your copy is on your own GitHub account",
                     "Your code is committed", "Your commit is pushed to GitHub"):
            report.line("SKIP", text)
        return
    report.line("PASS", "Git is installed")

    ok, _ = run_git("rev-parse", "--is-inside-work-tree")
    if not ok:
        report.line("FAIL", "This folder is a Git repository",
                    "This folder wasn't cloned with git clone.\n"
                    "Did you download the ZIP? Go back to step 2 in README.md.")
        for text in ("Your copy is on your own GitHub account",
                     "Your code is committed", "Your commit is pushed to GitHub"):
            report.line("SKIP", text)
        return
    report.line("PASS", "This folder is a Git repository")

    ok, url = run_git("config", "--get", "remote.origin.url")
    if not ok or "github.com" not in url.lower():
        report.line("FAIL", "Your copy is on your own GitHub account",
                    "This folder isn't connected to GitHub.\n"
                    "Go back to step 2 in README.md and clone YOUR copy.")
        report.line("SKIP", "Your code is committed")
        report.line("SKIP", "Your commit is pushed to GitHub")
        return
    if "github.com/cs1430/" in url.lower() or "github.com:cs1430/" in url.lower():
        report.line("FAIL", "Your copy is on your own GitHub account",
                    "You cloned the CLASS template, not your own copy.\n"
                    "Go back to step 1 in README.md: Use this template > Create a new repository.")
        report.line("SKIP", "Your code is committed")
        report.line("SKIP", "Your commit is pushed to GitHub")
        return
    report.line("PASS", "Your copy is on your own GitHub account")

    ok_root, roots = run_git("rev-list", "--max-parents=0", "HEAD")
    ok_status, status = run_git("status", "--porcelain", "--", "main.py")
    changed_since_template = False
    if ok_root and roots:
        root = roots.splitlines()[0]
        same, _ = run_git("diff", "--quiet", root, "HEAD", "--", "main.py")
        changed_since_template = not same
    if ok_status and status:
        report.line("FAIL", "Your code is committed",
                    "main.py has changes that aren't committed yet.\n"
                    "Save (Ctrl+S), then in Source Control type a message and click Commit.")
        report.line("SKIP", "Your commit is pushed to GitHub")
        return
    if not changed_since_template:
        report.line("FAIL", "Your code is committed",
                    "Your code isn't in a commit yet. Save (Ctrl+S), then in\n"
                    "Source Control type a message and click Commit.")
        report.line("SKIP", "Your commit is pushed to GitHub")
        return
    report.line("PASS", "Your code is committed")

    ok_local, local = run_git("rev-parse", "HEAD")
    ok_remote, remote = run_git("ls-remote", "origin", "HEAD", timeout=30)
    if not ok_remote:
        report.line("FAIL", "Your commit is pushed to GitHub",
                    "Could not reach GitHub to check. Make sure you're online,\n"
                    "then run this file again.")
        return
    remote_sha = remote.split()[0] if remote else ""
    if ok_local and local == remote_sha:
        report.line("PASS", "Your commit is pushed to GitHub")
    else:
        report.line("FAIL", "Your commit is pushed to GitHub",
                    "Committing saves your work on this computer. PUSH sends it\n"
                    "to GitHub. Click Sync Changes (or run git push), then run this file again.")


def main():
    print(_paint("CS 1430 Practice 1 checker", "1"))
    report = Report()
    check_code(report)
    check_git(report)
    print()
    if report.failed:
        print("Fix the FIRST line that says FAIL, save, and run this file again.")
    else:
        print(_paint("All checks passed. Practice 1 is done.", "32"))


if __name__ == "__main__":
    main()
