# CEI-Labs-OTW-CTF 🚩

Part of the **CEI-Labs** ecosystem. 

This repository contains the infrastructure and challenge generation scripts to host a local Capture The Flag (CTF) event using **CTFd**, while leveraging the excellent educational wargames hosted by [OverTheWire](https://overthewire.org).

## 🎮 Featured Games
1. **Bandit:** Unix/Linux Basics
2. **Krypton:** Cryptography
3. **Natas:** Server-side Web Security

## 🚀 Setup Instructions

### 1. Generate the Challenges
The challenges are generated using Python scripts to format them perfectly for CTFd's `ctfcli` tool.

```bash
cd scripts/
python3 build_bandit.py
# python3 build_krypton.py
# python3 build_natas.py
