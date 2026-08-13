#!/usr/bin/env python3
"""Validate a local structured answer and release one per-team credential."""

import json
import sys

LAB_USERS = {
    "sentinel-start-here": "sentinel0",
    "sentinel-01": "sentinel0",
    "sentinel-02": "sentinel1",
    "sentinel-03": "sentinel2",
    "sentinel-04": "sentinel3",
    "sentinel-05": "sentinel4",
}
MAX_SUBMISSION_BYTES = 65536


def fail():
    print("invalid structured answer", file=sys.stderr)
    raise SystemExit(1)


def matches_expected(value, expected):
    if type(value) is not type(expected):
        return False
    if isinstance(expected, dict):
        return value.keys() == expected.keys() and all(matches_expected(value[key], expected[key]) for key in expected)
    if isinstance(expected, list):
        return len(value) == len(expected) and all(matches_expected(item, expected_item) for item, expected_item in zip(value, expected))
    return value == expected


def release(submission, caller, answers, credentials):
    if not isinstance(submission, dict):
        fail()
    lab = submission.get("lab")
    answer = submission.get("answer")
    if not isinstance(lab, str) or not isinstance(answer, dict):
        fail()
    if LAB_USERS.get(lab) != caller or lab not in answers or not matches_expected(answer, answers[lab]):
        fail()
    return credentials[lab]


def main():
    try:
        raw_submission = sys.stdin.buffer.read(MAX_SUBMISSION_BYTES + 1)
        if len(raw_submission) > MAX_SUBMISSION_BYTES:
            fail()
        submission = json.loads(raw_submission)
        if len(sys.argv) != 2:
            fail()
        with open("/var/lib/sentinel/answers.json", encoding="utf-8") as source:
            answers = json.load(source)
        with open("/var/lib/sentinel/credentials.json", encoding="utf-8") as source:
            credentials = json.load(source)
        print(release(submission, sys.argv[1], answers, credentials))
    except (KeyError, OSError, ValueError, json.JSONDecodeError, TypeError):
        fail()


if __name__ == "__main__":
    main()
