# CEI-Labs-OTW-CTF 🚩

Part of the **CEI-Labs** ecosystem. 

This repository contains the infrastructure and challenge generation scripts to host a local Capture The Flag (CTF) event using **CTFd**, while leveraging the excellent educational wargames hosted by [OverTheWire](https://overthewire.org).

## 🎮 Featured Games
1. **Bandit:** Unix/Linux Basics
2. **Krypton:** Cryptography
3. **Natas:** Server-side Web Security

## 🚀 Setup Instructions

### 1. Generate and Deploy the Challenges
You can build and deploy the entire training pipeline directly into your CTFd instance using the automated deployment script. 

Ensure you pass your CTFd scoreboard details as environment variables if running in an automated CI/CD runner:

```bash
export CTFD_URL="[https://your-ctfd-scoreboard.com](https://your-ctfd-scoreboard.com)"
export CTFD_TOKEN="your_admin_token_here"

# This builds all modules (Bandit, Krypton, Natas) and syncs them
chmod +x deploy.sh
./deploy.sh
