#!/usr/bin/env python3
"""Attach generated OSINT challenge files to a local CTFd instance.

Usage:
  CTFD_TOKEN=... python scripts/local-ctfd/upload_osint_files.py
"""

import argparse
import os
import re
from pathlib import Path

import requests
import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=os.environ.get("CTFD_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--token", default=os.environ.get("CTFD_TOKEN"))
    parser.add_argument("--remove-pdfs", action="store_true", help="delete every retired PDF attachment first")
    parser.add_argument("--username", default=os.environ.get("CTFD_ADMIN_NAME"))
    parser.add_argument("--password", default=os.environ.get("CTFD_ADMIN_PASSWORD"))
    parser.add_argument("--osint-dir", default="osint")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    client = requests.Session()
    headers = {"Authorization": f"Token {args.token}"} if args.token else {}
    if not args.token:
        if not args.username or not args.password:
            parser.error("set CTFD_TOKEN, or set CTFD_ADMIN_NAME and CTFD_ADMIN_PASSWORD")
        login_page = client.get(f"{base_url}/login")
        login_page.raise_for_status()
        nonce = re.search(r'name="nonce"[^>]*value="([a-f0-9]+)"', login_page.text)
        if not nonce:
            raise RuntimeError("could not find login CSRF nonce")
        response = client.post(
            f"{base_url}/login",
            data={"name": args.username, "password": args.password, "nonce": nonce.group(1)},
        )
        response.raise_for_status()
        base_url = args.url.rstrip("/")
    client = requests.Session()
    headers = {"Authorization": f"Token {args.token}"} if args.token else {}
    if not args.token:
        if not args.username or not args.password:
            parser.error("set CTFD_TOKEN, or set CTFD_ADMIN_NAME and CTFD_ADMIN_PASSWORD")
        login_page = client.get(f"{base_url}/login")
        login_page.raise_for_status()
        nonce = re.search(r'name="nonce"[^>]*value="([a-f0-9]+)"', login_page.text)
        if not nonce:
            raise RuntimeError("could not find login CSRF nonce")
        response = client.post(
            f"{base_url}/login",
            data={"name": args.username, "password": args.password, "nonce": nonce.group(1)},
        )
        response.raise_for_status()
        settings_page = client.get(f"{base_url}/settings")
        csrf = re.search(r"csrfNonce['\"]?\s*:\s*[\"']([a-f0-9]+)[\"']", settings_page.text)
        if csrf:
            headers["CSRF-Token"] = csrf.group(1)

    # CTFd's API authentication middleware expects JSON content negotiation on
    # non-multipart requests; do not send it with multipart file uploads.
    api_headers = {**headers, "Content-Type": "application/json"}
    response = client.get(f"{base_url}/api/v1/challenges?view=admin", headers=api_headers)
    response.raise_for_status()
    challenge_ids = {item["name"]: item["id"] for item in response.json()["data"]}

    if args.remove_pdfs:
        listing = client.get(f"{base_url}/api/v1/files?type=challenge", headers=api_headers)
        listing.raise_for_status()
        removed = 0
        for f in listing.json()["data"]:
            if f["location"].lower().endswith((".pdf", ".pdf?token")):
                r = client.delete(f"{base_url}/api/v1/files/{f['id']}", headers=api_headers)
                r.raise_for_status()
                removed += 1
                print(f"pruned-pdf: {f['location'].split('/')[-1]}")
        print(f"pruned {removed} retired PDF attachments.")

    uploaded = 0
    skipped = 0
    pruned = 0
    patched = 0
    for directory in sorted(Path(args.osint_dir).iterdir()):
        challenge_file = directory / "challenge.yml"
        files_dir = directory / "files"
        if not directory.is_dir() or not challenge_file.is_file():
            continue

        files = [item for item in files_dir.iterdir() if item.is_file()] if files_dir.is_dir() else []
        spec = yaml.safe_load(challenge_file.read_text(encoding="utf-8"))
        challenge_id = challenge_ids[spec["name"]]
        response = client.get(f"{base_url}/api/v1/challenges/{challenge_id}", headers=api_headers)
        response.raise_for_status()
        data = response.json()["data"]
        remote_files = data.get("files", [])
        local_names = {f.name for f in files}

        # Remove remote files that are no longer generated locally (retired PDFs).
        if remote_files:
            keep_basenames = {url.rsplit("/", 1)[-1].split("?")[0] for url in remote_files
                              if any(name and url.rsplit("/", 1)[-1].split("?")[0] == name for name in local_names)}
            for url in remote_files:
                remote_name = url.rsplit("/", 1)[-1].split("?")[0]
                if remote_name in keep_basenames:
                    continue
                file_id = _file_id_for(client, base_url, api_headers, url, challenge_id)
                if file_id:
                    r = client.delete(f"{base_url}/api/v1/files/{file_id}", headers=api_headers)
                    r.raise_for_status()
                    pruned += 1
                    print(f"pruned {directory.name}: {remote_name}")

        for local_file in files:
            if any(local_file.name in remote_file for remote_file in remote_files):
                skipped += 1
                continue

            with local_file.open("rb") as handle:
                response = client.post(
                    f"{base_url}/api/v1/files",
                    headers=headers,
                    files={"file": (local_file.name, handle)},
                    data={"challenge_id": challenge_id, "type": "challenge"},
                )
            if not response.ok:
                raise RuntimeError(f"upload failed for {directory.name}: HTTP {response.status_code}: {response.text}")
            uploaded += 1
            print(f"attached {directory.name}: {local_file.name}")

        # Keep the remote description identical to the generated YAML
        # (embeds the clickable briefing popup).
        if spec.get("description") != data.get("description"):
            r = client.patch(
                f"{base_url}/api/v1/challenges/{challenge_id}",
                headers=api_headers,
                json={"description": spec["description"]},
            )
            if not r.ok:
                raise RuntimeError(f"description patch failed for {directory.name}: HTTP {r.status_code}: {r.text}")
            patched += 1
            print(f"patched description {directory.name}")

    print(f"Sync complete: {uploaded} uploaded, {skipped} already attached, {pruned} pruned, {patched} descriptions updated.")


def _file_id_for(client, base_url, headers, remote_url, challenge_id):
    """Return the CTFd file id for a remote challenge-file URL, or None."""
    listing = client.get(f"{base_url}/api/v1/files?type=challenge", headers=headers)
    listing.raise_for_status()
    remote_name = remote_url.rsplit("/", 1)[-1].split("?")[0]
    for f in listing.json()["data"]:
        if f.get("challenge_id") == int(challenge_id) and f["location"].split("/")[-1] == remote_name:
            return f["id"]
    return None


if __name__ == "__main__":
    main()
