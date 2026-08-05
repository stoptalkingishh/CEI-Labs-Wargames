# CEI Labs Wargame Login Banners

Every per-level storyboard banner across Bandit, Krypton, and Natas, shown as
it would appear captured from a real SSH session (Bandit/Krypton) or the Natas
web login page's rendered `<pre>` block (Natas). ANSI color codes are stripped
here for markdown readability; in a real terminal/browser all three tracks
render in color (Bandit/Krypton via ANSI SGR, Natas via CSS matching its
existing per-level hue progression).

Each banner is one frame of a continuous journey through the track (see
[`wargame-themes.md`](wargame-themes.md)'s "Storyboard mechanic" section, and
[`wargame-story.md`](wargame-story.md) for the narrative each frame follows):
a fixed establishing-shot frame, plus a progress strip using `x`/`-` for
ground already covered, `o` for exactly where this level is, and `.` for
ground still ahead. Bandit additionally splits its 34 levels into 8 chapters
drawn in distinct bracket styles, plus a within-chapter position strip, so
adjacent levels stay visually distinct even inside the same chapter.

Each banner is laid out as a bordered frame: a large block-letter track
wordmark on top (colored with the level's own palette), the storyboard art
below it, then a divider and an info block with the account, next-step
guidance, and a numeric progress readout. The three acceptable-use policy
lines always close the banner, verbatim and uncolored.

## Bandit

### Track theme

"The Vault at Dryrock" -- an outlaw slips into a walled desert compound after dark, hunting a ledger locked in its deepest vault. The compound is split into 8 chapters following the track's own content clusters; the boxed row shows which chapter you're in, and "in this room" your exact position within it.

### bandit0: The First Step

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |>OO<| |    | |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [o....]                                         ║
║    -->  CEI Labs Bandit 0: The First Step                        ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit0                       Progress: 0/34 (0%)  ║
║  Submit this level, then use CTFd launch panel for bandit1.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit1: Dashed Hopes

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |>OO<| |    | |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xo...]                                         ║
║    -->  CEI Labs Bandit 1: Dashed Hopes                          ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit1                       Progress: 1/34 (3%)  ║
║  Submit this level, then use CTFd launch panel for bandit2.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit2: Spaces in Places

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |>OO<| |    | |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxo..]                                         ║
║    -->  CEI Labs Bandit 2: Spaces in Places                      ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit2                       Progress: 2/34 (6%)  ║
║  Submit this level, then use CTFd launch panel for bandit3.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit3: Hidden in Plain Sight

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |>OO<| |    | |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxo.]                                         ║
║    -->  CEI Labs Bandit 3: Hidden in Plain Sight                 ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit3                       Progress: 3/34 (9%)  ║
║  Submit this level, then use CTFd launch panel for bandit4.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit4: Human Readable

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |>OO<| |    | |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxxo]                                         ║
║    -->  CEI Labs Bandit 4: Human Readable                        ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit4                      Progress: 4/34 (12%)  ║
║  Submit this level, then use CTFd launch panel for bandit5.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit5: The Needle

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |>OO<| |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [o.....]                                        ║
║    -->  CEI Labs Bandit 5: The Needle                            ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit5                      Progress: 5/34 (15%)  ║
║  Submit this level, then use CTFd launch panel for bandit6.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit6: Server Search

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |>OO<| |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xo....]                                        ║
║    -->  CEI Labs Bandit 6: Server Search                         ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit6                      Progress: 6/34 (18%)  ║
║  Submit this level, then use CTFd launch panel for bandit7.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit7: The Millionth Word

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |>OO<| |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxo...]                                        ║
║    -->  CEI Labs Bandit 7: The Millionth Word                    ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit7                      Progress: 7/34 (21%)  ║
║  Submit this level, then use CTFd launch panel for bandit8.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit8: The Only One

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |>OO<| |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxo..]                                        ║
║    -->  CEI Labs Bandit 8: The Only One                          ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit8                      Progress: 8/34 (24%)  ║
║  Submit this level, then use CTFd launch panel for bandit9.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit9: Strings Attached

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |>OO<| |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxxo.]                                        ║
║    -->  CEI Labs Bandit 9: Strings Attached                      ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit9                      Progress: 9/34 (27%)  ║
║  Submit this level, then use CTFd launch panel for bandit10.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit10: Base Operations

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |>OO<| |    | |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxxxo]                                        ║
║    -->  CEI Labs Bandit 10: Base Operations                      ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit10                    Progress: 10/34 (30%)  ║
║  Submit this level, then use CTFd launch panel for bandit11.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit11: Substitution

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |>OO<| |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [o.....]                                        ║
║    -->  CEI Labs Bandit 11: Substitution                         ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit11                    Progress: 11/34 (33%)  ║
║  Submit this level, then use CTFd launch panel for bandit12.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit12: Matryoshka

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |>OO<| |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xo....]                                        ║
║    -->  CEI Labs Bandit 12: Matryoshka                           ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit12                    Progress: 12/34 (36%)  ║
║  Submit this level, then use CTFd launch panel for bandit13.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit13: Private Keys

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |>OO<| |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxo...]                                        ║
║    -->  CEI Labs Bandit 13: Private Keys                         ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit13                    Progress: 13/34 (39%)  ║
║  Submit this level, then use CTFd launch panel for bandit14.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit14: Port Submission

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |>OO<| |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxo..]                                        ║
║    -->  CEI Labs Bandit 14: Port Submission                      ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit14                    Progress: 14/34 (42%)  ║
║  Submit this level, then use CTFd launch panel for bandit15.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit15: SSL Encryption

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |>OO<| |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxxo.]                                        ║
║    -->  CEI Labs Bandit 15: SSL Encryption                       ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit15                    Progress: 15/34 (45%)  ║
║  Submit this level, then use CTFd launch panel for bandit16.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit16: SSL Port Scan

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |>OO<| |    | |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxxxo]                                        ║
║    -->  CEI Labs Bandit 16: SSL Port Scan                        ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit16                    Progress: 16/34 (48%)  ║
║  Submit this level, then use CTFd launch panel for bandit17.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit17: File Comparisons

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |>OO<| |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [o...]                                          ║
║    -->  CEI Labs Bandit 17: File Comparisons                     ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit17                    Progress: 17/34 (52%)  ║
║  Submit this level, then use CTFd launch panel for bandit18.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit18: Shell Bypass

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |>OO<| |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xo..]                                          ║
║    -->  CEI Labs Bandit 18: Shell Bypass                         ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit18                    Progress: 18/34 (55%)  ║
║  Submit this level, then use CTFd launch panel for bandit19.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit19: SUID Escalation

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |>OO<| |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxo.]                                          ║
║    -->  CEI Labs Bandit 19: SUID Escalation                      ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit19                    Progress: 19/34 (58%)  ║
║  Submit this level, then use CTFd launch panel for bandit20.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit20: Port Listener Connection

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |>OO<| |    | |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxo]                                          ║
║    -->  CEI Labs Bandit 20: Port Listener Connection             ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit20                    Progress: 20/34 (61%)  ║
║  Submit this level, then use CTFd launch panel for bandit21.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit21: Cron Jobs

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [o..]                                           ║
║    -->  CEI Labs Bandit 21: Cron Jobs                            ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit21                    Progress: 21/34 (64%)  ║
║  Submit this level, then use CTFd launch panel for bandit22.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit22: Cron Debugging

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xo.]                                           ║
║    -->  CEI Labs Bandit 22: Cron Debugging                       ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit22                    Progress: 22/34 (67%)  ║
║  Submit this level, then use CTFd launch panel for bandit23.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit23: Cron Scripting

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    | |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxo]                                           ║
║    -->  CEI Labs Bandit 23: Cron Scripting                       ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit23                    Progress: 23/34 (70%)  ║
║  Submit this level, then use CTFd launch panel for bandit24.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit24: PIN Brute Force

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [o..]                                           ║
║    -->  CEI Labs Bandit 24: PIN Brute Force                      ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit24                    Progress: 24/34 (73%)  ║
║  Submit this level, then use CTFd launch panel for bandit25.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit25: Shell Breakout

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xo.]                                           ║
║    -->  CEI Labs Bandit 25: Shell Breakout                       ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit25                    Progress: 25/34 (76%)  ║
║  Submit this level, then use CTFd launch panel for bandit26.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit26: Text UI Breakout

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    | |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxo]                                           ║
║    -->  CEI Labs Bandit 26: Text UI Breakout                     ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit26                    Progress: 26/34 (79%)  ║
║  Submit this level, then use CTFd launch panel for bandit27.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit27: Git Clone

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [o....]                                         ║
║    -->  CEI Labs Bandit 27: Git Clone                            ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit27                    Progress: 27/34 (82%)  ║
║  Submit this level, then use CTFd launch panel for bandit28.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit28: Git Commits

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xo...]                                         ║
║    -->  CEI Labs Bandit 28: Git Commits                          ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit28                    Progress: 28/34 (85%)  ║
║  Submit this level, then use CTFd launch panel for bandit29.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit29: Git Branches

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxo..]                                         ║
║    -->  CEI Labs Bandit 29: Git Branches                         ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit29                    Progress: 29/34 (88%)  ║
║  Submit this level, then use CTFd launch panel for bandit30.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit30: Git Tags

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxo.]                                         ║
║    -->  CEI Labs Bandit 30: Git Tags                             ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit30                    Progress: 30/34 (91%)  ║
║  Submit this level, then use CTFd launch panel for bandit31.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit31: Git Push

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<| |    |       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xxxxo]                                         ║
║    -->  CEI Labs Bandit 31: Git Push                             ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit31                    Progress: 31/34 (94%)  ║
║  Submit this level, then use CTFd launch panel for bandit32.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit32: Shell Overrides

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<|       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [o.]                                            ║
║    -->  CEI Labs Bandit 32: Shell Overrides                      ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit32                    Progress: 32/34 (97%)  ║
║  Submit this level, then use CTFd launch panel for bandit33.     ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit33: Final Escape

