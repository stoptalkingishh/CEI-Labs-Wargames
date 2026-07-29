# CEI Labs Agent

**Your friendly CTF training-wheels teammate — a small AI that runs on your own
laptop, helps you learn the wargames, and never needs an internet account, a
credit card, or an API key.**

CEI Labs Agent is a little coaching assistant for the CEI Labs Capture-the-Flag
event (the **Bandit**, **Krypton**, and **Natas** tracks). It is built for people
who are brand new to this and would otherwise be staring at a blank terminal
wondering where to even start.

It is **not** a robot that solves the challenge for you and hands you the answer.
It is a patient copilot that:

- actually runs commands on your assigned practice box (through the SSH details
  the challenge page gives you),
- reads the output and reasons about what it means,
- explains what is happening and nudges you toward the next step,
- and keeps private notes for you so you don't lose track of what you've found.

Think of it as sitting next to a helpful senior student who talks you through the
puzzle instead of just whispering the answer. When it finds a flag or a password,
it tells you **how** it got there and summarizes it — it deliberately avoids just
blurting out the raw flag, because the point is for *you* to learn.

---

## What makes it different

- **Runs entirely on your laptop.** The "brain" is a small local AI model served
  by [Ollama](https://ollama.com). Nothing you type and nothing from the
  challenge boxes is sent to any cloud service.
- **No API keys. No sign-ups. No cloud bill.** You never paste in a secret token
  or create an account anywhere. If your laptop can run it, you can use it — for
  free, forever.
- **No GPU required.** It's tuned to run on ordinary laptop CPUs. It won't be
  instant, but it works on the kind of machine most people bring to the event.
- **Sets itself up.** One command installs everything (the AI runtime, the agent,
  and its dependencies) and opens the app in your browser.
- **A real, friendly web app.** No cryptic command line to memorize — you get a
  clean chat window with dropdowns for picking your model and connecting to your
  challenge box.

---

## Install & run (one command)

Copy the single line for your operating system, paste it into your terminal, and
press Enter. It downloads and installs everything, then launches the app in your
web browser.

> The very first run downloads an AI model (a few gigabytes) and may take several
> minutes on a normal connection. That happens once — after that, start-up is
> quick. See **Not enough disk space** in
> [TROUBLESHOOTING.md](TROUBLESHOOTING.md#not-enough-disk-space) before you begin.

### macOS / Linux

Open the **Terminal** app and paste:

```sh
curl -fsSL https://raw.githubusercontent.com/Judgernaut777/CEI-Labs-Agent/main/bootstrap.sh | sh
```

### Windows

Open **PowerShell** (search for it in the Start menu, then click it) and paste:

```powershell
irm https://raw.githubusercontent.com/Judgernaut777/CEI-Labs-Agent/main/bootstrap.ps1 | iex
```

That's it. When the browser tab opens, you're ready to go.

### Starting it again later

After the first install, you don't need the long command again. Just open your
terminal and run:

```sh
ctf-agent
```

If your terminal says it can't find `ctf-agent`, **close it and open a fresh
one** — see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## Using it — the short version

1. **Pick a model.** When the app opens, the settings panel shows a menu of AI
   models. One is already pre-selected as the recommended choice for your laptop
   (more on this below). If it isn't installed yet, click **Install model** and
   watch the progress bar.
2. **Connect to your challenge box.** Your CTF challenge page (the instance
   launcher) gives you a host, port, username, and password. Type them into the
   SSH form and click **Test** to make sure it connects.
3. **Chat.** Ask it to help you with the level you're stuck on — for example,
   *"Help me figure out level 1 of Bandit."* Watch it run commands, read the
   results, and talk you through what it finds.

The chat shows you everything it does: the **commands** it runs, the **output**
it reads back, and its **explanation**. Nothing is hidden — that transparency is
part of the learning.

---

## Choosing a model (the model picker)

Different laptops have different amounts of memory (RAM), and bigger, smarter AI
models need more of it. So the app checks how much free memory you have and
**pre-selects the best model that comfortably fits your machine** — you don't
have to understand the details.

Each model in the menu is clearly labeled, so you can make an informed choice at a
glance:

- **Recommended** — the best all-round pick for a typical laptop. This is almost
  certainly the one you want. When in doubt, use it.
- **Installed** — you've already downloaded this one, so it starts instantly.
- **Fits / doesn't fit** — whether your laptop has enough free memory to run it
  smoothly. Models that don't fit are shown greyed out so you don't accidentally
  pick something that will crawl.
- **Tiers** — from **Featherweight** (for older or low-memory laptops) up through
  the **Default** and **Heavyweight** tiers to **Max** (for powerful machines with
  lots of RAM). Higher tiers reason better but need more memory and run slower.

Each model also offers one or two **presets** (like *Standard* and *Extended*)
that trade a bit more memory for more "working memory" during longer sessions.
The app tells you how much free memory each preset needs and greys out any that
won't fit. If you're not sure, leave the default preset selected.

**Bottom line:** open the app, take whatever it recommends, click Install if
needed, and start playing. You can always experiment with a different model later.

---

## A note on safety

CEI Labs Agent is designed to be safe to run on your own laptop, but it's worth
understanding what it does and doesn't do.

- **It only touches your practice box.** The agent's one and only "hands-on" tool
  is running commands over SSH against the challenge box you connect it to — the
  same box you could log into yourself. It **cannot** run commands on your own
  laptop. Local shell access is turned off by design.
- **Its notes are sandboxed.** The notes it keeps for you live in a single folder
  (`~/.cei-labs-agent/notes/`) and it cannot read or write anywhere else on your
  computer.
- **The wargames are deliberately sneaky — and so is the agent's guard against
  it.** CTF challenges sometimes contain text written specifically to trick
  automated tools ("prompt injection"). Because the agent reads challenge output,
  it's built to treat that content with suspicion and not blindly obey
  instructions hiding in it. Even in the worst case, the strict limits above mean
  the fallout is "the chat says something weird," never "something ran on your
  laptop."
- **This is a learning aid, not an anti-cheat system.** The gentle "explain,
  don't just hand over the flag" behavior is about helping you learn. Anyone who
  wants to can still SSH in and solve challenges by hand — that's fine and always
  was. The agent is simply a good default for people who'd otherwise be lost.

---

## What you'll need

- A **laptop** running macOS, Linux, or Windows.
- Roughly **8 GB of RAM or more** for a smooth experience (the app will pick a
  lighter model if you have less).
- A few **gigabytes of free disk space** for the AI model.
- The **SSH connection details** for your challenge box, from the CTF event's
  challenge page.
- A **normal internet connection** for the one-time setup and model download.
  After that, the agent itself runs offline.

You do **not** need: a graphics card, an API key, a cloud account, admin rights on
most machines, or any prior command-line experience.

---

## Having trouble?

Setup snags — not enough disk space, an antivirus or Windows SmartScreen warning,
a "command not found" message, or Ollama not starting — are all covered in
**[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**. If you're at the event, the live help
channel and loaner laptops are there for anything the guide doesn't fix.

---

## Verifying your setup (for the "AI Copilot Setup" CTF track)

If you're doing the CEI Labs CTF's **AI Copilot Setup** challenges, a separate
command checks your progress and prints the flag for each milestone you've
actually completed — installing correctly, running, connected to your box,
and so on:

```sh
ctf-agent-verify --host <your-challenge-host> --port <port> --user <username> --password <password> --prompt "Help me with Bandit level 1"
```

It's included automatically by the same one-line installer above. Run it
with no arguments any time to see which of the five checks still need
doing — each line tells you exactly what's missing. The `--prompt` value is
the same kind of message you'd type into the agent itself to ask for help
(see [Using it — the short version](#using-it--the-short-version) above);
any track/level works, it just needs to actually ask for help about a real
level.

---

## For the curious (how it works under the hood)

A small local AI model (served by Ollama) drives a plain, transparent
*act → run a tool → look at the result → act again* loop. Each turn, the model
proposes exactly one action as a small piece of structured text; the app runs it,
feeds the result back, and lets the model decide what to do next — until it has an
answer to explain to you. It's the same fundamental pattern the "big" AI agents
use, shrunk down to run comfortably on your own machine with training wheels on.

It's open source and lives at
<https://github.com/Judgernaut777/CEI-Labs-Agent>.
