#!/usr/bin/env python3
"""Missed deadline excuse: check the fixed entry, then write it out.

The work was finished on time, just in a timezone that has not
arrived yet. This program never accepts outside text: it holds exactly
one excuse, proves that excuse is well formed, and saves it to a file.
There is no input, no network access, no clock, and no randomness
anywhere in here.
"""

import sys

ENTRY = "I finished the work on time. The time was just in a different timezone, and it has not arrived yet."
CHAR_LIMIT = 200
DESTINATION = "/output/entry.txt"
ENDERS = (".", "!", "?")
FILLER = set(".,!?;:'\"-() ")


def fail(problem):
    """Print why the entry was refused and stop without writing."""
    print(f"refused: {problem}", file=sys.stderr)
    raise SystemExit(1)


def guard_nonempty(text):
    return bool(text and text.strip())


def guard_short_enough(text):
    return len(text) <= CHAR_LIMIT


def guard_no_controls(text):
    return all(ord(letter) >= 32 for letter in text)


def guard_tidy_spacing(text):
    stripped = text.strip()
    return text == stripped and "  " not in text and "\t" not in text


def guard_has_letters(text):
    return any(letter.isalpha() for letter in text)


def guard_not_only_marks(text):
    return not all(letter in FILLER for letter in text)


def guard_not_only_digits(text):
    return not text.strip().isdigit()


def guard_ends_with_mark(text):
    return text.rstrip().endswith(ENDERS)


def guard_names_timezone(text):
    return "timezone" in text.lower()


def guard_no_apology(text):
    # A good excuse never apologises; it reframes.
    return "sorry" not in text.lower()


def guard_no_links(text):
    # An excuse stands on its own; it does not point at a website.
    lowered = text.lower()
    return "http://" not in lowered and "https://" not in lowered and "www." not in lowered


# Every guard is listed with the complaint shown when it trips. The
# checker runs them in this order and stops at the first failure, so a
# bad entry never reaches the file.
RULES = [
    ("entry must mention a timezone", guard_names_timezone),
    ("entry must not apologise", guard_no_apology),
    ("entry must not contain a web link", guard_no_links),
    ("entry is empty", guard_nonempty),
    ("entry is longer than the 200 character limit", guard_short_enough),
    ("entry contains control characters", guard_no_controls),
    ("entry has ragged spacing or a tab", guard_tidy_spacing),
    ("entry contains no letters", guard_has_letters),
    ("entry is punctuation only", guard_not_only_marks),
    ("entry is digits only", guard_not_only_digits),
    ("entry does not end with punctuation", guard_ends_with_mark),
]


def check_entry(text):
    for problem, guard in RULES:
        if not guard(text):
            fail(problem)


def main():
    check_entry(ENTRY)
    with open(DESTINATION, "w", encoding="utf-8") as out:
        out.write(ENTRY + "\n")


if __name__ == "__main__":
    main()
