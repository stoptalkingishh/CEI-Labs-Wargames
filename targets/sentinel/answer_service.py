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


def fail():
    print("invalid structured answer", file=sys.stderr)
    raise SystemExit(1)


def release(submission, caller, answers, credentials):
    if not isinstance(submission, dict):
        fail()
    lab = submission.get("lab")
    answer = submission.get("answer")
    if not isinstance(lab, str) or not isinstance(answer, dict):
        fail()
    if LAB_USERS.get(lab) != caller or lab not in answers or answer != answers[lab]:
        fail()
    return credentials[lab]


def main():
    try:
        submission = json.load(sys.stdin)
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
