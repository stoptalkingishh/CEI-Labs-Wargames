import os

# Define the dataset for Bandit Levels 0 to 33
challenges_data = [
    {
        "id": "bandit-00",
        "name": "Bandit 0 -> 1: The First Step",
        "points": 100,
        "desc": "**Goal:** Connect to the server and retrieve the flag.\n\nSSH into `bandit.labs.overthewire.org` on port `2220`.\nUsername: `bandit0`\nPassword: `bandit0`\n\nRead the `readme` file in the home directory to find the password for the next level. Submit that password here as your flag.",
        "flag": "NH2SXQwcBdpmTEzi3bvBHRW9NXrY9B1b"
    },
    {
        "id": "bandit-01",
        "name": "Bandit 1 -> 2: Dashed Hopes",
        "points": 150,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit1`).\n\nFind the password for the next level hidden in the file named `-` (a single dash).",
        "flag": "rRGizSaX8Mk1RTb1CNQoXTcYZUR6OUZY"
    },
    {
        "id": "bandit-02",
        "name": "Bandit 2 -> 3: Spaces in Places",
        "points": 200,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit2`).\n\nThe password for the next level is stored in a file called `spaces in this filename` in the home directory.",
        "flag": "aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lEWG"
    },
    {
        "id": "bandit-03",
        "name": "Bandit 3 -> 4: Hidden in Plain Sight",
        "points": 250,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit3`).\n\nThe password for the next level is hidden in a file located in the `inhere` directory. You will need to view hidden files to find it.",
        "flag": "2EW7BBsr6aMMoJ2HjW067zg8WNkNzbpm"
    },
    {
        "id": "bandit-04",
        "name": "Bandit 4 -> 5: Human Readable",
        "points": 300,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit4`).\n\nThe password is in one of the files in the `inhere` directory. It is the only file that contains human-readable text.",
        "flag": "lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR"
    },
    {
        "id": "bandit-05",
        "name": "Bandit 5 -> 6: The Needle",
        "points": 350,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit5`).\n\nThe password is in a file somewhere under the `inhere` directory. The file has 3 properties:\n1. Human-readable\n2. Exactly 1033 bytes in size\n3. Not executable",
        "flag": "P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU"
    },
    {
        "id": "bandit-06",
        "name": "Bandit 6 -> 7: Server Search",
        "points": 400,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit6`).\n\nThe password is saved somewhere on the server. It is owned by user `bandit7`, owned by group `bandit6`, and is exactly 33 bytes in size.",
        "flag": "z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S"
    },
    {
        "id": "bandit-07",
        "name": "Bandit 7 -> 8: The Millionth Word",
        "points": 450,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit7`).\n\nThe password is in the file `data.txt` next to the word 'millionth'.",
        "flag": "TESKZC0XvTetK0S9xNwm25STk5iWrBvP"
    },
    {
        "id": "bandit-08",
        "name": "Bandit 8 -> 9: The Only One",
        "points": 500,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit8`).\n\nThe password is in the file `data.txt`. It is the only line of text that occurs exactly once.",
        "flag": "EN632PlfYiZbn3PhVK3XOGSlNInNE00t"
    },
    {
        "id": "bandit-09",
        "name": "Bandit 9 -> 10: Strings Attached",
        "points": 550,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit9`).\n\nThe password is in `data.txt` and is one of the few human-readable strings, preceded by several '=' characters.",
        "flag": "G7w8LIi6J3kTb8O7jPdkOYOsDhmi0n0m"
    },
    {
        "id": "bandit-10",
        "name": "Bandit 10 -> 11: Base Operations",
        "points": 600,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit10`).\n\nThe password in `data.txt` is encoded. You will need to decode it from base64 format.",
        "flag": "6zPeziLdR2RKNdNYFNb6nVCKzphlXHpt"
    },
    {
        "id": "bandit-11",
        "name": "Bandit 11 -> 12: Substitution",
        "points": 650,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit11`).\n\nThe password in `data.txt` has been obfuscated. All lowercase and uppercase letters have been rotated by 13 positions (ROT13).",
        "flag": "JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv"
    },
    {
        "id": "bandit-12",
        "name": "Bandit 12 -> 13: Matryoshka",
        "points": 700,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit12`).\n\n`data.txt` is a hexdump of a file that has been compressed multiple times. Revert the hexdump and decompress it repeatedly (gzip, bzip2, tar) to find the password.",
        "flag": "wbWdlBxEir4c8X3x5l9m5o5Wv8n9Uj4J"
    },
    {
        "id": "bandit-13",
        "name": "Bandit 13 -> 14: Private Keys",
        "points": 750,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit13`).\n\nYou must use the provided private SSH key (`sshkey.private` on the server) to log into the next level (`bandit14`) on localhost. Once logged in, read the password from `/etc/bandit_pass/bandit14`.",
        "flag": "fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq"
    },
    {
        "id": "bandit-14",
        "name": "Bandit 14 -> 15: Port Submission",
        "points": 800,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit14`).\n\nThe password for the next level can be retrieved by submitting the password of the current level to **port 30000 on localhost**.",
        "flag": "jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt"
    },
    {
        "id": "bandit-15",
        "name": "Bandit 15 -> 16: SSL Encryption",
        "points": 850,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit15`).\n\nThe password for the next level can be retrieved by submitting the password of the current level to **port 30001 on localhost** using SSL/TLS encryption.",
        "flag": "JQttfApK4SeyHwDlI9SXGR50qclOAil1"
    },
    {
        "id": "bandit-16",
        "name": "Bandit 16 -> 17: SSL Port Scan",
        "points": 900,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit16`).\n\nThe credentials for the next level can be retrieved by submitting the password of the current level to **a port on localhost in the range 31000 to 32000**.",
        "flag": "VwOSWtCAcEBcCU5TOk540Rh04UvwB1O8"
    },
    {
        "id": "bandit-17",
        "name": "Bandit 17 -> 18: File Comparisons",
        "points": 950,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit17`).\n\nThere are 2 files in the homedirectory: **passwords.old** and **passwords.new**. The password for the next level is in **passwords.new** and is the only line that has been changed.",
        "flag": "kfBf3eYk5BPBRzwjqutbbfE887SVc5ac"
    },
    {
        "id": "bandit-18",
        "name": "Bandit 18 -> 19: Shell Bypass",
        "points": 1000,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit18`).\n\nThe password for the next level is stored in a file **readme** in the homedirectory. Unfortunately, someone has modified **.bashrc** to log you out.",
        "flag": "IueksS7Ubh8G3DXwAFbnnjJ1XWeqro5r"
    },
    {
        "id": "bandit-19",
        "name": "Bandit 19 -> 20: SUID Escalation",
        "points": 1050,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit19`).\n\nTo gain access to the next level, you should use the setuid binary in the homedirectory.",
        "flag": "GbKksEFF4yrVs6il55v6gwY5aVje5f0j"
    },
    {
        "id": "bandit-20",
        "name": "Bandit 20 -> 21: Port Listener Connection",
        "points": 1100,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit20`).\n\nThere is a setuid binary in the homedirectory that makes a connection to localhost on the port you specify as a commandline argument, reads a line of text, and compares it to the previous password.",
        "flag": "gE269g2h3mw3pwgrj0LuIpTpNcfS1KMc"
    },
    {
        "id": "bandit-21",
        "name": "Bandit 21 -> 22: Cron Jobs",
        "points": 1150,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit21`).\n\nA program is running automatically at regular intervals from **cron**. Look in **/etc/cron.d/** for the configuration.",
        "flag": "Yk7oeL4H2E45qp7Z9EaA8F4e8G4Z5Jj7"
    },
    {
        "id": "bandit-22",
        "name": "Bandit 22 -> 23: Cron Debugging",
        "points": 1200,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit22`).\n\nA program is running automatically at regular intervals from **cron**. Look in **/etc/cron.d/** for the configuration and find what script is executing.",
        "flag": "jc1udXDznI2mD8tE8Zq2P17ZtGv6z5M0"
    },
    {
        "id": "bandit-23",
        "name": "Bandit 23 -> 24: Cron Scripting",
        "points": 1250,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit23`).\n\nA program is running automatically at regular intervals from **cron**. Write your own shell-script to extract the password.",
        "flag": "UoMYTrfrBFHyQXmg6R1YI7mIfUIna55J"
    },
    {
        "id": "bandit-24",
        "name": "Bandit 24 -> 25: PIN Brute Force",
        "points": 1300,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit24`).\n\nA daemon is listening on port 30002 and will give you the password if given the password for bandit24 and a secret numeric 4-digit pincode.",
        "flag": "uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG"
    },
    {
        "id": "bandit-25",
        "name": "Bandit 25 -> 26: Shell Breakout",
        "points": 1350,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit25`).\n\nThe shell for user bandit26 is not `/bin/bash`, but something else. Find out what it is and how to break out of it.",
        "flag": "5czgV9L3Xx8JPOyU3jO5B9I0A3bM9E3z"
    },
    {
        "id": "bandit-26",
        "name": "Bandit 26 -> 27: Text UI Breakout",
        "points": 1400,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using the flag from the previous level as your password (username `bandit26`).\n\nNow that you broke out of the shell, query the directory layout to locate the flag.",
        "flag": "3ba3118a22e93127a4ed485be72ef5ea"
    },
    {
        "id": "bandit-27",
        "name": "Bandit 27 -> 28: Git Clone",
        "points": 1450,
        "desc": "There is a git repository at `ssh://bandit27-git@bandit.labs.overthewire.org/home/bandit27-git/repo` via the port `2220`. Clone the repository and find the password.",
        "flag": "0ef186ac70e04ea33b4c1853d2526fa2"
    },
    {
        "id": "bandit-28",
        "name": "Bandit 28 -> 29: Git Commits",
        "points": 1500,
        "desc": "There is a git repository at `ssh://bandit28-git@bandit.labs.overthewire.org/home/bandit28-git/repo` via the port `2220`. Clone the repository and check commit history.",
        "flag": "bbc96594b4e001778eee9975372716b2"
    },
    {
        "id": "bandit-29",
        "name": "Bandit 29 -> 30: Git Branches",
        "points": 1550,
        "desc": "There is a git repository at `ssh://bandit29-git@bandit.labs.overthewire.org/home/bandit29-git/repo` via the port `2220`. Clone the repository and investigate branches.",
        "flag": "5b90576ed34ce8c56ad62351ab66e47c"
    },
    {
        "id": "bandit-30",
        "name": "Bandit 30 -> 31: Git Tags",
        "points": 1600,
        "desc": "There is a git repository at `ssh://bandit30-git@bandit.labs.overthewire.org/home/bandit30-git/repo` via the port `2220`. Clone the repository and look for git tags.",
        "flag": "47e603bb428404d265f59c42920d81e5"
    },
    {
        "id": "bandit-31",
        "name": "Bandit 31 -> 32: Git Push",
        "points": 1650,
        "desc": "There is a git repository at `ssh://bandit31-git@bandit.labs.overthewire.org/home/bandit31-git/repo` via the port `2220`. Push a file to retrieve the password.",
        "flag": "56a9bf19c63d650ce78e6ec0354ee45e"
    },
    {
        "id": "bandit-32",
        "name": "Bandit 32 -> 33: Shell Overrides",
        "points": 1700,
        "desc": "There is a git repository at `ssh://bandit31-git@bandit.labs.overthewire.org/home/bandit31-git/repo` via the port `2220`. Learn about shell syntax escape strings.",
        "flag": "c9c3199ddf4121b10fb58bb24580d440"
    },
    {
        "id": "bandit-33",
        "name": "Bandit 33 -> 34: Final Escape",
        "points": 1750,
        "desc": "SSH into `bandit.labs.overthewire.org` on port `2220` using username `bandit33`.\n\nAfter all this git stuff, it's time for another escape. Good luck!",
        "flag": "OdqthX2eZq2fFft2q3B5mJz7eIq3Zk2d"
    }
]

# Generate folder and files relative to the repo root folder dynamically
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))
os.makedirs(base_dir, exist_ok=True)

for ch in challenges_data:
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)
    
    escaped_desc = ch['desc'].replace('\n', '\n  ')
    yaml_content = f"""name: "{ch['name']}"
author: "OverTheWire"
category: "Linux Basics"
description: |
  {escaped_desc}
value: {ch['points']}
type: standard
flags:
  - "{ch['flag']}"
state: visible
version: "0.1"
"""
    
    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Bandit challenges inside '{base_dir}'!")