```
╔══════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗                  ║
║  ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝                  ║
║  ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║                     ║
║  ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║                     ║
║  ██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║                     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝                     ║
║                                                                  ║
║     ✦      .        ✧         .       ✦                          ║
║    █  █  █  █  █  █  █  █  █  █  █  █  █                         ║
║    ████████████████████████████████████                          ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |XXXX| |>OO<|       ║
║    .----. +----+ /----\ #----# ~----~ :----: *----* >----<       ║
║    in this room: [xo]                                            ║
║    -->  CEI Labs Bandit 33: Final Escape                         ║
╟──────────────────────────────────────────────────────────────────╢
║  Logged in as bandit33                   Progress: 33/34 (100%)  ║
║  Final level: submit your result; there is no next account.      ║
╚══════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

## Krypton

### Track theme

"Signal from the Dark" -- a deep-space listening post catches a transmission no one can place, and peels back layer after layer over one night shift. The transmission strip follows the signal traveling further from the dish with each level.

### krypton0: Base64 Decoding

```
╔════════════════════════════════════════════════════════════════════════════╗
║ K  K  RRR   Y   Y  PPP   TTTTT   OOO   N   N                               ║
║ K K   R  R   Y Y   P  P    T    O   O  NN  N                               ║
║ KK    RRR     Y    PPP     T    O   O  N N N                               ║
║ K K   R R     Y    P       T    O   O  N  NN                               ║
║ K  K  R  R    Y    P       T     OOO   N   N                               ║
║                                                                            ║
║      ★        .          ☆          .        ★                             ║
║   .     ★          .          ☆          .                                 ║
║   ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈                                ║
║   [o.......................................]                               ║
║   ~>  CEI Labs Krypton 0: Base64 Decoding                                  ║
╚════════════════════════════════════════════════════════════════════════════╝
──────────────────────────────────────────────────────────────────────────────
Logged in as krypton0
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton1.
Progress: 0/6 levels completed (0% through the track)
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton1: ROT13 Substitution Cipher

