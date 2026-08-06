# Troubleshooting

Most setup snags fall into one of a handful of buckets. Find your symptom below.
If nothing here fixes it and you're at the event, the **live help channel** and
the **loaner laptops** are your fastest path — don't spend the whole session
fighting your laptop.

Jump to:

- [Not enough disk space](#not-enough-disk-space)
- [A security warning appeared (antivirus / Windows SmartScreen / macOS Gatekeeper)](#a-security-warning-appeared)
- [`ctf-agent` isn't found after installing (refresh your PATH)](#ctf-agent-isnt-found-after-installing)
- [Ollama won't start / "connection refused"](#ollama-wont-start)
- [Locked-down corporate or school laptops](#locked-down-corporate-or-school-laptops)
- [The AI model download is stuck or failed](#the-ai-model-download-is-stuck-or-failed)
- [The SSH "Test" button fails](#the-ssh-test-button-fails)
- [It runs, but it's very slow](#its-slow)
- [Still stuck?](#still-stuck)

---

## Not enough disk space

This is the **single most common** first-run failure, and the error message is
often confusing because the underlying tools don't always check space before they
start.

The AI models are large — a few gigabytes each — plus room for the runtime.
**Make sure you have at least ~10 GB free** before you start, and more if you plan
to try a bigger model.

- **The installer stops early, or a model download dies partway through.** Almost
  always disk space. Free some up and run the command again — it safely resumes.
- **Check your free space:**
  - **macOS:** Apple menu → *About This Mac* → *More Info* → *Storage*.
  - **Windows:** open *This PC* in File Explorer and look at your `C:` drive bar.
  - **Linux:** run `df -h ~` in a terminal and read the *Avail* column.
- **Free space fast:** empty your Trash/Recycle Bin, clear your Downloads folder,
  or remove a big model you're not using with `ollama rm <model-name>`
  (for example `ollama rm qwen3:14b`).

If you're short on space, pick a **Featherweight** or **Default** tier model in
the app's model picker — they're the smallest downloads.

---

## A security warning appeared

Because you're running an install command you copied from the internet, your
computer's built-in protections may pop up a warning. This is expected for any
tool distributed this way — it does **not** mean something is wrong. Here's how to
get past each one.

### Windows SmartScreen ("Windows protected your PC")

If a blue box appears while the installer runs:

1. Click **More info**.
2. Click **Run anyway**.

The installer only sets its permission change for that **single command's session**
— it does not weaken your computer's protection afterward.

### Antivirus flags the script or the download

Some antivirus products are cautious about scripts that download other programs.
If your AV quarantines or blocks the bootstrap:

- Choose **Allow** / **Trust** / **Keep** if prompted.
- If it silently blocked the download, you may need to briefly allow it in your AV
  dashboard, then re-run the command.
- On a personal laptop this is safe to allow. On a **work or school laptop**, the
  AV may be centrally managed and you may not be able to override it — see
  [Locked-down laptops](#locked-down-corporate-or-school-laptops).

### macOS "cannot be opened because it is from an unidentified developer" (Gatekeeper)

If macOS blocks a piece of the toolchain from opening:

1. Open **System Settings → Privacy & Security**.
2. Scroll to the **Security** section — you'll see a message about the blocked
   item with an **Open Anyway** button. Click it.
3. Confirm once more if asked.

---

## `ctf-agent` isn't found after installing

You finish the install, type `ctf-agent`, and the terminal says *command not
found* (or *not recognized*). **This is normal and easy to fix.**

The installer adds `ctf-agent` to your system's list of runnable programs (your
"PATH"), but a terminal window that was **already open** doesn't know about the
change yet.

**The fix: fully close your terminal window and open a brand-new one.** Then type:

```sh
ctf-agent
```

- **Windows:** close **all** PowerShell windows and open a fresh PowerShell.
- **macOS / Linux:** quit the Terminal app entirely (not just the tab) and reopen
  it. Or, if you'd rather not, run `source ~/.bashrc` (or `source ~/.zshrc` on a
  Mac) to refresh the current window.

If it *still* isn't found after a fresh terminal, re-run the original one-line
install command from the [README](README.md) — it's safe to run again.

---

## Ollama won't start

Ollama is the piece that actually runs the AI model. If the app shows the Ollama
status dot as **down** (red), or you see a *"connection refused"* message, the
Ollama background service isn't running.

Try these in order:

1. **Start it manually.** Open a terminal and run:

   ```sh
   ollama serve
   ```

   Leave that window open and try the app again. (On Windows, Ollama usually
   starts on its own after install and login — if it didn't, launch **Ollama**
   from the Start menu.)

2. **Restart it.** Fully quit Ollama and start it again:
   - **Windows / macOS:** quit Ollama from the menu bar / system tray icon, then
     reopen it from the Start menu / Applications.
   - **Linux:** `ollama serve` in a terminal, or restart the service if you
     installed it as one.

3. **Did the install actually finish?** If `ollama` itself is *"command not
   found,"* the Ollama install step didn't complete — often disk space or a
   security prompt. Re-run the one-line installer from the [README](README.md)
   and watch for a warning you may have missed.

4. **Reboot.** If all else fails, a restart reliably gets Ollama's background
   service running, especially on Windows right after the first install.

Once Ollama is up, refresh the app in your browser and the status dot should turn
green.

---

## PowerShell says "running scripts is disabled" or "not digitally signed"

**Symptoms (Windows):** you downloaded `bootstrap.ps1` and ran it, and PowerShell
answers with a red error like `File ...\bootstrap.ps1 cannot be loaded because
running scripts is disabled on this system`, or (after
`Set-ExecutionPolicy RemoteSigned`) `... is not digitally signed`.

**Why:** Windows blocks downloaded `.ps1` files by default. This is normal and
expected — nothing is broken.

**Fix — use the one-liner from the challenge page instead.** It runs the script
with a bypass that applies to that single command only (no system setting is
changed, nothing to unblock):

```powershell
powershell -ExecutionPolicy Bypass -NoProfile -File "$env:USERPROFILE\Downloads\bootstrap.ps1"
```

(Adjust the path if you saved `bootstrap.ps1` somewhere other than Downloads.)

If you already ran `Set-ExecutionPolicy`, no harm done — but you do not need it
with the command above.

---

## Locked-down corporate or school laptops

**Heads up: heavily managed work or school laptops are a known non-goal.** If your
laptop is controlled by an IT department, it may block installing software,
downloading large files, running scripts, or changing security settings — and you
typically can't override that yourself.

Symptoms: the install command fails immediately with a permissions error, your
antivirus blocks everything with no "allow" option, or you're told you don't have
rights to install anything.

**We are not going to try to defeat your IT department's controls, and you
shouldn't either.** Instead:

- **Use a loaner laptop.** The event provides machines that are ready to go — this
  is the intended solution for locked-down devices. Ask at the help desk / help
  channel.
- **Use a personal laptop** if you have one with you.

This isn't a bug we can patch — it's your organization's policy, working as
intended.

---

## The AI model download is stuck or failed

The first time you pick a model, the app downloads it (a few GB). If the progress
bar stalls or errors out:

- **Check your internet connection** — a large download needs a stable one. On
  flaky conference Wi-Fi, try again when it's less congested.
- **Check disk space** — see [Not enough disk space](#not-enough-disk-space).
- **Just retry.** Click **Install model** again. Downloads resume rather than
  starting over, so a retry usually pushes it the rest of the way.
- **Pick a smaller model.** If a big model keeps failing, a **Featherweight** or
  **Default** tier model downloads much faster and still works well for the
  wargames.

---

## The SSH "Test" button fails

If connecting to your challenge box doesn't work:

- **Double-check the details.** Copy the host, port, username, and password
  *exactly* from your CTF challenge page (the instance launcher). A trailing space
  or a wrong port is the usual culprit.
- **Make sure your challenge instance is running.** Many CTF platforms only start
  your box after you click a "launch" / "start" button — and it may take a minute
  to come up.
- **Try again in a moment.** Freshly launched boxes sometimes aren't ready for the
  first few seconds.
- **Check the error message** the app shows — it usually says whether it was a
  wrong password, an unreachable host, or a timeout, which points you at the fix.

---

## It's slow

The AI runs on your laptop's CPU, so it thinks at "reading speed," not instantly —
that's expected, especially on modest hardware. To speed things up:

- **Use the recommended model and its default preset.** Bigger models and larger
  presets are smarter but noticeably slower.
- **Drop to a lighter tier.** A **Featherweight** or **Default** model responds
  faster on older laptops.
- **Close other heavy apps** (lots of browser tabs, video calls) to free up
  memory and CPU.

A little patience goes a long way — watching it work through a problem step by
step is part of the point.

---

## Still stuck?

- Re-run the one-line install command from the [README](README.md) — it's safe to
  run repeatedly and fixes many half-finished installs.
- **Restart your computer** — genuinely resolves a surprising number of first-run
  gremlins.
- Ask in the **event help channel** or grab a **loaner laptop**. You came here to
  learn the CTF, not to debug an installer — lean on the humans in the room.
