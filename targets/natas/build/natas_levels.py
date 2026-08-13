"""Shared Natas range definitions used by target build and runtime tooling."""

FIRST_LEVEL = 0
LAST_LEVEL = 34
LEVELS = range(FIRST_LEVEL, LAST_LEVEL + 1)
WEBPASS_LEVELS = range(1, LAST_LEVEL + 1)
# The deployed 0-14 CTFd contract terminates at Natas 14. The later webpass
# keys are reserved for future scenarios, but cannot replace this final flag
# until the atomic 36-challenge expansion changes the release contract.
TERMINAL_SECRET_KEY = "natas14final"
REQUIRED_SECRET_KEYS = frozenset(
    ["natas%d" % level for level in WEBPASS_LEVELS] + [TERMINAL_SECRET_KEY]
)

FOUNDATION_TITLES = {
    0: "View Source", 1: "Right-Click Block", 2: "Directory Traversal (Files)",
    3: "Web Crawlers (Robots.txt)", 4: "Referer Spoofing", 5: "Cookie Manipulation",
    6: "Hidden Inclusion Files", 7: "Local File Inclusion (LFI)",
    8: "Reversing Crypto Schemes", 9: "Command Injection I",
    10: "Command Injection II (Sanitization Bypass)", 11: "XOR Encryption Bypass",
    12: "Arbitrary File Upload (Web Shell)", 13: "File Upload Bypass (Magic Bytes)",
    14: "SQL Injection (SQLi)", 15: "Boolean Response Oracle",
    16: "Denylist Search Emulator", 17: "Timing Response Oracle",
    18: "Predictable Numeric Sessions", 19: "Encoded Weak Session Token",
    20: "Delimited Session Record", 21: "Cross-Route Session Trust",
    22: "Redirect Execution Mismatch", 23: "Toy Numeric Prefix Comparison",
    24: "Request Shape Confusion", 25: "Synthetic Audit Resolver",
    26: "JSON Export Model", 27: "Identity Normalization Model",
    28: "Visual Block Token Model", 29: "Virtual Command Catalog",
}


def title(level):
    return FOUNDATION_TITLES.get(level, "Scenario Pending")


def port(level):
    return 8000 + level
