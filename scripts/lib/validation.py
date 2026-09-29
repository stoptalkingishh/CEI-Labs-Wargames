"""Shared fail-loud assertion for the build scripts' self-validators.

bandit / krypton / natas each carried their own three-line `_require`; this
is the single copy. A builder that validates its own authored data (hint
tier counts, missing challenge ids, malformed flag shapes) must raise rather
than emit a subtly wrong challenge -- `check_inventory_sync.py` and
`validate_generated.py` are downstream of that guarantee.
"""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)
