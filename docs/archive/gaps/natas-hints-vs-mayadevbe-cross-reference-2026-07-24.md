# Natas hints cross-reference against mayadevbe.me (2026-07-24)

Same exercise as the Bandit and Krypton cross-references (PRs #13, #14,
and the companion Krypton doc), applied to Natas. Fetched
`https://mayadevbe.me/posts/overthewire/natas/natas0/` through
`natas6/` (7 pages, transitions 0->1 through 6->7) and compared against
`HINTS["natas-00"]` through `HINTS["natas-06"]` in
`CEI-Labs-Wargames/scripts/build_natas.py`. Our deployment goes further
(`natas-00` through `natas-14`); only the first 7 levels had a
published page to compare against in this pass. Notes only, no code
changed.

## Site's solve approach per level (as fetched 2026-07-24)

| Transition | Site's approach |
|---|---|
| 0->1 | View page source (F12 / "View Page Source"), find password in an HTML comment |
| 1->2 | Right-click is disabled; use devtools/view-source anyway, same HTML-comment pattern |
| 2->3 | View source to find a referenced file path (`files/pixel.png`), request the directory itself, find `users.txt` via directory listing |
| 3->4 | Check `/robots.txt`, follow the disallowed path it lists |
| 4->5 | Open devtools Network tab, "Copy as cURL", edit the `Referer` header, resend |
| 5->6 | Open devtools Storage/Cookies tab, flip `loggedin` cookie from `0` to `1` |
| 6->7 | View source to find `include "includes/secret.inc"`, request that file path directly, read `$secret` |

## Comparison against our `HINTS` dict

The underlying technique is identical level-for-level (HTML comments,
directory listing, `robots.txt`, Referer header, cookie tampering, PHP
include disclosure) -- no conceptual gap found for any of the 7 levels
checked.

The one consistent difference is **tooling, not technique**: the site
assumes a GUI browser with devtools throughout (F12, "Copy as cURL",
Firefox's Storage tab, "Edit and Resend"). Our hints are written
entirely around `curl` from what the hints call "the Kali attacker
workstation" -- e.g. `HINTS["natas-04"]` tier 3 uses
`curl -e '<referer>' http://...` where the site uses browser devtools
to edit and resend a captured request; `HINTS["natas-05"]` tier 3 uses
`curl -v` to see the `Set-Cookie` response header and `curl -b
'loggedin=1'` to resend it, where the site edits the cookie in a
browser's Storage panel.

This looks like a deliberate fit to how this event's environment is
actually set up (a CLI attacker box), not an oversight, so I'm not
treating "doesn't match the site's browser-based steps" as a gap. It's
called out explicitly so nobody "fixes" our Natas hints to describe
browser devtools steps that don't match how players actually reach the
targets in this deployment.

## What closing this needs

- No hint-content changes appear justified by this comparison for
  natas-00 through natas-06 -- technique coverage matches, and the
  curl-vs-devtools difference is an intentional environment fit, not a
  quality gap.
- Levels natas-07 through natas-14 (our deployment goes this far) were
  not checked in this pass -- the site's series may not extend that
  far, or may under a different URL pattern; not verified here.
