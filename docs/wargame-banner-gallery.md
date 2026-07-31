# CEI Labs Wargame Login Banners

Every per-level ASCII/Unicode art banner across Bandit, Krypton, and Natas,
shown as it would appear captured from a real SSH session (Bandit/Krypton) or
the Natas web login page's rendered `<pre>` block (Natas). ANSI color codes are
stripped here for markdown readability; in a real terminal/browser all three
tracks render in color (Bandit/Krypton via ANSI SGR, Natas via CSS matching its
existing per-level hue progression), and Unicode glyphs render as shown.

Each entry is preceded by the exact prompt used to generate that piece of art
(the shared template from `docs/wargame-themes.md`, filled in with the track's
theme and that level's title).

## Bandit

### Track theme

You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).

### bandit0: The First Step

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "The First Step"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   .---.
   | o | -->
   '---'  CEI Labs Bandit 0: The First Step
Logged in as bandit0
Submit this level, then use CTFd launch panel for bandit1.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit1: Dashed Hopes

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Dashed Hopes"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [-][ ][ ][ ]
      ^picked
   .-------.
   |   X   |
   '-------'  CEI Labs Bandit 1: Dashed Hopes
Logged in as bandit1
Submit this level, then use CTFd launch panel for bandit2.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit2: Spaces in Places

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Spaces in Places"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [ A    B ]
   <--joined-->
  |  |     |  |
  |  | o   |  |
  |  |     |  |  CEI Labs Bandit 2: Spaces in Places
Logged in as bandit2
Submit this level, then use CTFd launch panel for bandit3.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit3: Hidden in Plain Sight

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Hidden in Plain Sight"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [#][#][#]
  [#][o][#]
  [#][#][#]  CEI Labs Bandit 3: Hidden in Plain Sight
Logged in as bandit3
Submit this level, then use CTFd launch panel for bandit4.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit4: Human Readable

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Human Readable"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   ,-------.
   | note   |
   |  o     |
   `-------'  CEI Labs Bandit 4: Human Readable
Logged in as bandit4
Submit this level, then use CTFd launch panel for bandit5.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit5: The Needle

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "The Needle"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  ~~~~~~~~~~
  ~~~ | ~~~~
  ~~~~~~~~~~  CEI Labs Bandit 5: The Needle
Logged in as bandit5
Submit this level, then use CTFd launch panel for bandit6.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit6: Server Search

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Server Search"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [=][=][=]
  [=][=][=]  o
  [=][=][=]  CEI Labs Bandit 6: Server Search
Logged in as bandit6
Submit this level, then use CTFd launch panel for bandit7.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit7: The Millionth Word

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "The Millionth Word"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  1 2 3 ... (n) ...
        ^counted
  wwwwwwwwwwwww
  ww[W]wwwwwwww
  wwwwwwwwwwwww  CEI Labs Bandit 7: The Millionth Word
Logged in as bandit7
Submit this level, then use CTFd launch panel for bandit8.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit8: The Only One

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "The Only One"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  ooooooooo
  oo[*]oooo
  ooooooooo  CEI Labs Bandit 8: The Only One
Logged in as bandit8
Submit this level, then use CTFd launch panel for bandit9.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit9: Strings Attached

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Strings Attached"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
    \|/
     o
    /|\  CEI Labs Bandit 9: Strings Attached
Logged in as bandit9
Submit this level, then use CTFd launch panel for bandit10.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit10: Base Operations

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Base Operations"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [#$%@] --> [====]
   ####
   #  # o
   ####  CEI Labs Bandit 10: Base Operations
Logged in as bandit10
Submit this level, then use CTFd launch panel for bandit11.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit11: Substitution

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Substitution"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [A]<->[B]
      o
   swapped  CEI Labs Bandit 11: Substitution
Logged in as bandit11
Submit this level, then use CTFd launch panel for bandit12.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit12: Matryoshka

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Matryoshka"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [ [ [ o ] ] ]
   [ [ ] ]
    [ ]  CEI Labs Bandit 12: Matryoshka
Logged in as bandit12
Submit this level, then use CTFd launch panel for bandit13.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit13: Private Keys

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Private Keys"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   .--.
  ( () )==>[ o ]
   `--'  CEI Labs Bandit 13: Private Keys
Logged in as bandit13
Submit this level, then use CTFd launch panel for bandit14.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit14: Port Submission

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Port Submission"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   o -->
   [ ]  <-hatch  CEI Labs Bandit 14: Port Submission
Logged in as bandit14
Submit this level, then use CTFd launch panel for bandit15.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit15: SSL Encryption

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "SSL Encryption"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
    .--.
   /    \
  |--[]--| o  CEI Labs Bandit 15: SSL Encryption
Logged in as bandit15
Submit this level, then use CTFd launch panel for bandit16.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit16: SSL Port Scan

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "SSL Port Scan"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [ ][ ][ ]
   o  scan-->  CEI Labs Bandit 16: SSL Port Scan
Logged in as bandit16
Submit this level, then use CTFd launch panel for bandit17.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit17: File Comparisons

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "File Comparisons"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   [A]  [B]
     o  <->  CEI Labs Bandit 17: File Comparisons
Logged in as bandit17
Submit this level, then use CTFd launch panel for bandit18.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit18: Shell Bypass

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Shell Bypass"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  |||||
  ||| o -->
  |||||  CEI Labs Bandit 18: Shell Bypass
Logged in as bandit18
Submit this level, then use CTFd launch panel for bandit19.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit19: SUID Escalation

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "SUID Escalation"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
    ^
   /|
  o |  CEI Labs Bandit 19: SUID Escalation
Logged in as bandit19
Submit this level, then use CTFd launch panel for bandit20.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit20: Port Listener Connection

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Port Listener Connection"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  )))
  ))) o
   |  CEI Labs Bandit 20: Port Listener Connection
