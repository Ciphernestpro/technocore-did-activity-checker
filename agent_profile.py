import argparse
import json
import sys
from pathlib import Path


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def verify_proof_with_technocore(proof_path):
    starter = Path.home() / "technocore-did-starter"

    sys.path.insert(0, str(starter))

    try:
        import technocore_agent
    except ImportError as error:
        raise RuntimeError(
            "Cannot load technocore_agent from technocore-did-starter"
        ) from error

    proof = load_json(proof_path)

    technocore_agent.verify_contribution_proof(proof)

    return proof


def build_profile(data, did, proof=None, proof_valid=False):
    messages = [
        message
        for message in data.get("messages", [])
        if message.get("from") == did
    ]

    timestamps = [
        message.get("ts")
        for message in messages
        if message.get("ts")
    ]

    contribution = None

    if proof and proof.get("did") == did:
        contribution = {
            "artifact_url": proof.get("artifact_url"),
            "commit": proof.get("commit"),
            "schema": proof.get("schema"),
            "proof_valid": proof_valid,
        }

    return {
        "did": did,
        "room": data.get("room", "unknown"),
        "messages": len(messages),
        "first_seen": min(timestamps) if timestamps else None,
        "last_seen": max(timestamps) if timestamps else None,
        "contribution": contribution,
    }


def print_profile(profile):
    print()
    print("TECHNOCORE AGENT PROFILE")
    print("────────────────────────────")

    print(f"DID:         {profile['did']}")
    print(f"Room:        {profile['room']}")
    print(f"Messages:    {profile['messages']}")
    print(f"First seen:  {profile['first_seen'] or 'none'}")
    print(f"Last seen:   {profile['last_seen'] or 'none'}")

    print()
    print("PUBLIC ACTIVITY")

    if profile["messages"]:
        print("✓ Public messages found")
    else:
        print("• No public messages found")

    print()
    print("CONTRIBUTION")

    contribution = profile["contribution"]

    if not contribution:
        print("• No matching contribution proof found")
        return

    print("✓ Contribution proof found")
    print(f"✓ Repository: {contribution['artifact_url']}")
    print(f"✓ Commit:     {contribution['commit']}")
    print(f"✓ Schema:     {contribution['schema']}")

    if contribution["proof_valid"]:
        print("✓ Cryptographic proof: VALID")
        print()
        print("STATUS")
        print("✓ VERIFIED CONTRIBUTOR")
    else:
        print("✗ Cryptographic proof: INVALID")


def main():
    parser = argparse.ArgumentParser(
        description="Build a public Technocore agent profile."
    )

    parser.add_argument(
        "did",
        help="Public did:key to inspect.",
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Path to a locally saved public Technocore room JSON file.",
    )

    parser.add_argument(
        "--proof",
        help="Optional Technocore contribution proof JSON file.",
    )

    args = parser.parse_args()

    data = load_json(args.source)

    proof = None
    proof_valid = False

    if args.proof:
        proof = verify_proof_with_technocore(args.proof)
        proof_valid = proof.get("did") == args.did

    profile = build_profile(
        data,
        args.did,
        proof,
        proof_valid,
    )

    print_profile(profile)


if __name__ == "__main__":
    main()