```
╔════════════════════════════════════════════════════════════════════════════╗
║ K  K  RRR   Y   Y  PPP   TTTTT   OOO   N   N                               ║
║ K K   R  R   Y Y   P  P    T    O   O  NN  N                               ║
║ KK    RRR     Y    PPP     T    O   O  N N N                               ║
║ K K   R R     Y    P       T    O   O  N  NN                               ║
║ K  K  R  R    Y    P       T     OOO   N   N                               ║
║                                                                            ║
║      ★        .          ☆          .        ★                             ║
║   .     ★          .          ☆          .                                 ║
║   ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈                                ║
║   [------o.................................]                               ║
║   ~>  CEI Labs Krypton 1: ROT13 Substitution Cipher                        ║
╚════════════════════════════════════════════════════════════════════════════╝
──────────────────────────────────────────────────────────────────────────────
Logged in as krypton1
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton2.
Progress: 1/6 levels completed (17% through the track)
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton2: Caesar Cipher (Unknown Shift)

```
╔════════════════════════════════════════════════════════════════════════════╗
║ K  K  RRR   Y   Y  PPP   TTTTT   OOO   N   N                               ║
║ K K   R  R   Y Y   P  P    T    O   O  NN  N                               ║
║ KK    RRR     Y    PPP     T    O   O  N N N                               ║
║ K K   R R     Y    P       T    O   O  N  NN                               ║
║ K  K  R  R    Y    P       T     OOO   N   N                               ║
║                                                                            ║
║      ★        .          ☆          .        ★                             ║
║   .     ★          .          ☆          .                                 ║
║   ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈                                ║
║   [-------------o..........................]                               ║
║   ~>  CEI Labs Krypton 2: Caesar Cipher (Unknown Shift)                    ║
╚════════════════════════════════════════════════════════════════════════════╝
──────────────────────────────────────────────────────────────────────────────
Logged in as krypton2
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton3.
Progress: 2/6 levels completed (33% through the track)
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton3: Frequency Analysis

