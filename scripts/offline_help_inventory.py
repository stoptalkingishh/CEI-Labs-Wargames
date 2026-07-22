"""Tier-one command inventory; generator literals are read without execution."""
import ast, re, shlex
from pathlib import Path

def load_literal_assignment(path, name):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError("missing literal assignment: " + name)

def bandit_classifications(path=Path(__file__).with_name("build_bandit.py")):
    approved = load_literal_assignment(path, "APPROVED_TIER_ONE")
    expected = {"bandit-%02d" % level for level in range(34)}
    if set(approved) != expected: raise ValueError("Bandit Tier-1 coverage mismatch")
    entries=[]
    for challenge_id,(text,package) in approved.items():
        if package is None:
            entries.append({"challenge_ids":[challenge_id],"not_applicable":"non-command Tier-1 guidance"}); continue
        match=re.fullmatch(r"`([^`]+)`\.", text)
        if not match: raise ValueError("invalid command hint: " + challenge_id)
        package = {"util-linux (base image)":"util-linux", "base image":"bash"}.get(package, package)
        entries.append({"challenge_ids":[challenge_id],"argv":shlex.split(match.group(1)),"runtime":"bandit-target","package":package})
    return entries
INVENTORY=[
 {"id":"natas-curl","challenge_ids":["natas-00","natas-01","natas-02","natas-04","natas-05"],"argv":["curl","--help"],"runtime":"kali-attacker","image":"registry.invalid/kali@sha256:"+"0"*64},
]
NOT_APPLICABLE={"bandit-19","krypton-01","krypton-02","krypton-03","krypton-04","krypton-05","natas-03","natas-06","natas-07","natas-08","natas-09","natas-10","natas-11","natas-12","natas-13","natas-14"}

KRYPTON_CLASSIFICATIONS = [
 {"challenge_ids":["krypton-00"],"argv":["base64","--help"],"runtime":"krypton-target","package":"coreutils"},
 {"challenge_ids":["krypton-06"],"argv":["xxd","--help"],"runtime":"krypton-target","package":"xxd"},
 *[{"challenge_ids":["krypton-%02d" % n],"not_applicable":"cipher/topic guidance"} for n in range(1,6)],
]
NATAS_CLASSIFICATIONS = [
 {"challenge_ids":["natas-00","natas-01","natas-02","natas-04","natas-05"],"argv":["curl","--help"],"runtime":"kali-attacker","package":"curl"},
 *[{"challenge_ids":["natas-%02d" % n],"not_applicable":"browser/source/topic guidance"} for n in (3,6,7,8,9,10,11,12,13,14)],
]

def all_classifications():
    rows = bandit_classifications() + KRYPTON_CLASSIFICATIONS + NATAS_CLASSIFICATIONS
    ids = [challenge_id for row in rows for challenge_id in row["challenge_ids"]]
    if len(ids) != 56 or len(set(ids)) != 56: raise ValueError("offline help coverage must be exactly 56 unique challenges")
    if any("image" in row for row in rows): raise ValueError("capture image digest is runtime configuration")
    if any("argv" in row and (type(row.get("package")) is not str or not re.fullmatch(r"[a-z0-9][a-z0-9+.-]*", row["package"])) for row in rows): raise ValueError("invalid command package")
    return rows
