#!/usr/bin/env python3
"""
VSWorlde — a Wordle-like terminal game inspired by the popular word-guessing game.

This implementation intentionally avoids copying proprietary assets or data.
It implements the core gameplay: guess a 5-letter word in 6 tries with
feedback shown as colored emoji squares.

Run: python3 VSWorlde.py
For a quick automated check: python3 VSWorlde.py --selftest
"""
from __future__ import annotations
import argparse
import random
import sys
from typing import List, Tuple
import os

# A curated small set of possible solutions (all lowercase, 5 letters).
# This list is intentionally limited to avoid reproducing any proprietary list.
SOLUTIONS = [
    "apple", "grace", "plane", "crane", "stone", "light", "glass", "flame",
    "pride", "brave", "shard", "shoes", "prism", "civic", "rally", "karma",
    "honey", "bling", "mango", "charm", "fleet", "quota", "input", "zesty",
    "dance", "eagle", "fable", "gamer", "hippo", "jazzy", "kayak", "linen"
]

# An allowed guesses set — include the solutions plus some extras.
ALLOWED = set(SOLUTIONS) | {
    "about", "other", "which", "their", "there", "would", "these",
    "brown", "quick", "zebra", "vivid", "young", "quiet", "pound",
    "bound", "stony", "slope", "pride", "trace"
}


def _augment_from_system_dict():
    """Try to augment `ALLOWED` with 5-letter words from common system dictionaries.

    This avoids shipping huge word lists in the repo while still giving a
    much larger set of allowed guesses when the system dictionary exists.
    """
    dict_paths = [
        "/usr/share/dict/words",
        "/usr/dict/words",
        "/usr/dict/web2",
        "/usr/share/dict/web2",
    ]
    found = False
    for p in dict_paths:
        if os.path.exists(p):
            found = True
            try:
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        w = line.strip().lower()
                        if len(w) == 5 and w.isalpha():
                            ALLOWED.add(w)
            except OSError:
                # ignore unreadable system dicts
                pass
    # Also, if the project includes a `wordlists` folder with plain files,
    # load any 5-letter words found there.
    local_dir = os.path.join(os.path.dirname(__file__), "wordlists")
    if os.path.isdir(local_dir):
        for fname in os.listdir(local_dir):
            fpath = os.path.join(local_dir, fname)
            if os.path.isfile(fpath):
                try:
                    with open(fpath, encoding="utf-8", errors="ignore") as fh:
                        for line in fh:
                            w = line.strip().lower()
                            if len(w) == 5 and w.isalpha():
                                ALLOWED.add(w)
                except OSError:
                    pass


# Attempt to augment allowed guesses from available dictionaries.
_augment_from_system_dict()

GREEN = "🟩"
YELLOW = "🟨"
BLACK = "⬛"


def grade_guess(solution: str, guess: str) -> List[str]:
    """
    Return feedback per letter as a list of emoji strings.

    Implements the standard counting algorithm used in word-guessing games
    so duplicate letters are handled correctly.
    """
    solution = solution.lower()
    guess = guess.lower()
    if len(solution) != len(guess):
        raise ValueError("solution and guess must be same length")

    feedback = [BLACK] * len(guess)
    # Track letters in solution that haven't been matched as greens
    remaining = {}
    for i, ch in enumerate(solution):
        if guess[i] == ch:
            feedback[i] = GREEN
        else:
            remaining[ch] = remaining.get(ch, 0) + 1

    # Second pass: mark yellows where appropriate
    for i, ch in enumerate(guess):
        if feedback[i] == GREEN:
            continue
        if remaining.get(ch, 0) > 0:
            feedback[i] = YELLOW
            remaining[ch] -= 1

    return feedback


def play_interactive(solution: str | None = None) -> None:
    solution = (solution or random.choice(SOLUTIONS)).lower()
    length = len(solution)
    max_guesses = 6

    print("Welcome to VSWorlde — guess the 5-letter word!")
    print(f"You have {max_guesses} guesses. Feedback: {GREEN}=correct, {YELLOW}=present, {BLACK}=absent")
    # For debugging or test mode, the caller may pass solution explicitly.
    # (When playing normally, solution is not shown.)

    for attempt in range(1, max_guesses + 1):
        while True:
            guess = input(f"Guess {attempt}/{max_guesses}: ").strip().lower()
            if len(guess) != length:
                print(f"Please enter a {length}-letter word.")
                continue
            if guess not in ALLOWED:
                print("Word not in allowed list. Try another word.")
                continue
            break

        feedback = grade_guess(solution, guess)
        print("".join(feedback))
        if all(s == GREEN for s in feedback):
            print(f"Nice! You guessed the word in {attempt} guesses.")
            return

    print(f"Out of guesses — the word was: {solution}")


def _selftest() -> None:
    """Run a few deterministic checks on grading logic."""
    tests: List[Tuple[str, str, str]] = [
        ("apple", "apple", GREEN * 5),
        ("crane", "crate", GREEN + GREEN + GREEN + BLACK + GREEN),
        ("arrow", "rarer", YELLOW + YELLOW + GREEN + BLACK + BLACK),
        ("sense", "seeds", GREEN + GREEN + YELLOW + BLACK + YELLOW),
    ]

    for sol, guess, expected_str in tests:
        fb = grade_guess(sol, guess)
        got = "".join(fb)
        if got != expected_str:
            print("Self-test failed")
            print("Solution:", sol)
            print("Guess:", guess)
            print("Expected:", expected_str)
            print("Got:     ", got)
            sys.exit(2)

    print("All self-tests passed.")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="VSWorlde")
    parser.add_argument("--selftest", action="store_true", help="run internal self-tests and exit")
    parser.add_argument("--word", type=str, help="force the solution word (for testing)")
    parser.add_argument("--seed", type=int, help="random seed for deterministic runs")
    args = parser.parse_args(argv)

    if args.seed is not None:
        random.seed(args.seed)

    if args.selftest:
        _selftest()
        return 0

    forced = None
    if args.word:
        w = args.word.strip().lower()
        if len(w) != 5:
            print("--word must be a 5-letter word")
            return 2
        forced = w

    try:
        play_interactive(forced)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
