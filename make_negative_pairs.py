import pandas as pd
import random
from pathlib import Path


DATA_DIR = Path(r"D:\Dataset\Capstone_Dataset")

NEGATIVE_RATIO = 1.0
SEED = 42


def create_negative_pairs(df, split, ratio=1.0, seed=42):
    """
    Create negative Java-Python pairs by pairing snippets
    from different program IDs.
    """

    rng = random.Random(seed)

    target_count = int(len(df) * ratio)

    # We will use each positive row as a source of Java code.
    java_rows = df[
        ["pair_id", "program_id", "java_id", "code_a"]
    ].copy()

    # Python snippets will be shuffled independently.
    python_rows = df[
        ["pair_id", "program_id", "python_id", "code_b"]
    ].copy()

    negatives = []
    used_pairs = set()

    max_attempts = target_count * 20
    attempts = 0

    while len(negatives) < target_count and attempts < max_attempts:
        attempts += 1

        java_row = java_rows.iloc[
            rng.randrange(len(java_rows))
        ]

        python_row = python_rows.iloc[
            rng.randrange(len(python_rows))
        ]

        # Must come from different programs.
        if java_row["program_id"] == python_row["program_id"]:
            continue

        pair_key = (
            str(java_row["java_id"]),
            str(python_row["python_id"])
        )

        if pair_key in used_pairs:
            continue

        used_pairs.add(pair_key)

        negatives.append(
            {
                "pair_id": f"{split.upper()}_NEG_{len(negatives)+1:06d}",
                "program_id_a": java_row["program_id"],
                "program_id_b": python_row["program_id"],
                "java_id": java_row["java_id"],
                "python_id": python_row["python_id"],
                "language_a": "Java",
                "language_b": "Python",
                "code_a": java_row["code_a"],
                "code_b": python_row["code_b"],
                "label": 0,
                "pair_type": "negative",
                "split": split,
                "source": "XLCoST_constructed",
            }
        )

    if len(negatives) < target_count:
        raise RuntimeError(
            f"Could only create {len(negatives)} "
            f"negative pairs out of requested {target_count}."
        )

    return pd.DataFrame(negatives)


for split in ["train", "val", "test"]:

    positive_file = DATA_DIR / f"{split}_positive_subset.csv"
    negative_file = DATA_DIR / f"{split}_negative_pairs.csv"

    df = pd.read_csv(positive_file)

    negatives = create_negative_pairs(
        df,
        split=split,
        ratio=NEGATIVE_RATIO,
        seed=SEED
    )

    negatives.to_csv(
        negative_file,
        index=False
    )

    print(f"{split}:")
    print(f"  Positive pairs : {len(df):,}")
    print(f"  Negative pairs : {len(negatives):,}")
    print(f"  Saved to       : {negative_file}")
    print()