Logged in as bandit20
Submit this level, then use CTFd launch panel for bandit21.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit21: Cron Jobs

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Cron Jobs"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   _12_
  9  o  3
   `-6-'  CEI Labs Bandit 21: Cron Jobs
Logged in as bandit21
Submit this level, then use CTFd launch panel for bandit22.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit22: Cron Debugging

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Cron Debugging"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   _12_   ,_,
  9  o 3 (o.o)
   `-6-'  CEI Labs Bandit 22: Cron Debugging
Logged in as bandit22
Submit this level, then use CTFd launch panel for bandit23.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit23: Cron Scripting

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Cron Scripting"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   _12_  |~~~
  9  o 3 |~~~
   `-6-' |~~~  CEI Labs Bandit 23: Cron Scripting
Logged in as bandit23
Submit this level, then use CTFd launch panel for bandit24.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit24: PIN Brute Force

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "PIN Brute Force"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [1][2][3]
  [4][5][6] o
  [7][8][9]  CEI Labs Bandit 24: PIN Brute Force
Logged in as bandit24
Submit this level, then use CTFd launch panel for bandit25.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit25: Shell Breakout

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Shell Breakout"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  |||||
  ||X|| o-->
  |||||  CEI Labs Bandit 25: Shell Breakout
Logged in as bandit25
Submit this level, then use CTFd launch panel for bandit26.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit26: Text UI Breakout

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Text UI Breakout"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  +--//--+
  | o  //|
  +-------+  CEI Labs Bandit 26: Text UI Breakout
Logged in as bandit26
Submit this level, then use CTFd launch panel for bandit27.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit27: Git Clone

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Git Clone"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   o---o---o
        \
         o  CEI Labs Bandit 27: Git Clone
Logged in as bandit27
Submit this level, then use CTFd launch panel for bandit28.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit28: Git Commits

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Git Commits"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  o---o---o
   stack  o  CEI Labs Bandit 28: Git Commits
Logged in as bandit28
Submit this level, then use CTFd launch panel for bandit29.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit29: Git Branches

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Git Branches"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
      o--o
     /
  o-o--o--o  CEI Labs Bandit 29: Git Branches
Logged in as bandit29
Submit this level, then use CTFd launch panel for bandit30.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit30: Git Tags

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Git Tags"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   _____
  /     \--o
  \_____/  CEI Labs Bandit 30: Git Tags
Logged in as bandit30
Submit this level, then use CTFd launch panel for bandit31.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit31: Git Push

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Git Push"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
   .-~~-.
  (  o   )
   `-..-'
     ^  CEI Labs Bandit 31: Git Push
