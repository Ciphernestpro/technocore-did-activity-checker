import argparse
import json
from pathlib import Path


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def calculate_score(activity_count, verified_contributions):
    """
    Transparent heuristic score.

    Activity:
        Up to 10 points for public activity.

    Verified contributions:
        20 points per cryptographically valid contribution,
        capped at 60 points.

    The score is an informational reputation signal.
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


def count_activity(data, did):
    return sum(
        1
        for message in data.get("messages", [])
        if message.get("from") == did
    )


def verify_proof(proof_path, expected_did):
    """
    Verify a Technocore contribution proof using the official
    verifier from the local technocore-did-starter project.
    """

    starter = Path.home() / "technocore-did-starter"

    import sys

    sys.path.insert(0, str(starter))

    import technocore_agent

    proof = load_json(proof_path)

    technocore_agent.verify_contribution_proof(proof)

    if proof.get("did") != expected_did:
        raise ValueError(
            "proof DID does not match the requested agent DID"
        )

    return proof


def main():
    parser = argparse.ArgumentParser(
        description="Calculate a transparent Technocore contribution score."
    )

    parser.add_argument(
        "did",
        help="Public did:key to score.",
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Path to a public Technocore room JSON file.",
    )

    parser.add_argument(
        "--proof",
        action="append",
        default=[],
        help="Contribution proof JSON file. Can be supplied multiple times.",
    )

    args = parser.parse_args()

    data = load_json(args.source)

    activity_count = count_activity(data, args.did)

    valid_proofs = []

    for proof_path in args.proof:
        proof = verify_proof(proof_path, args.did)
        valid_proofs.append(proof)

    score = calculate_score(
        activity_count,
        len(valid_proofs),
    )

    print()
    print("TECHNOCORE CONTRIBUTION SCORE")
    print("────────────────────────────")
    print(f"DID:                    {args.did}")
    print(f"Public activity:        {activity_count}")
    print(f"Verified contributions: {len(valid_proofs)}")

    print()
    print("SCORE BREAKDOWN")
    print("────────────────────────────")
    print(f"Activity:               {score['activity']}/10")
    print(
        f"Verified contributions: {score['verified_contributions']}/60"
    )
    print("────────────────────────────")
    print(f"TOTAL:                  {score['total']}/70")

    print()
    print("VERIFIED PROOFS")

    if not valid_proofs:
        print("• None")
    else:
        for proof in valid_proofs:
            print(f"✓ {proof.get('artifact_url')}")
            print(f"  Commit: {proof.get('commit')}")

    print()
    print("NOTE")
    print(
        "This score is an informational, reproducible heuristic. "
        "It does not represent FLOP allocation or guaranteed rewards."
    )


if __name__ == "__main__":
    main()