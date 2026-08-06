import os
import shutil
import json

from hint_economy import managed_tiers

# This track has no per-team Docker instance at all -- there is nothing on
# VLAN 20 to launch. The "target" is the player's own laptop: install
# CEI Labs Agent there, point it at ANY challenge box they already have
# running (Bandit/Krypton/Natas), and prove the whole toolchain actually
# works end to end. So none of these challenges set instance_type/image/
# instance_group -- they are plain "standard" CTFd challenges with static
# flags, verified by the player running `ctf-agent-verify` locally and
# reading back the flag it prints for each milestone that genuinely passed.
#
# See https://github.com/Judgernaut777/CEI-Labs-Agent (the agent itself) and
# its src/cei_labs_agent/verify.py (the ctf-agent-verify tool this track is
# built around) for the actual verification logic these flags come from.

# Deliberately NOT one of the game-stages.yml wave-gated tracks (see that
# file and scripts/validate_game_stages.py): those exist to hide/reveal
# shared per-team boxes in timed waves, which doesn't apply here since there
# is no shared box. Visibility for this track is instead controlled by
# RELEASE_STATE below, a plain manual on/off switch -- not a timed wave.
#
# Defaults to "hidden": the organizer releases this track by choice, on
# their own schedule, not automatically alongside deploy. To release it,
# set the environment variable at generation time -- no repo edit:
#
#   CEI_AGENT_RELEASE_STATE=visible python3 scripts/build_agent.py
#
# then redeploy/resync (`ctf challenge sync challenges/cei-agent-*` or a
# full deploy.sh run). Or, without running this script at all: toggle each
# challenge's visibility directly in the CTFd admin UI (Challenges ->
# select -> Hidden/Visible).
#
# This used to be a hardcoded constant an organizer edited in place, which
# meant releasing the track dirtied a tracked file. On a real station that
# edit then sat uncommitted indefinitely, so `git status` could not
# distinguish "event-day toggle" from "unshipped work" -- and the machine's
# actual release state was invisible to anyone reading the repo. Sourcing it
# from the environment keeps the default honest in git while letting a
# station override it per run.
_VALID_RELEASE_STATES = ("hidden", "visible")
RELEASE_STATE = os.environ.get("CEI_AGENT_RELEASE_STATE", "hidden").strip().lower()
if RELEASE_STATE not in _VALID_RELEASE_STATES:
    raise SystemExit(
        f"CEI_AGENT_RELEASE_STATE must be one of {_VALID_RELEASE_STATES}, "
        f"got {RELEASE_STATE!r}. Leave it unset for the default "
        f"({_VALID_RELEASE_STATES[0]})."
    )

FLAG_START_HERE = (
    "CEI Labs Agent is a permitted exception to the 'no AI or outside "
    "tools' rule you read in Bandit/Krypton/Natas -- it is the one AI tool "
    "this event explicitly sanctions, and only for the purpose this track "
    "covers: setting it up and using it as your own copilot. It does not "
    "grant a blanket exception to use any other outside AI/tooling on the "
    "other tracks."
)

