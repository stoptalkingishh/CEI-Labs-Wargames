#!/bin/bash
# Password chain: bandit(N)'s login password = bandit-(N-1) challenge's flag
# in CEI-Labs-Wargames/challenges/bandit-*/challenge.yml (already live in
# CTFd -- these values are NOT ours to change). bandit0 uses the fixed
# starting credential matching the challenge text ("Username: bandit0,
# Password: bandit0"). Every other line here corresponds 1:1 to a flag
# already defined in scripts/build_bandit.py -- keep these in sync if that
# script's flags ever change.
set -e

chpasswd <<'EOF'
bandit0:bandit0
bandit1:NH2SXQwcBdpmTEzi3bvBHRW9NXrY9B1b
bandit2:rRGizSaX8Mk1RTb1CNQoXTcYZUR6OUZY
bandit3:aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lEWG
bandit4:2EW7BBsr6aMMoJ2HjW067zg8WNkNzbpm
bandit5:lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
bandit6:P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
bandit7:z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S
bandit8:TESKZC0XvTetK0S9xNwm25STk5iWrBvP
bandit9:EN632PlfYiZbn3PhVK3XOGSlNInNE00t
bandit10:G7w8LIi6J3kTb8O7jPdkOYOsDhmi0n0m
bandit11:6zPeziLdR2RKNdNYFNb6nVCKzphlXHpt
bandit12:JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv
bandit13:wbWdlBxEir4c8X3x5l9m5o5Wv8n9Uj4J
bandit14:fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq
bandit15:jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt
bandit16:JQttfApK4SeyHwDlI9SXGR50qclOAil1
bandit17:VwOSWtCAcEBcCU5TOk540Rh04UvwB1O8
bandit18:kfBf3eYk5BPBRzwjqutbbfE887SVc5ac
bandit19:IueksS7Ubh8G3DXwAFbnnjJ1XWeqro5r
bandit20:GbKksEFF4yrVs6il55v6gwY5aVje5f0j
bandit21:gE269g2h3mw3pwgrj0LuIpTpNcfS1KMc
bandit22:Yk7oeL4H2E45qp7Z9EaA8F4e8G4Z5Jj7
bandit23:jc1udXDznI2mD8tE8Zq2P17ZtGv6z5M0
bandit24:UoMYTrfrBFHyQXmg6R1YI7mIfUIna55J
bandit25:uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG
bandit26:5czgV9L3Xx8JPOyU3jO5B9I0A3bM9E3z
bandit27:3ba3118a22e93127a4ed485be72ef5ea
bandit28:0ef186ac70e04ea33b4c1853d2526fa2
bandit29:bbc96594b4e001778eee9975372716b2
bandit30:5b90576ed34ce8c56ad62351ab66e47c
bandit31:47e603bb428404d265f59c42920d81e5
bandit32:56a9bf19c63d650ce78e6ec0354ee45e
bandit33:c9c3199ddf4121b10fb58bb24580d440
EOF
# bandit33's own password isn't needed for login as bandit34 (there is no
# bandit34 -- level 33 is the final "escape" and its flag,
# OdqthX2eZq2fFft2q3B5mJz7eIq3Zk2d, is submitted directly to CTFd, not used
# as anyone's login credential).
