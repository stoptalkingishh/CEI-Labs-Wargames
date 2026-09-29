"""Shared account-progression note for the staged (per-instance) tracks.

Bandit and Krypton both run a "solve, then switch to the next account on the
same instance" chain, and both shipped a copy of the same function. Only four
things actually differ between the two tracks' versions:

  * `prefix`       -- Krypton separates the note with a `\\n\\n---\\n\\n`
                     horizontal rule; Bandit goes straight into the heading.
  * `account`      -- the per-level account name stem (`bandit` / `krypton`).
  * `track`        -- the human-facing track name for the finish-line text.
  * `final_level`  -- the last level in the chain (33 / 6).

The start-here body is *not* parameterised from a template: each track's
opening note genuinely says different things (Bandit points at the launch
panel, Krypton at Base64), so it is passed through verbatim.

Callers in the builders keep a one-line `_progression_note(challenge_id)`
wrapper that supplies their own track's parameters.
"""


def progression_note(
    challenge_id: str,
    *,
    prefix: str,
    account: str,
    track: str,
    final_level: int,
    start_here_id: str,
    start_here_body: str,
) -> str:
    """Return the trailing account-transition section (heading + body)."""
    if challenge_id == start_here_id:
        return f"{prefix}### Up next\n{start_here_body}"

    level = int(challenge_id.rsplit("-", 1)[1])
    if level == final_level:
        return (
            f"{prefix}### Finish line\n"
            f"You are working as `{account}{level}`. Submit the recovered "
            f"password here to complete the {track} track; no further account switch is required."
        )

    return (
        f"{prefix}### Moving on\n"
        f"You are working as `{account}{level}`. After "
        "recovering and submitting this password, exit and reconnect as "
        f"`{account}{level + 1}` at the host and port shown by the launch panel, using the "
        "recovered password, before starting the next level."
    )