Logged in as bandit31
Submit this level, then use CTFd launch panel for bandit32.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit32: Shell Overrides

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Shell Overrides"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  [cloak A]
      o
  [cloak B]  CEI Labs Bandit 32: Shell Overrides
Logged in as bandit32
Submit this level, then use CTFd launch panel for bandit33.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### bandit33: Final Escape

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: You are an outlaw breaking into a guarded compound: moving room to room, picking locks, slipping past guards, and stealing what's hidden deeper inside as you go. Per-level art follows this figure's progress from the outer wall (level 0) through increasingly deep rooms to an escape at the final level (33).
This piece is for the question titled: "Final Escape"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
   ✦      .        ✧         .       ✦
  ▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙▄▟█▙
  █▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓
  +--+
  |o |->
  +--+  CEI Labs Bandit 33: Final Escape
Logged in as bandit33
Final level: submit your result; there is no next account.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

## Krypton

### Track theme

Krypton is a distant, hidden world (Greek kryptos = "hidden") transmitting encoded signals across space. Each level is a signal that must be decoded, growing stranger and more alien-seeming the deeper you go.

### krypton0: Base64 Decoding

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: Krypton is a distant, hidden world (Greek kryptos = "hidden") transmitting encoded signals across space. Each level is a signal that must be decoded, growing stranger and more alien-seeming the deeper you go.
This piece is for the question titled: "Base64 Decoding"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
     ★        .          ☆          .        ★
  .     ★          .          ☆          .
  ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈
  [ %#&@ ]  -->  [ ==== ]
         << signal  CEI Labs Krypton 0: Base64 Decoding
Logged in as krypton0
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton1.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton1: ROT13 Substitution Cipher

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: Krypton is a distant, hidden world (Greek kryptos = "hidden") transmitting encoded signals across space. Each level is a signal that must be decoded, growing stranger and more alien-seeming the deeper you go.
This piece is for the question titled: "ROT13 Substitution Cipher"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
     ★        .          ☆          .        ★
  .     ★          .          ☆          .
  ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈
   \ | /
   -- O --  spinning
   / | \  CEI Labs Krypton 1: ROT13 Substitution Cipher
Logged in as krypton1
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton2.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton2: Caesar Cipher (Unknown Shift)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: Krypton is a distant, hidden world (Greek kryptos = "hidden") transmitting encoded signals across space. Each level is a signal that must be decoded, growing stranger and more alien-seeming the deeper you go.
This piece is for the question titled: "Caesar Cipher (Unknown Shift)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
     ★        .          ☆          .        ★
  .     ★          .          ☆          .
  ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈
   \ | /
   -- ? --  half-turned
   / | \  CEI Labs Krypton 2: Caesar Cipher (Unknown Shift)
Logged in as krypton2
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton3.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton3: Frequency Analysis

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: Krypton is a distant, hidden world (Greek kryptos = "hidden") transmitting encoded signals across space. Each level is a signal that must be decoded, growing stranger and more alien-seeming the deeper you go.
This piece is for the question titled: "Frequency Analysis"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
     ★        .          ☆          .        ★
  .     ★          .          ☆          .
  ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈
   |     ##
   |  #  ## #
   | ## ## ##
   +-----------  spectrum  CEI Labs Krypton 3: Frequency Analysis
Logged in as krypton3
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton4.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton4: Vigenere Cipher (Known Key Length)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: Krypton is a distant, hidden world (Greek kryptos = "hidden") transmitting encoded signals across space. Each level is a signal that must be decoded, growing stranger and more alien-seeming the deeper you go.
This piece is for the question titled: "Vigenere Cipher (Known Key Length)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
     ★        .          ☆          .        ★
  .     ★          .          ☆          .
  ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈
  [AA][AA][AA][AA]
  (( (( (( ))
   ((  core  ))
  (( (( (( ))  CEI Labs Krypton 4: Vigenere Cipher (Known Key Length)
Logged in as krypton4
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton5.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton5: Vigenere Cipher (Kasiski Test)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: Krypton is a distant, hidden world (Greek kryptos = "hidden") transmitting encoded signals across space. Each level is a signal that must be decoded, growing stranger and more alien-seeming the deeper you go.
This piece is for the question titled: "Vigenere Cipher (Kasiski Test)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
     ★        .          ☆          .        ★
  .     ★          .          ☆          .
  ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈
  [xxx]......[xxx]
   |<-- gap -->|
  ((( deeper ((((
  (( (((( ((  CEI Labs Krypton 5: Vigenere Cipher (Kasiski Test)
Logged in as krypton5
Player tools: krypton-tools --help
Submit this level, then use CTFd launch panel for krypton6.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### krypton6: Stream Cipher / LFSR

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: Krypton is a distant, hidden world (Greek kryptos = "hidden") transmitting encoded signals across space. Each level is a signal that must be decoded, growing stranger and more alien-seeming the deeper you go.
This piece is for the question titled: "Stream Cipher / LFSR"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**SSH capture:**
```
     ★        .          ☆          .        ★
  .     ★          .          ☆          .
  ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈
  [1][0][1][1]<-.
   ^____________|
   *
    \_/\_/\_
   endless loop  CEI Labs Krypton 6: Stream Cipher / LFSR
Logged in as krypton6
Player tools: krypton-tools --help
Final level: submit your result; there is no next account.
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

## Natas

### Track theme

"Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.

### natas0: View Source (color: #3791be)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "View Source"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
  [ page ]
  <!--   -->
  .-----.
  | text |
  '--v--'
   txet
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
   txet
  '--v--'
  | text |
  .-----.
  <!--   -->
  [ page ]
CEI Labs Natas 0: View Source
Account: natas0
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas1: Right-Click Block (color: #37b4be)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Right-Click Block"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
    [ menu ]
       X
      o
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
      o
       X
    [ menu ]
CEI Labs Natas 1: Right-Click Block
Account: natas1
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas2: Directory Traversal (Files) (color: #37bea4)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Directory Traversal (Files)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
  [/][/][..]-->
  [^][^][v]
  door door door
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
  door door door
  [^][^][v]
  [/][/][..]-->
CEI Labs Natas 2: Directory Traversal (Files)
Account: natas2
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas3: Web Crawlers (Robots.txt) (color: #37be81)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Web Crawlers (Robots.txt)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
    /|\
   --*--  web
    \|/
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
    \|/
   --*--  web
    /|\
CEI Labs Natas 3: Web Crawlers (Robots.txt)
Account: natas3
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas4: Referer Spoofing (color: #37be5e)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Referer Spoofing"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
   o
  /|\  letter
  / \  (mirrored)
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
  / \  (mirrored)
  /|\  letter
   o
CEI Labs Natas 4: Referer Spoofing
Account: natas4
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas5: Cookie Manipulation (color: #37be3a)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Cookie Manipulation"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
  ( o o )
  ( o X )  jar
  `-----'
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
  `-----'
  ( o X )  jar
  ( o o )
CEI Labs Natas 5: Cookie Manipulation
Account: natas5
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas6: Hidden Inclusion Files (color: #57be37)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Hidden Inclusion Files"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
  ~~~~~~~~
  ~~[ ]~~  rug
     |
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
     |
  ~~[ ]~~  rug
  ~~~~~~~~
CEI Labs Natas 6: Hidden Inclusion Files
Account: natas6
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas7: Local File Inclusion (LFI) (color: #7abe37)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Local File Inclusion (LFI)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
  [box]<--[../../file]
  [D][D][D]
   \  |  /
    [ ]
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
    [ ]
   \  |  /
  [D][D][D]
  [box]<--[../../file]
CEI Labs Natas 7: Local File Inclusion (LFI)
Account: natas7
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas8: Reversing Crypto Schemes (color: #9ebe37)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Reversing Crypto Schemes"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
   .--.
  ( () )
   `--'
  (mirrored)
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
  (mirrored)
   `--'
  ( () )
   .--.
CEI Labs Natas 8: Reversing Crypto Schemes
Account: natas8
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas9: Command Injection I (color: #bebb37)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Command Injection I"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
   o
  /|\  ...
  / \
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
  / \
  /|\  ...
   o
CEI Labs Natas 9: Command Injection I
Account: natas9
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas10: Command Injection II (Sanitization Bypass) (color: #be9737)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Command Injection II (Sanitization Bypass)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
   o
  /|\ -->[ ]
  / \
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
  / \
  /|\ -->[ ]
   o
CEI Labs Natas 10: Command Injection II (Sanitization Bypass)
Account: natas10
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas11: XOR Encryption Bypass (color: #be7437)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "XOR Encryption Bypass"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
  \   /
   \ /
    X
   / \
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
   / \
    X
   \ /
  \   /
CEI Labs Natas 11: XOR Encryption Bypass
Account: natas11
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas12: Arbitrary File Upload (Web Shell) (color: #be5137)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "Arbitrary File Upload (Web Shell)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
   o
  /|\  [==>
  / \   slot
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
  / \   slot
  /|\  [==>
   o
CEI Labs Natas 12: Arbitrary File Upload (Web Shell)
Account: natas12
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas13: File Upload Bypass (Magic Bytes) (color: #be3741)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "File Upload Bypass (Magic Bytes)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
  [ parcel ]
     (o)
   false seal
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
   false seal
     (o)
  [ parcel ]
CEI Labs Natas 13: File Upload Bypass (Magic Bytes)
Account: natas13
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

### natas14: SQL Injection (SQLi) (color: #be3764)

**Prompt used:**
```
You are creating a small ASCII/Unicode art image for a CTF training login banner.

Output constraints: each line <=80 single-width characters (box-drawing,
block-element, and dingbat glyphs are fine; no emoji, no CJK-width
characters -- one character must equal one terminal column), no
profanity, no real-world hate symbols, no copyrighted characters or
logos. There is no hard line-count cap.

Overall track theme: "Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down digital underworld where the ordinary logic of the web gets inverted and manipulated -- the same mirrored visual language as the attacker workstation's desktop wallpaper. Banner art color follows the page's own cool-blue-to-hot-magenta per-level hue progression.
This piece is for the question titled: "SQL Injection (SQLi)"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general nature of the question (what kind of technique or
vulnerability is involved) -- visual depictions of what kind of thing is
going on are fine. Do NOT write any actual instructional text/words that
explain, name, or spell out the specific command, tool, payload, or step
needed to solve it. Output only the art, nothing else.
```
**Rendered banner (`<pre class="cei-login-banner">` block, art colorized in browser):**
```
  [=======]
  [=cracked=]
  [=======]
  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
  [=======]
  [=cracked=]
  [=======]
CEI Labs Natas 14: SQL Injection (SQLi)
Account: natas14
Authorized CEI Labs training only. Misuse of this system is prohibited.
Do not use AI or external tools/services to cheat or obtain answers.
Stay within your assigned challenge environment only.
```

