# Bandit hints: full-series cross-reference against mayadevbe.me (2026-07-24)

Follow-up to `bandit-hints-vs-external-walkthrough-gap-2026-07-24.md`
(PR #13), which only checked bandit-05 against one page. The user then
supplied the series index, `https://mayadevbe.me/posts/`, which links a
walkthrough for every Bandit level (`.../bandit/level0/` through
`.../bandit/level33/`), plus separate Krypton and Natas series. This
pass fetches and cross-references the full Bandit series. Notes only,
no code changed.

## URL numbering, confirmed

Fetching `level0` through `level33` shows a consistent pattern: page
`levelN` documents the transition `(N-1) -> N` (e.g. `level6` = Bandit
5 -> 6, `level33` = Bandit 32 -> 33). `level0` itself is the entry page
(initial SSH connect), not a password transition.

## Site's solve command per transition (as fetched 2026-07-24)

| Transition | Site's final command(s) |
|---|---|
| 0->1 | `cat readme` |
| 1->2 | `cat ./-` |
| 2->3 | `cat "spaces in this filename"` |
| 3->4 | `cat inhere/.hidden` |
| 4->5 | `file ./*` then `cat ./-file07` |
| 5->6 | `find . -type f -size 1033c ! -executable -exec file '{}' \; \| grep ASCII` |
| 6->7 | `find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null` |
| 7->8 | `cat data.txt \| grep millionth` |
| 8->9 | `sort data.txt \| uniq -u` |
| 9->10 | `strings data.txt \| grep ===` |
| 10->11 | `base64 -d data.txt` |
| 11->12 | `cat data.txt \| tr 'A-Za-z' 'N-ZA-Mn-za-m'` |
| 12->13 | repeated `xxd -r` / `gzip -d` / `bzip2 -d` / `tar -xf` until `cat data8` |
| 13->14 | `ssh -i sshkey.private bandit14@... -p 2220` |
| 14->15 | `nc localhost 30000`, then type current password |
| 15->16 | `openssl s_client -connect localhost:30001`, then type current password |
| 16->17 | `nmap -sV localhost -p 31000-32000` to find the SSL port, then `openssl s_client` |
| 17->18 | `diff passwords.old passwords.new` |
| 18->19 | `ssh bandit18@... -p 2220 cat readme` (non-interactive remote command) |
| 19->20 | `./bandit20-do cat /etc/bandit_pass/bandit20` |
| 20->21 | `nc -l -p 1234 &` then `./suconnect 1234` |
| 21->22 | read `/etc/cron.d/`, `cat` the `/tmp/...` file it writes |
| 22->23 | reproduce `echo I am user bandit23 \| md5sum \| cut -d' ' -f1`, `cat` that `/tmp` path |
| 23->24 | drop a script into the world-writable cron-scanned dir owned as bandit24 |
| 24->25 | brute-force loop of all 10,000 PINs piped through `nc`, filter out `Wrong!` |
| 25->26 | shrink terminal so `more` pauses, press `v` to reach vi |
| 26->27 | from vi: `:set shell=/bin/bash` then `:shell` |
| 27->28 | `git clone ssh://bandit27-git@.../repo`, `cat README` |
| 28->29 | `git log -p` (or `git show <commit>`), find password in an earlier diff |
| 29->30 | `git branch -a`, `git checkout dev`, `cat README.md` |
| 30->31 | `git tag`, `git show <tagname>` |
| 31->32 | `git add -f key.txt` (bypassing `.gitignore`), commit, `git push` |
| 32->33 | type `$0` at the uppercase-only shell to spawn a real bash |

## Comparison against our `HINTS` dict (`CEI-Labs-Wargames/scripts/build_bandit.py`)

For the levels checked, our tier-2/tier-3 hints already name the same
tools and predicates the site uses (confirmed by reading `HINTS["bandit-00"]`
through `HINTS["bandit-33"]` directly). The recurring, consistent
structural gap from the bandit-05-only pass holds across the series:

- Our hints generally **describe** the concept and predicate set, then
  tell the player to combine them, rather than **handing over the
  single, copy-pasteable, self-contained command** the way the site
  does for nearly every level (e.g. our bandit-09 hint says run
  `strings data.txt | grep '^='`, which actually already IS
  self-contained and matches the site's shape well; but bandit-05's
  tier 3, per the prior PR, still splits `find` and `file` into two
  steps where the site folds them into one `-exec ... | grep ASCII`
  pipeline).
- Where the underlying task is multi-step by nature (cron levels
  21-24, git levels 27-31, the vi/shell-escape levels 25-26), both our
  hints and the site's walkthroughs are necessarily multi-step, so
  there's no real gap there -- the site isn't doing anything we aren't
  already doing structurally for those.
- The site consistently opens with the plain-language framing of *why*
  a tool applies before giving the command (e.g. bandit-08: "sort
  groups duplicates, uniq -u shows only what's left"), which our tier-2
  hints already do in similar or greater depth (compare our
  `HINTS["bandit-08"]` tier 2, which explains adjacency-only detection
  and the sort-then-uniq ordering requirement -- arguably more thorough
  than the site's one-liner explanation).

Net: the content/coverage gap flagged for bandit-05 does not appear to
be a series-wide pattern once compared level by level -- most of our
hints already match or exceed the site's explanatory depth. The
concrete, actionable item that generalizes is specifically the
"hand over one self-contained final command instead of a command plus
a separate manual filtering step" shape, which so far has only been
confirmed as a real gap for bandit-05.

## Important caveat: level numbering does not line up cleanly for 29-32

Comparing content, not just labels, `HINTS["bandit-31"]` in our repo
describes a generic "read the README for an exact required file/name/
content, create it, then push" task -- it does not name `.gitignore` or
`key.txt` specifically. The site's `31->32` transition is specifically
about bypassing a `.gitignore` rule with `git add -f key.txt`. Our
`HINTS["bandit-32"]` is the `$0` uppercase-shell escape, which the site
places at `32->33` instead. Our `HINTS["bandit-33"]` describes a
different final escape (a restricted shell where `find`'s `-exec`
action launches an arbitrary program), which isn't covered by any site
page since the site's series stops at `level33` (`32->33`).

This means our level content and the site's level content are **not
guaranteed to be the same challenge at the same number** past roughly
level 29-30 -- whether because our deployment intentionally customized/
reordered content in that range, or because of an unrelated indexing
difference. Nobody should port site text into our hints level-by-level
by number alone without first confirming the actual on-box challenge
content at that number matches what the site describes. This wasn't
checked against our `targets/bandit/build/` setup scripts in this pass
-- doing so is necessary before any rewrite in this range.

## What closing this needs

- For bandit-05 specifically (already scoped in PR #13): fold the
  `find` + `file` steps into one `-exec`/`grep`-based command in tier 3.
- Reconcile our bandit-29 through bandit-33 content against
  `targets/bandit/build/*.py` (not this doc's site comparison) to
  confirm what each of our levels actually tests, before treating the
  site's 29-32 transitions as applicable reference material for those
  specific numbers.
- Krypton and Natas each have their own separate walkthrough series
  linked from the same index (`.../krypton/level0-5/`,
  `.../natas/natas0-6/`) -- neither was fetched or compared in this
  pass; that would be separate follow-up work, not covered here.
