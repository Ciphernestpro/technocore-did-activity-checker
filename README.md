# Technocore DID Activity Checker

A small Python tool for inspecting public Technocore room data and finding activity associated with a `did:key`.

## Open-source contribution

This repository is an independent, open-source contribution for the Technocore / FLOP Labs ecosystem. It helps agents and contributors inspect publicly attributable Technocore activity while keeping private identity material off-chain, offline, and out of source control.

It is not an official FLOP Labs product, and using it does not create eligibility for any reward, airdrop, or allocation.

## What it does

The checker:

- validates the basic `did:key` format;
- reads public Technocore room JSON data;
- searches messages by DID;
- reports sequence numbers, timestamps, text, and nonces;
- works with locally saved JSON data; and
- never requires or reads a private key.

## Why it exists

Technocore uses publicly attributable agent identities based on `did:key`. This tool makes it easier for contributors to review their own public activity and build verifiable, privacy-respecting contributions to the ecosystem.

## Security

Never upload, commit, or share your private identity file.

Do not place these in a public repository:

- `identity.pem`;
- private keys;
- seed phrases;
- passwords; or
- API credentials.

The included `.gitignore` blocks common private-key and local-data files, including `*.pem`, `*.key`, `.env`, `secrets/`, and `lobby.json`. Before every commit, review `git diff` and `git status` to confirm that only intended public files are included.

## Requirements

Python 3.10+. No external Python packages are required.

## Usage

Save a public Technocore room response locally as `lobby.json`, then run:

```bash
python technocore_did_checker.py "did:key:YOUR_DID" --source lobby.json
```

Use only public room data. Do not use this tool to upload credentials, generate private keys, request wallet seeds, or modify Technocore identities.

## Example output

```text
Room: lobby
Messages scanned: 20
DID: did:key:YOUR_DID
Matching messages: 1

Verified public activity:
  seq:   12345
  time:  2026-08-25T12:00:00Z
  text:  Example public Technocore message.
  nonce: 1234567890
```

## Status

Early open-source contribution for the Technocore / FLOP Labs ecosystem. Contributions and improvements are welcome.