challenges_data = [
    {
        "id": "cei-agent-start-here",
        "name": "AI Copilot Setup: Start Here",
        "points": 10,
        "desc": (
            "## Goal\n"
            "Read the rules for this track, then set up your own local AI "
            "copilot for the rest of the event.\n\n"
            "---\n\n"
            "### What this is\n"
            "[CEI Labs Agent](https://github.com/Judgernaut777/CEI-Labs-Agent) is a small, "
            "free AI assistant that runs entirely on YOUR laptop (via [Ollama](https://ollama.com), "
            "no API key, no account, no cloud bill) and helps coach you through the Bandit, "
            "Krypton, and Natas tracks -- it runs real commands against a challenge box you "
            "point it at, explains what it finds, and nudges you toward the next step instead "
            "of just handing you the answer.\n\n"
            "**This is the one and only sanctioned exception to the 'no AI or outside tools' "
            "rule** you already read at the start of Bandit/Krypton/Natas -- it applies "
            "specifically to installing and using this one tool, for this track. It does not "
            "excuse using any other outside AI/service to solve the other tracks' levels "
            "directly; that rule still stands everywhere else.\n\n"
            "---\n\n"
            "### Get started\n"
            "1. Download `bootstrap.sh` (macOS/Linux) or `bootstrap.ps1` (Windows) below, "
            "then run ONE command -- it installs Ollama, the agent, and its dependencies, "
            "then opens the app in your browser:\n"
            "   - **Windows** (open PowerShell, paste this one line; it works even though "
            "Windows blocks downloaded scripts by default -- `-ExecutionPolicy Bypass` "
            "applies to this command only, no system setting is changed and you do NOT "
            "need `Set-ExecutionPolicy` or `Unblock-File`):\n"
            "     ```powershell\n"
            "     powershell -ExecutionPolicy Bypass -NoProfile -File \"$env:USERPROFILE\\Downloads\\bootstrap.ps1\"\n"
            "     ```\n"
            "     (If you saved `bootstrap.ps1` somewhere other than Downloads, adjust the "
            "path.)\n"
            "   - **macOS / Linux** (in Terminal):\n"
            "     ```sh\n"
            "     bash ~/Downloads/bootstrap.sh\n"
            "     ```\n"
            "2. `README.md` and `TROUBLESHOOTING.md` (also attached) cover the full setup "
            "story and every common snag (disk space, security warnings, PATH issues, and "
            "more) -- keep them handy.\n"
            "3. `cei-labs-agent-site-offline.zip` is a complete offline copy of the project's "
            "info site, in case venue Wi-Fi is unreliable -- see the `HOW-TO-RUN-OFFLINE.md` "
            "inside it for how to serve it locally with one command.\n\n"
            "---\n\n"
            "### How verification works\n"
            "Every challenge in this track is verified by a small command-line tool that "
            "ships with the agent, `ctf-agent-verify` -- it checks a real, specific milestone "
            "and prints that challenge's flag only when the milestone is genuinely true on "
            "your machine. Nothing here is guessable without actually doing the step.\n\n"
            "---\n\n"
            "### Flag\n"
            "Run `ctf-agent-verify` after finishing setup and it will tell you "
            "which of the five later challenges you've already completed. For THIS "
            "challenge, submit the exact sentence below (word for word) confirming you "
            "understand the AI-use exception this track carves out -- copy it precisely:\n\n"
            f"> {FLAG_START_HERE}"
        ),
        "flag": FLAG_START_HERE,
        "files": [
            "files/bootstrap.sh",
            "files/bootstrap.ps1",
            "files/README.md",
            "files/TROUBLESHOOTING.md",
            "files/cei-labs-agent-site-offline.zip",
        ],
    },
    {
        "id": "cei-agent-01-ollama",
        "name": "AI Copilot Setup 1: Get Your Local Brain Running",
        "points": 100,
        "desc": (
            "## Goal\n"
            "Get Ollama (the local AI runtime CEI Labs Agent depends on) "
            "installed and running.\n\n"
            "---\n\n"
            "### Why it matters\n"
            "Nothing else in this track works until this piece is alive -- the agent "
            "itself is just a thin app that talks to Ollama over a small local network "
            "API; if that service isn't running, there is no 'brain' behind it yet.\n\n"
            "---\n\n"
            "### Do this\n"
            "Run the bootstrap script from **Start Here** if you haven't -- it installs "
            "Ollama for you automatically. Then run:\n```\nctf-agent-verify\n```\n"
            "and read the flag next to check `[1/5]` once it reports PASS."
        ),
        "flag": "CEI-AGENT-1-OLLAMA-IS-ALIVE",
    },
    {
        "id": "cei-agent-02-model",
        "name": "AI Copilot Setup 2: Pull a Model",
        "points": 100,
        "desc": (
            "## Goal\n"
            "Get at least one AI model actually downloaded and installed.\n\n"
            "---\n\n"
            "### Why it matters\n"
            "An AI runtime with no model loaded can't think about anything yet -- Ollama "
            "needs to be told which specific model to download and use. The app's "
            "settings panel pre-selects one sized to fit your laptop's memory; click "
            "**Install model** there and wait for it to finish.\n\n"
            "---\n\n"
            "### Do this\n"
            "Then re-run:\n```\nctf-agent-verify\n```\n"
            "and check `[2/5]` for the flag."
        ),
        "flag": "CEI-AGENT-2-A-BRAIN-IS-INSTALLED",
    },
    {
        "id": "cei-agent-03-install",
        "name": "AI Copilot Setup 3: Install and Launch the Agent",
        "points": 100,
        "desc": (
            "## Goal\n"
            "Get `ctf-agent` itself properly installed on your machine, not "
            "just downloaded.\n\n"
            "---\n\n"
            "### Why it matters\n"
            "Running the bootstrap script from **Start Here** installs `uv` (a Python "
            "tool manager), then uses it to install the `ctf-agent`/`ctf-agent-verify` "
            "commands from the CEI Labs Agent repository, and finally launches the app.\n\n"
            "---\n\n"
            "### Do this\n"
            "Once it's finished, open a terminal and run:\n```\nctf-agent-verify\n```\n"
            "(If it says the command isn't found, close your terminal and open a fresh "
            "one -- see TROUBLESHOOTING.md.) Check `[3/5]` for the flag."
        ),
        "flag": "CEI-AGENT-3-CTF-AGENT-IS-RUNNING",
    },
    {
        "id": "cei-agent-04-ssh",
        "name": "AI Copilot Setup 4: Point It At Your Box",
        "points": 150,
        "desc": (
            "## Goal\n"
            "Prove the agent can actually reach and run a real command on a "
            "challenge box -- not just chat.\n\n"
            "---\n\n"
            "### Why it matters\n"
            "The whole point of CEI Labs Agent is that it *acts*: it runs real commands "
            "over SSH against a box you point it at, reads the result, and reasons about "
            "it. This check performs a genuine SSH connection using the exact same tool "
            "code the agent itself uses internally -- so passing it proves that core "
            "capability really works end to end, not just in theory.\n\n"
            "---\n\n"
            "### Do this\n"
            "Launch (or reuse) **any** currently-running instance from Bandit, Krypton, "
            "or Natas, and copy its Host, Port, username, and password from that "
            "challenge's connect panel. Then run:\n```\nctf-agent-verify --host <host> --port <port> --user <username> --password <password>\n```\n"
            "Check `[4/5]` for the flag."
        ),
        "flag": "CEI-AGENT-4-CONNECTED-TO-MY-BOX",
    },
    {
        "id": "cei-agent-05-prompt",
        "name": "AI Copilot Setup 5: Know How To Ask For Help",
        "points": 150,
        "desc": (
            "## Goal\n"
            "Show you know the basic shape of a good first prompt.\n\n"
            "---\n\n"
            "### Why it matters\n"
            "CEI Labs Agent isn't a mind-reader -- what you type is the only thing that "
            "tells it which track and level you want help with, and that you're actually "
            "asking for help rather than just chatting. Naming a track (Bandit, Krypton, "
            "or Natas) and a level number, alongside an explicit ask like 'Help me with...', "
            "is the pattern that lets it orient itself immediately instead of guessing.\n\n"
            "---\n\n"
            "### Do this\n"
            "Run:\n```\nctf-agent-verify --prompt \"Help me with Bandit level 1\"\n```\n"
            "(any track and level number works -- it just has to follow that same shape). "
            "Check `[5/5]` for the flag, then go type that same kind of message into the "
            "real agent chat window and watch it actually work."
        ),
        "flag": "CEI-AGENT-5-I-KNOW-HOW-TO-ASK",
    },
]

