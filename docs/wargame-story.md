# Wargame Storyboard: Story & Generation Prompts

A simple, on-theme story for each track, split into the same beats the storyboard banners already visualize structurally (see [`wargame-themes.md`](wargame-themes.md)'s "Storyboard mechanic" section). Every level has its own prompt below.

**What these prompts are for.** They are the canonical brief for any future hand-drawn or regenerated per-level art. They are *not* a build input today: current banner art is produced programmatically (chapter boxes, transmission strips, depth shafts) by the three `generate_banners.py` scripts, so nothing here is read at build time. Level titles and Bandit's chapter boundaries in this file are pulled straight from those generators, so the two can't silently drift apart.

**Chapters are internal.** Chapter and beat names are design vocabulary for us; they are deliberately *not* printed in the banners players see. The banner conveys position visually (which chapter box you're in, and where inside it), not by name.

## Shared constraints

Every prompt below is read together with these, rather than repeating them 56 times:

```
Single-width characters only -- ASCII plus box-drawing, block-element,
and dingbat glyphs. No emoji, no CJK-width characters (one character
must equal one terminal column). Each line <= 80 columns. Height is
flexible: SSH clients scroll, so a banner may exceed one screen, but
keep it proportionate to the banners around it.

Stay inside the story's world. The general KIND of thing happening may
come through -- something searched, something turned, something opened
-- but never write text or draw anything that names or spells out the
specific command, tool, payload, or step needed to solve the challenge.
A player must never be able to read a solution off a banner.
```

## Bandit -- "The Vault at Dryrock"

An outlaw known only by reputation slips into the walled desert compound of Dryrock Hold after dark, hunting a ledger locked in its deepest vault -- proof enough to clear an old debt, or bury it forever. Room by room they search, borrow authority that isn't theirs, wait out the bell, and work deeper, until the record room opens and the escape is made through the far wall.

Chapter boundaries follow the track's own content clusters (the cron levels stay together, the git levels stay together, and so on) rather than an even numeric split, so a chapter change always lands where the material actually changes.

| # | Chapter | Levels | Arc |
|---|---|---|---|
| 1 | Over the Wall | bandit0-4 | the outer gate and the first steps inside the compound |
| 2 | The Storeyard | bandit5-10 | a yard of crates and outbuildings, searched for anything useful |
| 3 | The Inner Halls | bandit11-16 | corridors, curtained hatches, and doors that want keys |
| 4 | The Guardroom | bandit17-20 | where the compound's authority is kept, and borrowed |
| 5 | The Bell Tower | bandit21-23 | everything here runs on the schedule the bell keeps |
| 6 | The Locked Wing | bandit24-26 | rooms built to hold someone, worked open from inside |
| 7 | The Archive | bandit27-31 | the record room at the heart of it -- the ledger, and its whole history |
| 8 | The Escape | bandit32-33 | out through the far wall with what you came for |

| Level | Title | Chapter | Prompt |
|---|---|---|---|
| bandit0 | The First Step | Over the Wall | Depict this moment: the outer gate gives, and the first footfall lands inside the walls. Chapter setting: Over the Wall. Carry the mood of the title "The First Step". |
| bandit1 | Dashed Hopes | Over the Wall | Depict this moment: the first passage ends at nothing -- a blank wall where a way should have been. Chapter setting: Over the Wall. Carry the mood of the title "Dashed Hopes". |
| bandit2 | Spaces in Places | Over the Wall | Depict this moment: a gap between two structures, just wide enough to turn sideways and pass. Chapter setting: Over the Wall. Carry the mood of the title "Spaces in Places". |
| bandit3 | Hidden in Plain Sight | Over the Wall | Depict this moment: something left out in the open, unremarkable enough that nobody thought to guard it. Chapter setting: Over the Wall. Carry the mood of the title "Hidden in Plain Sight". |
| bandit4 | Human Readable | Over the Wall | Depict this moment: a note left behind, in a hand that can actually be read. Chapter setting: Over the Wall. Carry the mood of the title "Human Readable". |
| bandit5 | The Needle | The Storeyard | Depict this moment: one small thing worth having, buried in a yard holding everything else. Chapter setting: The Storeyard. Carry the mood of the title "The Needle". |
| bandit6 | Server Search | The Storeyard | Depict this moment: the search widens to every shed and outbuilding on the grounds. Chapter setting: The Storeyard. Carry the mood of the title "Server Search". |
| bandit7 | The Millionth Word | The Storeyard | Depict this moment: a counted place, deep in a very long manifest of stored goods. Chapter setting: The Storeyard. Carry the mood of the title "The Millionth Word". |
| bandit8 | The Only One | The Storeyard | Depict this moment: a single item that appears exactly once where everything else repeats. Chapter setting: The Storeyard. Carry the mood of the title "The Only One". |
| bandit9 | Strings Attached | The Storeyard | Depict this moment: readable marks scratched along the side of something otherwise blank. Chapter setting: The Storeyard. Carry the mood of the title "Strings Attached". |
| bandit10 | Base Operations | The Storeyard | Depict this moment: goods packed tight for transport, meaningless until they're unpacked. Chapter setting: The Storeyard. Carry the mood of the title "Base Operations". |
| bandit11 | Substitution | The Inner Halls | Depict this moment: one thing quietly exchanged for another, and nobody looks twice. Chapter setting: The Inner Halls. Carry the mood of the title "Substitution". |
| bandit12 | Matryoshka | The Inner Halls | Depict this moment: a case inside a case inside a case, each opened in its turn. Chapter setting: The Inner Halls. Carry the mood of the title "Matryoshka". |
| bandit13 | Private Keys | The Inner Halls | Depict this moment: a key belonging to one person only, now held in the wrong hand. Chapter setting: The Inner Halls. Carry the mood of the title "Private Keys". |
| bandit14 | Port Submission | The Inner Halls | Depict this moment: a message pushed through a narrow hatch to whoever waits on the far side. Chapter setting: The Inner Halls. Carry the mood of the title "Port Submission". |
| bandit15 | SSL Encryption | The Inner Halls | Depict this moment: the same hatch, but the exchange now happens behind a drawn curtain. Chapter setting: The Inner Halls. Carry the mood of the title "SSL Encryption". |
| bandit16 | SSL Port Scan | The Inner Halls | Depict this moment: a corridor of curtained hatches, walked end to end, testing which one answers. Chapter setting: The Inner Halls. Carry the mood of the title "SSL Port Scan". |
| bandit17 | File Comparisons | The Guardroom | Depict this moment: two near-identical ledgers laid side by side to find the one difference. Chapter setting: The Guardroom. Carry the mood of the title "File Comparisons". |
| bandit18 | Shell Bypass | The Guardroom | Depict this moment: the door shuts the instant it opens; a way in that doesn't use the door. Chapter setting: The Guardroom. Carry the mood of the title "Shell Bypass". |
| bandit19 | SUID Escalation | The Guardroom | Depict this moment: borrowing a uniform that opens doors your own never would. Chapter setting: The Guardroom. Carry the mood of the title "SUID Escalation". |
| bandit20 | Port Listener Connection | The Guardroom | Depict this moment: arranging for someone inside to answer when you knock. Chapter setting: The Guardroom. Carry the mood of the title "Port Listener Connection". |
| bandit21 | Cron Jobs | The Bell Tower | Depict this moment: the tower bell marks the rounds -- everything here happens on a schedule. Chapter setting: The Bell Tower. Carry the mood of the title "Cron Jobs". |
| bandit22 | Cron Debugging | The Bell Tower | Depict this moment: a scheduled round that isn't running the way the schedule claims. Chapter setting: The Bell Tower. Carry the mood of the title "Cron Debugging". |
| bandit23 | Cron Scripting | The Bell Tower | Depict this moment: leaving your own instruction for the next time the bell rings. Chapter setting: The Bell Tower. Carry the mood of the title "Cron Scripting". |
| bandit24 | PIN Brute Force | The Locked Wing | Depict this moment: a numbered lock, no key, and patience enough to try every setting. Chapter setting: The Locked Wing. Carry the mood of the title "PIN Brute Force". |
| bandit25 | Shell Breakout | The Locked Wing | Depict this moment: held in a room built to hold you; finding the seam in it anyway. Chapter setting: The Locked Wing. Carry the mood of the title "Shell Breakout". |
| bandit26 | Text UI Breakout | The Locked Wing | Depict this moment: a narrower cell than the last, with even less left to work with. Chapter setting: The Locked Wing. Carry the mood of the title "Text UI Breakout". |
| bandit27 | Git Clone | The Archive | Depict this moment: the record room at last -- a full copy of the trail, taken to read elsewhere. Chapter setting: The Archive. Carry the mood of the title "Git Clone". |
| bandit28 | Git Commits | The Archive | Depict this moment: reading back through the ledger, entry by dated entry. Chapter setting: The Archive. Carry the mood of the title "Git Commits". |
| bandit29 | Git Branches | The Archive | Depict this moment: the record splits into two versions of the same events, kept side by side. Chapter setting: The Archive. Carry the mood of the title "Git Branches". |
| bandit30 | Git Tags | The Archive | Depict this moment: certain entries marked out as weightier than the rest. Chapter setting: The Archive. Carry the mood of the title "Git Tags". |
| bandit31 | Git Push | The Archive | Depict this moment: writing something new back into the record, in your own hand. Chapter setting: The Archive. Carry the mood of the title "Git Push". |
| bandit32 | Shell Overrides | The Escape | Depict this moment: the last door answers to a different master than it should. Chapter setting: The Escape. Carry the mood of the title "Shell Overrides". |
| bandit33 | Final Escape | The Escape | Depict this moment: out through the far wall with the ledger, into open dark. Chapter setting: The Escape. Carry the mood of the title "Final Escape". |

## Krypton -- "Signal from the Dark"

A deep-space listening post catches a faint transmission no one can place. Over one long night shift the operator peels back layer after layer, watching the signal grow stranger -- less like noise, more like something reaching back -- until the last layer reveals a pattern that never quite repeats, and never quite stops.

| Level | Title | Beat | Prompt |
|---|---|---|---|
| krypton0 | Base64 Decoding | First Contact | Depict this moment: the initial garbled burst arrives -- barely a shape yet, just noise waiting to be unpacked. Beat: "First Contact". Carry the mood of the title "Base64 Decoding". |
| krypton1 | ROT13 Substitution Cipher | A Simple Turn | Depict this moment: cleaned up, the signal reveals a plain rotating pattern, easy enough once you see it spin. Beat: "A Simple Turn". Carry the mood of the title "ROT13 Substitution Cipher". |
| krypton2 | Caesar Cipher (Unknown Shift) | Off by Some Amount | Depict this moment: the same kind of turn, but the amount is unknown now, hidden in shadow. Beat: "Off by Some Amount". Carry the mood of the title "Caesar Cipher (Unknown Shift)". |
| krypton3 | Frequency Analysis | Listening Closer | Depict this moment: studying which parts of the signal recur, looking for structure inside the noise. Beat: "Listening Closer". Carry the mood of the title "Frequency Analysis". |
| krypton4 | Vigenere Cipher (Known Key Length) | A Recurring Shape | Depict this moment: a repeating structure surfaces at a steady interval, like a heartbeat. Beat: "A Recurring Shape". Carry the mood of the title "Vigenere Cipher (Known Key Length)". |
| krypton5 | Vigenere Cipher (Kasiski Test) | Finding the Rhythm | Depict this moment: hunting repeated fragments across the whole transmission to learn its hidden interval. Beat: "Finding the Rhythm". Carry the mood of the title "Vigenere Cipher (Kasiski Test)". |
| krypton6 | Stream Cipher / LFSR | The Deepest Layer | Depict this moment: the signal folds back on itself endlessly, alien and self-referential, its source still unseen. Beat: "The Deepest Layer". Carry the mood of the title "Stream Cipher / LFSR". |

## Natas -- "Into the Mirror"

A researcher logs into a web application built like an inverted underworld -- every layer of ordinary web logic mirrored, twisted, or hidden just beneath the surface. Each floor down leads further from what a browser is supposed to show you, toward the raw records at the bottom.

| Level | Title | Beat | Prompt |
|---|---|---|---|
| natas0 | View Source | Just Beneath the Surface | Depict this moment: peering past what the page shows you, to what it's actually made of. Beat: "Just Beneath the Surface". Carry the mood of the title "View Source". |
| natas1 | Right-Click Block | A Simple Obstacle | Depict this moment: a small, easily sidestepped barrier built to look like a wall. Beat: "A Simple Obstacle". Carry the mood of the title "Right-Click Block". |
| natas2 | Directory Traversal (Files) | Unlisted Rooms | Depict this moment: wandering into corridors that were never meant to be found. Beat: "Unlisted Rooms". Carry the mood of the title "Directory Traversal (Files)". |
| natas3 | Web Crawlers (Robots.txt) | The Sign No One Reads | Depict this moment: a posted notice that only politely asks you not to look. Beat: "The Sign No One Reads". Carry the mood of the title "Web Crawlers (Robots.txt)". |
| natas4 | Referer Spoofing | A Forged Invitation | Depict this moment: claiming to have arrived from somewhere you never were. Beat: "A Forged Invitation". Carry the mood of the title "Referer Spoofing". |
| natas5 | Cookie Manipulation | A Jar Left Open | Depict this moment: something small and personal, left where it can be changed. Beat: "A Jar Left Open". Carry the mood of the title "Cookie Manipulation". |
| natas6 | Hidden Inclusion Files | Beneath the Rug | Depict this moment: a trapdoor tucked under something entirely ordinary-looking. Beat: "Beneath the Rug". Carry the mood of the title "Hidden Inclusion Files". |
| natas7 | Local File Inclusion (LFI) | A Path Too Far | Depict this moment: a door that opens further than it was ever meant to. Beat: "A Path Too Far". Carry the mood of the title "Local File Inclusion (LFI)". |
| natas8 | Reversing Crypto Schemes | Its Own Reflection | Depict this moment: a lock that, mirrored, shows you its own key. Beat: "Its Own Reflection". Carry the mood of the title "Reversing Crypto Schemes". |
| natas9 | Command Injection I | An Extra Word | Depict this moment: slipping one more instruction in among the expected ones. Beat: "An Extra Word". Carry the mood of the title "Command Injection I". |
| natas10 | Command Injection II (Sanitization Bypass) | Past the Watchman | Depict this moment: the same trick, but something is standing guard over it now. Beat: "Past the Watchman". Carry the mood of the title "Command Injection II (Sanitization Bypass)". |
| natas11 | XOR Encryption Bypass | Two Crossed Beams | Depict this moment: where two things overlap, a third thing appears. Beat: "Two Crossed Beams". Carry the mood of the title "XOR Encryption Bypass". |
| natas12 | Arbitrary File Upload (Web Shell) | Through the Slot | Depict this moment: passing something of your own choosing to the other side. Beat: "Through the Slot". Carry the mood of the title "Arbitrary File Upload (Web Shell)". |
| natas13 | File Upload Bypass (Magic Bytes) | A False Seal | Depict this moment: the same delivery, wearing a disguise good enough to pass inspection. Beat: "A False Seal". Carry the mood of the title "File Upload Bypass (Magic Bytes)". |
| natas14 | SQL Injection (SQLi) | The Vault of Records | Depict this moment: the deepest floor, where everything is finally kept plainly -- and cracked open. Beat: "The Vault of Records". Carry the mood of the title "SQL Injection (SQLi)". |
