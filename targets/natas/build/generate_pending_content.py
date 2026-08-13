"""Generate intentionally inert authenticated pages for unreleased levels."""
from pathlib import Path

from natas_levels import LAST_LEVEL


def main(root):
    root = Path(root)
    # Batch C supplies real scenarios through level 29.  Leave later range
    # foundation endpoints inert until their corresponding implementation.
    for level in range(30, LAST_LEVEL + 1):
        directory = root / ("natas%d" % level)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.php").write_text(
            "<!doctype html><html><head><title>Natas %d</title></head>"
            "<body><h1>Natas %d</h1>"
            "<p>SCENARIO_PENDING: Level content is intentionally not implemented yet.</p>"
            "<p>This marker is not a password, flag, or secret.</p></body></html>\n" % (level, level),
            encoding="ascii",
        )


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
