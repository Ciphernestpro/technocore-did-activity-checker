import argparse
import json
import sys
from pathlib import Path


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def collect_activity(source_paths, did):
    """
    Collect public messages for a DID from multiple snapshots.

    Messages are deduplicated using sequence + timestamp + nonce + text.
    """

    messages = []
    seen = set()

    for source_path in source_paths:
        data = load_json(source_path)

        for message in data.get("messages", []):
            if message.get("from") != did:
                continue

            identity = (
                message.get("seq"),
                message.get("ts"),
                message.get("nonce"),
                message.get("text"),
            )

            if identity in seen:
                continue

            seen.add(identity)
            messages.append(message)

    messages.sort(
        key=lambda message: (
            message.get("ts") or "",
            message.get("seq") or 0,
        )
    )

    return messages


def verify_proof(proof_path, expected_did):
    """
    Verify a Technocore contribution proof using the official
    verifier from the local technocore-did-starter project.
    """

    starter = Path.home() / "technocore-did-starter"

    sys.path.insert(0, str(starter))

    import technocore_agent

    proof = load_json(proof_path)

    technocore_agent.verify_contribution_proof(proof)

    if proof.get("did") != expected_did:
        raise ValueError(
            "proof DID does not match the requested agent DID"
        )

    return proof


def calculate_score(activity_count, verified_contributions):
    """
    Transparent heuristic score.

    Activity:
        Up to 10 points for public activity.

    Verified contributions:
        20 points per cryptographically valid contribution,
        capped at 60 points.

    This score is informational only.
    It does NOT represent FLOP allocation or guaranteed rewards.
    """

    activity_points = min(activity_count, 10)

    contribution_points = min(
        verified_contributions * 20,
        60,
    )

    total = activity_points + contribution_points

    return {
        "activity": activity_points,
        "verified_contributions": contribution_points,
        "total": total,
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Calculate a transparent Technocore contribution "
            "score from one or more public snapshots."
        )
    )

    parser.add_argument(
        "did",
        help="Public did:key to score.",
    )

    parser.add_argument(
        "--source",
        action="append",
        required=True,
        help=(
            "Path to a public Technocore room JSON snapshot. "
            "Can be supplied multiple times."
        ),
    )

    parser.add_argument(
        "--proof",
        action="append",
        default=[],
        help=(
            "Contribution proof JSON file. "
            "Can be supplied multiple times."
        ),
    )

    args = parser.parse_args()

    activity = collect_activity(
        args.source,
        args.did,
    )

    valid_proofs = []

    for proof_path in args.proof:
        proof = verify_proof(
            proof_path,
            args.did,
        )
        valid_proofs.append(proof)

    score = calculate_score(
        len(activity),
        len(valid_proofs),
    )

    timestamps = [
        message.get("ts")
        for message in activity
        if message.get("ts")
    ]

    print()
    print("TECHNOCORE AGENT CONTRIBUTION REPORT")
    print("────────────────────────────────────")
    print(f"DID:                    {args.did}")
    print(f"Snapshots scanned:      {len(args.source)}")
    print(f"Unique public activity: {len(activity)}")

    print()
    print("ACTIVITY HISTORY")
    print("────────────────────────────────────")

    if not activity:
        print("• No public messages found")
    else:
        print(f"First seen: {min(timestamps)}")
        print(f"Last seen:  {max(timestamps)}")

        for message in activity:
            print(
                f"• seq={message.get('seq')} "
                f"time={message.get('ts')}"
            )

    print()
    print("VERIFIED CONTRIBUTIONS")
    print("────────────────────────────────────")

    if not valid_proofs:
        print("• None")
    else:
        for number, proof in enumerate(valid_proofs, start=1):
            print(f"✓ Proof #{number}")
            print(f"  Repository: {proof.get('artifact_url')}")
            print(f"  Commit:     {proof.get('commit')}")
            print(f"  Schema:     {proof.get('schema')}")
            print("  Cryptographic proof: VALID")

    print()
    print("REPUTATION SCORE")
    print("────────────────────────────────────")
    print(f"Activity:               {score['activity']}/10")
    print(
        f"Verified contributions: "
        f"{score['verified_contributions']}/60"
    )
    print("────────────────────────────────────")
    print(f"TOTAL:                  {score['total']}/70")

    print()
    print("NOTE")
    print(
        "This score is an informational, reproducible heuristic. "
        "It does not represent FLOP allocation or guaranteed rewards."
    )


if __name__ == "__main__":
    main()