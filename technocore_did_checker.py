import argparse
import json
import re
import sys
from pathlib import Path


DID_PATTERN = re.compile(r"^did:key:z[1-9A-HJ-NP-Za-km-z]+$")


def check_did(did):
    return bool(DID_PATTERN.fullmatch(did))


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def inspect_messages(data, did):
    messages = data.get("messages", [])

    matches = [
        message
        for message in messages
        if message.get("from") == did
    ]

    print(f"Room: {data.get('room', 'unknown')}")
    print(f"Messages scanned: {len(messages)}")
    print(f"DID: {did}")
    print(f"Matching messages: {len(matches)}")

    if not matches:
        print("\nNo messages found for this DID.")
        return

    print("\nVerified public activity:")
    for message in matches:
        print(f"  seq:   {message.get('seq')}")
        print(f"  time:  {message.get('ts')}")
        print(f"  text:  {message.get('text')}")
        print(f"  nonce: {message.get('nonce')}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Inspect public Technocore room activity for a did:key."
    )

    parser.add_argument("did")
    parser.add_argument("--source", required=True)

    args = parser.parse_args()

    if not check_did(args.did):
        print("ERROR: invalid did:key format.")
        sys.exit(1)

    try:
        data = load_json(args.source)
        inspect_messages(data, args.did)
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()