```
╔════════════════════════════════════════════════════════════════════════════╗
║ K  K  RRR   Y   Y  PPP   TTTTT   OOO   N   N                               ║
║ K K   R  R   Y Y   P  P    T    O   O  NN  N                               ║
║ KK    RRR     Y    PPP     T    O   O  N N N                               ║
║ K K   R R     Y    P       T    O   O  N  NN                               ║
║ K  K  R  R    Y    P       T     OOO   N   N                               ║
║                                                                            ║
║      ★        .          ☆          .        ★                             ║
║   .     ★          .          ☆          .                                 ║
║   ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈                                ║
║   [--------------------o...................]                               ║
║   ~>  CEI Labs Krypton 3: Frequency Analysis                               ║
╚════════════════════════════════════════════════════════════════════════════╝
──────────────────────────────────────────────────────────────────────────────
Logged in as krypton3
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton4.
Progress: 3/6 levels completed (50% through the track)
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton4: Vigenere Cipher (Known Key Length)

```
╔════════════════════════════════════════════════════════════════════════════╗
║ K  K  RRR   Y   Y  PPP   TTTTT   OOO   N   N                               ║
║ K K   R  R   Y Y   P  P    T    O   O  NN  N                               ║
║ KK    RRR     Y    PPP     T    O   O  N N N                               ║
║ K K   R R     Y    P       T    O   O  N  NN                               ║
║ K  K  R  R    Y    P       T     OOO   N   N                               ║
║                                                                            ║
║      ★        .          ☆          .        ★                             ║
║   .     ★          .          ☆          .                                 ║
║   ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈                                ║
║   [--------------------------o.............]                               ║
║   ~>  CEI Labs Krypton 4: Vigenere Cipher (Known Key Length)               ║
╚════════════════════════════════════════════════════════════════════════════╝
──────────────────────────────────────────────────────────────────────────────
Logged in as krypton4
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton5.
Progress: 4/6 levels completed (67% through the track)
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton5: Vigenere Cipher (Kasiski Test)

```
╔════════════════════════════════════════════════════════════════════════════╗
║ K  K  RRR   Y   Y  PPP   TTTTT   OOO   N   N                               ║
║ K K   R  R   Y Y   P  P    T    O   O  NN  N                               ║
║ KK    RRR     Y    PPP     T    O   O  N N N                               ║
║ K K   R R     Y    P       T    O   O  N  NN                               ║
║ K  K  R  R    Y    P       T     OOO   N   N                               ║
║                                                                            ║
║      ★        .          ☆          .        ★                             ║
║   .     ★          .          ☆          .                                 ║
║   ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈                                ║
║   [--------------------------------o.......]                               ║
║   ~>  CEI Labs Krypton 5: Vigenere Cipher (Kasiski Test)                   ║
╚════════════════════════════════════════════════════════════════════════════╝
──────────────────────────────────────────────────────────────────────────────
Logged in as krypton5
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton6.
Progress: 5/6 levels completed (83% through the track)
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton6: Stream Cipher / LFSR

```
╔════════════════════════════════════════════════════════════════════════════╗
║ K  K  RRR   Y   Y  PPP   TTTTT   OOO   N   N                               ║
║ K K   R  R   Y Y   P  P    T    O   O  NN  N                               ║
║ KK    RRR     Y    PPP     T    O   O  N N N                               ║
║ K K   R R     Y    P       T    O   O  N  NN                               ║
║ K  K  R  R    Y    P       T     OOO   N   N                               ║
║                                                                            ║
║      ★        .          ☆          .        ★                             ║
║   .     ★          .          ☆          .                                 ║
║   ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈                                ║
║   [---------------------------------------o]                               ║
║   ~>  CEI Labs Krypton 6: Stream Cipher / LFSR                             ║
╚════════════════════════════════════════════════════════════════════════════╝
──────────────────────────────────────────────────────────────────────────────
Logged in as krypton6
Player tools: krypton-tools --help
Final level: submit your result; there is no next account.
Progress: 6/6 levels completed (100% through the track)
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

## Natas

### Track theme

"Into the Mirror" -- a researcher descends an inverted underworld of a web application, each floor further from what a browser should show. The depth shaft follows the descent from the surface (natas0) to the raw records at the bottom (natas14), reinforced by the page's own cool-to-hot color progression.

