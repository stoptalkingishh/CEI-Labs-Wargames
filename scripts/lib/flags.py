"""Shared renderer for a challenge's `flags:` block in generated challenge YAML.

Every staged track (bandit / krypton / natas) emitted its own byte-identical
copy of this function; the copies had already drifted apart in their
docstrings, which is exactly the failure mode this module removes.

Note the docstring below deliberately mentions BOTH dynamic flag type names:
`per_team_dynamic` (krypton / natas / sentinel) and `per_team_dynamic_fixed`
(bandit). That distinction is real, but it lives in the authored `flag` dicts
in each builder -- the rendering below is one code path for all of them.
"""


def flags_yaml(flag) -> str:
    """A challenge's `flag` field is either a plain string (the historical
    shorthand -- ctfcli treats it as a static, case-sensitive flag) or a
    dict (per_team_dynamic, per_team_dynamic_fixed, and any future
    non-static type) -- ctfcli's _create_flags() POSTs a non-string entry to
    /api/v1/flags verbatim, so the dict's keys must already match that API's
    real fields (type/content/data)."""
    if isinstance(flag, dict):
        lines = [f"  - type: {flag['type']}\n"]
        lines.append(f"    content: \"{flag['content']}\"\n")
        if "data" in flag:
            lines.append(f"    data: \"{flag['data']}\"\n")
        return "".join(lines)
    return f'  - "{flag}"\n'