HINTS = {
    "cei-agent-01-ollama": [
        "An AI model that runs entirely on your own laptop, with no account, no API key, and no monthly bill, has to be POWERED by something running locally that can actually load and execute it. What piece of software is that, and how would you know if it's already running versus not?",
        "Ollama is that piece: a small background service that loads AI models and exposes them over a tiny local network API (by default at `http://localhost:11434`), the same way a web server exposes a website. The agent app and the verification tool both just check whether that local address answers at all -- nothing more elaborate than that. If it's not installed yet, or installed but not currently running, that address won't respond.",
        "Run the bootstrap script from the **Start Here** challenge's downloadable files -- it installs Ollama automatically. If it's installed but not running, start it manually (`ollama serve` in a terminal on macOS/Linux, or launch the **Ollama** app from the Start Menu on Windows -- it usually starts itself after install and login). Then confirm:\n```\n$ ctf-agent-verify\n[1/5] PASS -- Ollama is installed and running\n      flag: CEI-AGENT-1-OLLAMA-IS-ALIVE\n```",
    ],
    "cei-agent-02-model": [
        "The runtime that CAN load an AI model isn't the same thing as actually HAVING one loaded. Where does the model itself -- the multi-gigabyte file with the actual 'thinking' in it -- come from, and does that happen automatically the first time you open the app?",
        "Models are downloaded ('pulled') separately from Ollama itself, and different models need different amounts of memory to run well. The app's settings panel checks how much free RAM your laptop has and pre-selects a model that should comfortably fit, with an **Install model** button that triggers the actual download -- this is a one-time, multi-gigabyte transfer, so it can take a few minutes the first time.",
        "Open the app (`ctf-agent`), take the pre-selected recommended model, and click **Install model** -- watch the progress bar until it finishes (or run `ollama pull <model-name>` directly in a terminal for the identical effect). Then confirm:\n```\n$ ctf-agent-verify\n[2/5] PASS -- At least one model is installed\n      flag: CEI-AGENT-2-A-BRAIN-IS-INSTALLED\n```",
    ],
    "cei-agent-03-install": [
        "Downloading a bootstrap script and actually having a working, on-PATH command afterward are two different milestones -- an installer can partially succeed, or install something that a CURRENTLY OPEN terminal window simply doesn't know about yet. What would tell you the difference between 'ran an install script' and 'genuinely have a working command'?",
        "The bootstrap script chains three real installs: a Python tool manager (`uv`), then the actual `ctf-agent`/`ctf-agent-verify` package pulled from its repository through that tool manager, and finally it launches the app once. A terminal window that was already open before the install finished won't see the new PATH entry -- that's normal, not a failure, and the fix is simply opening a fresh terminal.",
        "Run the bootstrap script from **Start Here** for your OS. Once it finishes, open a **new** terminal window (closing the old one, not just a new tab) and run:\n```\n$ ctf-agent-verify\n[3/5] PASS -- ctf-agent is installed and importable\n      flag: CEI-AGENT-3-CTF-AGENT-IS-RUNNING\n```\nIf the command still isn't found, see TROUBLESHOOTING.md's PATH section.",
    ],
    "cei-agent-04-ssh": [
        "An AI assistant that only ever talks in a chat window, without ever touching a real system, isn't actually doing the job this one is built for. What would genuinely PROVE it can reach out and interact with a real machine, rather than just claiming it can?",
        "The agent's one 'hands-on' capability is running a real command over SSH against whatever box you connect it to -- the exact same kind of connection you'd make yourself with a normal SSH client. The verification tool exercises that identical code path directly: it opens a real SSH session to a host you provide, runs a harmless command, and checks that a real response comes back -- proving the connectivity, not just trusting that it should work.",
        "Launch (or reuse) any Bandit, Krypton, or Natas instance and copy its Host/Port/username/password from that challenge's own connect panel. Then run:\n```\n$ ctf-agent-verify --host <host> --port <port> --user <username> --password <password>\n[4/5] PASS -- Connected to your challenge box over SSH\n      flag: CEI-AGENT-4-CONNECTED-TO-MY-BOX\n```\n(Illustrative only -- your real host/port/username/password will differ.)",
    ],
    "cei-agent-05-prompt": [
        "The agent has no way to read your mind about which level you're stuck on or that you even want help right now -- all of that has to come from what you actually type. What's the minimum information a message needs to carry for it to orient itself immediately, instead of guessing?",
        "The documented pattern is simple: name the track (Bandit, Krypton, or Natas), name a level, and explicitly ask for help -- something like 'Help me with Bandit level 1' or 'Help me figure out Natas level 3'. A vague message like just 'help' or 'I'm stuck' gives it nothing concrete to act on; naming the track and level is what lets it start reasoning about the right thing immediately.",
        "Run the verification tool with a prompt following that exact shape (any real track and level number is fine):\n```\n$ ctf-agent-verify --prompt \"Help me with Bandit level 1\"\n[5/5] PASS -- You know the basic help-prompt pattern\n      flag: CEI-AGENT-5-I-KNOW-HOW-TO-ASK\n```\nThen type that same kind of message into the real agent chat window and watch it actually go to work.",
    ],
}