### natas0: View Source (color: #3791be)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 0: View Source                                           ║
║  Account: natas0                                                         ║
║  Progress: 0/14 levels descended (0%)                                    ║
║  Next step: solve natas0 to descend to natas1                            ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas1: Right-Click Block (color: #37b4be)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 1: Right-Click Block                                     ║
║  Account: natas1                                                         ║
║  Progress: 1/14 levels descended (7%)                                    ║
║  Next step: solve natas1 to descend to natas2                            ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas2: Directory Traversal (Files) (color: #37bea4)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 2: Directory Traversal (Files)                           ║
║  Account: natas2                                                         ║
║  Progress: 2/14 levels descended (14%)                                   ║
║  Next step: solve natas2 to descend to natas3                            ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas3: Web Crawlers (Robots.txt) (color: #37be81)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 3: Web Crawlers (Robots.txt)                             ║
║  Account: natas3                                                         ║
║  Progress: 3/14 levels descended (21%)                                   ║
║  Next step: solve natas3 to descend to natas4                            ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas4: Referer Spoofing (color: #37be5e)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 4: Referer Spoofing                                      ║
║  Account: natas4                                                         ║
║  Progress: 4/14 levels descended (28%)                                   ║
║  Next step: solve natas4 to descend to natas5                            ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas5: Cookie Manipulation (color: #37be3a)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 5: Cookie Manipulation                                   ║
║  Account: natas5                                                         ║
║  Progress: 5/14 levels descended (35%)                                   ║
║  Next step: solve natas5 to descend to natas6                            ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas6: Hidden Inclusion Files (color: #57be37)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 6: Hidden Inclusion Files                                ║
║  Account: natas6                                                         ║
║  Progress: 6/14 levels descended (42%)                                   ║
║  Next step: solve natas6 to descend to natas7                            ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas7: Local File Inclusion (LFI) (color: #7abe37)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 7: Local File Inclusion (LFI)                            ║
║  Account: natas7                                                         ║
║  Progress: 7/14 levels descended (50%)                                   ║
║  Next step: solve natas7 to descend to natas8                            ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas8: Reversing Crypto Schemes (color: #9ebe37)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 8: Reversing Crypto Schemes                              ║
║  Account: natas8                                                         ║
║  Progress: 8/14 levels descended (57%)                                   ║
║  Next step: solve natas8 to descend to natas9                            ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas9: Command Injection I (color: #bebb37)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 9: Command Injection I                                   ║
║  Account: natas9                                                         ║
║  Progress: 9/14 levels descended (64%)                                   ║
║  Next step: solve natas9 to descend to natas10                           ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas10: Command Injection II (Sanitization Bypass) (color: #be9737)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 10: Command Injection II (Sanitization Bypass)           ║
║  Account: natas10                                                        ║
║  Progress: 10/14 levels descended (71%)                                  ║
║  Next step: solve natas10 to descend to natas11                          ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas11: XOR Encryption Bypass (color: #be7437)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 11: XOR Encryption Bypass                                ║
║  Account: natas11                                                        ║
║  Progress: 11/14 levels descended (78%)                                  ║
║  Next step: solve natas11 to descend to natas12                          ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas12: Arbitrary File Upload (Web Shell) (color: #be5137)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 12: Arbitrary File Upload (Web Shell)                    ║
║  Account: natas12                                                        ║
║  Progress: 12/14 levels descended (85%)                                  ║
║  Next step: solve natas12 to descend to natas13                          ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas13: File Upload Bypass (Magic Bytes) (color: #be3741)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  [.]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 13: File Upload Bypass (Magic Bytes)                     ║
║  Account: natas13                                                        ║
║  Progress: 13/14 levels descended (92%)                                  ║
║  Next step: solve natas13 to descend to natas14                          ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas14: SQL Injection (SQLi) (color: #be3764)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    N   N   AAA   TTTTT   AAA    SSS                      ║
║                    NN  N  A   A    T    A   A  S                         ║
║                    N N N  AAAAA    T    AAAAA   SS                       ║
║                    N  NN  A   A    T    A   A      S                     ║
║                    N   N  A   A    T    A   A  SSS                       ║
╠══════════════════════════════════════════════════════════════════════════╣
  surface
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [x]
  [o]
  depths
╠══════════════════════════════════════════════════════════════════════════╣
║  CEI Labs Natas 14: SQL Injection (SQLi)                                 ║
║  Account: natas14                                                        ║
║  Progress: 14/14 levels descended (100%)                                 ║
║  Next step: none -- you have reached the depths                          ║
╚══════════════════════════════════════════════════════════════════════════╝
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```