# Generate folder and files
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))
assets_dir = os.path.abspath(os.path.join(script_dir, "..", "assets", "cei-labs-agent"))
os.makedirs(base_dir, exist_ok=True)

for ch in challenges_data:
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)

    full_desc = ch["desc"]
    escaped_desc = full_desc.replace(chr(10), chr(10) + "  ")

    files = ch.get("files")
    files_yaml = ""
    if files:
        files_dir = os.path.join(folder_path, "files")
        os.makedirs(files_dir, exist_ok=True)
        for rel in files:
            filename = os.path.basename(rel)
            src = os.path.join(assets_dir, filename)
            dst = os.path.join(files_dir, filename)
            shutil.copyfile(src, dst)
        files_yaml = "files:\n" + "".join(f'  - "{f}"\n' for f in files)

    yaml_content = f"""name: "{ch['name']}"
author: "CEI Labs (setup track for github.com/Judgernaut777/CEI-Labs-Agent)"
category: "AI Copilot Setup"
description: |
  {escaped_desc}
value: {ch['points']}
type: standard
flags:
  - "{ch['flag']}"
{files_yaml}state: {RELEASE_STATE}
version: "0.1"
"""
    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} AI Copilot Setup challenges inside '{base_dir}'!")
with open(os.path.join(base_dir, "agent-hint-wallet.json"), "w", encoding="utf-8") as manifest:
    json.dump(
        {
            "schema_version": 1,
            "track": "agent",
            "entries": [
                {
                    "name": c["name"],
                    "tiers": [
                        {"tier": n, "cost": cost, "content": text}
                        for n, (text, cost) in enumerate(managed_tiers(c["points"], HINTS[c["id"]]), 1)
                    ],
                }
                for c in challenges_data
                if c["id"] in HINTS
            ],
        },
        manifest,
    )
